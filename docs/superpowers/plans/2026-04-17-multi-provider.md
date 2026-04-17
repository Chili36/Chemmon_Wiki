# Multi-Provider LLM Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the dual-SDK (Anthropic + OpenAI) architecture with a single OpenAI SDK routing to any provider via `base_url` switching, supporting 6 providers including local LM Studio.

**Architecture:** New `providers.py` module handles model-string parsing (`provider/model` format) and client construction. `WikiPageSelector` and `WikiAnswerer` each become a single class using `chat.completions.create()`. Streaming auto-falls-back to blocking when the provider doesn't support it.

**Tech Stack:** Python 3.12, `openai>=2.0`, `fastapi`, `pytest`. Drop `anthropic` dependency.

**Spec reference:** `docs/superpowers/specs/2026-04-17-multi-provider-design.md`

**Working directory:** `/Users/davidfoster/Dev/Chemmon_Wiki`
**Branch:** `feat/multi-provider`
**Test runner:** `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/ -v`

---

### Task 1: Provider Registry (`providers.py`)

**Files:**
- Create: `wiki_api/providers.py`
- Create: `tests/test_providers.py`

- [ ] **Step 1: Write tests for `resolve_provider`**

```python
# tests/test_providers.py
from __future__ import annotations

import pytest

from wiki_api.providers import resolve_provider, ProviderError


def test_explicit_provider_model():
    assert resolve_provider("anthropic/claude-sonnet-4-6") == ("anthropic", "claude-sonnet-4-6")


def test_explicit_provider_nested_model():
    assert resolve_provider("openrouter/deepseek/deepseek-r1") == ("openrouter", "deepseek/deepseek-r1")


def test_bare_claude_resolves_to_anthropic():
    assert resolve_provider("claude-sonnet-4-6") == ("anthropic", "claude-sonnet-4-6")


def test_bare_gpt_resolves_to_openai():
    assert resolve_provider("gpt-5.4-mini") == ("openai", "gpt-5.4-mini")


def test_bare_gemini_resolves_to_google():
    assert resolve_provider("gemini-2.5-pro") == ("google", "gemini-2.5-pro")


def test_bare_mistral_resolves_to_mistral():
    assert resolve_provider("mistral-large") == ("mistral", "mistral-large")


def test_lmstudio_provider():
    assert resolve_provider("lmstudio/llama-3-8b") == ("lmstudio", "llama-3-8b")


def test_unknown_bare_name_raises():
    with pytest.raises(ProviderError, match="provider/model"):
        resolve_provider("some-unknown-model")


def test_unknown_provider_raises():
    with pytest.raises(ProviderError, match="nope"):
        resolve_provider("nope/some-model")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/test_providers.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'wiki_api.providers'`

- [ ] **Step 3: Implement `providers.py`**

```python
# wiki_api/providers.py
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from openai import OpenAI


class ProviderError(ValueError):
    pass


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str | None
    key_env: str | None


PROVIDERS: dict[str, ProviderConfig] = {
    "openai": ProviderConfig(
        name="openai",
        base_url=None,
        key_env="OPENAI_API_KEY",
    ),
    "anthropic": ProviderConfig(
        name="anthropic",
        base_url="https://api.anthropic.com/v1/",
        key_env="ANTHROPIC_API_KEY",
    ),
    "google": ProviderConfig(
        name="google",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        key_env="GOOGLE_API_KEY",
    ),
    "mistral": ProviderConfig(
        name="mistral",
        base_url="https://api.mistral.ai/v1",
        key_env="MISTRAL_API_KEY",
    ),
    "openrouter": ProviderConfig(
        name="openrouter",
        base_url="https://openrouter.ai/api/v1",
        key_env="OPENROUTER_API_KEY",
    ),
    "lmstudio": ProviderConfig(
        name="lmstudio",
        base_url="http://localhost:1234/v1",
        key_env=None,
    ),
}

_BARE_PREFIX_MAP: list[tuple[str, str]] = [
    ("claude-", "anthropic"),
    ("gpt-", "openai"),
    ("gemini-", "google"),
    ("mistral-", "mistral"),
]

_client_cache: dict[str, OpenAI] = {}


def resolve_provider(model_str: str) -> tuple[str, str]:
    if "/" in model_str:
        provider_name, model_id = model_str.split("/", 1)
        if provider_name not in PROVIDERS:
            raise ProviderError(
                f"Unknown provider '{provider_name}'. "
                f"Known providers: {', '.join(sorted(PROVIDERS))}."
            )
        return provider_name, model_id

    for prefix, provider_name in _BARE_PREFIX_MAP:
        if model_str.startswith(prefix):
            return provider_name, model_str

    raise ProviderError(
        f"Cannot infer provider from bare model name '{model_str}'. "
        f"Use provider/model format (e.g., anthropic/{model_str})."
    )


def client_for_model(model_str: str) -> tuple[OpenAI, str]:
    provider_name, model_id = resolve_provider(model_str)
    if provider_name in _client_cache:
        return _client_cache[provider_name], model_id

    cfg = PROVIDERS[provider_name]
    api_key: str | None = None
    if cfg.key_env:
        api_key = os.environ.get(cfg.key_env)
        if not api_key:
            raise ProviderError(
                f"{cfg.key_env} is not set (required for provider '{provider_name}')"
            )

    kwargs: dict[str, Any] = {}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if api_key:
        kwargs["api_key"] = api_key
    else:
        kwargs["api_key"] = "not-needed"

    client = OpenAI(**kwargs)
    _client_cache[provider_name] = client
    return client, model_id


def clear_client_cache() -> None:
    _client_cache.clear()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/test_providers.py -v`
