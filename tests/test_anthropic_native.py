"""Anthropic models through the native Messages API: cached catalogue, enforced JSON, streaming."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import wiki_api.answerer as A
import wiki_api.page_selector as S
from wiki_api.jev_selector import JevWikiPageSelector, make_selector
from wiki_api.wiki_store import WikiStore

ROOT = Path(__file__).resolve().parents[1]
STORE = WikiStore(ROOT)


def message(text, stop="end_turn", **usage):
    counts = {"input_tokens": 100, "output_tokens": 20, "cache_creation_input_tokens": 0,
              "cache_read_input_tokens": 0, **usage}
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)], stop_reason=stop,
                           usage=SimpleNamespace(**counts))


def native(monkeypatch, module, reply):
    client = MagicMock()
    client.messages.create.return_value = reply
    monkeypatch.setattr(module, "native_client", lambda: client)
    return client


def test_selector_caches_rules_and_catalogue_and_enforces_json(monkeypatch):
    client = native(monkeypatch, S, message(json.dumps({"page_names": ["pesticide-reporting.md"]}),
                                            cache_read_input_tokens=5600))
    result = S.WikiPageSelector(store=STORE, model_str="anthropic/claude-haiku-5-5").run({"question": "q"})
    kwargs = client.messages.create.call_args.kwargs
    assert kwargs["model"] == "claude-haiku-5-5"
    system = kwargs["system"]
    assert system[-1]["cache_control"] == {"type": "ephemeral"} and "Topic catalog:" in system[-1]["text"]
    assert "q" in kwargs["messages"][0]["content"] and "Topic catalog" not in kwargs["messages"][0]["content"]
    assert kwargs["output_config"]["format"]["schema"]["required"] == ["page_names"]
    assert result.pages_used == ["pesticide-reporting.md"]
    assert result.token_summary["cache_read_input_tokens"] == 5600


def test_answerer_enforces_json_and_marks_its_instructions_for_caching(monkeypatch):
    client = native(monkeypatch, A, message(json.dumps({"answer": "Yes (a.md)", "citations": ["a.md"]})))
    result = A.WikiAnswerer(model_str="anthropic/claude-sonnet-5-5").run(question="q", pages=[])
    kwargs = client.messages.create.call_args.kwargs
    assert kwargs["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert kwargs["output_config"]["format"]["schema"]["required"] == ["answer", "citations"]
    assert kwargs["max_tokens"] == 8192
    assert result.answer == "Yes (a.md)" and result.citations == ["a.md"]


def test_answerer_streams_text_and_records_usage(monkeypatch):
    client = MagicMock()
    stream = MagicMock()
    stream.__enter__.return_value = stream
    stream.text_stream = iter(['{"answer": "Yes', ' (a.md)", "citations": ["a.md"]}'])
    stream.get_final_message.return_value = message("", output_tokens=7)
    client.messages.stream.return_value = stream
    monkeypatch.setattr(A, "native_client", lambda: client)
    events = list(A.WikiAnswerer(model_str="anthropic/claude-sonnet-5-5").stream(question="q", pages=[]))
    assert [e["text"] for e in events if e["type"] == "delta"] == ['{"answer": "Yes', ' (a.md)", "citations": ["a.md"]}']
    final = events[-1]["result"]
    assert final.answer == "Yes (a.md)" and final.token_summary["output_tokens"] == 7


def test_answerer_retries_once_with_a_larger_budget_when_cut_off(monkeypatch):
    client = native(monkeypatch, A, None)
    client.messages.create.side_effect = [message("", stop="max_tokens"),
                                          message(json.dumps({"answer": "ok", "citations": []}))]
    result = A.WikiAnswerer(model_str="anthropic/claude-sonnet-5-5").run(question="q", pages=[])
    budgets = [c.kwargs["max_tokens"] for c in client.messages.create.call_args_list]
    assert budgets == [8192, 16384] and result.answer == "ok"


def test_jev_routing_is_unaffected(monkeypatch):
    monkeypatch.setattr(S, "native_client", lambda: MagicMock())
    assert isinstance(make_selector(store=STORE, model_str="jev-1.13.0"), JevWikiPageSelector)
    assert make_selector(store=STORE, model_str="anthropic/claude-haiku-5-5").native is True


def test_cache_reads_and_writes_are_priced():
    from wiki_api.app import _compute_call_cost
    base = {"model": "claude-haiku-5-5", "calls": 1, "input_tokens": 1_000_000, "output_tokens": 0}
    assert _compute_call_cost(base) == 0.10
    assert round(_compute_call_cost({**base, "input_tokens": 0, "cache_read_input_tokens": 1_000_000}), 6) == 0.01
    assert round(_compute_call_cost({**base, "input_tokens": 0, "cache_creation_input_tokens": 1_000_000}), 6) == 0.125
