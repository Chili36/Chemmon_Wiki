---
title: "FoodEx2 Facet Reference (F01-F33)"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 43-51 (Table 4: FoodEx2 main facet descriptions and their relevance for each data domain)"
related:
  - "[[foodex2-in-chemmon]]"
  - "[[ssd2-elements-matrix]]"
  - "[[vmpr-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
  - "[[business-rules-cross-cutting]]"
---

# FoodEx2 Facet Reference (F01-F33)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 43-51, Table 4 -->

## Overview

FoodEx2 sample matrix codes are built from a **base term** (from the MTX catalogue) plus optional **facets** that add descriptive attributes. Each facet has a code in the form `F<number>` (F01 through F33). The relevance and requirement for each facet **depends on the reporting domain** — a facet may be mandatory for contaminants but ignored for pesticides, or vice versa.

This page summarises Table 4 from the source guidance: which facets matter in which domains, and what each facet is used for. For base term coding and general FoodEx2 rules see [[foodex2-in-chemmon]]; for sampMatCode element-level guidance see [[ssd2-elements-matrix]].

## Facet reference matrix

### F01 source

| Domain | Usage |
| --- | --- |
| **VMPR** | Indicates the type of animal species sampled (e.g. pig samples). Can include the purpose of rearing — e.g. whether the chickens are laying hens or broilers. **Classification of samples as bovines, pigs, sheep, goats, horses, poultry, aquaculture, rabbit or game is based on this facet.** It is important to select a facet at species level or lower. |
| **Pesticides** | — |
| **Contaminants** | Defines the 'origin' of the raw commodity; usually already assigned as an 'implicit facet'. |
| **Additives** | Plant, animal, organism or source of the raw agricultural commodity. For fish and seafood samples the species must be specified. For algae-based products the species of algae must be specified. |
| **Flavourings** | Same as additives. |

(ChemMon 2026 p43)

### F02 part-nature

| Domain | Usage |
| --- | --- |
| **VMPR** | Indicates the 'part' or 'tissue' of the animal tested (e.g. the liver). **Must be reported since the MRL legal limit applied is dependent on the target tissue.** The first step in the EFSA procedure for the VMPR matrix classification for samples such as eggs, milk or honey is based on this facet. |
| **Pesticides** | Part sampled — e.g. indicating fat samples from animals. |
| **Contaminants** | Part sampled. |
| **Additives** | Part sampled. |
| **Flavourings** | Part sampled. |

(ChemMon 2026 pp. 43-44)

### F03 physical state

| Domain | Usage |
| --- | --- |
| **VMPR** | — |
| **Pesticides** | — |
| **Contaminants** | For reporting the physical state (e.g. solid, jelly, liquid) of the tested food. |
| **Additives** | For reporting the physical state of the tested food. |
| **Flavourings** | For reporting the physical state of the tested food. |

(ChemMon 2026 p44)

### F04 ingredient

| Domain | Usage |
| --- | --- |
| **VMPR** | — |
| **Pesticides** | For reporting the ingredients of composite food samples. |
| **Contaminants** | For reporting the following products: 'Potato crisps', 'Pre-cooked French fries, potato products for home cooking', 'Breakfast cereals (excluding muesli and porridge)', 'Substitute coffee (dry)', 'Baby foods, other than processed cereal-based foods', rice-based products, algae-based foods for special nutritional uses, compound products for infants and small children (including ready-made meals, diet supplements, herb mixes and spice mixes). |
| **Additives** | Repeatable facet to be used to characterise composite foods. |
| **Flavourings** | Repeatable facet to be used to characterise composite foods. |

(ChemMon 2026 p44)

### F06 surrounding medium

| Domain | Usage |
| --- | --- |
| **Contaminants** | For reporting the surrounding medium (e.g. oil, fat) of the food. |
| other domains | — |

(ChemMon 2026 p44)

### F07 fat content

| Domain | Usage |
| --- | --- |
| **Contaminants** | For reporting the fat content of the food. To be reported when the expression of results is fat weight (`exprResType = B003A`). |
| other domains | — |

(ChemMon 2026 p45)

### F10 qualitative-info

| Domain | Usage |
| --- | --- |
| **Pesticides** | Where whole grain cereal (wheat, barley, oat, rye) is reported under the EUCP, flour integral/not refined (`A06HR`) can be reported along with the cereal-based term. |
| **Contaminants** | This facet is recommended for some substances (PARAM codes) belonging to the group of plasticising agents (e.g. phthalates) for expressing when a product is not packed; see also Table 8 for specific requirements. |
| other domains | — |

