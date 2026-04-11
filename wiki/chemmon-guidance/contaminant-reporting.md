---
title: "Contaminant Reporting"
type: "domain-guide"
domain: "contaminant"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-elements-result]]"
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

## Relevant Business Rules

Key contaminant-domain rules you'll hit frequently:

- **CHEMMON09/10**: dioxins/PCBs congener reporting expectations.
- **CHEMMON11**: moisture percentage (`moistPerc`) recommendation for mineral oils/mycotoxins.
- **CHEMMON12**: acrylamide requires legislative class facet F33.
- **CHEMMON14**: bisphenols require packaging material facet F19.
- **CHEMMON15**: PAHs packaging material facet F19 recommended.
- **CHEMMON17**: mycotoxins production-method facet F21 (organic vs conventional) recommended.
- **CHEMMON18**: arsenic in rice process facet F28 recommended to distinguish processed vs unprocessed.
- **CHEMMON19**: chlorates/perchlorates process facet F28 recommended.
- **CHEMMON20**: fish `origFishAreaCode`/text recommended (with freshwater/saltwater minimum when unknown).
- **CHEMMON21**: fat percentage (`fatPerc`) recommended for BFRs/dioxins/3-MCPD contexts.

See [[business-rules-contaminant]] for canonical rule text.

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

<!-- Source: ChemMon 2026 pp. 95-96 (Table 8: acrylamide) -->
### Ingredients facet (F04) for composite products (recommended)

For acrylamide, EFSA recommends providing an **ingredients list** in the FoodEx2 **ingredients facet (F04)** for composite items where ingredient detail materially affects classification. The table calls out, among others:

- potato crisps
- pre-cooked french fries / potato products for home cooking
- breakfast cereals (excluding muesli and porridge)
- substitute coffee (dry)
- baby foods (other than processed cereal-based foods)
- rice-based products
- algae-based foods for special nutritional uses
- compound products for infants and small children (including ready-made meals, diet supplements, herb mixes, spice mixes)

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

<!-- Source: ChemMon 2026 pp. 92-93 (Table 8: mycotoxins) -->
### Table 8 metadata recommendations (high signal)

- **Matrix detail (mandatory for grains)**: classify grain/grain-based matrices at the most detailed FoodEx2 level available, especially under "Grains and grain-based products" and "Food for infants and small children". (ChemMon 2026 Table 8)
- **Organic vs conventional (recommended)**: report production method facet **F21** when known. (CHEMMON17)
- **Recovery and uncertainty (recommended)**: report recovery rate (`resValRec`) and expanded uncertainty (`resValUncert`, typically 95% CI) when available. (ChemMon 2026 Table 8; see [[ssd2-elements-result]])
- **Moisture percentage (recommended)**: report `moistPerc` for feed samples and for processed cereal-based foods for infants/young children. (CHEMMON11; see [[ssd2-elements-result]])
- **Reconstitution protocol (recommended when applicable)**: if the sample was reconstituted before analysis (e.g. infant formula), provide the dry:fluid ratio and describe the fluid used. (ChemMon 2026 Table 8)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p58-62 -->
## Dioxins and PCBs

- For dioxin/dioxin-like PCB reporting, all 29 congeners (17 PCDD/Fs and 12 dl-PCBs) must be reported per Commission Regulation (EU) 2023/915. (CHEMMON09)
- For non-dioxin-like PCBs, the six indicator congeners must be reported: PCB 28, PCB 52, PCB 101, PCB 138, PCB 153, and PCB 180. (CHEMMON10)
- Fat percentage should always be reported regardless of the expression basis. (CHEMMON21)
- For fish samples: area of origin for fisheries (`origFishAreaCode`) must be specified. (CHEMMON20)
- If the precise fishing area is unknown, at minimum "from freshwater" or "from saltwater" must be indicated. (ChemMon 2026)
- Fish species must be precisely reported, especially for Baltic region fish. (ChemMon 2026)

<!-- Source: ChemMon 2026 pp. 87-88 (Table 8: dioxins/PCBs) -->
### Table 8 add-ons (rule-shaped)

