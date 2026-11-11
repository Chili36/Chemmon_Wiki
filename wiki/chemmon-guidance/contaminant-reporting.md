---
title: "Contaminant Reporting"
type: "domain-guide"
domain: "contaminant"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 85-96 (Section 4 and Table 8, all contaminant rows)"
  - "p42 (acrylamide explicit F33, drinking water)"
  - "pp. 44, 51-53 (Table 4 F04/F33 and acrylamide coding examples)"
  - "p69 (recovery correction prose)"
  - "pp. 114-117, 132, 135 (Table 10 rules cited here)"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[foodex2-facets-source-origin]]"
  - "[[foodex2-facets-state-process]]"
  - "[[foodex2-facets-packaging-consumer]]"
  - "[[foodex2-facets-legislative-descriptive]]"
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-elements-result]]"
  - "[[business-rules]]"
  - "[[food-additives-reporting]]"
  - "[[pesticide-reporting]]"
last_updated: "2026-11-11"
---

# Contaminant Reporting

<!-- Source: ChemMon 2026 p5 (scope), p85 (Section 4), pp. 86-96 (Table 8) -->
## Scope

- The contaminant domain is one of five [[chemmon-overview|ChemMon]] reporting domains (contaminants, food additives, food flavourings, pesticide residues, VMPR). (ChemMon 2026 p5)
- Maximum levels for contaminants in food are set by Commission Regulation (EU) 2023/915. (ChemMon 2026 p5)
- For some chemical results, more detailed information is necessary to describe the sample and the result. These specific requirements, mandatory or recommended, are listed in Table 8 and are updated annually. (ChemMon 2026 p85)
- The sections below transcribe every contaminant row of Table 8, one section per substance. The **Status** column gives the word printed in Table 8's "Status of data element" column; the **Requirement** column keeps the wording of its comment (for example "strongly recommended"). (ChemMon 2026 pp. 86-96)
- The Table 8 rows for food additives and food flavourings are on [[food-additives-reporting]].
- Matrix coding follows [[foodex2-in-chemmon]] rules. Rule text is on [[business-rules-contaminant]] and [[business-rules-cross-cutting]].

## Relevant Business Rules

Rules that Table 8 names for its rows (canonical text on [[business-rules-contaminant]]; ChemMon 2026 pp. 114-117, 135):

- **CHEMON09/10** (Warning): dioxins and dioxin-like PCBs, full set of 29 should be reported; non-dioxin-like PCBs, six indicator congeners should be reported.
- **CHEMON11** (Warning): `exprResPerc.moistPerc` should be reported for mineral oils and mycotoxins.
- **CHEMON12** (Error): acrylamide, legislative class facet F33 must be reported. See [[foodex2-facets-legislative-descriptive]].
- **CHEMON14** (Error): bisphenol compounds, packaging material facet F19 must be reported. See [[foodex2-facets-packaging-consumer]].
- **CHEMON15** (Warning): PAHs, packaging material facet F19 should be reported.
- **CHEMON17** (Warning): mycotoxins, production method facet F21 should be reported. See [[foodex2-facets-state-process]].
- **CHEMON18** (Warning): arsenic in rice grains, process facet F28 should be reported.
- **CHEMON19** (Warning): chlorates, perchlorate and QACs, process facet F28 should be reported.
- **CHEMON20** (Warning): fish matrices analysed for BFRs, dioxins and PCBs, or mercury, `origFishAreaCode` should be reported.
- **CHEMON21** (Warning): BFRs, dioxins and PCBs, 3-MCPDs, `exprResPerc.fatPerc` should be reported.
- **CHEMON90_a** (Warning) and **CHEMON90_b** (Error): copper, see the Copper section.

<!-- Source: ChemMon 2026 p69 (M.11/M.12 prose); pp. 92-95 (Table 8 M.11 rows); p132 (CHEMON80) -->
## Recovery rate: source discrepancy

**Source discrepancy:** the element prose says that for mycotoxins (Regulation (EU) 2023/2782), erucic acid (Regulation (EU) 2023/2783), nitrates (Regulation (EC) No 1882/2006) and lead, cadmium, mercury, inorganic tin, 3-MCPD and benzo(a)pyrene (Regulation (EC) No 333/2007) "the results must be adjusted for recovery and the recovery rate reported (unless specific conditions occur, e.g. for result significantly lower or higher than the maximum level)" (ChemMon 2026 p69). Table 8 gives the recovery rate (`resValRec`, M.11) the status "Recommended" for PAHs, mycotoxins, cadmium, lead and nitrates (ChemMon 2026 pp. 92-95). No business rule makes `resValRec` mandatory for these substances; for contaminants, CHEMON80 (Warning) asks only that `resValRecCorr` be reported (ChemMon 2026 p132). See [[ssd2-result-recovery-correction]].

