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
