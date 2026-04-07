from __future__ import annotations

import json
from pathlib import Path

from wiki_api.page_selector import AnthropicWikiPageSelector
from wiki_api.wiki_store import WikiStore


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


def _store() -> WikiStore:
    return WikiStore(Path("/Users/davidfoster/Dev/Chemmon_Wiki"))


def test_selector_picks_pages_via_tool_use() -> None:
    client = FakeAnthropicClient(
        [
            _response(
                stop_reason="tool_use",
                content=[
                    {
                        "type": "tool_use",
                        "id": "tool_1",
                        "name": "read_wiki_pages",
                        "input": {"page_names": []},
                    }
                ],
                input_tokens=100,
                output_tokens=25,
            )
        ]
    )

    selector = AnthropicWikiPageSelector(
        store=_store(), client=client, model="fake-model", max_pages=6
    )
    result = selector.run({"question": "What are the VMPR reporting rules?"})

    assert "index.md" in result.pages_used
    assert result.token_summary["calls"] == 1

    first_call = client.messages.calls[0]
    assert "ChemMon" in first_call["system"]
    payload = json.loads(first_call["messages"][0]["content"])
    assert "question" in payload
    assert "wiki_index" in payload


def test_selector_accepts_json_page_names_without_tool() -> None:
    client = FakeAnthropicClient(
        [
            _response(
                stop_reason="end_turn",
                content=[
                    {
                        "type": "text",
                        "text": json.dumps({"page_names": []}),
                    }
                ],
                input_tokens=100,
                output_tokens=25,
            )
        ]
    )

    selector = AnthropicWikiPageSelector(
        store=_store(), client=client, model="fake-model", max_pages=6
    )
    result = selector.run({"question": "test"})

    assert "index.md" in result.pages_used
    assert result.token_summary["calls"] == 1