<!-- Source: ChemMon 2026 p42 -->
## Drinking Water (A03DK)

EFSA encourages competent authorities and data providers to collect and submit available results for **pesticides and contaminants in drinking water intended for human consumption**, using FoodEx2 base term `A03DK` ("Drinking water") and its children. (ChemMon 2026 p42)

<!-- Source: ChemMon 2026 p86 (Table 8: brominated flame retardants) -->
## Brominated Flame Retardants

| Element | Status | Requirement |
| --- | --- | --- |
| `origFishAreaCode` and `origFishAreaText` (E.06, E.07) | Recommended | If data are reported on fish, it is recommended that the area of origin for fisheries is specified. When `origFishAreaCode` is not available (`M99` "Unknown"), as a minimum the fish's original environment should be given ("from freshwater" or "from saltwater") in `origFishAreaText`. Rule: CHEMON20. |
| `exprResPerc` percentage of fat (M.13) | Recommended | Strongly recommended that the percentage of fat in the original sample is always reported, regardless of whether the result is expressed in whole weight, fat weight or dry matter. Rule: CHEMON21. |

(ChemMon 2026 p86; see [[ssd2-analysis-context]])

<!-- Source: ChemMon 2026 p86 (Table 8: copper); p135 (CHEMON90_a, CHEMON90_b); p41 -->
## Copper

Table 8 lists copper (`paramCode` `RF-0102-001-PPP`) among the specific requirements, and the guidance describes coding of copper samples "under pesticides or contaminants" (ChemMon 2026 p41). The commodity-by-commodity F20/F28 codes are on [[pesticide-reporting]].

| Element | Status | Requirement |
| --- | --- | --- |
| `sampMatCode` (E.02): Part-consumed-analysed (F20) and/or Process (F28) | Highly Recommended | It is recommended that F20 and/or F28 are provided in the coded description of the matrix of the sample taken. EFSA informs that from next year onwards reporting F20 and/or F28 will become mandatory following CHEMON90_a. |
| `resValUncert` (M.17) | Mandatory | Information on the measurement uncertainty should be provided, as a range in the same units as `resVal`. Rule: CHEMON90_b. |

(ChemMon 2026 p86)

- CHEMON90_a is a Warning ("The use of facet F20 and/or F28 is needed") and becomes an Error in 2027. CHEMON90_b is an Error. Neither rule's condition names a domain: both apply when copper `RF-0102-001-PPP` is reported, whether under pesticides or contaminants. (ChemMon 2026 p135)
- **Source discrepancy:** Table 8 gives `resValUncert` for copper as "Mandatory" with no condition (ChemMon 2026 p86). CHEMON90_b says it "must be reported, if resType=VAL" (ChemMon 2026 p135). Validation enforces the rule, so the Error applies only when `resType` is `VAL`.

<!-- Source: ChemMon 2026 pp. 86-88 (Table 8: dioxins and dioxin-like PCBs, non-dioxin-like PCBs); p114, p117 (CHEMON09, 10, 20, 21) -->
## Dioxins and PCBs

Table 8 topic: "Dioxins and dioxin-like PCBs, non-dioxin-like PCBs".

