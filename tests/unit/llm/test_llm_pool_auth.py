"""The connection pool must send the real API key, not the masked SecretStr."""

from unittest.mock import AsyncMock, patch

import pytest
from pydantic import SecretStr

from src.core.llm_pool import LLMConnectionPool


def test_secret_unwraps_secretstr():
    assert LLMConnectionPool._secret(SecretStr("gsk-real")) == "gsk-real"


def test_secret_accepts_plain_strings_and_none():
    assert LLMConnectionPool._secret("plain") == "plain"
    assert LLMConnectionPool._secret(None) == ""


@pytest.mark.asyncio
async def test_groq_pool_uses_unmasked_key():
    pool = LLMConnectionPool()
    with (
        patch("src.core.llm_pool.settings") as fake_settings,
        patch.object(pool, "_create_pool", new_callable=AsyncMock) as create,
    ):
        fake_settings.groq_api_key = SecretStr("gsk-real")
        fake_settings.openai_api_key = None
        await pool.initialize()

    created = {call.args[0]: call.args[1] for call in create.await_args_list}
    assert created["groq"]["headers"]["Authorization"] == "Bearer gsk-real"
    assert "**********" not in created["groq"]["headers"]["Authorization"]
    assert "openai" not in created


@pytest.mark.asyncio
async def test_providers_without_key_are_skipped():
    pool = LLMConnectionPool()
    with (
        patch("src.core.llm_pool.settings") as fake_settings,
        patch.object(pool, "_create_pool", new_callable=AsyncMock) as create,
    ):
        fake_settings.groq_api_key = None
        fake_settings.openai_api_key = None
        await pool.initialize()

    create.assert_not_awaited()
