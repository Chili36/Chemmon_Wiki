# ChemMon Wiki MCP Server Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Serve the ChemMon wiki as an MCP server at `/mcp` on the existing :8005 API, with four read-only tools, usable from an agent in DMT's Docker container.

**Architecture:** A new module `wiki_api/mcp_server.py` defines an `MCPServer` whose tools call the existing endpoint functions in `wiki_api/app.py` in process (in a worker thread), translating `HTTPException`/validation errors into MCP tool errors. `app.py` mounts the server's Streamable HTTP app (stateless, JSON responses) at `/mcp` and enters its session manager in the FastAPI lifespan. A Host allowlist on the MCP app admits localhost, 127.0.0.1 and host.docker.internal.

**Tech Stack:** Python 3.12, FastAPI 0.135 / Starlette 1.0, official MCP Python SDK `mcp>=2.3,<3` (`mcp.server.mcpserver.MCPServer`, `mcp.Client`, `mcp.server.transport_security.TransportSecuritySettings`), pytest.

**Spec:** `docs/superpowers/specs/2026-10-18-mcp-server-design.md`

## Global Constraints

- SDK: `mcp>=2.3,<3` in `requirements.txt`; raise `fastapi`/`uvicorn` floors only if the SDK requires it.
- Endpoint at exactly `/mcp` on the existing app and port 8005 — not `/mcp/mcp`, no second process.
- Streamable HTTP, `stateless_http=True`, `json_response=True`; `ask_guidance` is not streamed.
- Tools call the same Python code as the HTTP endpoints, in process. No HTTP calls from the server to itself; no copied search/selection/answer logic.
- No tool returns "the code for X"; the wiki explains rules.
- Existing endpoints, response shapes, `/wiki/view` and the deploy UI unchanged; full test suite and `.venv/bin/python tools/health_check.py` green.
- Provider failures become tool errors with the API's existing safe messages — no upstream bodies, headers or keys.
- No model overrides exposed; never change an LLM model name without asking the user.
- Work order: GitHub issue → `feat/mcp-server` branch (exists, spec committed) → PR → brief Codex review (fix real findings, ignore nitpicks) → admin-bypass merge → deploy pin → container check.

## Review Focus

- A client POSTing to exactly `/mcp` (no trailing slash) must get the MCP response, not a 307 redirect — Task 3 `test_post_to_exact_path_is_not_redirected`.
- `Host: host.docker.internal:8005` (with port) must be accepted; `Host: evil.example` must get 421 — Task 3 `test_host_allowlist`.
- `ask_guidance` when the selector picks no pages must return the service's normal no-evidence answer, not an error — Task 2 `test_ask_with_no_selected_pages`.
- `get_guidance_page` with an unknown name must return a tool error naming the page, not crash the server — Task 1 `test_unknown_page_is_a_tool_error`.
- A model-provider failure must return a tool error with the API's fixed 503 message and no upstream detail — Task 2 `test_provider_failure_is_a_safe_tool_error`.

---

### Task 1: MCP server module with the two free tools

**Files:**
- Modify: `requirements.txt` (add `mcp>=2.3,<3`)
- Create: `wiki_api/mcp_server.py`
- Test: `tests/test_mcp_server.py`

**Interfaces:**
- Consumes: `wiki_api.app.search_pages(q: str, domain: str | None, limit: int) -> dict`, `wiki_api.app.get_page(page_name: str, include_content: bool) -> dict` (existing; import lazily inside tool bodies — `app.py` will import this module in Task 3).
- Produces:
  - `mcp: MCPServer` named `"chemmon-wiki"` with `instructions=INSTRUCTIONS`.
  - `async def _call(fn: Callable[..., T], *args, **kwargs) -> T` — runs `fn` via `anyio.to_thread.run_sync`; re-raises `fastapi.HTTPException` as `ToolError(str(exc.detail))` and `pydantic.ValidationError` as `ToolError` with the validation message.
  - Tool `search_guidance(query: str (1–20000 chars, non-blank), domain: str | None = None, limit: int = 20 (1–100)) -> dict` — returns `search_pages(...)` output unchanged.
  - Tool `get_guidance_page(page_name: str) -> dict` — returns `get_page(page_name, include_content=True)` output unchanged.

- [ ] **Step 1: Open the GitHub issue**

```bash
gh issue create --title "Serve the wiki as an MCP server at /mcp" --body "Spec: docs/superpowers/specs/2026-10-18-mcp-server-design.md (branch feat/mcp-server). Four read-only tools (search_guidance, get_guidance_page, get_reporting_context, ask_guidance) for DMT's agents."
```
Record the issue number for the PR.

