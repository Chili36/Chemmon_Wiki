from __future__ import annotations

import json

from wiki_api.answerer import AnthropicChemMonAnswerer


def _response(*, stop_reason: str, content: list[dict[str, object]], input_tokens: int, output_tokens: int):
    return {
        "stop_reason": stop_reason,
        "content": content,
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
        },
    }


class FakeMessages:
    def __init__(self, responses: list[dict[str, object]]) -> None:
        self._responses = responses
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(kwargs)
        return self._responses[len(self.calls) - 1]


class FakeAnthropicClient:
    def __init__(self, responses: list[dict[str, object]]) -> None:
        self.messages = FakeMessages(responses)


class FakeStream:
    def __init__(self, *, deltas: list[str], final_message: dict[str, object]) -> None:
        self.text_stream = iter(deltas)
        self._final_message = final_message

    def get_final_text(self) -> str:
        # The answerer expects the concatenated text blocks.
        content = self._final_message.get("content", [])
        if not isinstance(content, list) or not content:
            return ""
        first = content[0]
        if isinstance(first, dict):
            return str(first.get("text", ""))
        return str(getattr(first, "text", ""))

    def get_final_message(self) -> dict[str, object]:
        return self._final_message


class FakeStreamManager:
    def __init__(self, stream: FakeStream) -> None:
        self._stream = stream

    def __enter__(self) -> FakeStream:
        return self._stream

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        return None


class FakeStreamingMessages(FakeMessages):
    def __init__(self, responses: list[dict[str, object]], *, deltas: list[str], final_message: dict[str, object]) -> None:
        super().__init__(responses)
        self._deltas = deltas
        self._final_message = final_message
        self.stream_calls: list[dict[str, object]] = []

    def stream(self, **kwargs: object) -> FakeStreamManager:  # type: ignore[override]
        self.stream_calls.append(kwargs)
        return FakeStreamManager(FakeStream(deltas=self._deltas, final_message=self._final_message))


class FakeAnthropicStreamingClient:
    def __init__(self, *, deltas: list[str], final_message: dict[str, object]) -> None:
        self.messages = FakeStreamingMessages([], deltas=deltas, final_message=final_message)


def test_answerer_returns_answer_with_citations() -> None:
    answer_payload = {
        "answer": "Yes, F33 is mandatory for acrylamide even when implicit.",
        "citations": ["acrylamide-rules.md"],
    }
    client = FakeAnthropicClient(
        [
            _response(
                stop_reason="end_turn",
                content=[{"type": "text", "text": json.dumps(answer_payload)}],
                input_tokens=200,
                output_tokens=50,
            )
        ]
    )

    answerer = AnthropicChemMonAnswerer(client=client, model="fake-model")
    result = answerer.run(
        question="Do I need F33 for acrylamide?",
        pages=[
            {"page_name": "acrylamide-rules.md", "content": "F33 is mandatory for acrylamide."},
        ],
    )

    assert result.answer == "Yes, F33 is mandatory for acrylamide even when implicit."
    assert result.citations == ["acrylamide-rules.md"]
    assert result.token_summary["calls"] == 1
    assert result.timing_summary["answerer_wall_time_ms"] >= 0

    first_call = client.messages.calls[0]
    assert "ChemMon" in first_call["system"]
    payload = json.loads(first_call["messages"][0]["content"])
    assert payload["question"] == "Do I need F33 for acrylamide?"
    assert len(payload["pages"]) == 1


def test_answerer_handles_plain_text_response() -> None:
    client = FakeAnthropicClient(
        [
            _response(
                stop_reason="end_turn",
                content=[{"type": "text", "text": "The wiki does not cover this topic."}],
                input_tokens=200,
                output_tokens=30,
            )
        ]
    )

    answerer = AnthropicChemMonAnswerer(client=client, model="fake-model")
    result = answerer.run(
        question="What is the meaning of life?",
        pages=[],
    )

    assert result.answer == "The wiki does not cover this topic."
    assert result.citations == []
    assert result.token_summary["calls"] == 1


def test_answerer_stream_yields_deltas_then_final_result() -> None:
    answer_payload = {
        "answer": "Yes, F33 is mandatory for acrylamide even when implicit.",
        "citations": ["acrylamide-rules.md"],
    }
    final_text = json.dumps(answer_payload)
    deltas = [final_text[:15], final_text[15:]]
    final_message = _response(
        stop_reason="end_turn",
        content=[{"type": "text", "text": final_text}],
        input_tokens=200,
        output_tokens=50,
    )
    client = FakeAnthropicStreamingClient(deltas=deltas, final_message=final_message)

    answerer = AnthropicChemMonAnswerer(client=client, model="fake-model")
    events = list(
        answerer.stream(
            question="Do I need F33 for acrylamide?",
            pages=[{"page_name": "acrylamide-rules.md", "content": "F33 is mandatory for acrylamide."}],
        )
    )

    delta_text = "".join(e["text"] for e in events if e["type"] == "delta")
    assert delta_text == final_text

    finals = [e for e in events if e["type"] == "final"]
    assert len(finals) == 1
    result = finals[0]["result"]
    assert result.answer == answer_payload["answer"]
    assert result.citations == ["acrylamide-rules.md"]
    assert result.token_summary["calls"] == 1

    first_call = client.messages.stream_calls[0]
    assert "ChemMon" in first_call["system"]