| Element | Status | Requirement |
| --- | --- | --- |
| `origFishAreaCode` and `origFishAreaText` (E.06, E.07) | Recommended | If data are reported on fish, it is recommended that the area of origin for fisheries is specified. When `origFishAreaCode` is not available (`M99` "Unknown"), as a minimum the fish original environment should be given ("from freshwater" or "from saltwater") in `origFishAreaText`. Rule: CHEMON20. |
| `sampMatCode` (E.02) | Recommended | It is particularly important to classify samples of fish meat and fish products at the most detailed FoodEx2 level available. For fish, it is recommended that the analysed fish species be precisely reported, especially fish originating from the Baltic region. |
| `sampMatInfo` comment (E.10) | Recommended | If data are reported on fish, it is recommended that the length and/or weight of the fish samples be reported. Reference: Regulation (EC) 850/98 and Regulation (EC) 2187/2005. |
| `sampMatInfo` year, month and day of production (E.10) | Recommended | If data are reported on fish, it is recommended that when the fish have been caught be reported. |
| `paramCode` (K.02) | Recommended | The full set of the 29 dioxins and dioxin-like PCBs (17 PCDD/F, 12 dl-PCB) listed in the Appendix to Annex I of Regulation (EU) 2023/915 is strongly recommended to be reported. For non-dioxin-like PCBs, the six indicator congeners (PCB 28, PCB 52, PCB 101, PCB 138, PCB 153 and PCB 180) are strongly recommended to be reported. It is strongly recommended to report results at the congener level in the measured concentration. Rules: CHEMON09, CHEMON10. |
| `exprResPerc` percentage of fat (M.13) | Recommended | It is recommended to report the percentage of fat in the original sample for food samples with maximum or action levels expressed on a fat basis: products of terrestrial animal origin, marine oils and vegetable oils and fats (marine oils included). It is recommended to report food samples of fish and offal and foods of plant origin (except oils) on a whole weight basis. Feed should be reported on the basis of 88% dry matter. Rule: CHEMON21. References: Regulations (EU) 278/2012 and (EU) 644/2017. |
| `exprResPerc` percentage of fat (M.13) | Recommended | It is recommended that the percentage of fat is provided for the other samples, when the lipid content has been determined. Rule: CHEMON21. |
| Additional information on the result (M.20) | Recommended | If the sample was reconstituted before analysis, e.g. foods for infants and young children, it would be relevant to give the exact reconstitution protocol (ratio dry product: added fluid, with a description of the fluid). Examples: `10:90 (milk)`, `20:80 (water)`. |

(ChemMon 2026 pp. 86-88; see [[ssd2-analysis-context]] and [[ssd2-elements-result]])

- CHEMON09 and CHEMON10 are Warnings whose descriptions say the congeners "should be reported". **Source discrepancy:** their error messages say the set is "not reported, though mandatory" (ChemMon 2026 p114), while Table 8 gives the status "Recommended" (ChemMon 2026 p88). Validation returns a Warning, not an Error.
- CHEMON21 asks for `exprResPerc.fatPerc` for dioxins and PCBs regardless of whether the result is expressed on whole weight, fat weight or dry matter. (ChemMon 2026 p117)

<!-- Source: ChemMon 2026 p89 (Table 8: mineral oils); p96 (Table 8: mineral oil hydrocarbons) -->
## Mineral Oils

| Element | Status | Requirement |
| --- | --- | --- |
| `exprResPerc` percentage of moisture (M.13) | Recommended | It is recommended that the percentage of moisture in the original sample is always reported, regardless of whether the result is expressed in whole weight, fat weight or dry matter. Rule: CHEMON11. |
| Additional information on the result (M.20) | Recommended | Data providers are requested to report the molecular mass distribution expressed as the number of carbon atoms (referring to n-alkanes), including the range of carbon atoms and the maximum of the distribution curve. |
| Mineral oil hydrocarbons (no element or status printed) | (blank) | Additional SSD requirements for reporting mineral oil hydrocarbon analytical results are detailed in the JRC guidance (Bratinova S and Hoekstra E, 2019). |

(ChemMon 2026 p89, p96)

<!-- Source: ChemMon 2026 pp. 89-90 (Table 8: acrylamide); p42; p51 (Table 4 F33); p115 (CHEMON12) -->
## Acrylamide Requirements

