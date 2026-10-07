import asyncio
import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
import httpx

from wiki_api.answerer import WikiAnswerer


ANSWER = json.dumps({"answer": "Complete answer.", "citations": ["vmpr-reporting.md"]})


def response(text=ANSWER, reason="stop", output=30):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=text), finish_reason=reason)],
        usage=SimpleNamespace(prompt_tokens=100, completion_tokens=output),
    )


def chunks(text=ANSWER, reason="stop", output=30):
    return iter([
        SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=text), finish_reason=reason)], usage=None),
        SimpleNamespace(choices=[], usage=SimpleNamespace(prompt_tokens=100, completion_tokens=output)),
    ])


def answerer(*responses, **kwargs):
    client = MagicMock()
    client.chat.completions.create.side_effect = responses
    return WikiAnswerer(client=client, model_id="claude-sonnet-5-5", **kwargs), client


@pytest.mark.parametrize("partial", ["", '{"answer":"cut off', ANSWER])
def test_retry_discards_token_limited_response_and_counts_both_calls(partial):
    runner, client = answerer(response(partial, "length", 8192), response())
    result = runner.run("question", [])
    assert result.answer == "Complete answer."
    calls = client.chat.completions.create.call_args_list
    assert [c.kwargs["max_tokens"] for c in calls] == [8192, 16384]
    assert calls[0].kwargs["messages"] == calls[1].kwargs["messages"]
    assert result.token_summary["calls"] == 2
    assert result.token_summary["input_tokens"] == 200
    assert result.token_summary["output_tokens"] == 8222
    assert result.timing_summary["calls"] == 2
    assert [c["stop_reason"] for c in result.timing_summary["per_call"]] == ["length", "stop"]


def test_second_token_limit_fails_without_returning_partial_answer():
    runner, client = answerer(response("", "length"), response(ANSWER, "max_tokens"))
    with pytest.raises(RuntimeError, match="output limit"):
        runner.run("question", [])
    assert client.chat.completions.create.call_count == 2


def test_retry_ceiling_is_bounded_and_explicit_budget_is_respected():
    runner, client = answerer(response("", "length"), max_tokens=16384)
    with pytest.raises(RuntimeError, match="output limit"):
        runner.run("question", [])
    assert client.chat.completions.create.call_count == 1
    assert client.chat.completions.create.call_args.kwargs["max_tokens"] == 16384


def test_older_models_keep_their_existing_budget():
    client = MagicMock()
    client.chat.completions.create.return_value = response()
    runner = WikiAnswerer(client=client, model_id="claude-sonnet-4-6")
    runner.run("question", [])
    assert client.chat.completions.create.call_args.kwargs["max_tokens"] == 2000


def test_empty_success_response_is_not_returned_as_an_answer():
    runner, _ = answerer(response(""))
    with pytest.raises(RuntimeError, match="no answer"):
        runner.run("question", [])


def test_stream_retries_only_before_visible_text_and_counts_thinking_attempt():
    runner, client = answerer(chunks("", "length", 8192), chunks())
    events = list(runner.stream("question", []))
    assert "".join(e["text"] for e in events if e["type"] == "delta") == ANSWER
    result = events[-1]["result"]
    assert result.answer == "Complete answer."
    assert result.token_summary["calls"] == 2
    assert result.token_summary["output_tokens"] == 8222
    assert result.timing_summary["calls"] == 2
    assert [c.kwargs["max_tokens"] for c in client.chat.completions.create.call_args_list] == [8192, 16384]


def test_stream_with_visible_truncation_never_returns_success_or_appends_a_retry():
    runner, client = answerer(chunks('{"answer":"partial', "length"))
    events = []
    with pytest.raises(RuntimeError, match="output limit"):
        for event in runner.stream("question", []):
            events.append(event)
    assert [e["type"] for e in events] == ["delta"]
    assert client.chat.completions.create.call_count == 1


def test_stream_stops_after_one_retry_when_thinking_exhausts_both_attempts():
    runner, client = answerer(chunks("", "length"), chunks("", "length"))
    with pytest.raises(RuntimeError, match="output limit"):
        list(runner.stream("question", []))
    assert client.chat.completions.create.call_count == 2


def test_stream_without_a_completion_status_is_not_successful():
    runner, _ = answerer(chunks(ANSWER, None))
    with pytest.raises(RuntimeError, match="completion status"):
        list(runner.stream("question", []))


def test_truncated_stream_endpoint_emits_error_and_never_done(monkeypatch):
    import wiki_api.app as app_module
    from wiki_api.page_selector import PageSelectionResult

    selection = PageSelectionResult(
        pages_used=["vmpr-reporting.md"], tool_trace=[],
        token_summary={"calls": 0, "total_tracked_tokens": 0}, timing_summary={},
    )
    selector = SimpleNamespace(max_pages=6, model_id="test-selector", run=lambda _: selection)
    runner, _ = answerer(chunks('{"answer":"partial', "length"))
    monkeypatch.setattr(app_module, "selector_runner", selector)
    monkeypatch.setattr(app_module, "answerer_runner", runner)

    async def request():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app_module.app), base_url="http://test") as client:
            return await client.post("/wiki/ask", json={"question": "VMPR?", "stream": True})

    result = asyncio.run(request())
    assert "event: error" in result.text
    assert "output limit" in result.text
    assert "event: done" not in result.text
