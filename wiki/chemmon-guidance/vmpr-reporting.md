---
title: "VMPR Reporting"
type: "domain-guide"
domain: "vmpr"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[foodex2-facets-source-origin]]"
  - "[[foodex2-facets-state-process]]"
  - "[[foodex2-facets-packaging-consumer]]"
  - "[[foodex2-facets-legislative-descriptive]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[ssd2-matrix-vmpr-coding]]"
  - "[[business-rules]]"
  - "[[baby-food-reporting]]"
source_pages:
  - "pp. 20-21 (B.03 sampStrategy, B.04 progType)"
  - "pp. 23-25 (Table 2 and VMPR plan flags)"
  - "pp. 47, 51 (Table 4, F21 and F33 rows)"
  - "pp. 33-38 (VMPR, wild animal, feed/water, non-food, new categories, processed products)"
  - "p. 52 (matrix examples)"
  - "p. 71 (M.16 resType)"
  - "pp. 129, 135, 137-139 (Table 10: CHEMON63, CHEMON91, CHEMON96, CHEMON100, CHEMON102)"
last_updated: "2026-11-11"
---

# VMPR Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 23-25 -->
## Control Plan Types

VMPR (Veterinary Medicinal Product Residues) is one of five [[chemmon-overview|ChemMon]] reporting domains. EFSA assigns each VMPR sample (`progLegalRef` `N371A`) one of four flags from `progType`, `sampStrategy` and, for Plan 3, `sampPoint`:

| Flag | Meaning | Flag condition |
| --- | --- | --- |
| Plan 1 | National risk-based control plan for production in the Member States. | `progType` `K005A` or `K018A`, `sampStrategy` `ST20A`, and the sample is considered unprocessed. |
| Plan 2 | National randomised surveillance plan for production in the Member States. | `progType` `K005A` or `K018A`, `sampStrategy` `ST10A`, and the sample is considered unprocessed. |
| Plan 3 | National risk-based control plan for third-country imports. | `progType` `K038A`, `sampStrategy` `ST20A` and `sampPoint` `E010A` (Border Control Posts). |
| Other | Any additional sample not counted towards the minimum sampling frequencies of Regulation (EU) 2022/1646: mainly suspect samples and samples taken beyond that regulation (with `ST90A`). | Any combination not covered by the three plans, including processed products with a Plan 1 or Plan 2 combination, gets no plan flag and is categorised as Other. |

For Plan 1 and Plan 2 "an exception in the processing has been included for insects". (ChemMon 2026 p25)

EU MACP and MANCP are pesticide flags, not VMPR plans; see [[pesticide-reporting]]. (ChemMon 2026 pp. 25-26)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 20-21 -->
## Sampling Strategy Codes

Each VMPR sample carries a `sampStrategy` code. For VMPR National and Annual Reports, all results should be reported with the strategies Objective, Selective (target) or Suspect; Other is for results outside the national control plans. (ChemMon 2026 p20)

| Code | Strategy | VMPR use |
| --- | --- | --- |
| `ST10A` | Objective sampling (random surveillance). | Surveillance samples for the national randomised surveillance plan (Plan 2). |
| `ST20A` | Selective/targeted sampling (risk-based, to assess compliance with legislation). | Typically used for the national risk-based control plans for production in the Member States and for third-country imports (Plan 1 and Plan 3). |
| `ST30A` | Suspect sampling (e.g. follow-up enforcement samples, samples after RASFF notifications, emergency measures at import). | Flagged Other. |
| `ST90A` | Other. | Results not considered in the VMPR National Control Plans set up by Regulation (EU) 2022/1646, e.g. monitoring programmes under national legislation that go beyond that regulation. |

(ChemMon 2026 pp. 20-21, 25)

## Programme Type Codes