| Element | Status | Requirement |
| --- | --- | --- |
| `sampMatCode` ingredients facet F04 (E.02) | Recommended | It is recommended that the list of ingredients is provided in the Ingredients facet for these food items: "Potato crisps", "Pre-cooked French fries, potato products for home cooking", "Breakfast cereals (excluding muesli and porridge)", "Substitute coffee (dry)" and "Baby foods, other than processed cereal-based foods". |
| `sampMatCode` legislative classes facet F33 (E.02) | Mandatory | It is mandatory to provide additional product classification in the Legislative classes facet. Data providers must consult the list of legislative classes applicable to acrylamide in FoodEx2 catalogue facet F33. Rule: CHEMON12. Reference: Commission Regulation (EU) 2017/2158. |
| `procCountry` (E.08) | Recommended | It is recommended that the country where the food was processed is provided (ISO 3166-1-alpha-2). |
| `sampMatText` (E.03) | Recommended | It is recommended to mention in the text description: potato crisps (category 2), whether batch fried or continuously fried; pre-cooked French fries/home products (category 3), whether purchased fresh/frozen and whether the starting material is fresh potato or potato dough; crispbread (category 6), whether the product is/is not fermented; roasted coffee (category 7), the degree of roasting (light, medium, dark). |
| `resValUncert` (M.17) | Recommended | If available, information on the measurement uncertainty should be provided, as a range in the same units as `resVal`. |
| Additional information on the result (M.20) | Recommended | For food category 3 samples (e.g. pre-cooked French fries) prepared "as consumed" before analysis, it is relevant to give the exact cooking conditions (time, temperature and handling). If the sample has been reconstituted before analysis (e.g. instant coffee powder, foods for infants and young children), it is relevant to give the exact reconstitution protocol (ratio dry product: added fluid, with a description of the fluid). Examples: `2:100 (water)`, `10:90 (milk)`, `20:80 (water)`. Reference: Commission Recommendation 2010/307/EC. |

(ChemMon 2026 pp. 89-90)

- For acrylamide reporting under contaminants, explicit facet F33 Legislative classes must be reported. (ChemMon 2026 p42)
- Table 4 describes F33 as required for samples analysed for acrylamide, to describe the acrylamide legislative classes in Commission Recommendation (EU) 2019/1888 and Commission Regulation (EU) 2017/2158. (ChemMon 2026 p51)
- CHEMON12 (Error) fires when "sampMatCode.legis is not reported or does not contain a specific product code, though paramCode is acrylamide". The acrylamide `paramCode` is `RF-00000410-ORG`. (ChemMon 2026 p115)
- F04 for rice-based and algae-based products is an arsenic row, not an acrylamide row: see Arsenic. Table 4 lists the F04 products for contaminants in one cell, including "compound products for infants and small children, including ready-made meals, diet supplements, herb mixes and spice mixes", without naming a substance for that last item. (ChemMon 2026 p44)

<!-- Source: ChemMon 2026 pp. 52-53 (examples following Table 4) -->
### Acrylamide Worked Examples

Printed examples of the extent-of-cooking facet F17 and the process facet F28 for acrylamide food categories (ChemMon 2026 pp. 52-53):

| Product | `sampMatCode` | Meaning of the codes |
| --- | --- | --- |
| Potato crisp (category 2) | `A011L#F17.A07MY` | `A011L` = Potato crisps or sticks; `F17.A07MY` = Outside light brown |
| Crispbread (category 6), indicating whether the product is baked | `A0CHT#F28.A07GX` | `A0CHT` = Crispbread; `F28.A07GX` = Baking |
| Roasted coffee (category 7), light brown | `A03GL#F17.A07MY` | `A03GL` = Coffee beans, roasted; `F17.A07MY` = Outside light brown |
| Roasted coffee (category 7), brown | `A03GL#F17.A07MZ` | `F17.A07MZ` = Outside brown |
| Roasted coffee (category 7), outside dark brown/slightly burned | `A03GL#F17.A07NA` | `F17.A07NA` = Outside dark brown/slightly burned |

For roasted coffee the F17 facet "indicates the extent of cooking (light brown, brown, outside dark brown/slightly burned)". The food categories and sub-categories are based on Commission Recommendation 2010/307/EU and Commission Recommendation 2013/647/EU (Annex, point C). (ChemMon 2026 p53)

Wiki note (not in the guidance): `A07MY` is one of three F17 values, not a default; choose the one that matches the product. These printed examples show no F33 facet. An acrylamide record still needs the F33 legislative class (CHEMON12).

<!-- Source: ChemMon 2026 pp. 90-91 (Table 8: furan) -->
## Furan and Alkylfurans (Furan, 2-methylfuran, 3-methylfuran)

| Element | Status | Requirement |
| --- | --- | --- |
| `anMatCode` (G.01) | Recommended | If the sample has been analysed "as consumed", it should be described in the analysed sample as consumed. Reference: Commission Recommendation 2007/196/EC. |
| Additional information on the result (M.20) | Recommended | If the product is analysed as consumed, it is relevant to give the exact cooking preparation with time, temperature and handling information, using the `$` character to separate extra information. Example: `Heated in microwave$60°C$1.5min`. |
| `sampMethod` (B.05) | Recommended | For monitoring furan, 2-methylfuran and 3-methylfuran in food, and to ensure the samples are representative, it is advised to follow the sampling procedures in part B of the Annex to Commission Regulation (EC) No 333/2007: `<sampMethod>N011A</sampMethod>`. Reference: Commission Recommendation (EU) 2022/495. See [[ssd2-sampling-method-and-point]]. |

