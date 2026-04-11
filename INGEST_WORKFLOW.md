---
title: "Ingest Workflow"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
---

# Ingest Workflow

How new source material becomes wiki content in this repository. Read this
before touching any wiki page. It exists because the 2026-04-11 ingest pass
was run under the wrong mental model and produced pages optimized for a
specific eval rather than for reusability — see `log.md` for the retrospective.

## Your job

**Your job is not to summarize the source document.**
**Your job is to update the wiki with durable, reusable knowledge.**

The wiki is not a restructured copy of the PDFs in `chemmon_docs/`. It is a
set of small, topic-scoped pages that represent the *knowledge atoms* a
ChemMon reporting question might need. Sources are inputs; the atoms are
the deliverable. If a section of the source is pure narrative context with
no durable rule, definition, or decision logic, **it does not need to become
a wiki page.**

A wiki is an ontology of the domain. A source is raw material. The two have
different shapes, and the wiki's shape is determined by the domain, not by
the source.

## Prerequisites — read these first

Before touching any wiki file:

1. `PROJECT_CONTEXT.md` — why this wiki exists
2. `SCHEMA.md` — page types, required frontmatter, wiki-link convention
3. The last 2-3 entries of `log.md` — recent state, open items, known gaps
4. `index.md` — current page catalog

Then classify the source you're about to ingest. Pages in this wiki fall
into these types (see `SCHEMA.md`): **overview**, **reference**,
**domain-guide**, **rule-reference**, **hub**. Ask which of these the new
source contributes to — usually several.

## The three passes

Large-source ingest (annual guidance PDFs, major updates) uses three passes
over the source. **Never skip directly to writing.**

### Pass A — structure scan

Read the source end to end *without writing*. Build a short outline:

- Section numbers and titles
- Which sections contain durable rules
- Which sections are procedural/workflow descriptions
- Which sections are historical context or narrative intros
- Which existing wiki pages each rule-bearing section would patch
- Which genuinely new concepts (if any) need a new page

**Output of Pass A**: a list of pages to touch, marked as *expand* or
*create*. If you plan to create more than ~3 new pages in one ingest,
stop and re-check — you are probably defaulting to new pages when you
should be patching.

### Pass B — durable rule extraction

Go back through the sections Pass A marked as rule-bearing. For each,
extract only:

- **Definitions** — what a term, code, or field means
- **Rule statements** — declarative must/should/cannot
- **Tie-break logic** — which rule wins when two conflict
- **Explicit exceptions** — when the rule doesn't apply
- **Terminology and canonical codes**
- **Worked examples** — *only when the example teaches a reusable rule*,
  not when it illustrates a one-off scenario

**Discard** everything else: narrative intros, "this section describes",
re-statements of context, per-example anecdotes that don't generalize,
document navigation prose.

Write into target pages in **rule-first order**: the rule leads, then the
qualifier (when it applies, exceptions, domain), then the example if the
example teaches something reusable. Do not lead with context, overview, or
history. The first sentence of a page should be useful to the answerer.

### Pass C — gap sweep

After writing, re-walk the wiki as a whole and check:

- **Orphan pages** — pages with no inbound links from any other page
- **Unlinked concepts** — concepts mentioned in prose that should have their
  own page
- **Broken cross-references** — `[[page-name]]` pointing at pages that don't
  exist, or pages that should appear in another page's `related:` list
- **Stale frontmatter** — `last_updated` not bumped on every touched page,
  `sources:` missing the new source document
- **Index** — `index.md` doesn't list a newly-created page
- **Contradictions** — two pages that state incompatible things (flag these
  for the human to resolve; do not silently pick a winner)

Fix everything catchable before committing.

## Per-page rules

For every page you touch:

- **Keep YAML frontmatter up to date** — `title`, `type`, `domain`,
  `last_updated`, `sources`, `related`
- **Keep scope narrow** — one page, one topic. If the page grows to cover
  multiple decisions, split it.