| Code | Catalogue label | VMPR use |
| --- | --- | --- |
| `K005A` | Official (National) programme | Plan 1 (`ST20A`), Plan 2 (`ST10A`), Other (`ST30A`, `ST90A`). |
| `K018A` | Official (National and EU) programme | Plan 1 (`ST20A`), Plan 2 (`ST10A`), Other (`ST30A`, `ST90A`). The p. 21 example calls it "the code to be used when reporting VMPR results under the national risk-based and randomised surveillance plans for production in the Member States (Plan 1 and Plan 2)". |
| `K038A` | Official (National) programme for Third Country Import | Plan 3 (`ST20A`, with `sampPoint` `E010A`), Other (`ST30A`, `ST90A`). |
| `K009A` | Official (EU) programme | No VMPR (`N371A`) combination in Table 2. |
| `K019A` | EU increased control programme on imported food | No VMPR (`N371A`) combination in Table 2; used with `N317A` and `N422A`. |

(ChemMon 2026 p21; Table 2 pp. 23-24; p25)

Example (VMPR control Plan 1): `progLegalRef` `N371A`, `progType` `K018A`, `sampStrategy` `ST20A`. (ChemMon 2026 p26) For all domains see [[ssd2-programme-strategy-and-type]] and [[ssd2-programme-valid-combinations]].

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 33-38 -->
## FoodEx2 Coding for VMPR

VMPR has specific FoodEx2 requirements beyond the general rules in [[foodex2-in-chemmon]]. For the element-level matrix guidance behind these rules, see [[ssd2-matrix-vmpr-coding]]. For the Table 4 facet definitions, use [[foodex2-facets-source-origin]], [[foodex2-facets-state-process]], [[foodex2-facets-packaging-consumer]], and [[foodex2-facets-legislative-descriptive]]:

- **F01 (Source) and F02 (Part-nature)** must generally be present, implicitly or explicitly, except for the special feed/water and processed-composite cases. Apply the scoped guidance in [[ssd2-matrix-vmpr-coding]] rather than requiring both facets on every VMPR sample. (ChemMon 2026 p33)
- **Wild animals**: `A07RY` ("Wild, gathered or hunted", facet F21) must always be added to the base term as an explicit facet (p. 33); Table 4 words it as "A07RY should be used to identify wild game" and says classification as wild game is based on this facet (p. 47). (ChemMon 2026 pp. 33, 47)
- **Feed samples**: `sampMatCode` must always contain an implicit or explicit F23 (target consumer) code. (ChemMon 2026 p33)
- **Non-food matrices** (e.g. urine, retina or hair): use base term `A0C60` ("Non-food animal-related matrices") with explicit F01 and F02 facets to identify the animal species and the sample. (ChemMon 2026 p36)
- **Processed products**: F33 (legislative classes) is "Required for processed products" (Table 4), using one code under "Veterinary Medicinal Product Residues classes (Annex III – 2022/1646)". (ChemMon 2026 pp. 37, 51)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 33-36 -->
## Feed and Water Coding

Feed samples must use a `sampMatCode` from the **feed section** of the MTX catalogue. Feed base terms include "(feed)" wording to distinguish them from food products. (ChemMon 2026 p33)

- **F23 (target consumer)** must always be present (implicit or explicit) for feed samples. (ChemMon 2026 p33)
- If the target species is not known, or the feed is given to animals of different species, F23 does not need to be explicitly reported: select a code among the first feed categories that implicitly contain F23 `A07TV`; the sample is classified in the VMPR Product Category **"Other"**. (ChemMon 2026 p34)
- Source discrepancy: p. 34 says "the first 12 feed categories" and labels `A07TV` "Feed sample"; p. 35 says the feed codes are "grouped into 14 categories", that the first 13 implicitly contain `A07TV` = "Animal feed", and that for those "an explicit facet code for F23 target consumer must be selected by the data provider" (from the codes under `A07TX` "Feed for animals"). The guidance does not reconcile the count, the label, or optional versus "must". (ChemMon 2026 pp. 34-35)
- If a specific explicit F23 species code is reported, the sample is classified in the corresponding VMPR Product Category (e.g. `A0BBB#F23.A07VC` → Pigs). Explicit F23 codes for different species on the same sample put it in "Other". (ChemMon 2026 p34)
- The last feed category, "Compound feed (feed)" (`A0BT0`), already carries an implicit species F23, so no explicit F23 is needed; where a term cannot specify the species (e.g. `A0BV0` "Unspecified Complete Feed") an explicit F23 is needed if the record is intended for an Annual Report. (ChemMon 2026 p35)
- **Sheep/goat feed**: when the feed base term implicitly contains F23 `A07VF` ("Sheep and goat feed"), it is always necessary to add one of the four codes grouped under `A07VF`: for goats "Kids reared for reproduction or meat production feed" or "Dairy/reproductive goat feed"; for sheep "Lambs reared for reproduction or meat production feed" (`A18ET`) or "Dairy/reproductive sheep feed" (`A18EV`). Source discrepancy: p. 36 prints `A18EX` for both goat terms, so one is a typo; check the MTX catalogue. The table is on [[ssd2-matrix-vmpr-coding]]. (ChemMon 2026 p36)

