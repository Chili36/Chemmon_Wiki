---
title: "SSD2 Matrix: VMPR-Specific Matrix Coding"
type: "reference"
domain: "vmpr"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 33-36 (Section 2, VMPR-specific matrix coding)"
related:
  - "[[ssd2-elements-matrix]]"
  - "[[foodex2-in-chemmon]]"
  - "[[vmpr-reporting]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Matrix: VMPR-Specific Matrix Coding

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 33-36 -->

## Rule Summary (Rule-First)

- In VMPR, `F01` source and `F02` part-nature must generally be present on the final matrix code, except in the feed/water and processed-composite cases described below.
- For derivative or processed terms that do not carry an implicit `F01`, add `F01` explicitly.
- Wild game requires explicit `F21.A07RY`.
- Feed and water samples hinge on `F23` target-consumer coding; conflicting `F23` species collapse the record into VMPR category "Other".
- Non-food animal matrices use base term `A0C60` plus explicit `F01` and `F02`.

## Derivative and processed VMPR terms

<!-- Source: ChemMon 2026 p33 -->

For VMPR monitoring, `F01` and `F02` are expected to be present in the final FoodEx2 matrix description. In many reporting-hierarchy terms they are already implicit, but raw-primary-commodity derivatives and processed products often do not carry an implicit `F01`. In those cases the data provider must add `F01` explicitly. Typical examples include dried egg or milk powder. (ChemMon 2026 p33)

## Wild animal VMPR samples

<!-- Source: ChemMon 2026 p33 -->

Wild animal samples must carry `F21.A07RY` ("Wild, gathered or hunted") explicitly. This is the operational marker for wild-game coding in the VMPR domain. Wild game is still classified and included in the VMPR National Report, but under Regulations (EU) 2022/1644 and 2022/1646 it is no longer considered a VMPR product category for the EU Annual Report except in the third-country-import plan. (ChemMon 2026 p33)

## Feed and water samples

<!-- Source: ChemMon 2026 pp. 33-35 -->

### Core rule: `F23` target consumer drives VMPR feed classification

Feed samples must be coded from the feed section of the MTX reporting hierarchy. The decisive rule is that the final `sampMatCode` must contain an implicit or explicit `F23` target-consumer facet identifying the intended animal species. (ChemMon 2026 p33)

- If only the generic implicit `F23 = A07TV` ("Animal feed") remains, the record is classified as VMPR category "Other".
- If a specific explicit `F23` is added, the record is classified into the matching VMPR product category.
- If multiple conflicting explicit `F23` species are reported, the record is also classified as "Other". (ChemMon 2026 p33-34)

### Feed-category organisation

For the first 13 feed categories in the hierarchy, the implicit target consumer is generic `A07TV`, so a species-specific explicit `F23` is needed if the record is intended for species-level VMPR categorisation. The last category, "Compound feed (feed)" and its species-specific children, may already carry an implicit specific `F23`, in which case no explicit `F23` is needed unless the implicit target is still generic. (ChemMon 2026 p35)

### Sheep and goat feed special case

If the selected feed term carries the implicit grouped facet `A07VF` ("Sheep and goat feed"), it must be refined with one of the child sheep/goat feed codes so EFSA can classify the record to the right VMPR category. (ChemMon 2026 p36)

### Water for farmed animals

Water given to farmed animals is not coded as drinking water. Select from the non-food/environment terms and add an explicit `F23` target-consumer facet because these base terms do not provide it implicitly. (ChemMon 2026 p36)

## Non-food animal matrices

<!-- Source: ChemMon 2026 p36 -->

For non-food matrices such as urine, retina, or hair, use base term `A0C60` ("Non-food animal-related matrices") and add explicit `F01` and `F02` facets to identify the source animal and the sampled material. (ChemMon 2026 p36)

## Insects, reptiles, and edible casings

<!-- Source: ChemMon 2026 p36 -->

Regulation (EU) 2022/1646 introduced new VMPR product categories including insects, reptiles, and edible casings.

- Only the authorised novel-food insects listed in the guidance should be sampled and reported for food production.
- Edible casings use base term `A0F1J`, and the source commodity must be added manually with `F27`. (ChemMon 2026 p36)

## Related business rules

- `CHEMMON76` — same `sampEventId` in VMPR must preserve the same species/breed facet chain. See [[business-rules-vmpr]].
- `CHEMMON91` — only one VMPR legislative-class `F33` under the VR classes. See [[business-rules-vmpr]].
- `CHEMMON92` — `paramCode` base term must belong to the `vetDrugRes` hierarchy. See [[business-rules-vmpr]].
- `FOODEX2_SAMMAT` — sampled matrix must still be a valid FoodEx2 code. See [[business-rules-cross-cutting]].
