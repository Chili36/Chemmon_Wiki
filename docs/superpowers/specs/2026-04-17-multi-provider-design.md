# Multi-Provider LLM Support — Design Spec

Status: draft
Date: 2026-04-17
Scope: `wiki_api/` backend only. No deploy UI changes.

## Goal

Replace the current dual-SDK architecture (OpenAI SDK for selector, Anthropic SDK for answerer) with a single OpenAI SDK that routes to any provider via `base_url` switching. Support direct calls to major providers plus OpenRouter for exotic models and LM Studio for local/on-prem operation.

## Motivation

- **Political**: local operation via LM Studio enables data sovereignty conversations for EFSA compliance — prompts and documents never leave the network.
- **Flexibility**: mix providers per role (cheap selector on GPT, quality answerer on Claude) without maintaining separate SDK integrations.
- **Simplicity**: one SDK, one call pattern, one streaming interface. Drop the `anthropic` dependency entirely.

## Providers

| Provider | Base URL | API Key Env Var | Use case |
|---|---|---|---|
| `openai` | *(default)* | `OPENAI_API_KEY` | GPT models, selector default |
| `anthropic` | `https://api.anthropic.com/v1/` | `ANTHROPIC_API_KEY` | Claude models, answerer default |
| `google` | `https://generativelanguage.googleapis.com/v1beta/openai/` | `GOOGLE_API_KEY` | Gemini models |
| `mistral` | `https://api.mistral.ai/v1` | `MISTRAL_API_KEY` | Mistral models |
| `openrouter` | `https://openrouter.ai/api/v1` | `OPENROUTER_API_KEY` | Chinese/exotic models (DeepSeek etc.) |
| `lmstudio` | `http://localhost:1234/v1` | *(none)* | Local/on-prem, data sovereignty |

## Model String Format

Model strings use `provider/model-name` format:

```
anthropic/claude-sonnet-4-6
openai/gpt-5.4-mini
lmstudio/llama-3-8b
openrouter/deepseek/deepseek-r1
```

Bare names auto-resolve for backward compatibility:

| Prefix | Resolves to |
|---|---|
| `claude-*` | `anthropic` |
| `gpt-*` | `openai` |
| `gemini-*` | `google` |
| `mistral-*` | `mistral` |

Unrecognized bare names fail with a clear error listing the expected `provider/model` format.

## Configuration

Two env vars control which models are used (unchanged from today):

```
WIKI_SELECTOR_MODEL=openai/gpt-5.4-mini
WIKI_ANSWERER_MODEL=anthropic/claude-sonnet-4-6
```

Bare names still work: `gpt-5.4-mini` and `claude-sonnet-4-6` auto-resolve. Each role can independently use a different provider.

API key env vars are only required for the providers actually in use. Running with `lmstudio/llama-3-8b` for both roles requires no API keys at all.

## Architecture

### Provider Registry + Client Factory (`wiki_api/providers.py`)

New module. Single source of truth for provider configuration.

**`resolve_provider(model_str) → (provider_name, model_id)`**: Splits on the first `/` only (so `openrouter/deepseek/deepseek-r1` → provider `openrouter`, model `deepseek/deepseek-r1`). Falls back to prefix matching for bare names. Returns the provider key and the model ID to pass to the API.

**`client_for_model(model_str) → OpenAI`**: Calls `resolve_provider`, looks up the provider's `base_url` and `key_env`, returns an `OpenAI(base_url=..., api_key=...)` instance. Clients are cached in a module-level dict keyed by provider name (one client per provider, reused across calls). Construction is lazy — a client is built on first use, not at import. Missing API keys raise a clear error at construction time (first request using that provider), not silently at call time. Providers that are configured but never used don't require their API key to be set.

### Unified Selector (`wiki_api/page_selector.py`)

Replace `OpenAIWikiPageSelector` + `AnthropicWikiPageSelector` with a single `WikiPageSelector` class.

**Interface**: `run({"question": str}) → PageSelectionResult` (unchanged).

**Implementation**:
- Constructs client via `client_for_model(self.model)`
- Calls `client.chat.completions.create()` with:
  - `model`: the resolved model ID
  - `messages`: system prompt + user JSON payload (`{question, wiki_index}`)
  - `response_format`: `{"type": "json_object"}` to encourage structured output
- Parses response via `response.choices[0].message.content`
- JSON extraction fallback (`_extract_json_payload`) stays as a safety net for models that ignore `response_format`
- No streaming (selector output is small and fast)

**Removed**: Anthropic tool_use path, OpenAI `responses.create()` path, per-provider selector classes.

**Routing in `app.py`**: `get_selector_runner()` simplifies to `WikiPageSelector(model=env_var)` — no provider dispatch logic.

### Unified Answerer (`wiki_api/answerer.py`)

Replace `AnthropicChemMonAnswerer` with a single `WikiAnswerer` class.

**Interface**: `run(question, pages) → AnswerResult` and `stream(question, pages) → Iterator[AnswerStreamEvent]` (unchanged).

**`run()` implementation**:
- Constructs client via `client_for_model(self.model)`
- Calls `client.chat.completions.create(stream=False)` with:
  - `model`: the resolved model ID
  - `messages`: system prompt + user JSON payload (`{question, pages}`)
