---
title: "Wiki Log"
last_updated: "2026-04-10"
---

# Log

## [2026-04-10] refactor | Full patterns refactor (closes #1)

Aligned the repo with community best practices that have crystallized around Karpathy-style LLM wikis: compiled layer vs distilled tier, short opinionated files, selective injection, deterministic-first selection, schema + frontmatter, compiler-analogy layer naming.

**Structural changes:**

- **Split `business-rules.md`** (27 KB / 299 lines / 100+ rules) into **nine slice files** under `wiki/chemmon-guidance/business-rules-*.md`: gbr, cross-cutting, vmpr, pesticide, contaminant, additives, baby-food, legal-limits, 2026-changes. Rule text preserved verbatim 1:1 — IDs, severities, source comments, and citations unchanged. Only the hosting file changed.
- **Added a ninth slice (`business-rules-contaminant.md`)** beyond the original 8-file plan: 19 CONT-only CHEMMON rules had no clean home otherwise. Contaminant is a first-class domain in the wiki alongside VMPR, pesticide, additives, and baby-food.
- **`business-rules.md` rewritten as a short hub page** (~40 lines) linking to the 9 slices. Preserves `[[business-rules]]` as a valid backlink target for generic queries.
- **Renamed `raw/chemmon-guidance/` → `wiki/chemmon-guidance/`** to match the pattern-language tier naming. `chemmon_docs/` remains the raw PDF source layer.
- **Sliced files ARE the distilled layer** for rule-lookup-shaped flows. No separate `distilled/` tier added — that's only worth building if a task-shaped flow (e.g. "FoodEx2 code this roasted coffee") becomes painful.

**Schema and frontmatter:**

- **Added `SCHEMA.md`** defining five page types (overview, reference, domain-guide, rule-reference, hub), seven domain values, required frontmatter fields, wiki-link convention, source-comment convention, and rule ID conventions.
- **Enriched frontmatter on all 18 wiki pages** with `type` and `domain` fields per schema.

**Deterministic selector fast-path:**

- **Added `_try_deterministic_selection()` in `wiki_api/app.py`** short-circuiting the LLM page-selector call for 6 keyword patterns (vmpr, pesticide, baby-food, food-additive, contaminant, legal-limit) plus CHEMMON rule-ID lookups. Rule-ID mapping covers all 104 unique CHEMMON rules across the slice files.
- **Every fast-path hit includes `business-rules-cross-cutting.md`** as a default companion.
- **Trace marks fast-path calls** with `{"fast_path": true, ...}` in `tool_trace` and `"model": "fast-path"` in the selector token summary so observability stays consistent.
- **LLM selector remains the fallback** for questions that don't match any pattern.

**Health check:**

- **Added `tools/health_check.py`** validating frontmatter schema compliance, resolving every `[[wiki-link]]`, checking CHEMMON rule-ID coverage across slice files, and detecting stale `raw/chemmon-guidance/` prose references. Runnable standalone or via `tests/test_health.py` in CI.
- **Known source bug surfaced as a warning**: the EFSA guidance defines `CHEMMON03` twice with different text (once as an analytical method rule, once as a PPP country consistency rule). Both entries preserved verbatim in the slice files; the health check flags it as a warning (not error) for human review.

**Tests:**

- Updated `tests/test_wiki_store.py` and `tests/test_app.py` to check broader membership assertions (16+ pages) instead of hardcoded `"business-rules.md"` lookup.
- Added `tests/test_fast_path.py` (30 unit tests) covering rule-ID routing, each keyword pattern, fall-through behavior, and rule-to-slice mapping sanity.
- Added `tests/test_app.py::test_ask_fast_path_skips_llm_selector` for end-to-end fast-path validation.
- Added `tests/test_health.py` wrapping the health check for CI.
- Full suite: **50 tests passing, 0 failing, 1 warning** (the expected CHEMMON03 duplicate).

**Explicitly out of scope for this pass:**

- No second distilled tier (task-oriented decision files).
- No idea file capturing the pattern itself — this is a domain repo.
- No `WikiStore` subdirectory support (flat filenames sidestep the work).
- No static viewer changes.
- No rename of `chemmon_docs/` → `raw/`.
- No rule rewording, renumbering, or severity changes.

## [2026-04-07] setup | Initial ChemMon wiki repo

- Created the ChemMon wiki repo following the LLM wiki pattern.
- Set up empty source and guidance directories.
- Added wiki API with a single Q&A endpoint at /wiki/ask.

## [2026-04-07] ingest | Initial ChemMon guidance compilation

- Created seven topic-oriented markdown pages under `wiki/chemmon-guidance/` from the ChemMon 2026 reporting guidance and the SSD2 standard specification.
- Seeded pages for ChemMon overview, SSD2 data model, FoodEx2 in ChemMon, business rules (CHEMMON01-109), VMPR reporting, contaminant reporting, and food additives/flavourings reporting.
- Kept the source PDFs unchanged in `chemmon_docs/`.
- Updated `index.md` with the new page catalog.

## [2026-04-07] maintenance | Writing quality pass

- Fixed incorrect F27 description in foodex2-in-chemmon.md (was "brand or marketing type", should be "source commodity").
- Corrected CHEMMON100 and CHEMMON102 descriptions in vmpr-reporting.md to match the actual business rule definitions.
- Moved copper-specific F20 requirements from contaminant-reporting.md to a new pesticide-reporting.md page, since CHEMMON90_a/b are PPP-domain rules.
- Added pesticide-reporting.md covering legal references, sampling strategies, copper facet codes, and PPP-domain business rules.
- Added page number citations to contaminant-reporting.md source comments.

## [2026-04-08] ingest | Full-document second pass (pages 21-156)

- Expanded business-rules.md from 30 rules to 100+ rules across GBR, CHEMMON, and legal limit categories, organized into 9 subcategories.
- Added baby-food-reporting.md covering VMPR exclusion (CHEMMON55/63), accepted domains, classification codes, and legal limit basis.
- Expanded vmpr-reporting.md with feed/water coding, processed products with F33, wild game exclusions, insects as novel food, and baby food exclusion cross-reference.
- Expanded contaminant-reporting.md with 9 new substance sections: dioxins/PCBs, BFRs, arsenic, chlorates, bisphenol, PAHs, 3-MCPDs, mineral oils, and nitrates.
- Expanded food-additives-reporting.md with result reporting rules, 4 new worked examples, restriction/exception coding, and conclusion reporting.
- Updated index.md with revised page descriptions and the new baby food page.
