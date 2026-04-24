---
title: "SSD2 Evaluation: Legal Limit Value and Limit Type"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 73-74 (Section 2, elements N.01 and N.03)"
related:
  - "[[ssd2-elements-evaluation]]"
  - "[[legal-limits-database]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-pesticide]]"
---

# SSD2 Evaluation: Legal Limit Value and Limit Type

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 73-74 -->

## Rule Summary (Rule-First)

- `evalLowLimit` and `evalLimitType` describe the limit actually enforced against the result.
- In the ordinary SSD2 analytical path, EFSA's Legal Limits Database usually makes these fields unnecessary for standard EU MRL/MPL checks.
- They become important when a different or non-standard limit is being applied, such as a national limit.
- For pesticides, the allowed `evalLimitType` set is especially narrow.

## evalLowLimit / evalLimitType — Limit for the result evaluation

<!-- Source: ChemMon 2026 pp. 73-74 -->

**Element codes:** N.01, N.03 · **Names:** `evalLowLimit`, `evalLimitType` · **Catalogue:** `LMTTYP` · **Status:** optional, but needed in specific cases

### Purpose

These elements record the numeric legal limit used for evaluation and the type of limit applied. (ChemMon 2026 p73)

### When to report them

EFSA uses the Legal Limits Database to validate plausibility of `evalCode` against the reported result for standard EU pesticide and VMPR limits on unprocessed samples. Therefore, these fields are mainly needed when:

- a non-EU or non-standard limit is in use
- a national limit is being applied
- the standard automatic legal-limit lookup is not sufficient for the case

(ChemMon 2026 p73)

### Processed-product note

For non-regulated processed products, the limit to report is the one applicable to the corresponding unprocessed product. Transformation-factor detail can be described in `evalInfo.com` or `resInfo.com`. (ChemMon 2026 p73)

### Common limit types

For pesticides, the typical type is `W002A` (MRL). If `W990A` (national or local limit) is used, the result is disregarded from EU report analysis. (ChemMon 2026 p74)

For VMPR, the guidance lists these main values:

- `W002A` — MRL
- `W005A` — minimum required performance limit
- `W006A` — reference point of action
- `W012A` — presence
- `W001A` — maximum limit
- `W007A` — action level
- `W008A` — health-based guidance value
- `W990A` — other

## Related business rules

- `CHEMMON35` — allowed `evalLimitType` values. See [[business-rules-cross-cutting]].
- `CHEMMON46` — if `evalCode = J003A` and the limit is numeric rather than presence-based, `resType` must be `VAL`. See [[business-rules-cross-cutting]].
- `CHEMMON48` — if `paramType` is not `P002A` and `resVal >= evalLowLimit`, `evalCode` should not be `J029A`. See [[business-rules-cross-cutting]].
- `CHEMMON59` — pesticides only allow `W002A`, `W990A`, or blank. See [[business-rules-pesticide]].
