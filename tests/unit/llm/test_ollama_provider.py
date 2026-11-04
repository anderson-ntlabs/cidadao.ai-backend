"""
Unit tests for the self-hosted Ollama provider.

Ollama is what lets Cidadão.AI run with no closed LLM API at all, so these
tests pin down the three things a self-hosted deployment depends on: the
request goes to the operator's own server in the OpenAI-compatible shape, no
credential is sent, and a failing local model never silently falls back to a
third-party API.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.core import config as config_mod
from src.core.config import Settings
from src.llm import providers as providers_mod
from src.llm.providers import (
    LLMManager,
    LLMProvider,
    LLMRequest,
    OllamaProvider,
    create_llm_manager,
)
from src.services import dspy_agents
from src.services import maritaca_client as maritaca_client_mod


@pytest.fixture
def request_obj():
    return LLMRequest(
        messages=[{"role": "user", "content": "quem gastou mais?"}],
        system_prompt="voce e um auditor",
        temperature=0.2,
        max_tokens=256,
        top_p=0.8,
    )


def ollama_payload(content: str = "achei 3 anomalias") -> dict:
    return {
        "id": "chatcmpl-42",
        "object": "chat.completion",
        "model": "qwen2.5:7b",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }


class TestOllamaSettings:
    def test_defaults_point_to_a_local_server_and_an_open_model(self):
        fields = Settings.model_fields

        assert fields["ollama_base_url"].default == "http://localhost:11434/v1"
        assert fields["ollama_model"].default == "qwen2.5:7b"
        assert "ollama" in fields["llm_provider"].description


class TestOllamaProviderConfig:
    def test_base_url_and_model_come_from_settings(self):
        with (
            patch.object(
                providers_mod.settings, "ollama_base_url", "http://ollama:11434/v1/"
            ),
            patch.object(providers_mod.settings, "ollama_model", "llama3.1:8b"),
        ):
            provider = OllamaProvider()

        # Trailing slash is stripped so endpoints do not end up with "//".
        assert provider.base_url == "http://ollama:11434/v1"
        assert provider.default_model == "llama3.1:8b"

    def test_explicit_arguments_override_settings(self):
        provider = OllamaProvider(base_url="http://gpu-box:11434/v1", model="gemma2")

        assert provider.base_url == "http://gpu-box:11434/v1"
        assert provider.default_model == "gemma2"

    def test_no_credential_is_sent(self):
        headers = OllamaProvider()._get_headers()

        assert "Authorization" not in headers
        assert headers["Content-Type"] == "application/json"

    def test_shared_pool_is_bypassed(self):
        # The pool only holds clients for hosted APIs; routing Ollama through
        # it would fail and log a warning on every single request.
        provider = OllamaProvider()

        assert provider._use_pool is False
        assert not hasattr(provider, "_provider_name")


class TestOllamaRequestPayload:
    def test_payload_is_openai_compatible(self, request_obj):
        provider = OllamaProvider(model="qwen2.5:7b")

        data = provider._prepare_request_data(request_obj)

        assert data == {
            "model": "qwen2.5:7b",
            "messages": [
                {"role": "system", "content": "voce e um auditor"},
                {"role": "user", "content": "quem gastou mais?"},
            ],
            "temperature": 0.2,
            "max_tokens": 256,
            "top_p": 0.8,
            "stream": False,
        }

    def test_explicit_model_overrides_the_default(self):
        provider = OllamaProvider(model="qwen2.5:7b")
        request = LLMRequest(messages=[], model="llama3.1:8b")

        assert provider._prepare_request_data(request)["model"] == "llama3.1:8b"

    def test_no_system_prompt_means_no_system_message(self):
        provider = OllamaProvider()
        request = LLMRequest(messages=[{"role": "user", "content": "oi"}])

        messages = provider._prepare_request_data(request)["messages"]

        assert messages == [{"role": "user", "content": "oi"}]


class TestOllamaResponseParsing:
    def test_response_is_mapped_to_the_common_shape(self):
        provider = OllamaProvider()

        response = provider._parse_response(ollama_payload(), response_time=2.5)

        assert response.content == "achei 3 anomalias"
        assert response.provider == "ollama"
        assert response.model == "qwen2.5:7b"
        assert response.usage["total_tokens"] == 15
        assert response.metadata == {
            "finish_reason": "stop",
            "response_id": "chatcmpl-42",
        }
        assert response.response_time == 2.5

    def test_missing_model_falls_back_to_the_configured_one(self):
        provider = OllamaProvider(model="gemma2")
        payload = ollama_payload()
        del payload["model"]
        del payload["usage"]

        response = provider._parse_response(payload, response_time=0.1)

        assert response.model == "gemma2"
        assert response.usage == {}


class TestOllamaHttpLayer:
    @pytest.mark.asyncio
    async def test_complete_posts_to_the_local_server_without_the_pool(
        self, request_obj
    ):
        provider = OllamaProvider(base_url="http://ollama:11434/v1", model="qwen2.5:7b")
        client = AsyncMock()
        client.post = AsyncMock(
            return_value=httpx.Response(
                200,
                json=ollama_payload("ok"),
                request=httpx.Request(
                    "POST", "http://ollama:11434/v1/chat/completions"
                ),
            )
        )
        provider.client = client
        get_pool = AsyncMock()

        with patch.object(providers_mod, "get_llm_pool", get_pool):
            response = await provider.complete(request_obj)

        assert response.content == "ok"
        assert response.provider == "ollama"
        get_pool.assert_not_awaited()
        client.post.assert_awaited_once()
        call = client.post.await_args
        assert call.args[0] == "http://ollama:11434/v1/chat/completions"
        assert call.kwargs["json"]["model"] == "qwen2.5:7b"
        assert call.kwargs["json"]["messages"][0]["role"] == "system"
        assert "Authorization" not in call.kwargs["headers"]

    @pytest.mark.asyncio
    async def test_stream_yields_only_content_deltas(self, request_obj):
        provider = OllamaProvider()

        async def fake_stream(endpoint, data, stream=False):
            assert endpoint == "/chat/completions"
            assert data["stream"] is True
            for chunk in [
                {"choices": [{"delta": {"role": "assistant"}}]},
                {"choices": [{"delta": {"content": "Uai"}}]},
                {"choices": []},
                {"choices": [{"delta": {"content": ", sô"}}]},
            ]:
                yield chunk

        provider._make_request = fake_stream

        chunks = [c async for c in provider.stream_complete(request_obj)]

        assert chunks == ["Uai", ", sô"]


class TestOllamaRegistration:
    def test_enum_value(self):
        assert LLMProvider("ollama") is LLMProvider.OLLAMA

    def test_manager_registers_an_ollama_instance(self):
        manager = create_llm_manager(primary_provider="Ollama")

        assert manager.primary_provider is LLMProvider.OLLAMA
        assert isinstance(manager.providers[LLMProvider.OLLAMA], OllamaProvider)

    def test_ollama_primary_has_no_hosted_fallback_by_default(self):
        manager = create_llm_manager(primary_provider="ollama")

        assert manager.fallback_providers == []
        assert manager._build_provider_chain() == [LLMProvider.OLLAMA]

    def test_hosted_fallback_can_still_be_opted_into(self):
        manager = LLMManager(
            primary_provider=LLMProvider.OLLAMA,
            fallback_providers=[LLMProvider.MARITACA],
        )

        assert manager._build_provider_chain() == [
            LLMProvider.OLLAMA,
            LLMProvider.MARITACA,
        ]

    def test_other_primaries_keep_the_original_default_chain(self):
        manager = create_llm_manager(primary_provider="maritaca")

        assert manager.fallback_providers == [
            LLMProvider.TOGETHER,
            LLMProvider.HUGGINGFACE,
            LLMProvider.MARITACA,
        ]
        assert LLMProvider.OLLAMA not in manager._build_provider_chain()


class TestDSPyHonoursOllama:
    """The chat route and most agents answer through DSPy, not LLMManager."""

    def _service(self):
        # Skip __init__: it would configure the real LLM and build modules.
        return object.__new__(dspy_agents.DSPyAgentService)

    def test_ollama_provider_configures_dspy_against_the_local_server(self):
        fake_dspy = MagicMock()
        service = self._service()

        with (
            patch.object(dspy_agents, "dspy", fake_dspy),
            patch.object(dspy_agents.settings, "llm_provider", "ollama"),
            patch.object(
                dspy_agents.settings, "ollama_base_url", "http://ollama:11434/v1"
            ),
            patch.object(dspy_agents.settings, "ollama_model", "qwen2.5:7b"),
            patch.object(dspy_agents.settings, "maritaca_api_key", None),
        ):
            service._configure_llm()

        kwargs = fake_dspy.LM.call_args.kwargs
        assert kwargs["model"] == "openai/qwen2.5:7b"
        assert kwargs["api_base"] == "http://ollama:11434/v1"
        assert "maritaca" not in kwargs["api_base"]
        fake_dspy.configure.assert_called_once_with(lm=fake_dspy.LM.return_value)
        assert service.lm is fake_dspy.LM.return_value

    def test_maritaca_provider_still_uses_maritaca(self):
        fake_dspy = MagicMock()
        service = self._service()
        secret = MagicMock()
        secret.get_secret_value.return_value = "sk-unit-test"

        with (
            patch.object(dspy_agents, "dspy", fake_dspy),
            patch.object(dspy_agents.settings, "llm_provider", "maritaca"),
            patch.object(dspy_agents.settings, "maritaca_api_key", secret),
        ):
            service._configure_llm()

        kwargs = fake_dspy.LM.call_args.kwargs
        assert kwargs["api_base"] == "https://chat.maritaca.ai/api"
        assert kwargs["api_key"] == "sk-unit-test"


class TestOllamaChatClientFactory:
    """Agents that take a MaritacaClient directly get one bound to Ollama."""

    def test_returns_none_unless_ollama_is_selected(self):
        with patch.object(config_mod.settings, "llm_provider", "maritaca"):
            assert maritaca_client_mod.create_ollama_chat_client() is None

    def test_client_points_at_the_local_server_and_model(self):
        with (
            patch.object(config_mod.settings, "llm_provider", "ollama"),
            patch.object(
                config_mod.settings, "ollama_base_url", "http://ollama:11434/v1/"
            ),
            patch.object(config_mod.settings, "ollama_model", "qwen2.5:7b"),
        ):
            client = maritaca_client_mod.create_ollama_chat_client()

        assert isinstance(client, maritaca_client_mod.MaritacaClient)
        assert client.base_url == "http://ollama:11434/v1"
        assert client.default_model == "qwen2.5:7b"
        assert "maritaca.ai" not in client.base_url

    @pytest.mark.asyncio
    async def test_requests_reach_ollama_chat_completions(self):
        with (
            patch.object(config_mod.settings, "llm_provider", "ollama"),
            patch.object(
                config_mod.settings, "ollama_base_url", "http://ollama:11434/v1"
            ),
            patch.object(config_mod.settings, "ollama_model", "qwen2.5:7b"),
        ):
            client = maritaca_client_mod.create_ollama_chat_client()

        client.client = AsyncMock()
        client.client.post = AsyncMock(
            return_value=httpx.Response(
                200,
                json=ollama_payload("uai"),
                request=httpx.Request(
                    "POST", "http://ollama:11434/v1/chat/completions"
                ),
            )
        )

        response = await client.chat(messages=[{"role": "user", "content": "oi"}])

        assert response.content == "uai"
        call = client.client.post.await_args
        assert call.args[0] == "http://ollama:11434/v1/chat/completions"
        assert call.kwargs["json"]["model"] == "qwen2.5:7b"

    def test_drummond_uses_ollama_when_selected(self):
        from src.agents.drummond import CommunicationAgent

        agent = object.__new__(CommunicationAgent)
        agent.logger = MagicMock()
        agent.llm_client = None

        with (
            patch.object(config_mod.settings, "llm_provider", "ollama"),
            patch.object(
                config_mod.settings, "ollama_base_url", "http://ollama:11434/v1"
            ),
        ):
            agent._init_llm_client()

        assert agent.llm_client is not None
        assert agent.llm_client.base_url == "http://ollama:11434/v1"
