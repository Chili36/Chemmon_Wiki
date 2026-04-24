---
title: "FoodEx2 Facets: Packaging, Part Consumed, and Target Consumer"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 45-48 (Table 4: F18, F19, F20, F23)"
related:
  - "[[foodex2-facets]]"
  - "[[foodex2-in-chemmon]]"
  - "[[ssd2-matrix-vmpr-coding]]"
  - "[[vmpr-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
  - "[[baby-food-reporting]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-contaminant]]"
  - "[[business-rules-additives]]"
  - "[[business-rules-pesticide]]"
---

# FoodEx2 Facets: Packaging, Part Consumed, and Target Consumer

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 45-48 -->

## Rule Summary

- Use `F18` for packaging format where the container or contact shape matters.
- Use `F19` for packaging material, especially in contaminant migration contexts.
- Use `F20` for part consumed/analysed, including visible-fat or peel differences in pesticide-style sample preparation.
- Use `F23` for target consumer, including animal feed species and human population group.

## F18 Packaging Format

| Domain | Usage |
| --- | --- |
| **Contaminants** | Describes the shape of the container or wrapper that holds the marketed product. Recommended for some plasticising-agent parameters; see Table 8-specific requirements. |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 p45)

## F19 Packaging Material

| Domain | Usage |
| --- | --- |
| **Contaminants** | Describes the material of the container or wrapper that holds the marketed product. Crucial for some parameters, including bisphenol compounds and plasticising agents; see Table 8-specific requirements. |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 pp. 45-46)

## F20 Part-Consumed-Analysed

| Domain | Usage |
| --- | --- |
| **Pesticides** | Recommended for meat or meat sub-codes to indicate visible fat status: `A0F4V` excluding visible fat or `A0F4T` including visible fat. For muscle samples under Regulation (EC) No 396/2005, use `A0F4V` because MRLs for muscle apply to meat after removal of trimmable fat. |
| **Pesticides - copper** | For copper (`paramCode` RF-0102-001-PPP), EFSA expects `F20` and/or `F28` to reflect sample preparation. Some commodities differ depending on whether the result is treated as pesticide-residue-style vs contaminant-style, such as banana with peel versus without peel. |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 pp. 46-47)

## F23 Target Consumer

| Domain | Usage |
| --- | --- |
| **VMPR** | Must be used for feed samples to indicate the species for whom the feed is intended if not already implicit in the base term. |
| **Pesticides** | Must be used for feed samples to indicate the species for whom the feed is intended if not already implicit in the base term. |
| **Contaminants** | Must be used for feed samples to indicate the species for whom the feed is intended if not already implicit. It can also indicate age of the human consumer/population, such as infants, toddlers, children, or adults. |
| **Additives** | Same as contaminants. |
| **Flavourings** | Same as contaminants. |

(ChemMon 2026 p48)

## Related Business Rules

- `CHEMMON14`: for bisphenol compounds, `F19` packaging material is mandatory. See [[business-rules-contaminant]].
- `CHEMMON15`: for PAHs, `F19` packaging material should be reported. See [[business-rules-contaminant]].
- `CHEMMON73`: for VMPR feed/water matrices, `F23` should be reported. See [[business-rules-vmpr]].
- `CHEMMON83`: if `sampMatCode = F10.A18PX`, `F19` and `F18` should not be reported. See [[business-rules-contaminant]].
- `CHEMMON89`: for FA/FF category 13, `F23` target consumer is recommended. See [[business-rules-additives]].
- `CHEMMON90_a`: for pesticide copper, `F20` and/or `F28` are needed. See [[business-rules-pesticide]].

## Navigation

- For VMPR feed and water matrix coding, continue to [[ssd2-matrix-vmpr-coding]].
- For contaminant packaging requirements, continue to [[contaminant-reporting]].
- For infant and baby-food target-consumer cases, continue to [[baby-food-reporting]].