Expected: all 9 tests PASS.

- [ ] **Step 5: Add test for `client_for_model`**

Append to `tests/test_providers.py`:

```python
from unittest.mock import patch

from wiki_api.providers import client_for_model, clear_client_cache


def test_client_for_model_returns_openai_instance():
    clear_client_cache()
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        client, model_id = client_for_model("openai/gpt-5.4-mini")
        assert model_id == "gpt-5.4-mini"
        assert isinstance(client, OpenAI)


def test_client_for_model_lmstudio_no_key_needed():
    clear_client_cache()
    client, model_id = client_for_model("lmstudio/llama-3-8b")
    assert model_id == "llama-3-8b"
    assert isinstance(client, OpenAI)


def test_client_for_model_missing_key_raises():
    clear_client_cache()
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ProviderError, match="ANTHROPIC_API_KEY"):
            client_for_model("anthropic/claude-sonnet-4-6")


def test_client_cache_reuses_instance():
    clear_client_cache()
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        c1, _ = client_for_model("openai/gpt-5.4-mini")
        c2, _ = client_for_model("openai/gpt-4o")
        assert c1 is c2
```

- [ ] **Step 6: Run all provider tests**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/test_providers.py -v`
Expected: all 13 tests PASS.

- [ ] **Step 7: Commit**

```bash
cd /Users/davidfoster/Dev/Chemmon_Wiki && git add wiki_api/providers.py tests/test_providers.py
git commit -m "Add provider registry with model-string parsing and client factory"
```

---

### Task 2: Unified Page Selector

**Files:**
- Modify: `wiki_api/page_selector.py`
- Modify: `tests/test_page_selector.py`

- [ ] **Step 1: Write tests for the new `WikiPageSelector`**

Replace the contents of `tests/test_page_selector.py` with:

```python
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

from wiki_api.page_selector import WikiPageSelector
from wiki_api.wiki_store import WikiStore


def _chat_response(*, content: str, prompt_tokens: int = 100, completion_tokens: int = 25):
    msg = MagicMock()
    msg.content = content
    choice = MagicMock()
    choice.message = msg
    choice.finish_reason = "stop"
    usage = MagicMock()
    usage.prompt_tokens = prompt_tokens
    usage.completion_tokens = completion_tokens
    resp = MagicMock()
    resp.choices = [choice]
    resp.usage = usage
    return resp


def _fake_client(response):
    client = MagicMock()
    client.chat.completions.create.return_value = response
    return client


def _store() -> WikiStore:
    return WikiStore(Path("/Users/davidfoster/Dev/Chemmon_Wiki"))


def test_selector_picks_pages_from_json():
    payload = json.dumps({"page_names": ["chemmon-overview.md"]})
    client = _fake_client(_chat_response(content=payload))

    selector = WikiPageSelector(store=_store(), client=client, model_id="fake-model")
    result = selector.run({"question": "What is ChemMon?"})

    assert "index.md" in result.pages_used
    assert "chemmon-overview.md" in result.pages_used
    assert result.token_summary["calls"] == 1

    call_kwargs = client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "fake-model"
    msgs = call_kwargs["messages"]
    assert msgs[0]["role"] == "system"
    assert "ChemMon" in msgs[0]["content"]
    user_payload = json.loads(msgs[1]["content"])
    assert "question" in user_payload
    assert "wiki_index" in user_payload


