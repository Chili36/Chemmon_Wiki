# ChemMon wiki as an MCP server — design

**Date:** 2026-10-18 · **Status:** draft for review · **Repo:** Chemmon_Wiki (`wiki_api/`)

## Why

DMT is moving from static prompts to agents that look things up while they work. Its FoodEx2
agent already does this against the FoodEx2 wiki (`/wiki/context-pack`, `/wiki/ask-rag` over
HTTP). DMT's planned ChemMon parameter agent (DMT branch `feat/chemmon-param-agent`, spec
`2026-10-15-chemmon-param-agent-design.md`) needs the same from this wiki.

Instead of each DMT agent hand-writing HTTP tools against our endpoints, the wiki offers itself
as an MCP server. The wiki then owns its tool names, descriptions and contracts; a DMT agent
lists the tools and gets improvements without a code change on its side.

The first consumer is **an agent running inside DMT's Docker container**, which reaches this
service today at `http://host.docker.internal:8005`.

## Goals

1. An MCP endpoint at **`/mcp` on the existing API** (same FastAPI app, same process, port 8005),
   using MCP's Streamable HTTP transport.
2. Four read-only tools that mirror the FoodEx2 wiki's MCP tools (FoodEx2 repo `wiki_mcp/server.py`;
   uncommitted there at the time of writing, read as reference only):

   | Tool | Same behaviour as | Cost |
   |---|---|---|
   | `search_guidance(query, domain?, limit?)` | `GET /wiki/search` | free, no model |
   | `get_guidance_page(page_name)` | `GET /wiki/pages/{page_name}` with content | free |
   | `get_reporting_context(question, max_pages?, max_chars?)` | `POST /wiki/context-pack` — Haiku selects pages, raw page evidence returned, no answer | ~$0.0001 selection + page tokens in the caller's context |
   | `ask_guidance(question, max_pages?)` | `POST /wiki/ask` (non-streaming) — cited brief from Sonnet | most expensive |

   Tool descriptions say what each returns, what it costs relative to the others, and when to
   prefer which (search/page first when the caller knows a term or page; context when it will
   reason itself; ask for a prepared brief).
3. Server instructions carry the wiki's stance: it explains ChemMon/SSD2 reporting rules with
   citations; it does not look up, invent or validate codes; a missing search hit is not proof
   that no rule exists; cite page names; respect source authority as stated on pages.
4. Proven from a container: a client in a separate Docker container connects to
   `http://host.docker.internal:8005/mcp`, lists the four tools and calls each.
5. A short consumer section in `README.md`: URL, tools, and a minimal Python example of an
   Anthropic Messages tool loop that uses an MCP client session (list tools → pass to Claude →
   forward `tool_use` to `call_tool`). DMT copies this pattern later.

## Non-goals

- Changing DMT, or switching DMT's param agent to MCP — that belongs to the DMT plan.
- rd-bridge tools or any PARAM-code lookup. How DMT talks to rd-bridge is undecided and separate.
- Authentication. Same as today's API and the FoodEx2 wiki (see Known gaps).
- Replacing or changing the deploy repo (`chemmon_wiki_deploy`). That is a separate, later
  project. This work only needs the deploy pin moved so the container serves the new code.
- stdio transport, MCP resources or prompts. Not needed by the first consumer.
- Exposing selector/answerer model overrides as tool parameters. The service's configured models
  apply (Haiku 5.5 selects, Sonnet 5.5 answers).

## Anti-goals (failure even if it works)

- **Duplicated wiki logic.** Tools must call the same Python code paths as the HTTP endpoints, in
  process, so an endpoint fix is a tool fix. No HTTP calls from the server to itself, no copy of
  search/selection/answer logic in the MCP layer. Refactor endpoint bodies into shared functions
  where needed.
- **A code finder.** No tool returns "the PARAM/FoodEx2 code for X". The wiki stays a wiki.
- **Breaking existing callers.** `/wiki/ask`, `/wiki/context-pack`, the other endpoints, their
  response shapes, `/wiki/view` and the deploy UI on :8080 behave exactly as before. The existing
  test suite and `tools/` health check stay green.
