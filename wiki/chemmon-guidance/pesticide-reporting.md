---
title: "Pesticide Residues Reporting"
type: "domain-guide"
domain: "pesticide"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[business-rules]]"
  - "[[contaminant-reporting]]"
  - "[[vmpr-reporting]]"
  - "[[baby-food-reporting]]"
last_updated: "2026-04-11"
---

# Pesticide Residues Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p25-32 -->
## Scope

- Pesticide residues is one of five [[chemmon-overview|ChemMon]] reporting domains, covering monitoring and enforcement under Regulation (EC) No 396/2005. (ChemMon 2026 p25)
- Covers EU coordinated programmes, national monitoring programmes, and targeted enforcement sampling. (ChemMon 2026 p25-26)
- Matrix coding follows [[foodex2-in-chemmon]] rules. Copper reporting overlaps with [[contaminant-reporting]] (different F20 codes apply depending on domain).

## Mandatory Legal References

Each pesticide submission must carry a `progLegalRef` code identifying the regulatory basis:

| Code | Regulation |
| --- | --- |
| N027A | Regulation (EU) 2024/989 -- EU coordinated programme for pesticide residues |
| N028A / N318A | Regulation 2021/1355 -- baby food sampling. See [[baby-food-reporting]]. |
| N371A | Regulation 2022/1646 -- VMPR sampling. See [[vmpr-reporting]]. |
| N375A / N112A / N113A | Contamination control plans |
| N317A | Border control posts |
| N422A | Regulation (EU) -- intensified official controls at border control posts for animal-origin products (new 2026) |

(ChemMon 2026 p26-28)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p28-30 -->
## Sampling Strategies

| Code | Strategy |
| --- | --- |
| ST10A | Objective sampling (surveillance) |
| ST20A | Selective sampling (targeted) -- extended in 2026 to include K009A and K018A programme types |
| ST30A | Suspect sampling (enforcement) |

(ChemMon 2026 p28-29)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p30-32 -->
## Copper-Specific Requirements

Copper is reported in the pesticide domain. Specific F20 facet codes are required to distinguish preparation states across commodities.

- **CHEMMON90_a** (Warning): for copper, facet F20 (part-consumed-analysed) and/or facet F28 (process) is needed to describe sample preparation. (ChemMon 2026 Table 10)
- **CHEMMON90_b** (Error): for copper with `resType=VAL`, result value uncertainty (`resValUncert`) is mandatory. (ChemMon 2026 Table 10)

<!-- Source: ChemMon 2026 pp. 40-41 (Coding of copper samples under pesticides or contaminants) -->

### Copper sample-preparation facets (F20/F28)

For copper, EFSA asks data providers to include facets that describe sample preparation, because the same base term can be interpreted differently depending on whether the result is treated as pesticide-residue-style or contaminant-style data. In practice this means:

- **Pesticide residues**: use the facet/code that matches pesticide preparation.
- **Contaminants** (for reference): use the facet/code that matches contaminant preparation.

| Commodity group | Pesticide residues coding | Contaminants coding (reference) |
| --- | --- | --- |
| Citrus fruits, misc fruits with inedible peel, cucurbits with inedible peel, potatoes | With peel: `F20.A07QE` | Without peel: `F20.A07QF` |
| Chestnuts | With shell: `F20.A07QC` | Without shell: `F20.A07QD` |
| Stone fruits | With stone: `F20.A07QJ` | Without stone: `F20.A07QK` |
| Sweet corn | Kernels with cob: `F20.A07RE` | Kernels without cob: `F20.A07RF` |
| Products of animal origin (muscle) | After removal of trimmable fat: `F20.A0F4V` | With fat: `F20.A0F4T` |
| Fruits/vegetables/fungi (washed state matters) | No F28 code (not washed) | Washed: `F28.A07JG` |

For coffee beans specifically: contaminants use roasted beans (`F28.A07GY`), while pesticide residues use green beans. (ChemMon 2026 p41)

### Measurement uncertainty (resValUncert)

When reporting copper with `resType=VAL`, `resValUncert` is mandatory (CHEMMON90_b). (ChemMon 2026 p31)

<!-- Source: ChemMon 2026 p42 (Drinking water recommendation) -->
## Drinking Water (A03DK)

EFSA encourages data providers to collect and submit available information for pesticides (and contaminants) in **drinking water intended for human consumption**, using FoodEx2 base term `A03DK` ("Drinking water") and its children. (ChemMon 2026 p42)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p30-32 -->
## Pesticide-Specific Business Rules

| Rule | Severity | Description |
| --- | --- | --- |
| CHEMMON02 | Error | Country of sampling must equal reporting organisation country |
| CHEMMON03 | Error | `sampCountry`/`origCountry` consistency |
| CHEMMON90_a | Warning | Copper-specific F20 facet codes required |
| CHEMMON90_b | Error | Result value uncertainty mandatory for copper |
| CHEMMON94 | Error | Third-country import sampling point restriction (amended 2026) |
| CHEMMON95 | Warning | PPP sampling country validation (amended 2026) |
| CHEMMON101 | Error | N422A regulation programme type (new 2026) |
| CHEMMON104 | Error | N422A regulation exclusive programme reference (new 2026) |
| CHEMMON105 | Error | N317A regulation exclusive programme reference (new 2026) |

See [[business-rules]] for the full rule catalogue.
