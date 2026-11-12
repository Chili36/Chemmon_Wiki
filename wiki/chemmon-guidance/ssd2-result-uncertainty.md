---
title: "SSD2 Result: Measurement Uncertainty (resValUncert)"
type: "reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 72 (Section 2, element M.17)"
  - "p. 69 (Section 2, element M.11, erucic acid reference)"
  - "pp. 131, 135 (Table 10, CHEMON72, CHEMON90_b)"
related:
  - "[[ssd2-elements-result]]"
  - "[[ssd2-result-value-and-type]]"
  - "[[business-rules-pesticide]]"
---

# SSD2 Result: Measurement Uncertainty (resValUncert)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p. 72 -->

## Rule Summary (Rule-First)

- `resValUncert` is the expanded measurement uncertainty (typically 95% confidence interval) in the same unit as `resUnit`.
- `resValUncert` is requested only when `resType = VAL`.
- For results below LOQ, do not report MU.
- Some rules escalate MU from "recommended" to "mandatory" (notably copper, `paramCode` `RF-0102-001-PPP`: `CHEMON90_b` is triggered by the `paramCode` and names no domain flag; ChemMon 2026 p135).

## Relevant Business Rules

- **CHEMON72** — For pesticides, `resValUncert` should be reported when `resType = VAL`.
- **CHEMON90_b** (Error) — If `paramCode` `RF-0102-001-PPP` (Copper) is reported, `resValUncert` must be reported if `resType = VAL` (Table 10, p135).

See [[business-rules-pesticide]].

## resValUncert — Result value uncertainty

<!-- Source: ChemMon 2026 p72 -->

**Element code:** M.17 · **Name:** `resValUncert` · **Status:** optional

### Purpose

The `resValUncert` indicates the **expanded measurement uncertainty value** (usually 95% confidence interval) associated with the measurement. This uncertainty is expressed in the same unit as the one reported in the field `resUnit`.

### Recommendation for pesticide residues

For pesticide residue monitoring, it is recommended to populate this field especially if single residue methods are used and/or if for a multiresidue method the expanded measurement uncertainty (MU) is different than 50%. The `resValUncert` is requested only when `resType = VAL`. (ChemMon 2026 p72)

### Scope of use

According to Regulation (EU) 2023/2782 (on mycotoxins), Regulation (EC) No 705/2015 (on erucic acid), Regulation (EC) No 333/2007, and Regulation (EC) No 644/2017, the condition for acceptance of a lot should also take into consideration measurement uncertainty. (ChemMon 2026 p72)

**Source discrepancy:** for erucic acid, M.17 (p. 72) cites "Regulation (EC) No 705/2015", while M.11 (p. 69) cites Commission Regulation (EU) 2023/2783 (see [[ssd2-result-recovery-correction]]). The guidance does not explain the difference; both are quoted as printed.

### Note on below-LOQ values

For results below the LOQ value, no MU is to be reported as it is "a parameter characterising the dispersion of quantify values being attributed to a measurand" (International vocabulary of metrology, ISO-2007: ISO/IEC guide 99, VIM 3). (ChemMon 2026 p72)

