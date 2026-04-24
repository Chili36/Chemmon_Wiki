---
title: "FoodEx2 Facets: Legislative and Descriptive Facets"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 44-45, 50-51 (Table 4: F06, F07, F10, F11, F31, F32, F33)"
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
| **Flavourings** | Required to describe the sample legislative food category according to Regulation (EC) No 1334/2008. |

(ChemMon 2026 p51)

## Related Business Rules

- `CHEMMON12`: for acrylamide, `F33` is mandatory. See [[business-rules-contaminant]] and [[contaminant-reporting]].
- `CHEMMON39_a/b`: `F33` is mandatory for food additives and flavourings. See [[business-rules-additives]] and [[food-additives-reporting]].
- `CHEMMON91`: for VMPR, only one `F33` legislative class under the VR classes should be reported per sample. See [[business-rules-vmpr]].
- `CHEMMON109`: implicit `F33` makes explicit `F33` unnecessary for FA/FF. See [[business-rules-additives]].

## Navigation

- For acrylamide category coding, continue to [[contaminant-reporting]].
- For FA/FF legislative category coding, continue to [[food-additives-reporting]].
- For VMPR processed-product `F33` coding, continue to [[vmpr-reporting]].