(ChemMon 2026 pp. 90-91)

<!-- Source: ChemMon 2026 pp. 91-92 (Table 8: polycyclic aromatic hydrocarbons) -->
## PAHs

| Element | Status | Requirement |
| --- | --- | --- |
| `sampMatCode` packaging material facet F19 (E.02) | Recommended | It is recommended to describe the container or wrapper that holds the product as marketed, since the packaging is a source of PAH contamination in food. According to legislation, the sample container must be of inert material to eliminate migration contamination during sampling and analysis. Rule: CHEMON15. Reference: Commission Regulation (EC) 333/2007. |
| `resValRec` (M.11) | Recommended | Recommended to provide the recovery value associated with the concentration measurement (as a percentage) when an extraction step is applied in the analytical method. See the recovery source discrepancy above. |
| `resValUncert` (M.17) | Recommended | Recommended to provide the expanded uncertainty (95% confidence interval) associated with the concentration measurement, in units of the result. |

(ChemMon 2026 pp. 91-92)

<!-- Source: ChemMon 2026 p92 (Table 8: 3-MCPDs, 2-MCPDs and glycidyl esters) -->
## 3-MCPDs, 2-MCPDs and Glycidyl Esters

| Element | Status | Requirement |
| --- | --- | --- |
| `anMethCode` (L.04) | Mandatory | For the analysis of 3- and 2-MCPD esters and glycidyl esters it should be clarified whether the samples have been analysed with one of the four methods validated by ISO (EN ISO 18363-1:2021, 18363-2:2018, 18363-3:2024, 18363-4:2021). For the four methods, the appropriate code from the `ANLYMD` catalogue must be reported; otherwise, a reference to the different methods must be provided. The same applies for 3- and 2-MCPD total referring to the ester part of the sum. |
| `exprResPerc` percentage of fat (M.13) | Recommended | It is recommended that the percentage of fat in the original sample is always reported, regardless of whether the result is expressed in whole weight, fat weight or dry matter. Rule: CHEMON21. |

(ChemMon 2026 p92)

<!-- Source: ChemMon 2026 pp. 92-93 (Table 8: mycotoxins) -->
## Mycotoxins

| Element | Status | Requirement |
| --- | --- | --- |
| `sampMatCode` (E.02) | Mandatory | It is important to classify the food/feed samples of grains at the most detailed FoodEx2 level available. This is particularly needed for "Grains and grain-based products" and "Food for infants and small children". |
| `sampMatCode` production method facet F21 (E.02) | Recommended | It is recommended to report whether the sample was obtained from the produce of traditional (non-organic) or organic farming. Rule: CHEMON17. |
| `resValRec` (M.11) | Recommended | It is recommended that the recovery value associated with the concentration measurement is provided (as a percentage). Reference: Regulation (EU) 2023/2782. See the recovery source discrepancy above. |
| `exprResPerc` percentage of moisture (M.13) | Recommended | It is recommended that the percentage of moisture in the original sample of feed is reported, and for processed cereal-based foods for infants and young children. Rule: CHEMON11. |
| `resValUncert` (M.17) | Recommended | It is recommended that the expanded uncertainty (95% confidence interval) associated with the concentration measurement be provided. Reference: Regulation (EU) 2023/2782. |
| Additional information on the result (M.20) | Recommended | If the sample was reconstituted before analysis, e.g. infant formula and follow-on formula, it would be relevant to give the exact reconstitution protocol (ratio dry product: added fluid, with a description of the fluid). Example: `14:86 (water)`. |

(ChemMon 2026 pp. 92-93)

<!-- Source: ChemMon 2026 pp. 93-94 (Table 8: arsenic and derivatives) -->
## Arsenic