- Report results at **congener level** (not only totals) when possible, using the parameter coding approach intended for the congener set. (ChemMon 2026 Table 8)
- If a limit/action level is expressed on a **fat basis**, report `fatPerc` for the original sample; otherwise, prefer whole-weight reporting where appropriate (e.g. fish/offal and foods of plant origin except oils). (ChemMon 2026 Table 8)
- For feed, EFSA notes reporting on an **88% dry matter** basis. (ChemMon 2026 Table 8; see [[ssd2-elements-result]])
- If the sample was **reconstituted** before analysis, provide the reconstitution protocol in the additional result info field (SSD2 M.20). (ChemMon 2026 Table 8)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p62-63 -->
## Brominated Flame Retardants

- For fish with BFRs, `origFishAreaCode` must be specified. (CHEMMON20)
- Fat percentage should always be reported. (CHEMMON21)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p63-64 -->
## Arsenic

- For seaweed: the presence of alga Hijiki must be identified. (ChemMon 2026)
- For rice: specify the type of rice and distinguish raw vs processed using the F28 (Process) facet. (CHEMMON18)

<!-- Source: ChemMon 2026 pp. 92-93 (Table 8: arsenic) -->
### Table 8 add-ons

- For rice grains: in facet **F28 (process)**, report at least **processed vs unprocessed**; also indicate clearly if the original sample is **dehydrated**. (CHEMMON18; ChemMon 2026 Table 8)
- For rice-based composite products: include rice in the **ingredients facet (F04)** when relevant. (ChemMon 2026 Table 8)
- For algae-based foods for special nutritional uses: describe the **type of algae** in the ingredients facet (F04). (ChemMon 2026 Table 8)

<!-- Source: ChemMon 2026 p92 (Table 8: furan) -->
## Furan and Alkylfurans (Furan, 2-methylfuran, 3-methylfuran)

- If analysed **as consumed**, provide cooking/preparation details (time, temperature, handling) in the additional result info field (SSD2 M.20). (ChemMon 2026 Table 8)
- For furan monitoring, follow the sampling procedures referenced by the guidance and report `sampMethod=N011A` where applicable. See [[ssd2-elements-sampling#sampmethod-sampling-method]]. (ChemMon 2026 Table 8)

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

<!-- Source: ChemMon 2026 p91-92 (Table 8: 3-MCPD/2-MCPD/glycidyl) -->
### Table 8 add-on

- Clarify analytical method coding: report an appropriate analytical-method code where available; otherwise provide a reference to the method(s) used (the guidance references the EN ISO 18363 series). (ChemMon 2026 Table 8)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p68-69 -->
## Mineral Oils

- Moisture percentage should be reported. (CHEMMON11)
- Data providers should report molecular mass distribution information. (ChemMon 2026)

<!-- Source: ChemMon 2026 pp. 89, 95-96 (Table 8: mineral oils / mineral oil hydrocarbons) -->
### Table 8 add-ons

- Report the molecular-mass distribution as a **carbon-number range** (n-alkanes) and the **maximum** of the distribution curve in additional result info (SSD2 M.20). (ChemMon 2026 Table 8)
- The guidance points to the JRC guidance (Bratinova & Hoekstra, 2019) for additional SSD requirements specific to mineral oil hydrocarbons reporting. (ChemMon 2026 Table 8)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p69 -->
## Nitrates

- Recovery rate and measurement uncertainty are recommended. (ChemMon 2026)

<!-- Source: ChemMon 2026 p94-95 (Table 8: nitrates) -->
### Table 8 add-ons

- Report recovery rate (`resValRec`) and expanded uncertainty (`resValUncert`, 95% CI) when available. (ChemMon 2026 Table 8)

<!-- Source: ChemMon 2026 pp. 93-94 (Table 8: cadmium/lead/mercury) -->
## Metals (Cadmium, Lead, Mercury) (Table 8 notes)

- For cadmium and lead: report recovery rate and expanded uncertainty when available (especially when an extraction step is applied in the method). (ChemMon 2026 Table 8)
- For mercury: classify fish/seafood matrices at the most detailed FoodEx2 level available. (ChemMon 2026 Table 8)
