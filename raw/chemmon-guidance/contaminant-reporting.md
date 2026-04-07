---
title: "Contaminant Reporting"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[business-rules]]"
  - "[[food-additives-reporting]]"
  - "[[pesticide-reporting]]"
last_updated: "2026-04-07"
---

# Contaminant Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p51-58 -->
## Scope

- The contaminant domain covers chemical contaminants in food including acrylamide, mycotoxins, heavy metals, polycyclic aromatic hydrocarbons (PAHs), and mineral oils. (ChemMon 2026)
- Maximum levels for contaminants in foodstuffs are governed by Commission Regulation (EU) 2023/915. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p52-55 -->
## Acrylamide Requirements

- F33 legislative classes are MANDATORY for acrylamide samples, per Commission Regulation (EU) 2017/2158 and Recommendation (EU) 2019/1888. (ChemMon 2026)
- CHEMMON12 enforces this: "sampMatCode.legis is not reported or does not contain specific product code, though paramCode is acrylamide." (ChemMon 2026)
- F33 must be added even when the base term already carries an implicit F33 facet (EFSA clarification). (ChemMon 2026)
- The paramCode for acrylamide is `RF-00000410-ORG`. (ChemMon 2026)
- Specific food categories are required, including potato crisps, french fries, coffee, baby foods, and others defined in the legislation. (ChemMon 2026)

### Acrylamide Worked Examples

| Product | FoodEx2 Code | Notes |
| --- | --- | --- |
| Potato crisps | `A011L#F17.A07MY` | Standard product coding |
| Roasted coffee | `A03GL#F17.A07MY` | Standard product coding |
| French fries with F33 | `A0BYV#F33.A169H` | Legislative class AC-1.1 |

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p55-58 -->
## Mycotoxins

- Mycotoxin reporting follows Commission Regulation (EU) 2023/2782. (ChemMon 2026)
- Recovery rate corrections are mandatory for certain mycotoxin substances as specified in the regulation. (ChemMon 2026)
