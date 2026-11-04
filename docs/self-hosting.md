# Self-hosting with open components only

**Author**: Anderson Henrique da Silva
**Location**: Minas Gerais, Brazil
**Created**: 2026-11-03
**Last Updated**: 2026-11-03

---

The Cidadão.AI backend can run end to end on infrastructure you control, with
no proprietary service in the loop:

| Role | Hosted default | Open replacement |
|------|----------------|------------------|
| LLM | Maritaca AI (`sabia-4`, closed API) | [Ollama](https://ollama.com) serving an open-weight model |
| Database | Supabase / Railway PostgreSQL | PostgreSQL 16 container |
| Cache | Railway Redis | Redis 7 container |
| Frontend hosting | Vercel | not needed for the API; any static host works |

Everything below uses the `docker-compose.yml` at the repository root.

## Requirements

- Docker with the Compose plugin (`docker compose`) or `docker-compose`
- About 8 GB of free RAM for the default 7B model (CPU works; a GPU is faster)
- About 6 GB of disk for the model weights

## 1. Configure

Create a `.env` file next to `docker-compose.yml` (it is git-ignored, never
commit it):

```bash
SECRET_KEY=<output of: openssl rand -hex 32>
JWT_SECRET_KEY=<output of: openssl rand -hex 32>
POSTGRES_PASSWORD=<a strong local password>
# Optional
OLLAMA_MODEL=qwen2.5:7b
TRANSPARENCY_API_KEY=        # free key from portaldatransparencia.gov.br/api-de-dados
API_PORT=8000
```

The compose file already sets `LLM_PROVIDER=ollama`,
`OLLAMA_BASE_URL=http://ollama:11434/v1`, `DATABASE_URL` and `REDIS_URL`.
No Maritaca, Supabase or Vercel variable is needed. Without
`TRANSPARENCY_API_KEY` the data agents answer in demo mode; the key is a free
government credential, not a platform dependency.

## 2. Start the stack

```bash
docker compose up -d --build
```

Database migrations run automatically when the API starts.

## 3. Pull the model

The Ollama container starts empty. Pull the model once; it is kept in the
`ollama_data` volume:

```bash
docker compose exec ollama ollama pull qwen2.5:7b
```

Check it answers through the same OpenAI-compatible endpoint the backend uses:

```bash
docker compose exec ollama ollama run qwen2.5:7b "Diga olá em uma frase."
```

Then check the API: `curl http://localhost:8000/health`.

### Choosing a model

The default is `qwen2.5:7b` (Apache 2.0): it is one of the smallest open models
that holds a conversation in Brazilian Portuguese reasonably and follows system
prompts, which the agent personalities rely on, and it runs on a CPU-only
machine. Any chat model from the [Ollama library](https://ollama.com/library)
works; set `OLLAMA_MODEL` to its tag and pull it. Larger options trade memory
for quality, for example `qwen2.5:14b` or `llama3.1:8b`. Answers from a 7B
local model are noticeably weaker than `sabia-4`.

To use a GPU, uncomment the `deploy` block of the `ollama` service (requires
the NVIDIA Container Toolkit).

## Switching providers

The provider is a single variable:

| `LLM_PROVIDER` | Needs |
|----------------|-------|
| `ollama` | `OLLAMA_BASE_URL` (default `http://localhost:11434/v1`), `OLLAMA_MODEL` (default `qwen2.5:7b`) |
| `maritaca` (production default) | `MARITACA_API_KEY`, `MARITACA_MODEL` |
| `groq`, `together`, `huggingface` | the matching `*_API_KEY` |

Running the API outside Docker against a local Ollama:

```bash
ollama serve &                 # or the Ollama desktop app
ollama pull qwen2.5:7b
export LLM_PROVIDER=ollama
python -m src.api.app
```

When `LLM_PROVIDER=ollama`, the LLM manager does not fall back to hosted
providers if the local model fails, so prompts never leave your
infrastructure silently. Hosted fallbacks can still be enabled explicitly in
code through `LLMManager(fallback_providers=[...])`.

## What honours `LLM_PROVIDER=ollama`

- `src/llm/providers.py`: `OllamaProvider`, used by `LLMManager` /
  `create_llm_manager` / `LLMService`.
- `src/services/dspy_agents.py`: the DSPy personality service, which serves
  `POST /api/v1/chat/stream` and the agents that answer through it (Bo Bardi,
  Santos Dumont, the kids agents, and the streaming fallback for the others).
- Agents that take an OpenAI-compatible chat client directly, through
  `create_ollama_chat_client()` in `src/services/maritaca_client.py`:
  Drummond (`src/agents/drummond.py`, conversational answers of
  `POST /api/v1/chat/message`), Abaporu and Ayrton Senna in
  `src/api/routes/agents.py`, and `src/services/chat_data_integration.py`.

## Known limitations

- `POST /api/v1/chat/direct/maritaca`, `/direct/maritaca/stream`,
  `/direct/maritaca/health` and `/direct/maritaca/models`
  (`src/services/maritaca_direct_service.py`) are, by design, a direct
  Maritaca gateway. They fail without `MARITACA_API_KEY`; the rest of the API
  is unaffected.
- `src/agents/drummond_simple.py` and the self-description texts of Santos
  Dumont and the chat route still mention Maritaca as the provider. This is
  wording, not a runtime dependency.
- Ayrton Senna calls `llm_service.generate(...)`, which the chat client does
  not implement, so its LLM routing falls back to rule-based routing with any
  provider, Maritaca included. This predates Ollama support.
- `src/core/llm_pool.py` only pools connections to hosted APIs. Ollama
  requests use a direct HTTP client, which is fine for a local server.
- Cost tracking (`src/core/llm_cost_tracker.py`) has no price entry for
  Ollama models, which is correct for local inference but means the cost
  dashboards show nothing for them.
- The model quality and latency depend on your hardware; on CPU, a first
  answer can take tens of seconds while the model loads.