- [ ] **Step 2: Install the SDK**

Add `mcp>=2.3,<3` to `requirements.txt`; run `.venv/bin/pip install -r requirements.txt`. Expected: `mcp 2.3.x` installed, FastAPI/Starlette unchanged.

- [ ] **Step 3: Write the failing tests** (`tests/test_mcp_server.py`, sync tests with an `asyncio.run` helper like `tests/test_app.py`)

```python
from mcp import Client
from wiki_api.mcp_server import mcp
import wiki_api.app as app_module

def call(name, args):
    async def go():
        async with Client(mcp) as client:
            return await client.call_tool(name, args)
    return asyncio.run(go())

def test_four_tools_are_listed():  # passes fully after Task 2; in Task 1 assert the two free tools
    ...  # list_tools names == {"search_guidance", "get_guidance_page", "get_reporting_context", "ask_guidance"}

def test_search_matches_the_http_endpoint():
    result = call("search_guidance", {"query": "acrylamide", "limit": 5})
    assert not result.is_error
    assert result.structured_content == app_module.search_pages(q="acrylamide", domain=None, limit=5)

def test_page_matches_the_http_endpoint():
    result = call("get_guidance_page", {"page_name": "contaminant-reporting.md"})
    assert result.structured_content == app_module.get_page("contaminant-reporting.md", include_content=True)

def test_unknown_page_is_a_tool_error():
    result = call("get_guidance_page", {"page_name": "no-such-page.md"})
    assert result.is_error and "no-such-page" in result.content[0].text

def test_limit_out_of_range_is_rejected():
    assert call("search_guidance", {"query": "x", "limit": 101}).is_error
```

If `structured_content` wraps dict returns (e.g. `{"result": ...}`), compare against the wrapped form consistently across all tests — decide once here.

- [ ] **Step 4: Run to verify failure**

Run: `.venv/bin/python -m pytest tests/test_mcp_server.py -v` — Expected: FAIL (`ModuleNotFoundError: wiki_api.mcp_server`).

- [ ] **Step 5: Implement `wiki_api/mcp_server.py`**

`INSTRUCTIONS` (exact copy):

```
ChemMon wiki: EFSA Chemical Monitoring (SSD2) reporting guidance for pesticides, veterinary medicinal product residues, contaminants, food additives and flavourings. It explains reporting rules with citations to wiki pages and their EFSA sources; it does not look up, invent or validate codes. Prefer search_guidance and get_guidance_page (free) when you know a term, element name, rule ID or page. Use get_reporting_context when you will reason over the evidence yourself, and ask_guidance only when you want a prepared cited brief (most expensive). A missing search hit is not proof that no rule exists. Cite page names, and respect the source authority stated on each page.
```

Tool descriptions: one or two sentences each stating what is returned and relative cost (free / small selection cost plus page tokens / most expensive). Use `Annotated[..., Field(...)]` for the ranges.

- [ ] **Step 6: Run to verify pass**

Run: `.venv/bin/python -m pytest tests/test_mcp_server.py -v` — Expected: PASS (tool-list test limited to the two tools for now).

- [ ] **Step 7: Commit**

```bash
git add requirements.txt wiki_api/mcp_server.py tests/test_mcp_server.py
git commit -m "MCP server with search and page tools"
```

---

### Task 2: Context and ask tools

**Files:**
- Modify: `wiki_api/mcp_server.py`
- Test: `tests/test_mcp_server.py`

**Interfaces:**
- Consumes: `_call` (Task 1); `wiki_api.app.context_pack(request: ContextPackRequest) -> dict`, `wiki_api.app.ask_question(request: AskRequest) -> AskResponse`, `ContextPackRequest`, `AskRequest` (existing); test fakes `FakeSelector`, `FakeAnswerer` from `tests/test_app.py`, installed via `app_module.selector_runner` / `app_module.answerer_runner` as existing tests do.
- Produces:
  - Tool `get_reporting_context(question: str, max_pages: int = 6 (1–10), max_chars: int = 60000 (2000–120000)) -> dict` — `context_pack(ContextPackRequest(...))` output without the `"trace"` key, plus `"cost_usd"` = `trace["selector"]["estimated_cost_usd"]` (or `0.0` when no selector ran).
  - Tool `ask_guidance(question: str, max_pages: int = 6 (1–10)) -> dict` — from `ask_question(AskRequest(question=..., max_pages=..., stream=False))`: `{"answer", "citations", "pages_used", "cost_usd"}` where `cost_usd` = `trace["total"]["total_cost_usd"]` (may be `None`). Page contents are not returned (callers use `get_guidance_page`).

