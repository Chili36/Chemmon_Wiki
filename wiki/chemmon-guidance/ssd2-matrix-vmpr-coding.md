---
title: "SSD2 Matrix: VMPR-Specific Matrix Coding"
select_when: "VMPR matrix coding: F01/F02 exceptions for feed/water and processed/composite food, feed F23, sheep/goat coding, F33 groups and worked matrix examples."
type: "reference"
domain: "vmpr"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 33-38 (Section 2, VMPR samples coding: F01/F02, wild animals, feed and water, non-food matrices, new product categories, processed products)"
  - "pp. 131, 135-136 (Table 10: CHEMON76, CHEMON91, CHEMON92)"
related:
  - "[[ssd2-elements-matrix]]"
  - "[[foodex2-in-chemmon]]"
  - "[[foodex2-facets-source-origin]]"
  - "[[foodex2-facets-state-process]]"
  - "[[foodex2-facets-packaging-consumer]]"
  - "[[foodex2-facets-legislative-descriptive]]"
  - "[[vmpr-reporting]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Matrix: VMPR-Specific Matrix Coding

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 33-38 -->

## Rule Summary (Rule-First)

- In VMPR, `F01` source and `F02` part-nature "must always be present" (ChemMon 2026 p33) on the final matrix code, except in the feed/water and processed-composite cases described below. For the facet definitions, see [[foodex2-facets-source-origin]].
- For derivative or processed terms that do not carry an implicit `F01`, add `F01` explicitly.
- Wild game requires explicit `F21.A07RY`; see [[foodex2-facets-state-process]].
- Feed and water samples hinge on `F23` target-consumer coding; conflicting `F23` species (explicit or implicit) put the record into VMPR category "Other". See [[foodex2-facets-packaging-consumer]].
- Processed products under Plan 3 carry one `F33` code from the VMPR legislative classes; see the processed-product section below.
- Non-food animal matrices use base term `A0C60` plus explicit `F01` and `F02`.

## Derivative and processed VMPR terms

<!-- Source: ChemMon 2026 p33 -->

For VMPR monitoring, `F01` and `F02` must always be present in the final FoodEx2 matrix description (except for the special case of feed and water samples and processed-composite food). In most cases they are already pre-assigned as implicit facets in the reporting-hierarchy codes, but the `F01` is not implicitly pre-assigned in the codes for raw-primary-commodity (RPC) derivatives or 'Processed' products. In those cases the `F01` should be added by the data provider: for example, with `A031X` (Hen egg mixed whole, dried) or `A02PJ` (Milk powder) an `F01` code shall be reported, e.g. `F01.A057Z` (Gallus (chicken) (as animal)) or `F01.A057E` (Cattle (as animal)). (ChemMon 2026 p33)

If reported, an explicit facet supersedes the implicit facet already pre-assigned in the selected code when EFSA categorises the matrix according to the VMPR legislation for the national and annual EU reports. Non-food base terms are an example where `F01`/`F02` are not pre-assigned. (ChemMon 2026 p33)

## Wild animal VMPR samples

<!-- Source: ChemMon 2026 p33 -->

Wild animal samples must carry `F21.A07RY` ("Wild, gathered or hunted") explicitly. This is the operational marker for wild-game coding in the VMPR domain. Wild game is still classified and included in the VMPR National Report, but under Regulations (EU) 2022/1644 and 2022/1646 it is no longer considered a VMPR product category for the EU Annual Report except in the third-country-import plan. (ChemMon 2026 p33)

## Feed and water samples

<!-- Source: ChemMon 2026 pp. 33-35 -->

### Core rule: `F23` target consumer drives VMPR feed classification

Feed samples must be coded from the feed section of the MTX reporting hierarchy; each base term there contains the wording "(feed)", e.g. `A05CR` (Barley grain (feed)). The decisive rule is that the final `sampMatCode` must contain an implicit or explicit `F23` target-consumer facet identifying the intended animal species. (ChemMon 2026 p33)

- If only the generic implicit `F23 = A07TV` ("Animal feed") remains, the record is classified as VMPR category "Other".
- If a specific explicit `F23` is added, the record is classified into the matching VMPR product category.
- If more than one explicit `F23` code is reported and they refer to different animal species, the sample is classified as "Other" and the analytical result will not be included in the VMPR reports created by EFSA. An explicit `F23` that contradicts a species-specific implicit `F23` is also classified as "Other" (third example below). (ChemMon 2026 p33-34)
- If the target species is not known, or the feed is intended for and given to animals of different species, `F23` does not need to be selected and explicitly reported; select a code that implicitly contains `A07TV`, and the sample will always be classified as "Other". (ChemMon 2026 p34)