- **Leaking provider details.** Provider failures become MCP tool errors with the same safe
  messages the API gives (no upstream bodies, headers or keys), mirroring today's 503 handling.

## Constraints and decisions taken

- **SDK:** the official MCP Python SDK, `mcp>=2.3,<3` in `requirements.txt` (2.3.0 is current; the
  FoodEx2 wiki uses 2.3.0). Python 3.12 (venv and Docker image). FastAPI 0.135 / Starlette 1.0 in
  the venv; `requirements.txt` floors may need raising for the SDK.
- **Mounting** (SDK v2.3 docs, `docs/run/asgi.md`): `streamable_http_app()` mounted into the
  FastAPI app. Mounting disables the sub-app's lifespan, so the **host app's lifespan must enter
  `mcp.session_manager.run()`**, or the first request fails with "Task group is not initialized".
- **Stateless + JSON responses** (the SDK's recommended configuration): no session state to lose
  on restart, simplest for agent clients. `ask_guidance` is not streamed over MCP.
- **Host allowlist:** out of the box the SDK only answers requests addressed to localhost and
  returns 421 behind any other Host. Allow `localhost`, `127.0.0.1` and `host.docker.internal`
  by default, extendable through an environment variable (name left to the builder). This is DNS
  rebinding protection, not authentication. The allowlist must accept those hosts with a port
  (`host.docker.internal:8005`) and applies to `/mcp` only, not the rest of the API. The endpoint
  must end up at `/mcp`, not `/mcp/mcp` (mount path vs `streamable_http_path`). *(Designer's call.)*
- **Sync handlers from async tools:** the existing endpoint code is synchronous and calls models
  for seconds; tools run it in a worker thread so one slow `ask_guidance` doesn't block the event
  loop. *(Designer's call.)*
- **Tool results go into the calling agent's context.** Return what an agent needs — answer,
  citations, page names, page content, a compact cost/token summary — not the full internal
  `trace`. The exact fields are the builder's call, but `get_reporting_context` must return page
  content and citability exactly as `/wiki/context-pack` does, and `ask_guidance` the answer and
  citations exactly as `/wiki/ask` does.
- **Work order** (user's global rules): GitHub issue first, feature branch (`feat/mcp-server`), PR,
  Codex review handled briefly (fix real findings, ignore nitpicks), admin-bypass merge, then move
  the deploy pin and rebuild so :8005 serves it. Never change an LLM model name without asking.

## Testing and done

- Unit/integration tests in `tests/` using the SDK's client against the ASGI app (no network,
  model calls stubbed like the existing selector/answerer tests): tools listed with schemas; search
  and page results equal the HTTP endpoints' for the same input; context and ask call the same
  shared functions; provider errors surface as safe tool errors; Host allowlist accepts the three
  defaults and rejects others.
- Container check after deploy: from a throwaway container
  (`docker run --rm --add-host=host.docker.internal:host-gateway python:3.12-slim …` with `mcp`
  installed), connect to `http://host.docker.internal:8005/mcp`, list tools, call
  `search_guidance` and `get_guidance_page`, one `get_reporting_context`, and one `ask_guidance`
  (the last two cost a few cents). Record the command and output in the PR.
- **Done** = merged, deployed on :8005, container check passed, README consumer section written.

## Known gaps (recorded, not fixed here)

- The deploy container publishes :8005 on all interfaces with no authentication, so anyone on the
  local network can call `/wiki/ask` (and now `/mcp`) and spend Anthropic credit. Worth addressing
  in the deploy-repo replacement project.

## Left to the builder

- Module layout (e.g. `wiki_api/mcp_server.py`) and how endpoint bodies are factored into shared
  functions.
- Exact tool parameter defaults and limits (mirror the HTTP endpoints' validation), field names in
  trimmed results, and the wording of descriptions and instructions within the stance above.
- The environment variable name for extra allowed hosts.
