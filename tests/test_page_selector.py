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