| `sampMatCode` | Implicit facets | Explicit facet added | Result |
| --- | --- | --- | --- |
| `A0BBB#F23.A07VC` (Barley, roasted (feed)) | F02 feed-related; F23 animal feed | F23 `A07VC` pig feed | Correct coding; classified in VMPR Product Category "Pigs" |
| `A0BBB#F23.A07VC$F23.A18EH` | F02 feed-related; F23 animal feed | F23 `A07VC` pig feed and `A18EH` chicken feed | Feed fed to two different species (pigs and chicken); classified as "Other" |
| `A0BTL#F23.A07VC` (Turkeys/Complete feed (feed)) | F02 feed-related; F23 turkey feed (`A18EM`) | F23 `A07VC` pig feed | Incorrect, presumably a coding mistake: contradictory F23 codes. If not amended, classified as "Other", not "Poultry" nor "Pigs" |
| `A0BBB` | F02 feed-related; F23 animal feed | none | Acceptable coding, but classified as "Other" because the only F23 is the implicit `A07TV` |

(ChemMon 2026 p34-35)

### Feed-category organisation

The feed codes are grouped into 14 categories. If a base term is selected from one of the first 13 categories, the implicit target consumer is the generic `A07TV` (Animal feed), and an explicit `F23` must be selected by the data provider from the codes listed under `A07TX` (Feed for animals), e.g. `A07VE` (Rabbit feed). EFSA uses the implicit and/or explicit `F23` to classify results into the VMPR legislative matrix categories (bovines, pigs, sheep & goats, horses, poultry, rabbit, farmed game, wild game, aquaculture, milk, eggs and honey). (ChemMon 2026 p35)

