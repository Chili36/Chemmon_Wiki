---
title: "FoodEx2 Facets: State, Cooking, Production Method, and Process"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 44-45, 47-50 (Table 4: F03, F17, F21, F28)"
related:
  - "[[foodex2-facets]]"
  - "[[foodex2-in-chemmon]]"
  - "[[ssd2-matrix-vmpr-coding]]"
  - "[[vmpr-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
  - "[[business-rules-contaminant]]"
  - "[[business-rules-additives]]"
  - "[[business-rules-pesticide]]"
---

# FoodEx2 Facets: State, Cooking, Production Method, and Process

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 44-45, 47-50 -->

## Rule Summary

- Use `F03` for physical state where the domain needs solid/liquid/jelly or similar state information.
- Use `F17` for extent of cooking in contaminant contexts where heat treatment affects interpretation.
- Use `F21` for production method, including organic/conventional reporting and wild-game marking.
- Use `F28` for processing when the processed state is not already implicit in the chosen FoodEx2 base term.

## F03 Physical State

| Domain | Usage |
| --- | --- |
| **VMPR** | Not described as a domain-specific Table 4 requirement. |
| **Pesticides** | Not described as a domain-specific Table 4 requirement. |
| **Contaminants** | Physical state of the tested food, e.g. solid, jelly, liquid. |
| **Additives** | Physical state of the tested food. |
| **Flavourings** | Physical state of the tested food. |

(ChemMon 2026 p44)

## F17 Extent-of-Cooking

| Domain | Usage |
| --- | --- |
| **Contaminants** | Heat treatment applied to food, required for furans and acrylamide. |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 p45)

## F21 Production Method

| Domain | Usage |
| --- | --- |
| **VMPR** | `A07RY` should be used to identify wild game. Classification of samples as wild game is based on this facet. |
| **Pesticides** | Required for analysis of organic food compared with conventionally produced food. Use `A07SE` for organic production. If known to be non-organic, use `A0C6Y` (conventional non-organic production). If unknown, do not report this facet. `A07RY` also identifies wild/gathered/hunted game. |
| **Contaminants** | Recommended. Required for analysis of the mycotoxin situation in organic food compared with non-organic food. |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 pp. 47-48)

## F28 Process

| Domain | Usage |
| --- | --- |
| **VMPR** | Required to distinguish processed food samples. |
| **Pesticides** | Required to distinguish processed food samples, because MRL compliance is checked against results expressed for unprocessed samples. For processed products derived from raw agricultural products, select the most specific processing code. For copper results, the process applied to the analysed sample may need to be reported, e.g. roasting. |
| **Contaminants** | Required to distinguish processed food samples. Use a more detailed classification where possible. |
| **Additives** | Required to distinguish processed food samples. |
| **Flavourings** | Required to distinguish processed food samples. |

(ChemMon 2026 pp. 49-50)

## Related Business Rules

- `CHEMMON17`: for mycotoxins, `F21` production method should be reported. See [[business-rules-contaminant]].
- `CHEMMON18`: for arsenic in rice, `F28` should specify processed or unprocessed state. See [[business-rules-contaminant]].
- `CHEMMON19`: for chlorates/perchlorates/QACs, `F28` should be reported. See [[business-rules-contaminant]].
- `CHEMMON86`: `F03` is recommended for specified FA/FF categories where physical state affects legal limits. See [[business-rules-additives]].
- `CHEMMON90_a`: for pesticide copper, `F20` and/or `F28` are needed to describe sample preparation. See [[business-rules-pesticide]].
- `CHEMMON103`: organic and conventional production facets must not be reported together. See [[business-rules-cross-cutting]].

## Navigation

- For VMPR wild game and processed-product examples, continue to [[ssd2-matrix-vmpr-coding]].
- For pesticide copper preparation cases, continue to [[pesticide-reporting]].
- For contaminant substance-specific process expectations, continue to [[contaminant-reporting]].
