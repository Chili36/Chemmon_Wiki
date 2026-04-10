---
title: "Wiki Schema"
type: "reference"
domain: "all"
last_updated: "2026-04-10"
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
| `sources` | list of strings | Source PDF filenames from `chemmon_docs/`. Omit only for pure hub pages that host no substantive content. |
| `related` | list of wiki backlinks | Other pages the reader is likely to consult next. Uses `[[page-name]]` syntax without the `.md` extension. |

### Optional fields

| Field | Type | Notes |
|---|---|---|
| `source_pages` | list of strings | Page ranges in the source PDF, e.g. `["pp. 21-45"]`. Use when specific pages matter for verification. |

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

The comment is invisible in rendered output but lets a human or LLM verify a claim against the canonical PDF.

### Rule ID conventions

- **GBR rules**: `GBR2`, `GBR12`, `GBR27` — General Business Rules from SSD2.
- **CHEMMON rules**: `CHEMMON01` through `CHEMMON109+`, with letter suffixes like `CHEMMON79_a`, `CHEMMON79_b`, `CHEMMON79_c` for variant rules.
- **Legal Limit rules**: `LL_01 VMPR`, `LL_02 PPP`, `LL_03 FA_FF`, etc.
- **FoodEx2 validation**: `FOODEX2_SAMMAT`, `FOODEX2_ANMAT`.

Every `CHEMMON\d+` rule ID must appear **exactly once** across the 8 `business-rules-*.md` slice files. The health check enforces this to prevent duplication or silent drops during maintenance.

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
