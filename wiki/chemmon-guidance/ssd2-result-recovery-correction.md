---
title: "SSD2 Result: Recovery and Recovery Correction (resValRec, resValRecCorr)"
type: "reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 68-69 (Section 2, elements M.11-M.12)"
  - "pp. 92-95 (Table 8, M.11 rows)"
  - "pp. 122, 132 (Table 10, CHEMON42, CHEMON80)"
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
- Recovery correction is generally not applied to adjust numerical pesticide results, but the M.11 prose says results for specific contaminants must be adjusted for recovery and the recovery rate reported, while Table 8 lists `resValRec` as "Recommended" for PAHs, mycotoxins, cadmium, lead and nitrates (see the list and the source discrepancy below). (ChemMon 2026 pp. 69, 92-95)

## Relevant Business Rules

- **CHEMON04/05/42** — Recovery ranges and dependency rules for `resValRec`/`resValRecCorr`.
- **CHEMON80** — For contaminants, `resValRecCorr` should be reported.

See [[business-rules-cross-cutting]] for CHEMON04/05/42 and [[business-rules-contaminant]] for CHEMON80.

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

**Source discrepancy:** the M.11 prose (p. 69) says results for these substances "must be adjusted for recovery and the recovery rate reported", but Table 8 gives `resValRec` (M.11) the status "Recommended" for PAHs, mycotoxins, cadmium, lead and nitrates (ChemMon 2026 pp. 92-95). No business rule makes `resValRec` mandatory: `CHEMON80` (Warning, p. 132) asks only that `resValRecCorr` be reported for contaminants, and `CHEMON42` (Warning, p. 122) asks for `resValRec` when `resValRecCorr` = Y.

### Expression format

The result value recovery rate (`resValRec`) associated with the concentration measurement is expressed as a percentage (%), i.e. 100 should be reported for a 100% rate.

### Default and reporting flag

Unless otherwise specified, the result expressed is considered by EFSA as **not corrected for recovery**. It is strongly recommended to report whether the analytical result has been or not corrected for recovery within the data element `resValRecCorr` ("Yes" ("Y") or "No" ("N")). In case of an empty field in the data element `resValRecCorr`, the system will return a Warning message with respect to the chemical contaminants domain. If the data provider reports a result corrected for recovery, the data element `resValRecCorr` must be set to "Yes" ("Y"). If reported, the results recovery must be greater than "0". (ChemMon 2026 p69)

### Example

| Description | XML |
| --- | --- |
| The concentration of aflatoxin M1 was corrected for a recovery rate of 63% | `<resValRec>63</resValRec><resValRecCorr>Y</resValRecCorr>` |

### Related business rules

- **CHEMON04** — `resValRec` should be ≥ 1%.
- **CHEMON05** — `resValRec` should be between 50% and 150%.
- **CHEMON42** — If `resValRecCorr=Y`, `resValRec` should be reported (Warning). The error message mentions 70–120%, but the rule description is a presence condition; use CHEMON04/05 for their separate range warnings (Table 10, p. 122).
- **CHEMON80** — For contaminants, `resValRecCorr` should be reported.