| Element | Status | Requirement |
| --- | --- | --- |
| `sampMatCode` (E.02) | Recommended | For seaweed, it is strongly recommended that information is provided to identify the presence of the alga Hijiki. For rice, it is strongly recommended that information is provided about the type of rice. |
| `sampMatCode` process facet F28 (E.02) | Recommended | For rice as grains for human consumption: to distinguish raw rice from rice that has undergone any kind of treatment, it is recommended to provide at least the codes for "unprocessed" or "processed" in F28. Additionally, it is recommended to indicate clearly if the original sample is a dehydrated product. Rule: CHEMON18. |
| `sampMatCode` ingredients facet F04 (E.02) | Recommended | Rice-based products: if a product contains rice (e.g. a cereal-based ready-to-eat meal for children; rice cake) it should be specified in this facet. It is also recommended that the type of algae included in alga-based foods for special nutritional use is described. |

(ChemMon 2026 pp. 93-94; see [[foodex2-facets-state-process]])

<!-- Source: ChemMon 2026 pp. 94-95 (Table 8: cadmium, lead, mercury and their derivatives) -->
## Metals (Cadmium, Lead, Mercury)

| Substance | Element | Status | Requirement |
| --- | --- | --- | --- |
| Cadmium and derivatives | `resValRec` (M.11) | Recommended | It is recommended that the recovery value associated with the concentration measurement is provided (as a percentage) when an extraction step is applied in the analytical method. |
| Cadmium and derivatives | `resValUncert` (M.17) | Recommended | It is recommended that the expanded uncertainty (95% confidence interval) associated with the concentration measurement is provided. |
| Lead and derivatives | `resValRec` (M.11) | Recommended | It is recommended that the recovery value associated with the concentration measurement (as a percentage) is provided when an extraction step is applied in the analytical method. |
| Lead and derivatives | `resValUncert` (M.17) | Recommended | It is recommended that the expanded uncertainty (95% confidence interval) associated with the concentration measurement is provided. |
| Mercury and derivatives | `sampMatCode` (E.02) | Recommended | It is particularly important to classify samples of fish meat, seafood and fish/seafood products at the most detailed FoodEx2 level available. |
| Mercury and derivatives | `origFishAreaCode` and `origFishAreaText` (E.06, E.07) | Recommended | If data are reported on fish, it is recommended that the area of origin for fisheries is specified. If `origFishAreaCode` is not available (`M99` "Unknown"), at least the fish original environment should be given ("from fresh water" or "from salt water") in `origFishAreaText`. Rule: CHEMON20. |

(ChemMon 2026 pp. 94-95; reference for the cadmium and lead rows: Commission Regulation (EC) No 333/2007. For recovery, see the source discrepancy above.)

<!-- Source: ChemMon 2026 p95 (Table 8: nitrates in vegetables and other food commodities) -->
## Nitrates

Table 8 topic: "Nitrates in vegetables and other food commodities".

| Element | Status | Requirement |
| --- | --- | --- |
| `resValRec` (M.11) | Recommended | It is recommended that the recovery value associated with the concentration measurement is provided (as a percentage). See the recovery source discrepancy above. |
| `resValUncert` (M.17) | Recommended | It is recommended that the expanded uncertainty (95% confidence interval) associated with the concentration measurement is provided, in units of the result. |

(ChemMon 2026 p95; reference: Commission Regulation (EC) No 1882/2006)

<!-- Source: ChemMon 2026 p95 (Table 8: chlorates and perchlorates); p116 (CHEMON19) -->
## Chlorates and Perchlorates

| Element | Status | Requirement |
| --- | --- | --- |
| `sampMatCode` process facet F28 (E.02) | Recommended | Some product treatments, like deep-freezing, blanching or treatments at elevated temperatures, have a significant effect on the chlorate level in food. It is therefore recommended to report F28 and select at least the code for "processed" or "unprocessed"; if possible, specify the most appropriate process code. Rule: CHEMON19. References: Commission Recommendation (EU) 2015/682 and Regulation (EU) 2020/749. |

(ChemMon 2026 p95; see [[foodex2-facets-state-process]])

<!-- Source: ChemMon 2026 p96 (Table 8: bisphenol); p115 (CHEMON14) -->
## Bisphenol Compounds

| Element | Status | Requirement |
| --- | --- | --- |
| `sampMatCode` packaging material facet F19 (E.02) | Mandatory | It is mandatory to provide additional product classification based on the Commission Regulation on bisphenol, (EU) 2018/213. The list of codes to be used is provided in the F19 packaging material facet of the MTX catalogue. Rule: CHEMON14. |

(ChemMon 2026 p96; see [[foodex2-facets-packaging-consumer]])