The last category, "Compound feed (feed)" (`A0BT0`), already implicitly contains an `F23` designating the target species, so no explicit `F23` is needed. In some cases, e.g. `A0BV0` (Unspecified Complete Feed), no species can be specified in the implicit facets, so an explicit target-consumer facet is needed if the record is intended for inclusion in an Annual Report. Example: `A0BBB#F23.A07VC` (category #1, barley for breeding pigs) needs `F23.A07VC` to allocate the record to pigs; `A0BV8` (category #14, complementary feed for breeding pigs) does not. (ChemMon 2026 p35)

Source discrepancy: p. 35 says there are 14 categories and that the first 13 carry the generic `A07TV` "Animal feed"; p. 34 tells providers who do not know the species to select "among the first 12 feed categories" and names `A07TV` "Feed sample". The guidance does not reconcile the two numbers. (ChemMon 2026 p34, p35)

### Sheep and goat feed special case

If the selected feed term carries the implicit grouped facet `A07VF` ("Sheep and goat feed"), it is always necessary to add one of the four codes grouped under `A07VF`. (ChemMon 2026 p36)

| Feed for | Term | Code as printed |
| --- | --- | --- |
| Goats | Kids reared for reproduction or meat production feed | `A18EX` |
| Goats | Dairy/reproductive goat feed | `A18EX` |
| Sheep | Lambs reared for reproduction or meat production feed | `A18ET` |
| Sheep | Dairy/reproductive sheep feed | `A18EV` |

Source discrepancy: p. 36 prints the same code, `A18EX`, for both goat terms. One of the two is a typo in the guidance; check the MTX catalogue for the correct goat codes rather than relying on this table. (ChemMon 2026 p36)

### Water for farmed animals

Water given to farmed animals is not coded as drinking water. Select one of the codes in the "Environment" group under "Non-food matrices" in the reporting hierarchy; because these terms do not contain an implicit target-consumer facet, a code for `F23` must be added. Example: water from a "Watering place for animals" for cattle is `A0F7N#F23.A07TY`. (ChemMon 2026 p36)

## Non-food animal matrices

<!-- Source: ChemMon 2026 p36 -->

For non-food matrices such as urine, retina, or hair, use base term `A0C60` ("Non-food animal-related matrices") and add explicit `F01` and `F02` facets to identify the source animal and the sampled material. (ChemMon 2026 p36)

| Example | `sampMatCode` | Facets |
| --- | --- | --- |
| Cow hair sample | `A0C60#F02.A0ESP$F01.A057E` | F02 hair as part-nature (`A0ESP`); F01 cattle (as animal) (`A057E`) |
| Cow retina sample | `A0C60#F02.A0ESJ$F01.A057E` | F02 retina (as part-nature) (`A0ESJ`); F01 cattle (as animal) (`A057E`) |

(ChemMon 2026 p36)

## Insects, reptiles, and edible casings

<!-- Source: ChemMon 2026 pp. 36-37 -->

Regulation (EU) 2022/1646 introduces three new VMPR product categories: insects, reptiles and casings. (ChemMon 2026 p36)

- The only four insects authorised as novel food in the EU for food production are *Tenebrio molitor*, *Locusta migratoria*, *Acheta domesticus* and *Alphitobius diaperinus*; only those insects can be reported to EFSA. They can be sampled and reported as frozen/whole animal, dried and/or powdered. (ChemMon 2026 p36)
- Edible casings use base term `A0F1J`. When including the source, the source commodity (`F27`) must be manually inserted. (ChemMon 2026 p36)

| Example | `sampMatCode` | Facets |
| --- | --- | --- |
| Migratory locust, powdered | `A16XE#F01.A16VP$F28.A07LA` | Base term edible insect adults; F01 migratory locust (as animal); F28 grinding/milling/crushing |
| Snakes' meat | `A02LC` | Implicit: F02 reptile meat (`A0EMJ`); F01 snakes (as animal) (`A04SS`) |
| Casings from adult sheep | `A0F1J#F01.A0CDD$F27.A01ZQ` | F01 sheep over 1 year (as animal); F27 sheep edible offal, non-muscle, other than liver and kidney |

(ChemMon 2026 p37)

## Processed product samples (Plan 3)

<!-- Source: ChemMon 2026 pp. 37-38 -->

Annex III of Regulation (EU) 2022/1646 introduces the possibility of reporting processed products from the main raw product categories for samples gathered under the national risk-based control plan for third-country import (Plan 3). Processed products reported with a Plan 1 or Plan 2 combination get no plan flag and are categorised as "Other" (ChemMon 2026 p25). To map these samples to the main VMPR legislative commodity groups, the facet `F33` (legislative classes) has been introduced. The codes are under the parent term "Veterinary Medicinal Product Residues classes (Annex III – 2022/1646)", but only one code should be reported. For a mixed sample (e.g. mixed pork and beef), the data provider should decide to which VMPR legislative commodity the sample is counted by adding only one `F33` code. (ChemMon 2026 p37)

| Example | `sampMatCode` | Facets |
| --- | --- | --- |
| Canned meat, mixed poultry | `A024C#F04.A04DT$F04.A04ED$F33.A1ANV` | F04 chicken msm and turkey msm; F33 VR – Poultry |
| Whey protein | `A02PS#F33.A1ANY` | F33 VR – Milk |
| Mix cow/sheep hard cheese | `A02ZH#F27.A02LV$F27.A02MC$F33.A1ANY` | F27 cow milk and sheep milk; F33 VR – Milk |
| Pork spreadable cooked sausage | `A025K#F04.A01RG$F04.A01VA$F04.A01XJ$F33.A1ANS` | F04 pig fresh meat, pig fat tissue and pig liver; F33 VR – Pigs |
| Smoked salmon | `A02KF#F33.A1ANX` | F33 VR – Aquaculture |
| Egg powder | `A031X#F33.A1ANZ` | Base term hen egg mixed whole, dried; F33 VR – Eggs |
| Chicken sausage | `A024G#F33.A1ANV` | Base term fresh raw sausage; F33 VR – Poultry |
| Beef sausage | `A024G#F33.A1ANP` | Base term fresh raw sausage; F33 VR – Bovines |

(ChemMon 2026 p37-38)

## Related business rules

- `CHEMON76` — for VMPR samples with the same `sampEventId`, the `F01` facet code of `sampMatCode` shall be the same for each sample (Error). See [[business-rules-vmpr]].
- `CHEMON91` — only one VMPR legislative-class `F33` under the VR classes. See [[business-rules-vmpr]].
- `CHEMON92` — the base terms of `sampMatCode` and `anMatCode` must belong to the VetDrugRes matrix hierarchy. It does not validate `paramCode`. See [[business-rules-vmpr]].
- `FOODEX2_SAMPMAT` — sampled matrix must still be a valid FoodEx2 code. See [[business-rules-cross-cutting]].
