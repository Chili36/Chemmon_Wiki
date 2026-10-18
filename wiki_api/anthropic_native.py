"""Native Anthropic SDK access for the selector and answerer.

Anthropic's OpenAI-compatible endpoint supports neither prompt caching nor enforced structured
output (it ignores response_format), so Anthropic models are called through the Messages API
instead. Other providers keep the OpenAI-compatible path in providers.py.
"""
from __future__ import annotations

import os
from typing import Any

import anthropic

_client: anthropic.Anthropic | None = None


def native_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY is not set (required for provider 'anthropic')")
        _client = anthropic.Anthropic()
    return _client


def json_schema_format(schema: dict[str, Any]) -> dict[str, Any]:
    """output_config for an enforced JSON answer."""
    return {"format": {"type": "json_schema", "schema": schema}}


def response_text(message: Any) -> str:
    return "".join(block.text for block in message.content if getattr(block, "type", None) == "text")


def usage_dict(usage: Any, stop_reason: str | None) -> dict[str, int | str | None]:
    """Messages API usage in the shape the rest of the service records."""
    def count(name: str) -> int:
        return int(getattr(usage, name, 0) or 0) if usage is not None else 0
    tokens = {"input_tokens": count("input_tokens"), "output_tokens": count("output_tokens"),
              "cache_creation_input_tokens": count("cache_creation_input_tokens"),
              "cache_read_input_tokens": count("cache_read_input_tokens")}
    return {"stop_reason": stop_reason, **tokens, "total_tracked_tokens": sum(tokens.values())}
