---
title: "FoodEx2 Facets: Source, Part, Ingredient, and Origin"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 43-44, 49 (Table 4: F01, F02, F04, F27)"
related:
  - "[[foodex2-facets]]"
  - "[[foodex2-in-chemmon]]"
  - "[[ssd2-matrix-vmpr-coding]]"
  - "[[vmpr-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-contaminant]]"
  - "[[business-rules-additives]]"
---

# FoodEx2 Facets: Source, Part, Ingredient, and Origin

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 43-44, 49 -->

## Rule Summary

- Use `F01` for animal/plant/organism source where the domain expects source classification.
- Use `F02` for part or tissue, especially where legal limits depend on the sampled part.
- Use `F04` for ingredients of composite foods or rule-specific ingredient detail.
- Use `F27` for raw primary commodities from which derivatives or same-nature mixed products were obtained.

## F01 Source

| Domain | Usage |
| --- | --- |
| **VMPR** | Indicates the type of animal species sampled, such as pig samples. It can include the purpose of rearing, e.g. laying hens or broilers. Classification of samples as bovines, pigs, sheep, goats, horses, poultry, aquaculture, rabbit or game is based on this facet. Select a facet at species level or lower. |
| **Pesticides** | Not described as a domain-specific Table 4 requirement. |
| **Contaminants** | Defines the origin of the raw commodity; usually already assigned as an implicit facet. |
| **Additives** | Plant, animal, organism, or source of the raw agricultural commodity. For fish and seafood samples, the species must be specified. For algae-based products, the species of algae must be specified. |
| **Flavourings** | Same as additives. |

(ChemMon 2026 p43)

## F02 Part-Nature

| Domain | Usage |
| --- | --- |
| **VMPR** | Indicates the part or tissue of the animal tested, such as liver. It must be reported because the MRL legal limit applied depends on target tissue. The first step in the EFSA procedure for VMPR matrix classification for samples such as eggs, milk, or honey is based on this facet. |
| **Pesticides** | Part sampled, e.g. indicating fat samples from animals. |
| **Contaminants** | Part sampled. |
| **Additives** | Part sampled. |
| **Flavourings** | Part sampled. |

(ChemMon 2026 pp. 43-44)

## F04 Ingredient

| Domain | Usage |
| --- | --- |
| **VMPR** | Not described as a domain-specific Table 4 requirement. |
| **Pesticides** | Ingredients of composite food samples. |
| **Contaminants** | Used for products where ingredient detail affects classification, including potato crisps, pre-cooked French fries / potato products for home cooking, breakfast cereals excluding muesli and porridge, substitute coffee dry, baby foods other than processed cereal-based foods, rice-based products, algae-based foods for special nutritional uses, and compound products for infants and small children. |
| **Additives** | Repeatable facet used to characterise composite foods. |
| **Flavourings** | Repeatable facet used to characterise composite foods. |

(ChemMon 2026 p44)

## F27 Source-Commodities

| Domain | Usage |
| --- | --- |
| **Pesticides** | Report the representative lead crop. Defines the origin of derivatives for processed samples made from one single food or ingredient, such as orange juice or wine. |
| **Contaminants** | Describes the raw primary commodity from which an ingredient or derivative has been obtained. Also applies to same-nature products from mixed raw sources, such as cheese or fruit juice. |
| other domains | Not described as a domain-specific Table 4 requirement. |

(ChemMon 2026 p49)

## Related Business Rules

- `CHEMMON76`: for VMPR with the same `sampEventId`, the `F01` species/breed facet must be identical. See [[business-rules-vmpr]].
- `CHEMMON12`: for acrylamide, `F04` ingredient detail is recommended for specific composite and baby-food contexts, while `F33` remains mandatory. See [[business-rules-contaminant]] and [[contaminant-reporting]].
- `CHEMMON108`: additives/flavourings require matrix specificity for food colour/additive classification. See [[business-rules-additives]].

## Navigation

- For VMPR feed, water, non-food matrices, wild game, and processed-products examples, continue to [[ssd2-matrix-vmpr-coding]].
- For FoodEx2 syntax and implicit/explicit facet examples, continue to [[foodex2-in-chemmon]].
