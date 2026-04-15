---
title: "SSD2 Result: Recovery and Recovery Correction (resValRec, resValRecCorr)"
type: "reference"
domain: "all"
last_updated: "2026-04-15"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 68-69 (Section 2, elements M.11-M.12)"
related:
  - "[[ssd2-elements-result]]"
  - "[[ssd2-result-value-and-type]]"
  - "[[business-rules-contaminant]]"
---

# SSD2 Result: Recovery and Recovery Correction

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 68-69 -->

## Rule Summary (Rule-First)

- Unless explicitly flagged, EFSA treats reported results as **not corrected for recovery**.
- If the result is corrected for recovery, set `resValRecCorr = Y` and report `resValRec` as a percentage.
- Recovery correction is generally not applied to adjust numerical pesticide results, but is mandatory for specific contaminant frameworks (see list below).

## Relevant Business Rules

- **CHEMMON04/05/42** — Recovery ranges and dependency rules for `resValRec`/`resValRecCorr`.
- **CHEMMON80** — For contaminants, `resValRecCorr` should be reported.

See [[business-rules-contaminant]].

## resValRec / resValRecCorr — Recovery and recovery correction

<!-- Source: ChemMon 2026 pp. 68-69 -->

**Element codes:** M.11, M.12 · **Names:** `resValRec`, `resValRecCorr` · **Status:** optional

### Purpose

The results from analytical methods which **do not include an extraction step** or analytical methods which use **certified reference material at a certified concentration** must be reported uncorrected for extraction recovery during the sample preparation. (ChemMon 2026 p68)

Calculated recovery corrections are typically used to assess the performance of the method. These should not be applied to adjust the numerical results of pesticide residue analysis.

### Mandatory recovery correction for specific contaminants

However, for the following the results must be **adjusted for recovery and the recovery rate reported** (unless specific conditions occur, e.g. for result significantly lower or higher than the maximum level):

- mycotoxins per Commission Regulation (EU) 2023/2782
- erucic acid per Commission Regulation (EU) 2023/2783
- nitrates per Commission Regulation (EC) No 1882/2006
- lead, cadmium, mercury, inorganic tin, 3-MCPD and benzo(a)pyrene per Commission Regulation 333/2007

(ChemMon 2026 p69)

### Expression format

The result value recovery rate (`resValRec`) associated with the concentration measurement is expressed as a percentage (%), i.e. 100 should be reported for a 100% rate.

### Default and reporting flag

Unless otherwise specified, the result expressed is considered by EFSA as **not corrected for recovery**. It is strongly recommended to report whether the analytical result has been or not corrected for recovery within the data element `resValRecCorr` ("Yes" ("Y") or "No" ("N")). In case of an empty field in the data element `resValRecCorr`, the system will return a Warning message with respect to the chemical contaminants domain. If the data provider reports a result corrected for recovery, the data element `resValRecCorr` must be set to "Yes" ("Y"). If reported, the results recovery must be greater than "0". (ChemMon 2026 p69)

### Example

| Description | XML |
| --- | --- |
| The concentration of aflatoxin M1 was corrected for a recovery rate of 63% | `<resValRec>63</resValRec><resValRecCorr>Y</resValRecCorr>` |

### Related business rules

- **CHEMMON04** — `resValRec` should be ≥ 1%.
- **CHEMMON05** — `resValRec` should be between 50% and 150%.
- **CHEMMON42** — If `resValRecCorr` = Yes, `resValRec` must be reported and should be in 70-120% range.
- **CHEMMON80** — For contaminants, `resValRecCorr` should be reported.

