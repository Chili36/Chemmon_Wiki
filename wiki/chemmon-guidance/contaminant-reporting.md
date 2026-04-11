---
title: "Contaminant Reporting"
type: "domain-guide"
domain: "contaminant"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[business-rules]]"
  - "[[food-additives-reporting]]"
  - "[[pesticide-reporting]]"
last_updated: "2026-04-11"
---

# Contaminant Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p51-58 -->
## Scope

- The contaminant domain is one of five [[chemmon-overview|ChemMon]] reporting domains. It covers chemical contaminants in food including acrylamide, mycotoxins, heavy metals, polycyclic aromatic hydrocarbons (PAHs), and mineral oils. (ChemMon 2026)
- Maximum levels for contaminants in foodstuffs are governed by Commission Regulation (EU) 2023/915. (ChemMon 2026)
- Matrix coding follows [[foodex2-in-chemmon]] rules. Validation is enforced by [[business-rules-contaminant]] and [[business-rules-cross-cutting]]. Some contaminants overlap with [[pesticide-reporting]] (e.g., copper) or [[food-additives-reporting]] (e.g., substances with dual classification).

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p42 -->
## Drinking Water (A03DK)

EFSA encourages competent authorities and data providers to collect and submit available results for **pesticides and contaminants in drinking water intended for human consumption**, using FoodEx2 base term `A03DK` ("Drinking water") and its children. (ChemMon 2026 p42)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p52-55 -->
## Acrylamide Requirements

- F33 legislative classes are MANDATORY for acrylamide samples, per Commission Regulation (EU) 2017/2158 and Recommendation (EU) 2019/1888. (ChemMon 2026)
- CHEMMON12 enforces this: "sampMatCode.legis is not reported or does not contain specific product code, though paramCode is acrylamide." (ChemMon 2026)
- F33 must be added even when the base term already carries an implicit F33 facet (EFSA clarification). (ChemMon 2026)
- The paramCode for acrylamide is `RF-00000410-ORG`. (ChemMon 2026)
- Specific food categories are required, including potato crisps, french fries, coffee, baby foods (see [[baby-food-reporting]]), and others defined in the legislation. (ChemMon 2026)

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

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p58-62 -->
## Dioxins and PCBs

- For dioxin/dioxin-like PCB reporting, all 29 congeners (17 PCDD/Fs and 12 dl-PCBs) must be reported per Commission Regulation (EU) 2023/915. (CHEMMON09)
- For non-dioxin-like PCBs, the six indicator congeners must be reported: PCB 28, PCB 52, PCB 101, PCB 138, PCB 153, and PCB 180. (CHEMMON10)
- Fat percentage should always be reported regardless of the expression basis. (CHEMMON21)
- For fish samples: area of origin for fisheries (`origFishAreaCode`) must be specified. (CHEMMON20)
- If the precise fishing area is unknown, at minimum "from freshwater" or "from saltwater" must be indicated. (ChemMon 2026)
- Fish species must be precisely reported, especially for Baltic region fish. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p62-63 -->
## Brominated Flame Retardants

- For fish with BFRs, `origFishAreaCode` must be specified. (CHEMMON20)
- Fat percentage should always be reported. (CHEMMON21)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p63-64 -->
## Arsenic

- For seaweed: the presence of alga Hijiki must be identified. (ChemMon 2026)
- For rice: specify the type of rice and distinguish raw vs processed using the F28 (Process) facet. (CHEMMON18)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p64-65 -->
## Chlorates and Perchlorates

- F28 (Process) is recommended to distinguish processed vs unprocessed food. (CHEMMON19)
- Treatments like deep-freezing and blanching have a significant effect on chlorate levels. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p65-66 -->
## Bisphenol Compounds

- F19 (packaging material) is mandatory. (CHEMMON14)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p66-67 -->
## PAHs

- F19 (packaging material) is recommended since packaging is a source of PAH contamination. (CHEMMON15)
- Recovery rate and measurement uncertainty are recommended. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p67-68 -->
## 3-MCPDs, 2-MCPDs and Glycidyl Esters

- The analytical method must clarify whether an ISO validated method was used (EN ISO 18363-1 through 18363-4). (ChemMon 2026)
- Fat percentage should be reported. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p68-69 -->
## Mineral Oils

- Moisture percentage should be reported. (CHEMMON11)
- Data providers should report molecular mass distribution information. (ChemMon 2026)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p69 -->
## Nitrates

- Recovery rate and measurement uncertainty are recommended. (ChemMon 2026)