- **Add `sources`** — every source PDF the content draws from
- **Add `related`** — nearest-neighbor pages in `[[page-name]]` syntax
- **Add inline `[[cross-links]]`** where concepts materially depend on each
  other — load-bearing, not decorative
- **Add `<!-- Source: <pdf>, <page range> -->` HTML comments** next to
  claims a maintainer would need to verify against the source
- **Add a `Relevant Business Rules` section** when CHEMMON / GBR / LL rules
  materially constrain the page — list them with the rule ID and a short
  explanation of how they constrain the topic
- **Add a `Relevant Policy` section** when decision order matters — e.g.
  "legal limit wins over prose guidance", "rule A trumps rule B when they
  both fire"
- **Prefer patching existing pages over creating new ones**

## When to patch vs when to create

**Patch an existing page** when:

- The new content adds a rule or clarification to a topic the existing
  page already covers
- The new content is an exception or edge case for an existing rule
- The new content updates the `last_updated` on an existing page because
  it changes what's true

**Create a new page** only when:

- The new content is about a concept that has no existing home
- The concept is genuinely cross-cutting and would bloat any single
  existing page
- The concept represents a whole new sub-domain

**Default is patch.** Creating a new page is the exception, not the norm.
If you're unsure, patch — a future ingest can split it.

## Anti-patterns observed on 2026-04-11

Recorded here so the next pass doesn't repeat them:

1. **Creating new pages instead of patching.** The ingest created six new
   element-reference pages (`ssd2-elements-programme.md`, `-sampling.md`,
   `-matrix.md`, `-analysis.md`, `-result.md`, `-evaluation.md`) instead of
   patching the existing `ssd2-data-model.md`. Two or three patched pages
   would have been sufficient.

2. **Preserving document-order narrative.** `ssd2-elements-result.md` walks
   M.01 through M.20 in PDF order. That's a restructured archive, not a
   knowledge base. Same content compressed to rule-first atoms would be
   smaller and more retrievable.

3. **Scoping ingest to the current eval.** PDF Sections 3-11 were skipped
   because the current failure modes didn't hit them. A principled ingest
   covers the whole source unless the source itself is out of scope. The
   concept eval run later the same day exposed exactly which sections had
   been dropped.

4. **No Pass A structure scan.** Sections were read and transcribed
   linearly. Without a structure scan, every decision — which pages to
   create, which to patch, which sections to skip — was made reactively.

5. **Big pages over small ones.** `foodex2-facets.md` is a single page
   covering F01 through F33. A question about "what does F33 do" retrieves
   the whole 33-facet table instead of a narrowly-scoped atom.

## Commit discipline

Each pass (A, B, C) can be its own commit, or pass B can be split across
commits by page family. Every commit message must state:

- Which source document was ingested
- Which sections of the source the commit covers
- Which pages were **patched** vs **created** (prefer patch)
- Which sections are known-deferred and why, if any

Update `log.md` with a dated entry for every ingest pass. Always include
both what was done and what was left out — the latter matters as much as
the former.

## When you're done

Run:

```bash
. .venv/bin/activate
python tools/health_check.py      # frontmatter, cross-links, rule-ID coverage
pytest -q                          # public API + store behavior
```

Both must pass. The health check catches broken cross-links, missing
frontmatter fields, and duplicate rule IDs. The test suite guards the
store and API contract.

## What NOT to do

- **Do not read the eval test sets during ingest.** `chemmon_testset_50.json`
  and its siblings are measurement tools, not guidance signals. Reading
  them during ingest structurally contaminates any subsequent accuracy
  comparison. Use the source PDFs only.
- **Do not optimize for a specific test's failure modes.** Optimizing for
  a test produces a wiki that scores well on that test and badly on
  everything else. Build the wiki the domain needs, then measure.
- **Do not create a new page just because the source has a new section.**
  Ask: is this a new *concept* the wiki doesn't cover, or just a new
  *source* restating an existing concept?
- **Do not dump document-order prose.** Compress to rules. If you can't
  compress it to a rule, it probably doesn't belong in the wiki.
- **Do not skip Pass A.** Structure scan is what prevents reactive ingests.
