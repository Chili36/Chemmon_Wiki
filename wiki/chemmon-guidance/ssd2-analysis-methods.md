---
title: "SSD2 Analysis: Analytical Method Identification and Type"
type: "reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 63-64 (Section 2, elements L.01, L.03, L.04)"
  - "pp. 83, 92, 144 (Tables 7, 8 and 11, catalogue name ANLYMD)"
  - "pp. 100-101 (Table 9, GBR11, GBR18)"
  - "pp. 118-120, 132 (Table 10, CHEMON23, CHEMON30, CHEMON33, CHEMON34, CHEMON79)"
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

`anMethRefCode`, `anMethCode`, `anMethText`, and `anMethInfo` must be constant (the same) for all results with the same `anMethRefId`. (ChemMon 2026 p63; `GBR11`, Error, Table 9 p100)

Example of coding `anMethRefId` per laboratory and method combination (ChemMon 2026 p64):

| Lab | Result | `anMethCode` | `anMethText` | `anMethInfo` | `anMethRefId` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1, 2, 3 | `F027A` | LC-MS/MS | combinationMS_LC | `XX12_LC_MS_Lab1` |
| 2 | 4, 5, 6 | `F027A` | LC-MS/MS | combination_lab2 | `XX12_LC_MS_Lab2` |

Other `anMethRefId` examples: `BulkMilkAntibioticSCR2017` (Delvo test for antibacterial substances in bulk milk validated in 2017), `NRLGC-MSHoney`, `2020-LC-MS-E951`, `2019-LC-GC-FID-Veg-Oil`. (ChemMon 2026 p63)

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

**Element code:** L.04 · **Name:** `anMethCode` · **Catalogue:** `ANLYMD` · **Status:** mandatory

### Purpose

`anMethCode` describes the type of analysis performed by the laboratory. It is strongly advised to report the specific analytical method instead of `F001A` ("Classification not possible"). If the generic code `F001A` is reported, enter also `anMethText`. (ChemMon 2026 p64)

Codes for `anMethType` and `anMethCode` can be selected from the ANLYTYP catalogue and the ANYLMD catalogue (spelling as printed). (ChemMon 2026 p64) **Source discrepancy:** p. 64 prints "ANYLMD", while Table 7 (p. 83), Table 8 (p. 92) and Table 11 (p. 144) print `ANLYMD`. The guidance does not explain the difference.

| Example | `anMethType` | `anMethCode` |
| --- | --- | --- |
| Charm II test to screen for tetracyclines in animal tissues | `AT06A` | `F580A` |
| Multiresidue method using gas chromatography with tandem mass spectrometry | `AT08A` | `F049A` |
| Liquid chromatography–tandem mass spectrometry used to quantify unauthorised residues in animal samples | `AT08A` | `F027A` |

(ChemMon 2026 p64)

### Special restriction for contaminants, additives, and flavourings

For chemical contaminants, food additives and food flavourings, the system returns an error message if `anMethCode` is reported as `F001A` (ChemMon 2026 p64). `CHEMON79` (Error) covers contaminants, food additives and food flavourings and also blocks `F500A` (Unknown) and `F598A` (Unspecified) (Table 10, p132).

**Source discrepancy:** the same p. 64 sentence continues "if the generic code F001A is reported, enter also anMethText", which reads as if `F001A` with text were acceptable for these three domains; `CHEMON79` (p. 132) rejects `F001A` for them with an Error, so validation enforces the rule. The text requirement itself is the general rule below.

## Related business rules

- `GBR11` (Error) — `anMethRefCode`, `anMethCode`, `anMethText` and `anMethInfo` must be constant for all records with the same `anMethRefId` (Table 9, p100).
- `GBR18` (Error) — if `anMethCode.base` is `F001A` (Classification not possible), a text must be reported in `anMethText` (Table 9, p101).
- `CHEMON23` — `anMethType` must be `AT06A` or `AT08A`. See [[business-rules-cross-cutting]].
- `CHEMON30` — if `evalCode = J003A`, `anMethType` must be `AT08A`. See [[business-rules-cross-cutting]].
- `CHEMON33` — if `resType=BIN`, `anMethType` must be AT06A; published severity is **Error**, despite “should” in the description (Table 10, p. 120). See [[business-rules-cross-cutting]].
- `CHEMON34` (Warning) — if `anMethType = AT08A`, `resType` should not be `BIN` and `resQualValue` should not be reported (Table 10, p120). See [[business-rules-cross-cutting]].
- `CHEMON79` (Error) — for contaminants, food additives and food flavourings, `anMethCode` must be different from `F001A` (Classification not possible), `F500A` (Unknown) and `F598A` (Unspecified); the description says "should be different", the error message "must be different" (Table 10, p132). See [[business-rules-cross-cutting]].
