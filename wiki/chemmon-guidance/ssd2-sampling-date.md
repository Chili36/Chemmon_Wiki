---
title: "SSD2 Sampling: Date of Sampling"
type: "reference"
domain: "all"
last_updated: "2026-04-23"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 32 (Section 2, elements D.06-D.08)"
related:
  - "[[ssd2-elements-sampling]]"
  - "[[legal-limits-database]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-additives]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Sampling: Date of Sampling

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p32 -->

## Rule Summary (Rule-First)

- The full sampling date (`sampY`, `sampM`, `sampD`) is mandatory.
- The sampling date determines which legal limit applies and whether the result falls into the relevant annual-report window.
- Pesticides and VMPR are constrained to the expected reporting-year window. Additives/flavourings may include historical samples, but the annual report only counts the specific calendar year equal to submission year minus one.

## sampY / sampM / sampD — Date of sampling

<!-- Source: ChemMon 2026 p32 -->

**Element codes:** D.06, D.07, D.08 · **Names:** `sampY`, `sampM`, `sampD` · **Status:** mandatory

### Purpose

The complete date on which the sample was taken is mandatory. This information is required to check compliance against legal limits applicable at the time of sampling and to select results for inclusion in annual reports.

### Reporting window rules

- Samples taken in any year can be transmitted to the EFSA sDWH when the data provider has the data ready.
- For VMPR and pesticides, each EU report should only include samples taken in the specific calendar year and submitted within the agreed deadlines.
- For contaminants, food additives, and food flavourings, historical data may be reported. However, only samples from the specific calendar year equal to the submission year minus one are considered in the food additives/flavourings report.

### Example

| Description | XML |
| --- | --- |
| Friday 16 February 2019 | `<sampY>2019</sampY><sampM>02</sampM><sampD>16</sampD>` |

### Related business rules

- `CHEMMON43` — for pesticides/VMPR, `sampY` must be less than or equal to submission year minus one.
- `CHEMMON43_b` — for additives/flavourings, `sampY` must be less than submission year minus one.
