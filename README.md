# ChemMon Wiki

This repository contains a structured markdown knowledge base for EFSA Chemical Monitoring reporting guidance.

It follows the "LLM wiki" pattern: raw source documents stay immutable, while an LLM incrementally builds and maintains a topic-oriented markdown layer that is easier to read, search, cite, and update over time.

See [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) for the project rationale.

## Directory Layout

```text
chemmon_docs/
  Raw EFSA PDF sources (annual ChemMon reporting guidance)

wiki/chemmon-guidance/
  Topic-oriented markdown knowledge pages derived from the guidance PDFs
  and EFSA official clarifications

wiki_api/
  FastAPI service exposing the wiki catalog, raw page reads, and
  a Q&A endpoint for answering ChemMon reporting questions
```

## Page Conventions

Each wiki page should:

- Use YAML frontmatter
- List source PDFs or clarification references
- Include related-page links
- Keep source-page comments such as `<!-- Source: ... -->`
- Stay concise and scannable
- Attribute claims to source pages or sections
- Prefer topic pages over document dumps

## Wiki API

Create and use the repo-local environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Copy and edit the environment file:

```bash
cp .env.example .env
```

Set at least:

```bash
ANTHROPIC_API_KEY=...
WIKI_SELECTOR_MODEL=claude-sonnet-4-6
WIKI_ANSWERER_MODEL=claude-sonnet-4-6
```

Run it locally with:

```bash
. .venv/bin/activate
uvicorn wiki_api.app:app --reload --port 8005
```

Main endpoints:

- `GET /health`: service health check
- `GET /wiki/index`: raw `index.md`
- `GET /wiki/pages`: page catalog with titles and summaries
- `GET /wiki/pages/{page_name}`: one wiki page
- `GET /wiki/pages/{page_name}/backlinks`: topic pages linking to a page
- `GET /wiki/search?q=resLOQ`: search topic titles, summaries and body text
- `GET /wiki/view`: browser-based wiki viewer
- `POST /wiki/ask`: ask a question, get a grounded answer with citations

### Evidence and navigation contracts

- `max_pages` (1–10, default 6) caps the complete evidence response. The index
  helps discovery but is never returned to the answerer as evidence.
- Related-page summary expansion is off by default. Opt in with
  `use_graph_expansion: true`; it uses remaining page slots only. Returned pages
  identify `evidence_kind` as `full` or `summary`. Only full pages are citable.
- Source filenames, page ranges and claim-adjacent source locators are retained
  in model evidence. Citation membership is checked; factual support still needs
  semantic review and answer evaluation.
- An empty selection returns an insufficient-evidence response without calling
  the answer model. A malformed selector response returns an error.
- `/wiki/pages` includes topic and orientation documents and exposes `type`,
  `domain`, `last_updated` and `source_pages`. The topic selector excludes
  orientation and maintenance documents.
- The viewer provides full-text topic search, exact-domain filtering, clickable
  wiki links and backlinks. Search accepts an optional `domain` and `limit`.

The change from the previous release affects clients relying on `index.md` in
`pages_used`, automatic related summaries, or a topic-only `/wiki/pages` list.
Use the returned `type` to exclude orientation documents where needed.

## Maintenance and roadmap

Run `python tools/health_check.py` and `pytest -q` after changes. GitHub Actions
runs both checks on pull requests and pushes to main or `codex/**` branches.
The health check validates topic metadata, dates, links including `related`,
local sources, index/API registration and duplicate CHEMMON IDs. The known
CHEMMON03 source duplicate remains a warning. These checks do not establish
rule completeness or semantic accuracy.

See the [improvement plan](docs/plans/2026-10-05-foodex2-parity.md) for milestone
status, acceptance criteria, the source audit, evaluation and integration work.

Run tests with:

```bash
. .venv/bin/activate
pytest -q
```