(ChemMon 2026 p45)

### F11 alcohol content

| Domain | Usage |
| --- | --- |
| **Contaminants** | For reporting the alcohol content of the food. |
| other domains | — |

(ChemMon 2026 p45)

### F17 extent-of-cooking

| Domain | Usage |
| --- | --- |
| **Contaminants** | Heat treatment applied to food required for furans and acrylamide. |
| other domains | — |

(ChemMon 2026 p45)

### F18 packaging format

| Domain | Usage |
| --- | --- |
| **Contaminants** | Allows sampling officers to describe the shape of the container or wrapper that holds the marketed product. This facet is recommended for some substances (PARAM codes) belonging to the group of plasticising agents (e.g. phthalates); see also Table 8 for specific requirements. |
| other domains | — |

(ChemMon 2026 p45)

### F19 packaging material

| Domain | Usage |
| --- | --- |
| **Contaminants** | Allows sampling officers to describe the material of the container or wrapper that holds the marketed product. This facet is **crucial for some substances** (PARAM codes), e.g. bisphenol, group of plasticising agents (e.g. phthalates); see also Table 8 for specific requirements. |
| other domains | — |

(ChemMon 2026 pp. 45-46)

### F20 part-consumed-analysed

| Domain | Usage |
| --- | --- |
| **Pesticides** | Where meat (as part nature) or its sub-codes are reported, then part-consumed-analysed is recommended to be used, to indicate the presence of fat: `A0F4V` = 'Excluding visible fat' or `A0F4T` = 'Including visible fat'. According to Regulation (EC) No 396/2005 the MRLs for 'Muscle' apply to "Meat after removal of trimmable fat". Therefore, to report muscle samples the code `A0F4V` — 'Excluding visible fat' should be used. |
| | When reporting **copper** (`paramCode` RF-0102-001-PPP), EFSA expects facet **F20 (part-consumed-analysed)** and/or **F28 (process)** to reflect **sample preparation** (CHEMMON90_a). Some commodities use different facet values depending on whether the result is treated as pesticide-residue-style vs contaminant-style (e.g. banana with peel `...#F20.A07QE` vs without peel `...#F20.A07QF`). See [[pesticide-reporting]]. |
| other domains | — |

(ChemMon 2026 pp. 46-47)

### F21 production method

| Domain | Usage |
| --- | --- |
| **VMPR** | `A07RY` should be used to identify wild game. **Classification of samples as wild game is based on this facet.** |
| **Pesticides** | Required to perform the data analysis regarding the residue situation for organic food compared with conventionally produced food. Organic production methods can be reported here using the term `A07SE`. If the production method is known to be non-organic, the term `A0C6Y` (conventional non-organic production) should be reported. This term has always been mapped to the former SSD1 value 'non-organic' and has been renamed for better clarity. Where the production method is unknown, this facet must not be reported. For the purposes of reporting, 'non-organic' and no facet F21 value reported will be grouped as 'non-organic' production, since legislation only requires that organic production must be clearly declared. Intensity of production, when known, can also be reported in this facet using `A0C6Q` (intensive production) or `A18FG` (extensive (non-intensive)) production. `A07RY` (wild or gathered or hunted) should be used to identify wild game (e.g. to distinguish wild boar (farmed) from wild). |
| **Contaminants** | Recommended. Required to perform the data analysis regarding the mycotoxin situation in organic food compared with non-organic food. |
| other domains | — |

(ChemMon 2026 pp. 47-48)

### F23 target consumer

| Domain | Usage |
| --- | --- |
| **VMPR** | This facet **must be used for feed samples** to indicate the species for whom the feed is intended if not already implicitly included in the base term selected. |
| **Pesticides** | This facet must be used for feed samples to indicate the species for whom the feed is intended if not already implicitly included in the base term selected. |
| **Contaminants** | This facet must be used for feed samples to indicate the species for whom the feed is intended if not already implicitly included in the base term selected. Also, it can be used to indicate the age of the human consumer/population (e.g. infants, toddlers, children, and adults). |
| **Additives** | Same as contaminants. |
| **Flavourings** | Same as contaminants. |

(ChemMon 2026 p48)

### F27 source-commodities