**Water given to farmed animals**: select one of the codes in the "Environment" group of the "Non-food matrices" list in the reporting hierarchy. These terms have no implicit target-consumer facet, so an F23 code must be added. (ChemMon 2026 p36)

### Worked Example -- Feed and Water

- Water from a "Watering place for animals" for cattle: `A0F7N#F23.A07TY` (ChemMon 2026 p36)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 25, 37-38 -->
## Processed Products for VMPR

Annex III of Regulation (EU) 2022/1646 introduces the possibility of reporting processed products from the main raw product categories **for samples gathered under the national risk-based control plan for third-country import (Plan 3)**. (ChemMon 2026 p37) Processed products with a Plan 1 or Plan 2 combination get no plan flag and are categorised as Other. (ChemMon 2026 p25)

- **F33 (legislative classes)** maps the sample to a VMPR legislative commodity group; it is "Required for processed products" (Table 4). (ChemMon 2026 pp. 37, 51)
- Only **one F33 code** should be reported. For a mixed sample (e.g. pork and beef) the data provider decides which VMPR commodity group applies. (ChemMon 2026 p37) CHEMON91 is a Warning when more than one F33 under the VMPR classes parent (`A1ANN`) is reported for a VMPR result. (ChemMon 2026 Table 10 p. 135)

### Worked Examples -- Processed Products

| Description | Code | VMPR Category |
| --- | --- | --- |
| Canned meat mixed poultry | `A024C#F04.A04DT$F04.A04ED$F33.A1ANV` | VR - Poultry |
| Whey protein | `A02PS#F33.A1ANY` | VR - Milk |
| Mix cow/sheep hard cheese | `A02ZH#F27.A02LV$F27.A02MC$F33.A1ANY` | VR - Milk |
| Pork spreadable cooked sausage | `A025K#F04.A01RG$F04.A01VA$F04.A01XJ$F33.A1ANS` | VR - Pigs |
| Smoked salmon | `A02KF#F33.A1ANX` | VR - Aquaculture |
| Egg powder | `A031X#F33.A1ANZ` | VR - Eggs |
| Chicken sausage | `A024G#F33.A1ANV` | VR - Poultry |
| Beef sausage | `A024G#F33.A1ANP` | VR - Bovines |

(ChemMon 2026 pp. 37-38)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p. 33 -->
## Wild Game

- **`F21.A07RY`** ("Wild, gathered or hunted") must always be added for samples related to wild animals (p. 33; Table 4, p. 47, says it "should be used to identify wild game"). (ChemMon 2026 pp. 33, 47)
- Regulation (EU) 2022/1644 and 2022/1646 **no longer consider Wild Game as a VMPR Product Category**, except for results of the national risk-based control plan for third countries (Plan 3). (ChemMon 2026 p33)
- The samples are still classified as Wild Game and are included in the VMPR National Report, but are **not considered** for the VMPR EU Annual Report except for results of that plan. (ChemMon 2026 p33)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 36-37 -->
## Insects as Novel Food

Regulation (EU) 2022/1646 introduces three new VMPR product categories: insects, reptiles and casings (for reptile and casing coding see [[ssd2-matrix-vmpr-coding]]). Only **four insects** are authorised as novel food in the EU, and only those can be reported to EFSA (as frozen/whole animal, dried and/or powdered):
- *Tenebrio molitor*
- *Locusta migratoria*
- *Acheta domesticus*
- *Alphitobius diaperinus*

