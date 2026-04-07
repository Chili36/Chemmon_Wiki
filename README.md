# ChemMon Wiki

This repository contains a structured markdown knowledge base for EFSA Chemical Monitoring reporting guidance.

It follows the "LLM wiki" pattern: raw source documents stay immutable, while an LLM incrementally builds and maintains a topic-oriented markdown layer that is easier to read, search, cite, and update over time.

See [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) for the project rationale.

## Directory Layout

```text
chemmon_docs/
  Raw EFSA PDF sources (annual ChemMon reporting guidance)

raw/chemmon-guidance/
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
WIKI_SELECTOR_MODEL=claude-3-7-sonnet-latest
WIKI_ANSWERER_MODEL=claude-3-7-sonnet-latest
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
- `GET /wiki/view`: browser-based wiki viewer
- `POST /wiki/ask`: ask a question, get a grounded answer with citations

Run tests with:

```bash
. .venv/bin/activate
pytest -q
```
