---
title: "SSD2 Elements: Result Values (resId through resInfo)"
type: "reference"
domain: "all"
last_updated: "2026-04-15"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 64-73 (Section 2, elements M.01-M.20)"
related:
  - "[[ssd2-elements-evaluation]]"
  - "[[ssd2-data-model]]"
  - "[[ssd2-result-units-and-limits]]"
  - "[[ssd2-result-value-and-type]]"
  - "[[ssd2-result-expression-basis]]"
  - "[[ssd2-result-method-accreditation]]"
  - "[[ssd2-result-recovery-correction]]"
  - "[[ssd2-result-uncertainty]]"
  - "[[ssd2-result-identification]]"
---

# SSD2 Elements: Result Values

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 64-73 -->

## Overview

The result group captures the numeric and qualitative outputs of the analysis: detection/quantification limits, the measured value, units, recovery, expression basis (whole/fat/dry weight), result type, and measurement uncertainty. See [[ssd2-elements-evaluation]] for how the result is compared against legal limits.

This page is intentionally kept short and acts as a navigation hub plus a "fast path" summary. Detailed per-element guidance is split into narrowly-scoped subpages (below) so the wiki stays retrievable and reusable.

## Rule Summary (Rule-First)

Use these as the "fast path" when coding/debugging result records:

- `resType` drives which value fields are allowed/required (e.g. `VAL` -> `resVal`, `LOD` -> `resLOD`, `LOQ` -> `resLOQ`, `BIN` -> qualitative value).
- `resLOQ` is expected for most chemical-monitoring results; the guidance lists narrow exceptions (unvalidated methods, some VMPR cases, `resType=BIN`, and sum/not-summed scenarios).
- VMPR: at least one of `resLOD`, `resLOQ`, `CCalpha`, or `CCbeta` must be reported per result (and CCalpha/CCbeta become mandatory in specific accreditation/method cases).
- Expression basis matters: when expressing results on fat or dry-matter basis, the corresponding percentage (fat/moisture) must be available where required.
- Processed products: report the result for the sample analysed (the processed product) without "back-calculating" to the unprocessed commodity (with specific pesticide-domain compliance caveats handled via facets, not by altering the numeric result).

## Relevant Business Rules

This page is constrained by business rules; the most load-bearing ones:

- GBR result-shape rules (units/required fields): GBR27/28/29, GBR36/39/46/47/48, GBR37, GBR102. See [[business-rules-gbr]].
- `resLOQ`/limits rules: CHEMMON44/45, CHEMMON78, CHEMMON82. See [[business-rules-cross-cutting]].
- VMPR CCalpha/CCbeta requirements: CHEMMON31/32. See [[business-rules-vmpr]].
- Recovery metadata: CHEMMON04/05/42, CHEMMON80. See [[business-rules-contaminant]].
- Uncertainty: CHEMMON72 (recommended for pesticides), CHEMMON90_b (mandatory for copper). See [[business-rules-pesticide]].

## Relevant Policy

- If prose guidance and business rules conflict on mandatory/optional status, follow the business rule (and the current-year ChemMon guidance) for what passes DCF validation.
- Prefer encoding context via the appropriate elements/facets (e.g. expression basis, sample-preparation facets) rather than altering numeric results to "fit" a downstream interpretation.

## Subpages

- [[ssd2-result-units-and-limits]] — `resUnit`, `resLOD`, `resLOQ`, and `resInfo.notSummed` (LOQ exceptions and placeholder bans).
- [[ssd2-result-method-accreditation]] — `accredProc`, `CCalpha`, `CCbeta` and VMPR-specific requirements.
- [[ssd2-result-value-and-type]] — `resVal`, `resQualValue`, and `resType` (including AWR).
- [[ssd2-result-recovery-correction]] — recovery metadata (`resValRec`, `resValRecCorr`).
- [[ssd2-result-expression-basis]] — expression basis (`exprResType`, `exprResPerc`) by domain.
- [[ssd2-result-uncertainty]] — measurement uncertainty (`resValUncert`).
- [[ssd2-result-identification]] — result identifier (`resId`) uniqueness and naming guidance.
