from __future__ import annotations

import json
import pytest
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
    return WikiStore(Path(__file__).resolve().parents[1])


def test_selector_picks_pages_from_json():
    payload = json.dumps({"page_names": ["chemmon-overview.md"]})
    client = _fake_client(_chat_response(content=payload))

    selector = WikiPageSelector(store=_store(), client=client, model_id="fake-model")
    result = selector.run({"question": "What is ChemMon?"})

    assert "index.md" not in result.pages_used
    assert "chemmon-overview.md" in result.pages_used
    assert result.token_summary["calls"] == 1

    call_kwargs = client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "fake-model"
    msgs = call_kwargs["messages"]
    assert msgs[0]["role"] == "system"
    assert "ChemMon" in msgs[0]["content"]
    user_payload = json.loads(msgs[1]["content"])
    assert "question" in user_payload
    assert "catalog" in user_payload
    assert user_payload["max_pages"] == 6


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

    assert result.pages_used == []


def test_selector_handles_plain_text_fallback():
    client = _fake_client(_chat_response(content="I don't know which pages to select."))

    selector = WikiPageSelector(store=_store(), client=client, model_id="fake-model")
    with pytest.raises(ValueError, match="page_names array"):
        selector.run({"question": "Something weird"})


@pytest.mark.parametrize("limit", [1, 2, 7])
def test_page_limit_counts_only_topic_evidence(limit):
    store = _store()
    candidates = store.list_pages()[:8]
    names = ["index.md", "README.md", "unknown.md", *candidates, candidates[0]]
    client = _fake_client(_chat_response(content=json.dumps({"page_names": names})))
    selector = WikiPageSelector(store=store, client=client, model_id="fake-model")
    result = selector.run({"question": "test", "max_pages": limit})
    assert result.pages_used == candidates[:limit]
    assert selector.max_pages == 6
    payload = json.loads(client.chat.completions.create.call_args.kwargs["messages"][1]["content"])
    assert payload["max_pages"] == limit
    assert "README.md" not in payload["catalog"]


@pytest.mark.parametrize("content", ['{"page_names":"x.md"}', '{"page_names":[12]}', '{"page_names":["unknown.md"]}'])
def test_selector_rejects_invalid_selections(content):
    selector = WikiPageSelector(store=_store(), client=_fake_client(_chat_response(content=content)), model_id="fake-model")
    with pytest.raises(ValueError):
        selector.run({"question": "test"})