- [ ] **Step 1: Write the failing tests**

```python
def test_context_matches_the_http_endpoint(fakes):
    result = call("get_reporting_context", {"question": "acrylamide F33", "max_pages": 4})
    expected = app_module.context_pack(app_module.ContextPackRequest(question="acrylamide F33", max_pages=4))
    got = result.structured_content
    assert "trace" not in got and got["pages"] == expected["pages"] and got["citable_pages"] == expected["citable_pages"]
    assert "cost_usd" in got

def test_ask_returns_answer_and_citations(fakes):
    got = call("ask_guidance", {"question": "Is F33 mandatory for acrylamide?"}).structured_content
    assert got["answer"] == "F33 is mandatory for acrylamide per CHEMMON12."
    assert got["citations"] == ["contaminant-reporting.md"] and got["pages_used"] == ["contaminant-reporting.md"]
    assert set(got) == {"answer", "citations", "pages_used", "cost_usd"}

def test_ask_with_no_selected_pages(fakes):  # selector fake returning pages_used=[]
    result = call("ask_guidance", {"question": "unrelated"})
    assert not result.is_error and result.structured_content["citations"] == []

def test_provider_failure_is_a_safe_tool_error():  # selector fake raising anthropic.APIError(... body containing "secret upstream")
    result = call("ask_guidance", {"question": "q"})
    assert result.is_error and "Model provider request failed" in result.content[0].text
    assert "secret" not in result.content[0].text

def test_max_pages_out_of_range_is_rejected():
    assert call("ask_guidance", {"question": "q", "max_pages": 11}).is_error
```

`fakes` is a pytest fixture installing `FakeSelector()`/`FakeAnswerer()` and restoring the previous runners afterwards. Extend the Task 1 tool-list test to all four names.

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/python -m pytest tests/test_mcp_server.py -v` — Expected: new tests FAIL (unknown tool).

- [ ] **Step 3: Implement both tools in `wiki_api/mcp_server.py`** per the Interfaces block.

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/python -m pytest tests/test_mcp_server.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add wiki_api/mcp_server.py tests/test_mcp_server.py
git commit -m "MCP context and ask tools"
```

---

### Task 3: Mount at /mcp with lifespan and Host allowlist

**Files:**
- Modify: `wiki_api/mcp_server.py` (add `allowed_hosts()`, `http_app()`)
- Modify: `wiki_api/app.py` (FastAPI `lifespan`, mount)
- Test: `tests/test_mcp_http.py`

**Interfaces:**
- Consumes: `mcp` (Task 1).
- Produces:
  - `allowed_hosts() -> list[str]` — for each of `localhost`, `127.0.0.1`, `host.docker.internal`, plus comma-separated extras in env `WIKI_MCP_ALLOWED_HOSTS`: both `"<host>"` and `"<host>:*"`.
  - `http_app() -> Starlette` — `mcp.streamable_http_app(streamable_http_path=..., stateless_http=True, json_response=True, transport_security=TransportSecuritySettings(allowed_hosts=allowed_hosts()))`, built once.
  - `app.py`: `FastAPI(..., lifespan=lifespan)` where `lifespan` enters `mcp.session_manager.run()`; the MCP app mounted so the endpoint is exactly `/mcp`. (Mounting disables the sub-app lifespan; `session_manager` exists only after `streamable_http_app()` is called; `run()` works once per manager.)

- [ ] **Step 1: Write the failing tests** (`tests/test_mcp_http.py`)

Use one **module-scoped** `starlette.testclient.TestClient(app_module.app, base_url="http://localhost:8005")` entered as a context manager (runs the lifespan once — a second lifespan entry on the same manager raises). Send raw JSON-RPC with headers `Content-Type: application/json`, `Accept: application/json, text/event-stream`.

```python
def test_post_to_exact_path_is_not_redirected(client):
    r = client.post("/mcp", json=TOOLS_LIST, headers=HEADERS, follow_redirects=False)
    assert r.status_code == 200
    assert {t["name"] for t in r.json()["result"]["tools"]} == {"search_guidance", "get_guidance_page", "get_reporting_context", "ask_guidance"}

def test_host_allowlist(client):
    assert client.post("/mcp", json=TOOLS_LIST, headers={**HEADERS, "Host": "host.docker.internal:8005"}).status_code == 200
    assert client.post("/mcp", json=TOOLS_LIST, headers={**HEADERS, "Host": "evil.example"}).status_code == 421

def test_extra_hosts_from_env(monkeypatch):
    monkeypatch.setenv("WIKI_MCP_ALLOWED_HOSTS", "wiki.lan")
    assert {"wiki.lan", "wiki.lan:*", "host.docker.internal:*"} <= set(mcp_server.allowed_hosts())

def test_rest_api_is_unaffected_by_the_allowlist(client):
    assert client.get("/health", headers={"Host": "evil.example"}).status_code == 200
```