(ChemMon 2026 p36)

### Worked Example -- Insects

- Migratory locust, powdered: `A16XE#F01.A16VP$F28.A07LA` (base term Edible insect adults; F01 Migratory locust; F28 Grinding/milling/crushing) (ChemMon 2026 p37)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 85, 129 -->
## Baby Food Exclusion

Baby food samples are **excluded** from the VMPR Annual Report: CHEMON63 (Error) does not allow `progLegalRef` `N371A` when `sampMatCode` is under `A03PZ`. (ChemMon 2026 p85; Table 10 p. 129)

See [[baby-food-reporting]] for full baby food rules.

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p. 71 -->
## Result Types

`resType` (mandatory, `VALTYP` catalogue) examples from the guidance:

| Code | Meaning |
| --- | --- |
| `VAL` | The result can be quantified at a validated level and `resVal` is reported. |
| `CCA` | The residue can be quantified but is below the reported value for CCalpha. |
| `LOQ` | The residue is below the LOQ. |
| `LOD` | The residue is below the LOD and `resLOD` is reported. |
| `BIN` | The result of a qualitative screening test. |
| `CCB` | The residue cannot be detected and CCbeta is reported. |

VMPR-specific cases (ChemMon 2026 p71):

- If the residue cannot be quantified and CCalpha is reported, `resType` = `CCA` must be reported; if `resLOQ` is reported and is below CCalpha, `LOQ` should be reported when the result is below `resLOQ`.
- For qualitative screening results the expected `resType` is `BIN` (with `resQualValue` = `NEG` and `resVal` blank), with detection capability reported in CCbeta, or alternatively the LOD in `resLOD`.
- For positive screening results, report the quantitative confirmatory test results, not binary positive screening results.

See [[ssd2-result-value-and-type]] for the full element guidance.

## VMPR-Specific Business Rules

The following business rules apply specifically to the VMPR domain:

- **CHEMON96** (Error from 2026): for VMPR results with `progType` `K005A`, `sampStrategy` can only be `ST10A`, `ST20A`, `ST30A` or `ST90A`. (ChemMon 2026 Table 10 p. 137)
- **CHEMON100** (Warning, new 2026; becomes an Error in 2027): for VMPR results, `evalCode` can only be `J002A`, `J003A`, `J029A`, `J031A`, `J041A` or `J040A`. (ChemMon 2026 Table 10 p. 138)
- **CHEMON102** (Warning, new 2026; becomes an Error in 2027): for VMPR records with the same `sampEventId`, `repCountry`, `sampCountry`, `sampArea`, `origCountry`, `origArea`, `origFishAreaCode`, `origFishAreaText`, `procCountry` and `procArea` should be constant. (ChemMon 2026 Table 10 p. 139)

See [[business-rules]] for the full rule catalogue.

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p. 52 -->
## Worked Examples

### Urine from dairy cow
- Code: `A0C60#F01.A0C9L$F02.A0CET$F31.A0C8V`
- `A0C60` is the non-food matrix base term. F01 `A0C9L` identifies the source animal (dairy cow), F02 `A0CET` the matrix (urine, as part nature), and F31 `A0C8V` the animal age class (printed as "Young non-adult mammal (above 1 year)"). (ChemMon 2026 p52)
- Source discrepancy: in the same p. 52 example the split-element lines print `sampMatCode.source` `A057F`, `sampMatCode.part` `A0F0Y` and `sampMatCode.animal-age-class` `A0F0Y`, which do not match the facets in the full code (`A0C9L`, `A0CET`, `A0C8V`). The guidance does not say which is right; see [[foodex2-in-chemmon]]. (ChemMon 2026 p52)

### Sheep for meat production, blood serum
- Code: `A0C60#F01.A0CDE$F02.A0CEY` (ChemMon 2026 p52)

### Royal jelly
- Code: `A0CVG` (base term only). (ChemMon 2026 p52)