| Domain | Usage |
| --- | --- |
| **Pesticides** | Report the representative lead crop. It defines the origin of the derivatives for 'processed' food samples made up of one single food/ingredient (e.g. orange juice or wine). This facet describes the raw primary commodity (RPC) from which an ingredient or derivative has been obtained. However, in some food groups, like cheese or fruit juice, products of the same nature as those from one raw source, but from mixed raw sources, are encountered. |
| **Contaminants** | This facet describes the raw primary commodity (RPC) from which an ingredient or derivative has been obtained. However, in some food groups, like cheese or fruit juice, products of the same nature as those from one raw source, but from mixed raw sources, are encountered. |
| other domains | — |

(ChemMon 2026 p49)

### F28 process

| Domain | Usage |
| --- | --- |
| **VMPR** | Required to distinguish processed food samples. |
| **Pesticides** | Required to distinguish processed food samples. This distinction is important for the pesticide residue data as MRL compliance is checked/verified considering the results expressed for 'unprocessed' food samples. For processed products derived from raw agricultural products (as specified in Annex I of Regulation (EC) No 396/2005), the most specific code for processing must be selected. When reporting copper results, the processing applied to the analysed sample needs to be reported (e.g. `F28.A07GY` 'roasting'). |
| **Contaminants** | Required to distinguish processed food samples. However, a more detailed classification should be used where possible. |
| **Additives** | Required to distinguish processed food samples. |
| **Flavourings** | Required to distinguish processed food samples. |

(ChemMon 2026 pp. 49-50)

### F31 animal-age-class

| Domain | Usage |
| --- | --- |
| **VMPR** | Although not mandatory, this information is very useful for the interpretation of the results, especially in cases of non-compliance due to residues belonging to the substance groups of anti-thyroid agents (A1b) and steroids (A1c). |
| other domains | — |

(ChemMon 2026 p50)

### F32 gender

| Domain | Usage |
| --- | --- |
| **VMPR** | Although not mandatory, this information is very useful for the interpretation of the results, especially in cases of non-compliance due to residues belonging to the substance groups of anti-thyroid agents (A1b) and steroids (A1c). |
| other domains | — |

(ChemMon 2026 p51)

### F33 legislative class — the key facet for additives, flavourings, contaminants

| Domain | Usage |
| --- | --- |
| **VMPR** | **Required for processed products.** |
| **Pesticides** | — |
| **Contaminants** | **Required for samples analysed for acrylamide** to describe the acrylamide legislative classes in Commission Recommendation 2019/1888/EU and Commission Regulation (EC) 2017/2158. |
| **Additives** | **Required** to describe the sample legislative food category, according to Regulation (EC) 1333/2008. |
| **Flavourings** | **Required** to describe the sample legislative food category according to Regulation (EC) 1334/2008. |

(ChemMon 2026 p51)

### Related business rules

- **CHEMMON12** — For acrylamide, F33 (legislative class) facet is mandatory. See [[business-rules-contaminant]].
- **CHEMMON14** — For bisphenol compounds, F19 (packaging material) facet is mandatory. See [[business-rules-contaminant]].
- **CHEMMON15** — For PAHs, F19 (packaging material) facet should be reported.
- **CHEMMON17** — For mycotoxins, F21 (production method) facet should be reported.
- **CHEMMON18** — For arsenic in rice, F28 (process) facet should specify processed or unprocessed.
- **CHEMMON19** — For chlorates/perchlorates/QACs, F28 (process) facet should be reported.
- **CHEMMON39_a/b** — F33 (legislative classes) facet is mandatory for food additives and flavourings. See [[business-rules-additives]].
- **CHEMMON73** — For VMPR feed/water matrices, F23 (target consumer) facet should be reported. See [[business-rules-vmpr]].
- **CHEMMON76** — For VMPR with the same `sampEventId`, the F01 (species/breed) facet must be identical.
- **CHEMMON83** — If `sampMatCode = F10.A18PX`, F19 (packaging) and F18 (contact surface) should NOT be reported.
- **CHEMMON86** — F03 (physical state) facet recommended for specific food categories where physical state affects legal limits. See [[business-rules-additives]].
- **CHEMMON89** — For food category 13 (food for specific groups), F23 (target consumer) facet is recommended.
- **CHEMMON90_a** — For copper parameters, F20 (part consumed analysed) and/or F28 (process) facets are needed. See [[business-rules-pesticide]].
- **CHEMMON91** — For VMPR, only one F33 (legislative class) facet under VR classes should be reported per sample.
- **CHEMMON103** — Organic production (A07SE) and conventional production (A0C6Y) facets must not be reported together. See [[business-rules-cross-cutting]].
- **CHEMMON109** — Implicit F33 makes explicit F33 unnecessary for food additives/flavourings. See [[business-rules-additives]].