def test_selector_handles_fenced_json():
    payload = '```json\n{"page_names": ["vmpr-reporting.md"]}\n```'
    client = _fake_client(_chat_response(content=payload))

    selector = WikiPageSelector(store=_store(), client=client, model_id="fake-model")
    result = selector.run({"question": "VMPR rules?"})

    assert "vmpr-reporting.md" in result.pages_used


def test_selector_handles_empty_page_list():
    payload = json.dumps({"page_names": []})
    client = _fake_client(_chat_response(content=payload))

    selector = WikiPageSelector(store=_store(), client=client, model_id="fake-model")
    result = selector.run({"question": "Hello"})

    assert result.pages_used == ["index.md"]


def test_selector_handles_plain_text_fallback():
    client = _fake_client(_chat_response(content="I don't know which pages to select."))

    selector = WikiPageSelector(store=_store(), client=client, model_id="fake-model")
    result = selector.run({"question": "Something weird"})

    assert result.pages_used == ["index.md"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/test_page_selector.py -v`
Expected: FAIL — `ImportError: cannot import name 'WikiPageSelector'`

- [ ] **Step 3: Rewrite `page_selector.py`**

Replace `wiki_api/page_selector.py` with the unified version. Keep the helper functions (`_extract_json_payload`, `_read_pages_payload`, `_aggregate_usage`, `_aggregate_timing`, `PageSelectionResult`, `SELECTION_SYSTEM_PROMPT`). Delete: `OpenAIWikiPageSelector`, `AnthropicWikiPageSelector`, `build_anthropic_client`, `build_openai_client`, `_openai_usage_dict`, `_selection_payload_from_response`, `AnthropicMessagesClient`, `AnthropicClientProtocol`, `READ_WIKI_PAGES_TOOL`, `TOOLS`.

New `WikiPageSelector` class:

```python
class WikiPageSelector:
    def __init__(
        self,
        *,
        store: WikiStore,
        client: Any | None = None,
        model_id: str | None = None,
        model_str: str | None = None,
        max_pages: int = 6,
    ):
        self.store = store
        self.max_pages = max_pages
        if client and model_id:
            self.client = client
            self.model_id = model_id
        else:
            resolved_str = model_str or os.getenv("WIKI_SELECTOR_MODEL", "openai/gpt-5.4-mini")
            self.client, self.model_id = client_for_model(resolved_str)

    def run(self, payload: dict[str, Any]) -> PageSelectionResult:
        selector_started = time.perf_counter()
        index_content = self.store.read_page("index.md").content
        llm_started = time.perf_counter()

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": SELECTION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {"question": payload["question"], "wiki_index": index_content},
                        ensure_ascii=False,
                    ),
                },
            ],
            response_format={"type": "json_object"},
        )

        llm_duration_ms = int((time.perf_counter() - llm_started) * 1000)
        finish_reason = response.choices[0].finish_reason if response.choices else None
        usage = _normalize_usage(response.usage, finish_reason)
        timing_trace = [{"call_number": 1, "duration_ms": llm_duration_ms, "stop_reason": finish_reason}]

        output_text = response.choices[0].message.content or "" if response.choices else ""
        try:
            data = _extract_json_payload(output_text)
            raw = data.get("page_names", []) if isinstance(data, dict) else []
            if not isinstance(raw, list):
                raw = [raw]
            selected_page_names = [str(name) for name in raw]
        except (ValueError, json.JSONDecodeError, AttributeError):
            selected_page_names = []

        pages_read: list[str] = []
        tool_trace: list[dict[str, Any]] = []
        _read_pages_payload(
            store=self.store,
            requested_page_names=selected_page_names,
            max_pages=self.max_pages,
            pages_read=pages_read,
            tool_trace=tool_trace,
        )

        return PageSelectionResult(
            pages_used=list(dict.fromkeys(["index.md", *pages_read])),
            tool_trace=tool_trace,
            token_summary=_aggregate_usage([usage], self.model_id),
            timing_summary={
                **_aggregate_timing(timing_trace),
                "selector_wall_time_ms": int((time.perf_counter() - selector_started) * 1000),
            },
        )