- Parses `response.choices[0].message.content` via `_extract_json_payload`
- Returns `AnswerResult` with answer, citations, token summary, timing

**`stream()` implementation with auto-fallback**:
- Tries `client.chat.completions.create(stream=True)`
- On success: iterates `chunk.choices[0].delta.content` for each chunk, yields `{"type": "delta", "text": text}`
- On stream completion: reassembles full text, extracts JSON payload, yields `{"type": "final", "result": AnswerResult}` with token summary from the final chunk's `usage` field
- **Fallback**: if the streaming call raises an exception (provider doesn't support it, LM Studio flaky on a model, network issue), catches the error, calls `run()` instead, and emits:
  1. `{"type": "delta", "text": full_answer}` — entire answer as one delta
  2. `{"type": "final", "result": answer_result}` — the complete result

  The SSE layer in `app.py` consumes the same iterator interface either way. The UI sees either progressive deltas or one big delta — both work.

**Token tracking normalization**:
- OpenAI SDK returns `usage.prompt_tokens` / `usage.completion_tokens`
- Anthropic SDK returned `usage.input_tokens` / `usage.output_tokens`
- Normalize into one internal format: `{"input_tokens", "output_tokens", "total_tracked_tokens"}`. Map field names in `_usage_dict()` based on which fields are present.
- LM Studio and some providers may not return usage at all — default to zeros.

### App orchestration (`wiki_api/app.py`)

The flow stays the same: selector → read pages → graph expansion → answerer → response.

Changes:
- `get_selector_runner()`: drops the `if model.startswith("gpt-")` dispatch. Returns `WikiPageSelector(model=env_var)`.
- `get_answerer_runner()`: drops the Anthropic-specific builder. Returns `WikiAnswerer(model=env_var)`.
- `build_anthropic_client()` and `build_openai_client()` functions: deleted. Client construction moves to `providers.py`.
- Protocol types (`AnthropicMessagesClient`, `AnthropicClientProtocol`): deleted. Tests mock the `OpenAI` client instead.

### Dependency changes

- **Remove**: `anthropic` from `requirements.txt` / `pyproject.toml`
- **Keep**: `openai` (already present)
- **No additions**

### Environment file (`.env.example`)

```
# Required — set keys only for providers you use.
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
# GOOGLE_API_KEY=
# MISTRAL_API_KEY=
# OPENROUTER_API_KEY=

# Model selection — use provider/model format.
# Bare names auto-resolve (claude-* → anthropic, gpt-* → openai).
WIKI_SELECTOR_MODEL=openai/gpt-5.4-mini
WIKI_ANSWERER_MODEL=anthropic/claude-sonnet-4-6

# For local models via LM Studio:
# WIKI_SELECTOR_MODEL=lmstudio/llama-3-8b
# WIKI_ANSWERER_MODEL=lmstudio/llama-3-8b
# (No API keys needed for lmstudio)
```

## Files Changed

| File | Change |
|---|---|
| `wiki_api/providers.py` | **New** — provider registry, model string parser, client cache |
| `wiki_api/page_selector.py` | Rewrite — two classes → one `WikiPageSelector` |
| `wiki_api/answerer.py` | Rewrite — one class → one `WikiAnswerer` |
| `wiki_api/app.py` | Simplify — remove provider dispatch, delete client builders |
| `.env.example` | Add new key env vars, document `provider/model` format |
| `requirements.txt` or `pyproject.toml` | Remove `anthropic` |
| `tests/test_page_selector.py` | Update mocks to `OpenAI` client |
| `tests/test_answerer.py` | Update mocks to `OpenAI` client |

## What Stays the Same

- `WikiStore`, page reading, graph expansion logic
- `app.py` orchestration flow shape (selector → pages → expand → answerer → response)
- SSE streaming endpoint — consumes same `stream()` iterator
- All dataclasses (`PageSelectionResult`, `AnswerResult`, `PageSummary`, `AnswerStreamEvent`)
- System prompts (`SELECTION_SYSTEM_PROMPT`, `ANSWERER_SYSTEM_PROMPT`)
- The deploy repo UI — zero changes

## Out of Scope

- Per-request model override from the UI (future enhancement)
- Model-specific prompt tuning (same prompts for all providers for now)
- Per-provider cost calculation (different pricing models) — use whatever `usage` the API returns
- Retry/failover logic between providers
- Model capability discovery or validation

## Acceptance Criteria

1. `WIKI_SELECTOR_MODEL=openai/gpt-5.4-mini` + `WIKI_ANSWERER_MODEL=anthropic/claude-sonnet-4-6` produces the same quality answers as today.
2. Swapping to `WIKI_ANSWERER_MODEL=openai/gpt-4o` works without code changes — just env var.
3. `WIKI_ANSWERER_MODEL=lmstudio/llama-3-8b` connects to `localhost:1234`, no API key needed. If streaming fails, auto-falls back to non-streaming.
4. Bare model names (`gpt-5.4-mini`, `claude-sonnet-4-6`) still work (backward compat).
5. Invalid provider or missing API key fails fast with a clear error message at startup, not at first request.
6. SSE streaming from `/wiki/ask?stream=true` works for all providers that support it, and degrades gracefully for those that don't.
7. `anthropic` is no longer in the dependency list.
8. All existing tests pass (updated to mock the OpenAI client).
