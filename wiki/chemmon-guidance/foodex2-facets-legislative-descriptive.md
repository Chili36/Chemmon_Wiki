---
title: "FoodEx2 Facets: Legislative and Descriptive Facets"
type: "reference"
domain: "all"
last_updated: "2026-11-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 44-45, 50-51 (Table 4: F06, F07, F10, F11, F31, F32, F33)"
  - "pp. 38, 42 (F33 for additives and flavourings)"
  - "p. 96 (Table 8: food flavourings F33)"
  - "p. 121 (Table 10: CHEMON39)"
related:
  - "[[foodex2-facets]]"
  - "[[foodex2-in-chemmon]]"
  - "[[vmpr-reporting]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-contaminant]]"
  - "[[business-rules-additives]]"
---

# FoodEx2 Facets: Legislative and Descriptive Facets

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 44-45, 50-51 -->

## Rule Summary

- Use `F06`, `F07`, `F10`, and `F11` for descriptive food attributes where the domain or substance-specific rule asks for them.
- Use `F31` and `F32` for VMPR interpretation context such as animal age class and gender.
- Use `F33` for legislative class, especially acrylamide, VMPR processed products, and FA/FF categories.

## F06 Surrounding Medium

| Domain | Usage |
| --- | --- |
| **Contaminants** | Surrounding medium of the food, such as oil or fat. |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 p44)

## F07 Fat Content

| Domain | Usage |
| --- | --- |
| **Contaminants** | Fat content of the food. Report when the expression of results is fat weight (`exprResType = B003A`). |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 p45)

## F10 Qualitative-Info

| Domain | Usage |
| --- | --- |
| **Pesticides** | For EUCP whole grain cereal records (wheat, barley, oat, rye), flour integral/not refined (`A06HR`) can be reported with the cereal-based term. |
| **Contaminants** | Recommended for some plasticising-agent parameters, e.g. phthalates, to express that a product is not packed. |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 p45)

## F11 Alcohol Content

| Domain | Usage |
| --- | --- |
| **Contaminants** | Alcohol content of the food. |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 p45)

## F31 Animal-Age-Class

| Domain | Usage |
| --- | --- |
| **VMPR** | Useful for interpretation, especially in non-compliance cases for anti-thyroid agents (A1b) and steroids (A1c). |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 p50)

## F32 Gender

| Domain | Usage |
| --- | --- |
| **VMPR** | Useful for interpretation, especially in non-compliance cases for anti-thyroid agents (A1b) and steroids (A1c). |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 p51)

## F33 Legislative Class

| Domain | Usage |
| --- | --- |
| **VMPR** | Required for processed products. |
| **Pesticides** | Not described as a domain-specific Table 4 requirement. |
| **Contaminants** | Required for samples analysed for acrylamide to describe acrylamide legislative classes in Commission Recommendation 2019/1888/EU and Commission Regulation (EU) 2017/2158. |
| **Additives** | Required to describe the sample legislative food category according to Regulation (EC) No 1333/2008. |
| **Flavourings** | Recommended to describe the sample legislative food category according to Regulation (EC) No 1334/2008. See the Source discrepancy note below. |

(ChemMon 2026 p51)

Source discrepancy: Table 4 prints "Recommended" for flavourings (ChemMon 2026 p51), but the prose says that for additives and flavourings the F33 facet "must always be present" and that it is mandatory to report it (ChemMon 2026 p38, p42), and Table 8 gives the food flavourings F33 element the status "Mandatory", although the same row says that if F33 is not implicitly assigned "it is recommended to add it" (the food additives row says "it is required to add it") (ChemMon 2026 pp. 95-96). Validation enforces the mandatory reading: the F33 rule for `is_add=1` or `is_flav=1` returns an Error (ChemMon 2026 p121).

## Related Business Rules

- `CHEMON12`: for acrylamide, `F33` is mandatory. See [[business-rules-contaminant]] and [[contaminant-reporting]].
- `CHEMON39`: `F33` is mandatory for food additives and flavourings. See [[business-rules-additives]] and [[food-additives-reporting]].
- `CHEMON91`: for VMPR, only one F33 under A1ANN (Veterinary Medicinal Product Residues Classes) should be reported for `sampMatCode` and for `anMatCode`. See [[business-rules-vmpr]].
- `CHEMON109`: implicit `F33` makes explicit `F33` unnecessary for FA/FF. See [[business-rules-additives]].

## Navigation

- For acrylamide category coding, continue to [[contaminant-reporting]].
- For FA/FF legislative category coding, continue to [[food-additives-reporting]].
- For VMPR processed-product `F33` coding, continue to [[vmpr-reporting]].
