---
title: "Food Additives and Flavourings Reporting"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[business-rules]]"
  - "[[contaminant-reporting]]"
last_updated: "2026-04-07"
---

# Food Additives and Flavourings Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Scope

- Food additives are regulated under Regulation (EC) No 1333/2008. (ChemMon 2026)
- Food flavourings are regulated under Regulation (EC) No 1334/2008. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Mandatory Facets

- **F33 (Legislative classes)**: MANDATORY for both food additive and flavouring samples. (ChemMon 2026)
- **F03 (Physical state)**: recommended for dairy products, cereals, soups, sauces, infant foods, juices, and food supplements. (ChemMon 2026)
- **F23 (Target consumer)**: required for infant formulas and follow-on formulas. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Expression Type

- The `exprResType` element is mandatory for food additives and flavourings (amended 2026). (ChemMon 2026)
- Individual substances must be expressed as specified in the legislation, e.g. sorbic acid-sorbates expressed as free acid. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Key Business Rules

| Rule | Description | Status |
| --- | --- | --- |
| CHEMMON39_a/b | Legislative class validation | Merged 2026 |
| CHEMMON84_a | Result type validation | Amended 2026 |
| CHEMMON86 | Physical-state facet recommendation | Amended 2026 |
| CHEMMON106 | Potassium sorbate `paramText` requirement | New 2026 |
| CHEMMON107 | Sorbic acid derivative LOD reporting | New 2026 |
| CHEMMON108 | Food colour/additive classification codes | New 2026 |
| CHEMMON109 | Implicit additive/flavouring legislative category | New 2026 |

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Legal Limit Rules (New 2026)

| Rule | Purpose |
| --- | --- |
| LL_01_FA_FF | Maximum Permitted Level comparison |
| LL_02_FA_FF | MPL threshold evaluation |
| LL_03_FA_FF | Legislative category substance authorization |

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Drinking Water

- Drinking water samples use the FoodEx2 code `A03DK`. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Worked Examples

| Product | FoodEx2 Code | Notes |
| --- | --- | --- |
| Cheese with legislative class | `A02RH#F03.A06JA$F33.A0C5F` | FA-01.7.2 Ripened cheese |