```

Also add `_normalize_usage` to replace both `_usage_dict` and `_openai_usage_dict`:

```python
def _normalize_usage(usage: Any, finish_reason: str | None) -> dict[str, int | str | None]:
    if usage is None:
        return {
            "stop_reason": finish_reason,
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "total_tracked_tokens": 0,
        }
    input_tokens = int(getattr(usage, "prompt_tokens", 0) or getattr(usage, "input_tokens", 0) or 0)
    output_tokens = int(getattr(usage, "completion_tokens", 0) or getattr(usage, "output_tokens", 0) or 0)
    cache_creation = int(getattr(usage, "cache_creation_input_tokens", 0) or 0)
    cache_read = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    return {
        "stop_reason": finish_reason,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_creation_input_tokens": cache_creation,
        "cache_read_input_tokens": cache_read,
        "total_tracked_tokens": input_tokens + output_tokens + cache_creation + cache_read,
    }
```

Update imports at the top: remove `from anthropic import Anthropic`, add `from .providers import client_for_model`.

- [ ] **Step 4: Run tests**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/test_page_selector.py -v`
Expected: all 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/davidfoster/Dev/Chemmon_Wiki && git add wiki_api/page_selector.py tests/test_page_selector.py
git commit -m "Unify page selector into single WikiPageSelector using chat.completions"
```

---

### Task 3: Unified Answerer — `run()` method

**Files:**
- Modify: `wiki_api/answerer.py`
- Modify: `tests/test_answerer.py`

- [ ] **Step 1: Write tests for the new `WikiAnswerer.run()`**

Replace `tests/test_answerer.py` with:

```python
from __future__ import annotations

import json
from unittest.mock import MagicMock

from wiki_api.answerer import WikiAnswerer


def _chat_response(*, content: str, prompt_tokens: int = 200, completion_tokens: int = 50):
    msg = MagicMock()
    msg.content = content
    choice = MagicMock()
    choice.message = msg
    choice.finish_reason = "stop"
    usage = MagicMock()
    usage.prompt_tokens = prompt_tokens
    usage.completion_tokens = completion_tokens
    resp = MagicMock()
    resp.choices = [choice]
    resp.usage = usage
    return resp


def _fake_client(response):
    client = MagicMock()
    client.chat.completions.create.return_value = response
    return client


def test_answerer_returns_answer_with_citations():
    answer_payload = {
        "answer": "Yes, F33 is mandatory for acrylamide even when implicit.",
        "citations": ["acrylamide-rules.md"],
    }
    client = _fake_client(_chat_response(content=json.dumps(answer_payload)))

    answerer = WikiAnswerer(client=client, model_id="fake-model")
    result = answerer.run(
        question="Do I need F33 for acrylamide?",
        pages=[{"page_name": "acrylamide-rules.md", "content": "F33 is mandatory for acrylamide."}],
    )

    assert result.answer == "Yes, F33 is mandatory for acrylamide even when implicit."
    assert result.citations == ["acrylamide-rules.md"]
    assert result.token_summary["calls"] == 1
    assert result.timing_summary["answerer_wall_time_ms"] >= 0

    call_kwargs = client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "fake-model"
    assert call_kwargs["stream"] is False
    msgs = call_kwargs["messages"]
    assert "ChemMon" in msgs[0]["content"]
    payload = json.loads(msgs[1]["content"])
    assert payload["question"] == "Do I need F33 for acrylamide?"


def test_answerer_handles_plain_text_response():
    client = _fake_client(_chat_response(content="The wiki does not cover this topic."))

    answerer = WikiAnswerer(client=client, model_id="fake-model")
    result = answerer.run(question="What is the meaning of life?", pages=[])

    assert result.answer == "The wiki does not cover this topic."
    assert result.citations == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/test_answerer.py::test_answerer_returns_answer_with_citations tests/test_answerer.py::test_answerer_handles_plain_text_response -v`
Expected: FAIL — `ImportError: cannot import name 'WikiAnswerer'`

- [ ] **Step 3: Rewrite `answerer.py` with `run()` only (streaming in Task 4)**

Replace `wiki_api/answerer.py`. Keep: `ANSWERER_SYSTEM_PROMPT`, `AnswerResult`, `AnswerStreamDelta`, `AnswerStreamFinal`, `AnswerStreamEvent`, `_extract_json_payload`. Delete: `AnthropicChemMonAnswerer`, `build_anthropic_client`, `AnthropicMessagesClient`, `AnthropicClientProtocol`, `_usage_dict`, `_response_text`, `_get_block_value`, `_resolve_model`.

Add `_normalize_usage` (same as in `page_selector.py` — we'll extract to a shared location in Task 5).

New `WikiAnswerer` class:

```python
from .providers import client_for_model


