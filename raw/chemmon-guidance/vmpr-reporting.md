---
title: "VMPR Reporting"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[business-rules]]"
last_updated: "2026-04-07"
---

# VMPR Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p41-50 -->
## Control Plan Types

VMPR data originates from several types of monitoring and control programmes:

| Plan | Description |
| --- | --- |
| Plan 1 | National risk-based control for domestic production. |
| Plan 2 | National randomised surveillance for domestic production. |
| Plan 3 | National risk-based control for third-country imports. |
| EU MACP | EU Multi-Annual Control Programme -- coordinated monitoring across Member States. |
| MANCP | Multi-annual national control plan -- umbrella framework covering all national food-chain controls. |

(ChemMon 2026 p41-43)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p43-45 -->
## Sampling Strategy Codes

Each VMPR sample carries a sampling strategy code describing how it was selected:

| Code | Strategy |
| --- | --- |
| ST10A | Objective (random or systematic) sampling. |
| ST20A | Selective (targeted/risk-based) sampling. |
| ST30A | Suspect sampling (follow-up on a positive or non-compliant finding). |
| ST90A | Other sampling strategy not covered above. |

(ChemMon 2026 p43-44)

## Programme Type Codes

| Code | Programme |
| --- | --- |
| K005A | National residue monitoring plan (Plan 1 / Plan 2). |
| K009A | Import controls (Plan 3). |
| K018A | EU MACP. |
| K019A | MANCP. |
| K038A | Other official control programme. |

(ChemMon 2026 p44-45)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p45-48 -->
## FoodEx2 Coding for VMPR

VMPR has specific FoodEx2 requirements beyond the general rules in [[foodex2-in-chemmon]]:

- **F01 (Source) and F02 (Part-nature)** are always required -- these two facets must be present on every VMPR sample. (ChemMon 2026 p45)
- **Wild game**: F21.A07RY (production method = wild/hunted) is mandatory for wild game samples. (ChemMon 2026 p46)
- **Feed samples**: F23 (target consumer) is required whenever the sample is animal feed rather than a food product. (ChemMon 2026 p46)
- **Non-food matrices** (urine, retina, hair, blood serum, etc.): use base term `A0C60` with explicit F01 and F02 facets to identify the animal species and the specific matrix. (ChemMon 2026 p46-47)
- **Processed products**: F33 (legislative classes) is mandatory for processed products as defined in Annex III of Regulation (EU) 2022/1646. (ChemMon 2026 p47)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p48-50 -->
## Result Types

VMPR analytical results are reported using one of these result type codes:

| Code | Meaning |
| --- | --- |
| VAL | Quantified numerical value (concentration measured). |
| LOQ | Result below the limit of quantification. |
| LOD | Result below the limit of detection. |
| BIN | Binary result (detected / not detected). |
| CCA | Decision limit (CC-alpha) -- used for substances with no permitted limit. |
| CCD | Detection capability (CC-beta) -- used for confirmatory method performance. |

(ChemMon 2026 p48-49)

## VMPR-Specific Business Rules

The following business rules apply specifically to the VMPR domain:

- **CHEMMON96**: Validates that VMPR samples carry the correct sampling strategy for the declared programme type (amended 2026). (ChemMon 2026 p49)
- **CHEMMON100**: Restricts which evaluation codes are permitted for VMPR results (new 2026). (ChemMon 2026 p49)
- **CHEMMON102**: Checks consistency across records sharing the same `sampleEventId` in VMPR submissions (new 2026). (ChemMon 2026 p50)

See [[business-rules]] for the full rule catalogue.

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p46-47 -->
## Worked Examples

### Urine from dairy cow
- Code: `A0C60#F01.A0C9L$F02.A0CET$F31.A0C8V`
- A0C60 is the non-food matrix base term. F01 identifies the source animal (dairy cow), F02 specifies the matrix (urine), and F31 provides additional classification detail. (ChemMon 2026 p46)

### Royal jelly
- Code: `A0CVG`
- Royal jelly has a dedicated base term with no explicit facets needed -- source and part-nature are implicit. (ChemMon 2026 p47)
