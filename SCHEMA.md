---
title: "Wiki Schema"
type: "reference"
domain: "all"
last_updated: "2026-10-13"
---

# Schema

This file defines the structural conventions for every page under `wiki/chemmon-guidance/`. It exists so that:

- An LLM can reason about page *type* before reading content.
- A health check can validate frontmatter and cross-links deterministically.
- New pages have a clear target shape to conform to.

The schema is grounded in the frontmatter fields already in use across the wiki — it formalizes rather than invents.

## Page Types

Every wiki page declares a `type` field. The allowed values and their meaning:

| type | Purpose | Examples |
|---|---|---|
| `overview` | High-level orientation for ChemMon as a whole. One per wiki. | `chemmon-overview.md` |
| `reference` | Stable specifications derived from external standards (data models, classification systems). | `ssd2-data-model.md`, `foodex2-in-chemmon.md` |
| `domain-guide` | Reporting rules and worked examples for a specific reporting domain. | `vmpr-reporting.md`, `pesticide-reporting.md`, `contaminant-reporting.md`, `food-additives-reporting.md`, `baby-food-reporting.md` |
| `rule-reference` | Canonical EFSA business rules (GBR, CHEMMON, Legal Limit) grouped by applicability. | `business-rules-gbr.md`, `business-rules-cross-cutting.md`, `business-rules-vmpr.md`, `business-rules-pesticide.md`, `business-rules-additives.md`, `business-rules-baby-food.md`, `business-rules-legal-limits.md`, `business-rules-2026-changes.md` |
| `hub` | Short orientation page that links to a family of related pages. No rule text of its own. | `business-rules.md` |

## Domain Values

Every wiki page declares a `domain` field. Allowed values:

| domain | Meaning |
|---|---|
| `all` | Applies to every reporting domain (overview, references, cross-cutting rules) |
| `vmpr` | Veterinary Medicinal Product Residues |
| `pesticide` | Pesticide residues / Plant Protection Products (PPP) |
| `contaminant` | Chemical contaminants (acrylamide, dioxins, BFRs, arsenic, mycotoxins, etc.) |
| `additives` | Food additives and flavourings |
| `baby-food` | Baby food, infant formula, follow-on formula |
| `cross-cutting` | Rules or guidance that apply across multiple domains |

## Frontmatter

### Required fields

| Field | Type | Notes |
|---|---|---|
| `title` | string | Human-readable page title |
| `type` | enum | One of the values in the Page Types table |
| `domain` | enum | One of the values in the Domain Values table |
| `last_updated` | ISO date (`YYYY-MM-DD`) | Updated whenever the page's rule text or substantive content changes |

### Recommended fields

| Field | Type | Notes |
|---|---|---|
| `sources` | list of strings | Source PDF filenames from `chemmon_docs/`, or a pinned dataset file such as `datasets/rd-bridge/residue_param_map.json`. Omit only for pure hub pages that host no substantive content. |
| `related` | list of wiki backlinks | Other pages the reader is likely to consult next. Uses `[[page-name]]` syntax without the `.md` extension. |

### Optional fields

| Field | Type | Notes |
|---|---|---|
| `source_pages` | list of strings | Page ranges in the source PDF, e.g. `["pp. 21-45"]`. Use when specific pages matter for verification. |
| `select_when` | string | Optional situation-based selection hint, at most 400 characters. Describe the decision the page helps resolve; otherwise the selector uses the index summary. |

## Conventions

### Wiki-style backlinks

Internal references between wiki pages use double-bracket syntax **without** the `.md` extension:

```markdown
See [[business-rules-vmpr]] for VMPR-specific rules.
Related: [[chemmon-overview]], [[foodex2-in-chemmon]].
```

This keeps cross-links path-agnostic so directory renames don't cascade edits. The health check resolves each backlink to a file under `wiki/chemmon-guidance/`.

### Source comments in body text

Rule text and prose claims are attributed to source documents via HTML comments next to the relevant section:

```markdown
## Analytical Method Rules

<!-- Source: EFSA Supporting Publications - 2026 - Chemical monitoring reporting guidance 2026 data collection.pdf, pp. 14-16 -->

**CHEMMON03**: ...
```

The comment is invisible in the human viewer. Model evidence preserves it as a
visible `Source:` line so source locators remain adjacent to the relevant claims.

### Dataset source comments

Claims taken from a pinned dataset snapshot (see [[INGEST_WORKFLOW]], dataset
sources) use a locator naming the file, the snapshot commit and the records:

```markdown
<!-- Source: datasets/rd-bridge/residue_param_map.json @ 104448e, residue_id 10, 210 -->
```

The health check reads the text from such a comment to the next `Source:`
comment. Every PARAM code and every Annex I commodity code written in
backticks (`` `1020000` ``) in it must occur in the cited records. In table rows, a code beside Annex I codes must be the
whole-residue code of an exception with exactly those included and excluded
codes, and a code in a row marked "Default" must be a default code. A
locator whose commit differs from the current snapshot is a warning until the
page is re-checked. These checks catch code drift, not wording errors.

Readings of residue-definition wording cite rd-bridge's curated
interpretation rules by ID:

```markdown
<!-- Source: datasets/rd-bridge/interpretation_guidance.json @ b4e9020, rules OECD-EXPRESSION-BASIS, EU-TEXT-CONTROLS -->
```

Each cited rule must exist in the snapshot. No PARAM code may appear under
such a comment; cite the residue records for codes.

### Generated pages

A page rendered from a dataset says so in an HTML comment under its title and
is never edited by hand: `pesticide-residue-definitions-by-food.md`,
`pesticide-residue-definitions-without-param-link.md` and
`pesticide-residue-definition-lookup.md` (whose records are attached per question by
`wiki_api/residue_lookup.py`); see [[INGEST_WORKFLOW]].

### Rule ID conventions

- **GBR rules**: `GBR2`, `GBR12`, `GBR27` — General Business Rules from SSD2.
- **CHEMMON rules**: preserve source IDs and suffixes, such as `CHEMMON03`, `CHEMMON84_a` and `CHEMMON90_b`. The PDF spells the prefix `CHEMON`; the wiki uses `CHEMMON` as an explicit alias. Numbering has gaps and merged IDs; do not infer a continuous range.
- **Legal Limit rules**: `LL_01_VMPR`, `LL_02_PPP`, `LL_03_FA_FF`, etc.; preserve the source-derived inventory's underscore form.
- **FoodEx2 validation**: `FOODEX2_SAMPMAT`, `FOODEX2_ANMAT`.

Canonical SSD2 rule definitions belong in the topic/domain
`business-rules-*.md` files; the annual-change page describes deltas. PRE and
USE definitions belong to their separate data-model pages. The health check
compares all five families with the independently source-derived inventory,
reporting missing, unexpected, duplicate and inactive definitions. The former
CHEMMON03 duplicate was a wiki error, corrected on 5 October 2026.
ID coverage is complete for applicable active rows, including all 83 generic
rules, but this does **not** prove that every description matches its source.
See [[SOURCE_REVIEW]] for completed source comparisons, unresolved PDF wording and review limits.

## Example: valid frontmatter block

```yaml
---
title: "VMPR-Specific Business Rules"
type: "rule-reference"
domain: "vmpr"
last_updated: "2026-04-10"
sources:
  - "EFSA Supporting Publications - 2026 - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 45-48"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[vmpr-reporting]]"
---
```