class WikiAnswerer:
    def __init__(
        self,
        *,
        client: Any | None = None,
        model_id: str | None = None,
        model_str: str | None = None,
        max_tokens: int = 2000,
    ):
        self.max_tokens = max_tokens
        if client and model_id:
            self.client = client
            self.model_id = model_id
        else:
            resolved_str = model_str or os.getenv("WIKI_ANSWERER_MODEL", "anthropic/claude-sonnet-4-6")
            self.client, self.model_id = client_for_model(resolved_str)

    def _build_messages(self, question: str, pages: list[dict[str, Any]]) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": ANSWERER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    {"question": question, "pages": pages},
                    ensure_ascii=False,
                ),
            },
        ]

    def _parse_answer(self, text: str) -> tuple[str, list[str]]:
        data = _extract_json_payload(text)
        if data and "answer" in data:
            return data["answer"], data.get("citations", [])
        return text.strip(), []

    def run(self, question: str, pages: list[dict[str, Any]]) -> AnswerResult:
        answerer_started = time.perf_counter()
        llm_started = time.perf_counter()

        response = self.client.chat.completions.create(
            model=self.model_id,
            max_tokens=self.max_tokens,
            messages=self._build_messages(question, pages),
            stream=False,
        )

        llm_duration_ms = int((time.perf_counter() - llm_started) * 1000)
        finish_reason = response.choices[0].finish_reason if response.choices else None
        usage = _normalize_usage(response.usage, finish_reason)
        text = response.choices[0].message.content or "" if response.choices else ""
        answer, citations = self._parse_answer(text)

        return AnswerResult(
            answer=answer,
            citations=citations,
            token_summary={
                "model": self.model_id,
                "calls": 1,
                **{k: usage[k] for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "total_tracked_tokens")},
                "per_call": [usage],
            },
            timing_summary={
                "calls": 1,
                "llm_time_ms": llm_duration_ms,
                "answerer_wall_time_ms": int((time.perf_counter() - answerer_started) * 1000),
                "per_call": [{"call_number": 1, "duration_ms": llm_duration_ms, "stop_reason": finish_reason}],
            },
        )
```

- [ ] **Step 4: Run tests**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/test_answerer.py -v`
Expected: 2 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/davidfoster/Dev/Chemmon_Wiki && git add wiki_api/answerer.py tests/test_answerer.py
git commit -m "Unify answerer into WikiAnswerer with chat.completions (run only)"
```

---

### Task 4: Answerer Streaming with Auto-Fallback

**Files:**
- Modify: `wiki_api/answerer.py`
- Modify: `tests/test_answerer.py`

- [ ] **Step 1: Write streaming test**

Append to `tests/test_answerer.py`:

```python
def test_answerer_stream_yields_deltas_then_final():
    answer_payload = {
        "answer": "Yes, F33 is mandatory.",
        "citations": ["acrylamide-rules.md"],
    }
    full_text = json.dumps(answer_payload)

    chunk1 = MagicMock()
    chunk1.choices = [MagicMock()]
    chunk1.choices[0].delta = MagicMock()
    chunk1.choices[0].delta.content = full_text[:20]
    chunk1.choices[0].finish_reason = None
    chunk1.usage = None

    chunk2 = MagicMock()
    chunk2.choices = [MagicMock()]
    chunk2.choices[0].delta = MagicMock()
    chunk2.choices[0].delta.content = full_text[20:]
    chunk2.choices[0].finish_reason = "stop"
    chunk2.usage = None

    chunk_final = MagicMock()
    chunk_final.choices = []
    usage = MagicMock()
    usage.prompt_tokens = 200
    usage.completion_tokens = 50
    chunk_final.usage = usage

    client = MagicMock()
    client.chat.completions.create.return_value = iter([chunk1, chunk2, chunk_final])

    answerer = WikiAnswerer(client=client, model_id="fake-model")
    events = list(
        answerer.stream(
            question="Do I need F33?",
            pages=[{"page_name": "acrylamide-rules.md", "content": "F33 is mandatory."}],
        )
    )

    delta_text = "".join(e["text"] for e in events if e["type"] == "delta")
    assert delta_text == full_text

    finals = [e for e in events if e["type"] == "final"]
    assert len(finals) == 1
    result = finals[0]["result"]
    assert result.answer == "Yes, F33 is mandatory."
    assert result.citations == ["acrylamide-rules.md"]

    call_kwargs = client.chat.completions.create.call_args.kwargs
    assert call_kwargs["stream"] is True


