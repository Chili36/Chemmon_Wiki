"""MCP tools: same results as the HTTP endpoints, errors as tool errors (no network)."""
from __future__ import annotations

import asyncio
import json

from mcp import Client

import wiki_api.app as app_module
from wiki_api.mcp_server import mcp


def run(coro):
    return asyncio.run(coro)


def call(name: str, args: dict):
    async def go():
        async with Client(mcp) as client:
            return await client.call_tool(name, args)
    return run(go())


def as_json(value):
    """What an HTTP or MCP client receives (tuples become lists)."""
    return json.loads(json.dumps(value))


def tool_names() -> set[str]:
    async def go():
        async with Client(mcp) as client:
            return {tool.name for tool in (await client.list_tools()).tools}
    return run(go())


def test_tools_are_listed():
    assert {"search_guidance", "get_guidance_page"} <= tool_names()


def test_search_matches_the_http_endpoint():
    result = call("search_guidance", {"query": "acrylamide", "limit": 5})
    assert not result.is_error
    assert result.structured_content == as_json(app_module.search_pages(q="acrylamide", domain=None, limit=5))


def test_page_matches_the_http_endpoint():
    result = call("get_guidance_page", {"page_name": "contaminant-reporting.md"})
    assert not result.is_error
    assert result.structured_content == as_json(app_module.get_page("contaminant-reporting.md", include_content=True))


def test_unknown_page_is_a_tool_error():
    result = call("get_guidance_page", {"page_name": "no-such-page.md"})
    assert result.is_error and "no-such-page" in result.content[0].text


def test_limit_out_of_range_is_rejected():
    assert call("search_guidance", {"query": "x", "limit": 101}).is_error
