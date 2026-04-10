---
title: "Food Additives and Flavourings Reporting"
type: "domain-guide"
domain: "additives"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[business-rules]]"
  - "[[contaminant-reporting]]"
  - "[[baby-food-reporting]]"
last_updated: "2026-04-10"
---

# Food Additives and Flavourings Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Scope

- Food additives and flavourings form two of the five [[chemmon-overview|ChemMon]] reporting domains. (ChemMon 2026)
- Food additives are regulated under Regulation (EC) No 1333/2008. (ChemMon 2026)
- Food flavourings are regulated under Regulation (EC) No 1334/2008. (ChemMon 2026)
- Matrix coding follows [[foodex2-in-chemmon]] rules. Validation is enforced by [[business-rules-additives]] and [[business-rules-cross-cutting]]. Some substances overlap with [[contaminant-reporting]] (e.g., naturally occurring substances with dual classification).

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Mandatory Facets

- **F33 (Legislative classes)**: MANDATORY for both food additive and flavouring samples. (ChemMon 2026)
- **F03 (Physical state)**: recommended for dairy products, cereals, soups, sauces, infant foods, juices, and food supplements. (ChemMon 2026)
- **F23 (Target consumer)**: required for infant formulas and follow-on formulas. See [[baby-food-reporting]] for baby food classification and domain routing. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Expression Type

- The `exprResType` element is mandatory for food additives and flavourings (amended 2026). (ChemMon 2026)
- Individual substances must be expressed as specified in the legislation, e.g. sorbic acid-sorbates expressed as free acid. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Result Reporting

- For food additives regulated as groups, `paramText` must state "Expressed as free acid" or "Expressed as salt". (CHEMMON106, e.g. for potassium sorbate)
- If `resType=BIN` and `resQualValue=NEG`, it is highly recommended to report the LOD -- otherwise the data cannot be used for dietary exposure estimation. (CHEMMON107)
- Sum should be reported if it complements individual substance results and MPLs are regulated at the sum level. (ChemMon 2026)

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
| Wine, red | `A03MX` | Implicit F33=FA-14.2.2 Wine and products |
| Omelette, plain | `A03YN#F33.A0C33` | Implicit F33=FA-10.2 Processed eggs |
| Infant formula milk/soya-based liquid | `A03QH` | Implicit F33=FA-13.1.1 Infant formulae |
| Vitamin supplements syrup | `A03SL#F03.A1BY$F33.A0C15` | FA-17.2 supplements liquid form |

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Restriction/Exception

- `evalInfo.restrictionException` provides restrictions and exceptions per Regulation 1333/2008. (ChemMon 2026)
- Codes are drawn from the ADDFOOD catalogue; the most detailed code should be chosen. (ChemMon 2026)
- The same substance can be authorised at different MPLs depending on the restriction/exception. (ChemMon 2026)
- Examples: `ADD00197A` (mozzarella for lactic acid), `ADD00386A` (milk chocolate for citric acid). (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Conclusion Reporting

- `evalInfo.conclusion` is highly recommended. (CHEMMON87)
- Indicates whether the food additive was on the label (`C19A`) or not (`C20A`), or is of natural occurrence (`C05A`). (ChemMon 2026)
- Multiple conclusions may apply; for example, ascorbic acid added as a food additive and also naturally occurring: `C19A$C05A`. (ChemMon 2026)