def test_answerer_stream_falls_back_on_error():
    answer_payload = {
        "answer": "Fallback answer.",
        "citations": [],
    }

    client = MagicMock()
    client.chat.completions.create.side_effect = [
        Exception("streaming not supported"),
        _chat_response(content=json.dumps(answer_payload)),
    ]

    answerer = WikiAnswerer(client=client, model_id="fake-model")
    events = list(
        answerer.stream(
            question="Something?",
            pages=[],
        )
    )

    assert client.chat.completions.create.call_count == 2
    first_call = client.chat.completions.create.call_args_list[0].kwargs
    assert first_call["stream"] is True
    second_call = client.chat.completions.create.call_args_list[1].kwargs
    assert second_call["stream"] is False

    delta_text = "".join(e["text"] for e in events if e["type"] == "delta")
    assert delta_text == "Fallback answer."

    finals = [e for e in events if e["type"] == "final"]
    assert len(finals) == 1
    assert finals[0]["result"].answer == "Fallback answer."
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/test_answerer.py::test_answerer_stream_yields_deltas_then_final tests/test_answerer.py::test_answerer_stream_falls_back_on_error -v`
Expected: FAIL — `WikiAnswerer` has no `stream` method.

- [ ] **Step 3: Add `stream()` method to `WikiAnswerer`**

Add this method to the `WikiAnswerer` class in `wiki_api/answerer.py`:

```python
    def stream(
        self,
        question: str,
        pages: list[dict[str, Any]],
    ) -> Iterator[AnswerStreamEvent]:
        answerer_started = time.perf_counter()
        llm_started = time.perf_counter()
        accumulated_text = ""
        usage_data: Any = None
        finish_reason: str | None = None

        try:
            response_stream = self.client.chat.completions.create(
                model=self.model_id,
                max_tokens=self.max_tokens,
                messages=self._build_messages(question, pages),
                stream=True,
                stream_options={"include_usage": True},
            )

            for chunk in response_stream:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        accumulated_text += delta.content
                        yield {"type": "delta", "text": delta.content}
                    if chunk.choices[0].finish_reason:
                        finish_reason = chunk.choices[0].finish_reason
                if chunk.usage:
                    usage_data = chunk.usage

        except Exception:
            result = self.run(question, pages)
            yield {"type": "delta", "text": result.answer}
            yield {"type": "final", "result": result}
            return

        llm_duration_ms = int((time.perf_counter() - llm_started) * 1000)
        usage = _normalize_usage(usage_data, finish_reason)
        answer, citations = self._parse_answer(accumulated_text)

        yield {
            "type": "final",
            "result": AnswerResult(
                answer=answer,
                citations=citations,
                token_summary={
                    "model": self.model_id,
                    "calls": 1,
                    **{k: usage[k] for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "total_tracked_tokens")},
                    "per_call": [usage],
                },
                timing_summary={
                    "calls": 1,
                    "llm_time_ms": llm_duration_ms,
                    "answerer_wall_time_ms": int((time.perf_counter() - answerer_started) * 1000),
                    "per_call": [{"call_number": 1, "duration_ms": llm_duration_ms, "stop_reason": finish_reason}],
                },
            ),
        }