`TOOLS_LIST` is a `tools/list` JSON-RPC request. If the SDK's stateless mode requires an `initialize` exchange first, do it in the fixture and keep the assertions.

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/python -m pytest tests/test_mcp_http.py -v` — Expected: FAIL (404 on `/mcp`).

- [ ] **Step 3: Implement** `allowed_hosts()`, `http_app()` and the `app.py` lifespan + mount per the Interfaces block.

- [ ] **Step 4: Run the new and the whole suite**

Run: `.venv/bin/python -m pytest -q` and `.venv/bin/python tools/health_check.py` — Expected: all pass, including every pre-existing test.

- [ ] **Step 5: Smoke over real HTTP**

Run `.venv/bin/python -m uvicorn wiki_api.app:app --port 8015` in the background, then a short script with `mcp.Client("http://127.0.0.1:8015/mcp")` calling `list_tools` and `search_guidance`. Expected: four tools, a non-empty search result. Stop the server.

- [ ] **Step 6: Commit**

```bash
git add wiki_api/mcp_server.py wiki_api/app.py tests/test_mcp_http.py
git commit -m "Mount the MCP server at /mcp with a Host allowlist"
```

---

### Task 4: Consumer docs, PR and merge

**Files:**
- Modify: `README.md` (new "MCP server" section)

- [ ] **Step 1: Write the README section**

Contents: URL (`http://127.0.0.1:8005/mcp`; from a container `http://host.docker.internal:8005/mcp`); transport (Streamable HTTP, stateless, JSON); the four tools with one line each and relative cost; `WIKI_MCP_ALLOWED_HOSTS`; no authentication (known gap: :8005 is published on all interfaces); a minimal Python example: `async with Client(url) as mcp_client` → `list_tools()` → convert each tool to an Anthropic tool (`name`, `description`, `input_schema`) → `client.messages.create(model="claude-sonnet-5-5", tools=..., ...)` loop forwarding each `tool_use` to `mcp_client.call_tool` and returning a `tool_result` (with `is_error` when the result is an error). Use the model the service already uses; no new model names.

- [ ] **Step 2: Commit, push, PR**

```bash
git add README.md && git commit -m "README: MCP server for consumers"
git push -u origin feat/mcp-server
gh pr create --title "Serve the wiki as an MCP server at /mcp" --body "Closes #<issue>. ..."
```

- [ ] **Step 3: Review and merge**

Wait briefly for Codex review; fix real findings, ignore repeated nitpicks; CI green; `gh pr merge --admin --merge`.

---

### Task 5: Deploy and container check

**Files:** `~/Dev/chemmon_wiki_deploy` (submodule pin only)

- [ ] **Step 1: Move the pin**

In `~/Dev/chemmon_wiki_deploy`: branch `deploy/wiki-<sha>`, `git -C chemmon_wiki fetch && git -C chemmon_wiki checkout <merged main sha>`, commit `Pin ChemMon wiki to <sha>`, PR, admin merge, then `docker compose up -d --build api`. Expected: `curl -s localhost:8005/health` → `{"status":"ok"}`.

- [ ] **Step 2: Container check**

```bash
docker run --rm --add-host=host.docker.internal:host-gateway python:3.12-slim sh -c \
  'pip -q install "mcp>=2.3,<3" && python - <<EOF
import asyncio
from mcp import Client
async def main():
    async with Client("http://host.docker.internal:8005/mcp") as c:
        print(sorted(t.name for t in (await c.list_tools()).tools))
        for name, args in [("search_guidance", {"query": "acrylamide"}),
                           ("get_guidance_page", {"page_name": "contaminant-reporting.md"}),
                           ("get_reporting_context", {"question": "Is F33 mandatory for acrylamide?"}),
                           ("ask_guidance", {"question": "Is F33 mandatory for acrylamide?"})]:
            r = await c.call_tool(name, args)
            print(name, "error" if r.is_error else "ok", str(r.structured_content)[:200])
asyncio.run(main())
EOF'
```

Expected: four tool names; four `ok` lines; the ask line shows an answer citing `contaminant-reporting.md`. Paste the output as a comment on the merged PR.

- [ ] **Step 3: Update memory pin note** (`project_live_deploy_pin.md`) with the new pin and that `/mcp` is live.
