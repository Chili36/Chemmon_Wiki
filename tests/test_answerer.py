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