```

- [ ] **Step 4: Run all answerer tests**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/test_answerer.py -v`
Expected: all 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/davidfoster/Dev/Chemmon_Wiki && git add wiki_api/answerer.py tests/test_answerer.py
git commit -m "Add streaming with auto-fallback to WikiAnswerer"
```

---

### Task 5: Extract shared `_normalize_usage` + wire up `app.py`

**Files:**
- Modify: `wiki_api/providers.py` (add `_normalize_usage`)
- Modify: `wiki_api/page_selector.py` (import from providers)
- Modify: `wiki_api/answerer.py` (import from providers)
- Modify: `wiki_api/app.py` (use new classes)

- [ ] **Step 1: Move `_normalize_usage` to `providers.py`**

Add to the end of `wiki_api/providers.py`:

```python
def normalize_usage(usage: Any, finish_reason: str | None) -> dict[str, int | str | None]:
    if usage is None:
        return {
            "stop_reason": finish_reason,
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "total_tracked_tokens": 0,
        }
    input_tokens = int(getattr(usage, "prompt_tokens", 0) or getattr(usage, "input_tokens", 0) or 0)
    output_tokens = int(getattr(usage, "completion_tokens", 0) or getattr(usage, "output_tokens", 0) or 0)
    cache_creation = int(getattr(usage, "cache_creation_input_tokens", 0) or 0)
    cache_read = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    return {
        "stop_reason": finish_reason,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_creation_input_tokens": cache_creation,
        "cache_read_input_tokens": cache_read,
        "total_tracked_tokens": input_tokens + output_tokens + cache_creation + cache_read,
    }
```

- [ ] **Step 2: Update `page_selector.py` and `answerer.py` imports**

In `page_selector.py`, replace the local `_normalize_usage` with:

```python
from .providers import client_for_model, normalize_usage as _normalize_usage
```

In `answerer.py`, replace the local `_normalize_usage` with:

```python
from .providers import client_for_model, normalize_usage as _normalize_usage
```

Delete the local `_normalize_usage` function from both files.

- [ ] **Step 3: Update `app.py`**

Replace the imports at the top of `wiki_api/app.py`:

```python
from .answerer import AnthropicChemMonAnswerer
from .page_selector import AnthropicWikiPageSelector, OpenAIWikiPageSelector
```

with:

```python
from .answerer import WikiAnswerer
from .page_selector import WikiPageSelector
```

Replace `get_selector_runner`:

```python
def get_selector_runner() -> WikiPageSelector:
    global selector_runner
    if selector_runner is None:
        selector_runner = WikiPageSelector(store=store)
    return selector_runner
```

Replace `get_answerer_runner`:

```python
def get_answerer_runner() -> WikiAnswerer:
    global answerer_runner
    if answerer_runner is None:
        answerer_runner = WikiAnswerer()
    return answerer_runner
```

Update the type annotations for the globals:

```python
selector_runner: WikiPageSelector | None = None
answerer_runner: WikiAnswerer | None = None
```

- [ ] **Step 4: Run all tests**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/ -v`
Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/davidfoster/Dev/Chemmon_Wiki && git add wiki_api/providers.py wiki_api/page_selector.py wiki_api/answerer.py wiki_api/app.py
git commit -m "Wire app.py to unified selector/answerer; extract shared normalize_usage"
```

---

### Task 6: Config files + drop anthropic dependency

**Files:**
- Modify: `.env.example`
- Modify: `requirements.txt`

- [ ] **Step 1: Update `.env.example`**

Replace the contents of `.env.example` with:

```
# Required — set keys only for providers you use.
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
# GOOGLE_API_KEY=
# MISTRAL_API_KEY=
# OPENROUTER_API_KEY=

# Model selection — use provider/model format.
# Bare names auto-resolve (claude-* → anthropic, gpt-* → openai).
WIKI_SELECTOR_MODEL=openai/gpt-5.4-mini
WIKI_ANSWERER_MODEL=anthropic/claude-sonnet-4-6

# For local models via LM Studio (no API keys needed):
# WIKI_SELECTOR_MODEL=lmstudio/llama-3-8b
# WIKI_ANSWERER_MODEL=lmstudio/llama-3-8b
```

- [ ] **Step 2: Remove `anthropic` from `requirements.txt`**

Delete the line `anthropic>=0.79,<1.0` from `requirements.txt`.

- [ ] **Step 3: Verify no remaining anthropic imports**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && grep -rn "from anthropic\|import anthropic" wiki_api/ tests/`
Expected: no matches.

- [ ] **Step 4: Run all tests**

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && python -m pytest tests/ -v`
Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/davidfoster/Dev/Chemmon_Wiki && git add .env.example requirements.txt
git commit -m "Update .env.example for multi-provider; drop anthropic dependency"
```

