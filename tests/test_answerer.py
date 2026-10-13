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


# Sonnet 5.5 usually answers in prose with inline "(page.md)" citations and
# ignores a JSON-only instruction; citations must not depend on the envelope.
PROSE_ANSWER = (
    "Per the pinned snapshot, no. Glyphosate is not on the list "
    "(pesticide-residue-definitions-by-food.md). The legislation decides "
    "(pesticide-residue-definition-by-matrix.md; pesticide-residue-definitions-by-food.md)."
)


def test_prose_answer_takes_citations_from_inline_page_names():
    client = _fake_client(_chat_response(content=PROSE_ANSWER))
    result = WikiAnswerer(client=client, model_id="fake-model").run(question="q", pages=[])
    assert result.answer == PROSE_ANSWER
    assert result.citations == ["pesticide-residue-definitions-by-food.md", "pesticide-residue-definition-by-matrix.md"]


def test_prose_followed_by_json_copy_returns_one_answer():
    payload = {"answer": "Short JSON answer (a.md).", "citations": ["b.md"]}
    client = _fake_client(_chat_response(content=PROSE_ANSWER + "\n\n" + json.dumps(payload)))
    result = WikiAnswerer(client=client, model_id="fake-model").run(question="q", pages=[])
    assert result.answer == "Short JSON answer (a.md)."
    assert result.citations == ["b.md", "a.md"]


def test_unverified_provider_gets_plain_text_contract_without_response_format():
    client = _fake_client(_chat_response(content=PROSE_ANSWER))
    WikiAnswerer(client=client, model_id="fake-model").run(question="q", pages=[])
    kwargs = client.chat.completions.create.call_args.kwargs
    assert "response_format" not in kwargs
    system = kwargs["messages"][0]["content"]
    assert "(page-name.md)" in system and "JSON" not in system


def test_structured_provider_sends_strict_schema_and_parses_it():
    payload = {"answer": "GBR28 requires resQualValue (business-rules-gbr-results.md).", "citations": ["x.md"]}
    client = _fake_client(_chat_response(content=json.dumps(payload)))
    result = WikiAnswerer(client=client, model_id="claude-sonnet-5-5", structured_output=True).run(question="q", pages=[])
    kwargs = client.chat.completions.create.call_args.kwargs
    schema = kwargs["response_format"]["json_schema"]
    assert kwargs["response_format"]["type"] == "json_schema" and schema["strict"] is True
    assert schema["schema"]["required"] == ["answer", "citations"]
    assert "(page-name.md)" in kwargs["messages"][0]["content"]
    assert result.answer == payload["answer"]
    assert result.citations == ["x.md", "business-rules-gbr-results.md"]


def test_structured_output_is_enabled_only_for_verified_providers(monkeypatch):
    import wiki_api.answerer as A
    monkeypatch.setattr(A, "client_for_model", lambda s: (MagicMock(), s.split("/")[-1]))
    assert A.WikiAnswerer(model_str="anthropic/claude-sonnet-5-5").structured_output is True
    assert A.WikiAnswerer(model_str="openai/gpt-5.4-mini").structured_output is True
    assert A.WikiAnswerer(model_str="google/gemini-3-pro").structured_output is False
    assert A.WikiAnswerer(model_str="lmstudio/local-model").structured_output is False


def test_streamed_prose_answer_has_inline_citations():
    chunk = MagicMock()
    chunk.choices = [MagicMock()]
    chunk.choices[0].delta.content = PROSE_ANSWER
    chunk.choices[0].finish_reason = "stop"
    chunk.usage = None
    end = MagicMock()
    end.choices = []
    end.usage = MagicMock(prompt_tokens=10, completion_tokens=5)
    client = MagicMock()
    client.chat.completions.create.return_value = iter([chunk, end])
    events = list(WikiAnswerer(client=client, model_id="fake-model").stream(question="q", pages=[]))
    final = events[-1]["result"]
    assert final.citations == ["pesticide-residue-definitions-by-food.md", "pesticide-residue-definition-by-matrix.md"]


def test_openai_answerer_sends_max_completion_tokens(monkeypatch):
    import wiki_api.answerer as A
    client = _fake_client(_chat_response(content=json.dumps({"answer": "x (a.md)", "citations": ["a.md"]})))
    monkeypatch.setattr(A, "client_for_model", lambda s: (client, s.split("/")[-1]))
    A.WikiAnswerer(model_str="openai/gpt-5.4-mini").run(question="q", pages=[])
    kwargs = client.chat.completions.create.call_args.kwargs
    assert "max_tokens" not in kwargs and kwargs["max_completion_tokens"] > 0


def test_other_providers_keep_max_tokens(monkeypatch):
    import wiki_api.answerer as A
    client = _fake_client(_chat_response(content="x (a.md)"))
    monkeypatch.setattr(A, "client_for_model", lambda s: (client, s.split("/")[-1]))
    A.WikiAnswerer(model_str="anthropic/claude-sonnet-5-5").run(question="q", pages=[])
    kwargs = client.chat.completions.create.call_args.kwargs
    assert kwargs["max_tokens"] == 8192 and "max_completion_tokens" not in kwargs
