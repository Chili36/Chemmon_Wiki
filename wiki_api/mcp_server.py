"""The wiki as an MCP server for agents (DMT first); spec docs/superpowers/specs/2026-10-18-mcp-server-design.md.

Tools call the HTTP endpoint functions in app.py in process, so an endpoint fix is a tool fix.
app.py imports this module to mount it, so the endpoint functions are imported inside the tools.
"""
from __future__ import annotations

import os
from typing import Annotated, Any, Callable, TypeVar

import anyio
from fastapi import HTTPException
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations
from pydantic import Field, ValidationError
from starlette.applications import Starlette

T = TypeVar("T")

INSTRUCTIONS = (
    "ChemMon wiki: EFSA Chemical Monitoring (SSD2) reporting guidance for pesticides, veterinary "
    "medicinal product residues, contaminants, food additives and flavourings. It explains reporting "
    "rules with citations to wiki pages and their EFSA sources; it does not look up, invent or validate "
    "codes. Prefer search_guidance and get_guidance_page (free) when you know a term, element name, rule "
    "ID or page. Use get_reporting_context when you will reason over the evidence yourself, and "
    "ask_guidance only when you want a prepared cited brief (most expensive). A missing search hit is "
    "not proof that no rule exists. Cite page names, and respect the source authority stated on each page."
)

READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)

mcp = MCPServer("chemmon-wiki", instructions=INSTRUCTIONS)

Question = Annotated[str, Field(min_length=1, max_length=20000, pattern=r"\S", description="Question about ChemMon reporting.")]


async def _call(fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Run a synchronous endpoint function in a worker thread; its errors become tool errors."""
    try:
        return await anyio.to_thread.run_sync(lambda: fn(*args, **kwargs))
    except HTTPException as exc:
        raise ToolError(str(exc.detail)) from None
    except ValidationError as exc:
        raise ToolError(str(exc)) from None


@mcp.tool(annotations=READ_ONLY)
async def search_guidance(
    query: Annotated[str, Field(min_length=1, max_length=20000, pattern=r"\S", description="Words, element names or rule IDs; every word must match.")],
    domain: Annotated[str | None, Field(description="Only pages of this domain, e.g. pesticides or contaminants.")] = None,
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
) -> dict[str, Any]:
    """Text search over wiki pages (no model, free). Returns ranked page names, titles and summaries."""
    from .app import search_pages
    return await _call(search_pages, q=query, domain=domain, limit=limit)


@mcp.tool(annotations=READ_ONLY)
async def get_guidance_page(
    page_name: Annotated[str, Field(min_length=1, max_length=200, description="Page file name, e.g. contaminant-reporting.md.")],
) -> dict[str, Any]:
    """One full wiki page with its metadata and sources (free)."""
    from .app import get_page
    return await _call(get_page, page_name, include_content=True)


@mcp.tool(annotations=READ_ONLY)
async def get_reporting_context(
    question: Question,
    max_pages: Annotated[int, Field(ge=1, le=10)] = 6,
    max_chars: Annotated[int, Field(ge=2000, le=120000)] = 60000,
) -> dict[str, Any]:
    """Wiki evidence for a question, for you to reason over: a small model selects pages and their
    content comes back with citability; no answer is written. Costs a page selection plus the page
    tokens in your context."""
    from .app import ContextPackRequest, context_pack
    pack = await _call(lambda: context_pack(ContextPackRequest(question=question, max_pages=max_pages, max_chars=max_chars)))
    trace = pack.pop("trace", {})
    pack["cost_usd"] = trace.get("selector", {}).get("estimated_cost_usd", 0.0)
    return pack


@mcp.tool(annotations=READ_ONLY)
async def ask_guidance(
    question: Question,
    max_pages: Annotated[int, Field(ge=1, le=10)] = 6,
) -> dict[str, Any]:
    """A prepared answer to a ChemMon reporting question, citing the wiki pages it rests on (most
    expensive tool). Read cited pages with get_guidance_page."""
    from .app import AskRequest, ask_question
    response = await _call(lambda: ask_question(AskRequest(question=question, max_pages=max_pages, stream=False)))
    return {"answer": response.answer, "citations": response.citations, "pages_used": response.pages_used,
            "cost_usd": response.trace.get("total", {}).get("total_cost_usd")}


DEFAULT_HOSTS = ("localhost", "127.0.0.1", "host.docker.internal")
_http_app: Starlette | None = None


def allowed_hosts() -> list[str]:
    """Host headers /mcp answers (DNS-rebinding protection, not authentication), with and without a port.
    WIKI_MCP_ALLOWED_HOSTS adds comma-separated hosts."""
    extra = [h.strip() for h in os.getenv("WIKI_MCP_ALLOWED_HOSTS", "").split(",") if h.strip()]
    return [form for host in (*DEFAULT_HOSTS, *extra) for form in (host, f"{host}:*")]


def http_app() -> Starlette:
    """The Streamable HTTP app (stateless, JSON responses), built once; app.py mounts it."""
    global _http_app
    if _http_app is None:
        _http_app = mcp.streamable_http_app(
            streamable_http_path="/mcp", stateless_http=True, json_response=True,
            transport_security=TransportSecuritySettings(allowed_hosts=allowed_hosts()))
    return _http_app