---

### Task 7: Integration Verification

**Files:** None (verification only)

- [ ] **Step 1: Start the API with current env vars**

Ensure `.env` has `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` set, and:
```
WIKI_SELECTOR_MODEL=openai/gpt-5.4-mini
WIKI_ANSWERER_MODEL=anthropic/claude-sonnet-4-6
```

Run: `cd /Users/davidfoster/Dev/Chemmon_Wiki && . .venv/bin/activate && uvicorn wiki_api.app:app --reload --port 8005`

Expected: server starts without import errors.

- [ ] **Step 2: Test non-streaming**

```bash
curl -s -X POST http://127.0.0.1:8005/wiki/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"What is ChemMon?","max_pages":3,"use_graph_expansion":false}' \
  | python3 -m json.tool | head -20
```

Expected: JSON response with `answer`, `citations`, `pages_used`, `trace`.

- [ ] **Step 3: Test streaming**

```bash
curl -s -N -X POST http://127.0.0.1:8005/wiki/ask \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  -d '{"question":"What is ChemMon?","max_pages":3,"use_graph_expansion":false,"stream":true}' \
  --max-time 20 | head -15
```

Expected: SSE events — `event: meta`, then `event: delta` chunks, then `event: done`.

- [ ] **Step 4: Test backward compat with bare model names**

Set `WIKI_SELECTOR_MODEL=gpt-5.4-mini` (no provider prefix) in `.env`, restart uvicorn, re-run the curl from Step 2.

Expected: same result — bare name auto-resolves.

- [ ] **Step 5: Push branch and open PR**

```bash
cd /Users/davidfoster/Dev/Chemmon_Wiki && git push origin feat/multi-provider
```

```bash
gh pr create --repo Chili36/Chemmon_Wiki \
  --title "Multi-provider LLM support via OpenAI SDK base_url switching" \
  --body "$(cat <<'EOF'
## Summary
- Replaces dual Anthropic+OpenAI SDK architecture with a single OpenAI SDK routing to any provider via `base_url`.
- New `providers.py`: model string parser (`provider/model` format), provider registry (6 providers), lazy client cache.
- `WikiPageSelector`: single class replacing `OpenAIWikiPageSelector` + `AnthropicWikiPageSelector`, uses `chat.completions.create()`.
- `WikiAnswerer`: single class replacing `AnthropicChemMonAnswerer`, with streaming auto-fallback (tries `stream=True`, catches failure, falls back to `run()`).
- Drops `anthropic` from dependencies.
- Spec: `docs/superpowers/specs/2026-04-17-multi-provider-design.md`

## Supported providers
| Provider | Base URL | Use case |
|---|---|---|
| openai | default | GPT models |
| anthropic | api.anthropic.com/v1/ | Claude models |
| google | generativelanguage.googleapis.com | Gemini models |
| mistral | api.mistral.ai/v1 | Mistral models |
| openrouter | openrouter.ai/api/v1 | Chinese/exotic models |
| lmstudio | localhost:1234/v1 | Local/on-prem |

## Test plan
- [ ] `pytest tests/ -v` — all unit tests pass
- [ ] Non-streaming curl with `openai/gpt-5.4-mini` selector + `anthropic/claude-sonnet-4-6` answerer
- [ ] SSE streaming curl — meta → delta* → done
- [ ] Bare model names (`gpt-5.4-mini`) auto-resolve
- [ ] Missing API key fails at first request with clear error

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Self-Review Notes

- **Spec coverage:** Provider registry → Task 1. Unified selector → Task 2. Unified answerer run() → Task 3. Streaming with fallback → Task 4. App wiring → Task 5. Config/deps → Task 6. Acceptance criteria 1-8 → Task 7.
- **No placeholders:** All code blocks are complete. All commands have expected outputs.
- **Type consistency:** `WikiPageSelector(store, client, model_id)` signature used in Tasks 2 and 5. `WikiAnswerer(client, model_id)` used in Tasks 3, 4, and 5. `resolve_provider` and `client_for_model` signatures match between Task 1 and all consumers. `_normalize_usage` extracted in Task 5 with same signature used in Tasks 2-4. `AnswerStreamEvent` type alias unchanged from current codebase.
- **Spec gaps found:** None — all 8 acceptance criteria map to verification steps in Task 7.
