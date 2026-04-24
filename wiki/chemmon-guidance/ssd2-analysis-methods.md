---
title: "SSD2 Analysis: Analytical Method Identification and Type"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 63-64 (Section 2, elements L.01, L.03, L.04)"
related:
  - "[[ssd2-elements-analysis]]"
  - "[[ssd2-result-method-accreditation]]"
  - "[[business-rules-cross-cutting]]"
---

# SSD2 Analysis: Analytical Method Identification and Type

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 63-64 -->

## Rule Summary (Rule-First)

- `anMethRefId` is the laboratory’s stable identifier for the analytical method and must be present.
- Records that share the same `anMethRefId` must keep the associated method metadata consistent.
- `anMethType` is effectively a screening-vs-confirmation switch.
- `anMethCode` should be specific; generic fallback values are especially problematic for contaminants, additives, and flavourings.

## anMethRefId — Analytical method reference

<!-- Source: ChemMon 2026 pp. 63-64 -->

**Element code:** L.01 · **Name:** `anMethRefId` · **Status:** mandatory · **Length:** <= 50

### Purpose

`anMethRefId` is the laboratory’s internal identifier for the analytical method. It groups all results obtained from the same method. (ChemMon 2026 p63)

### Consistency rule

`anMethRefCode`, `anMethCode`, `anMethText`, and `anMethInfo` must stay constant for all results that share the same `anMethRefId`. (ChemMon 2026 p63)

## anMethType — Analytical method type

<!-- Source: ChemMon 2026 p64 -->

**Element code:** L.03 · **Name:** `anMethType` · **Catalogue:** `ANLYTYP` · **Status:** mandatory

### Main values

| Code | Meaning |
| --- | --- |
| `AT06A` | Screening |
| `AT08A` | Confirmation |

Screening should be used only when a qualitative method returns a negative result; confirmation is the expected route for quantitative or semi-quantitative methods. (ChemMon 2026 p64)

## anMethCode — Analytical method code

<!-- Source: ChemMon 2026 p64 -->

**Element code:** L.04 · **Name:** `anMethCode` · **Catalogue:** `ANYLMD` · **Status:** mandatory

### Purpose

`anMethCode` identifies the specific analytical method used by the laboratory. The guidance strongly recommends reporting the specific method instead of generic fallback codes such as `F001A` ("Classification not possible"). (ChemMon 2026 p64)

### Special restriction for contaminants, additives, and flavourings

For contaminants, food additives, and food flavourings, generic fallback method codes are not acceptable in the same way they might be elsewhere. If `F001A` is used, additional method text is also required, and several fallback codes are explicitly blocked by business rules. (ChemMon 2026 p64)

## Related business rules

- `CHEMMON23` — `anMethType` must be `AT06A` or `AT08A`. See [[business-rules-cross-cutting]].
- `CHEMMON30` — if `evalCode = J003A`, `anMethType` must be `AT08A`. See [[business-rules-cross-cutting]].
- `CHEMMON33` — if `resType = BIN`, `anMethType` should be `AT06A`. See [[business-rules-cross-cutting]].
- `CHEMMON34` — if `anMethType = AT08A`, `resType` should not be `BIN`. See [[business-rules-cross-cutting]].
- `CHEMMON79_a/b/c` — contaminants/additives/flavourings cannot use generic fallback analytical-method codes such as `F001A`, `F500A`, or `F598A`. See [[business-rules-cross-cutting]].
