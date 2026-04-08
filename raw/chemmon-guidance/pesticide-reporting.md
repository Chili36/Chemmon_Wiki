---
title: "Pesticide Residues Reporting"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[business-rules]]"
  - "[[contaminant-reporting]]"
  - "[[vmpr-reporting]]"
  - "[[baby-food-reporting]]"
last_updated: "2026-04-07"
---

# Pesticide Residues Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p25-32 -->
## Scope

- Pesticide residues monitoring and enforcement under Regulation (EC) No 396/2005. (ChemMon 2026 p25)
- Covers EU coordinated programmes, national monitoring programmes, and targeted enforcement sampling. (ChemMon 2026 p25-26)

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
## Copper-Specific Requirements (New 2026)

Copper is reported in the pesticide domain. Specific F20 facet codes are required to distinguish preparation states across commodities.

- **CHEMMON90_a** (Warning): specific F20 facet codes required for different commodity types. (ChemMon 2026 p30)
- **CHEMMON90_b** (Error): result value uncertainty is mandatory for copper results. (ChemMon 2026 p31)

### Required F20 Codes by Commodity

| Commodity | With Peel/Shell/Stone | Without Peel/Shell/Stone |
| --- | --- | --- |
| Citrus fruits | `F20.A07QF` (with peel) | `F20.A07QE` (without peel) |
| Chestnuts | `F20.A07QD` (with shell) | `F20.A07QC` (without shell) |
| Stone fruits | `F20.A07QK` (with stone) | `F20.A07QJ` (without stone) |
| Sweet corn | `F20.A07RF` (kernels with cob) | `F20.A07RE` (kernels without cob) |
| Animal products | `F20.A0F4T` (muscle with trimmable fat) | `F20.A0F4V` (muscle without trimmable fat) |

- Roasted coffee beans: `F28.A07GY` (roasted beans only). (ChemMon 2026 p31)
- Fruits and vegetables: `F28.A07G` (unwashed) when applicable. (ChemMon 2026 p31)

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
