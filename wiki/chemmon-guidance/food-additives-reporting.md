---
title: "Food Additives and Flavourings Reporting"
select_when: "Identify which FA/FF path applies: SSD2 analytical results, no-presence records, or aggregated use levels. Compare field names and requirement strength before choosing a detailed model page."
type: "domain-guide"
domain: "additives"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[foodex2-facets-state-process]]"
  - "[[foodex2-facets-packaging-consumer]]"
  - "[[foodex2-facets-legislative-descriptive]]"
  - "[[business-rules]]"
  - "[[business-rules-additives]]"
  - "[[fa-ff-no-presence-data-model]]"
  - "[[fa-ff-use-levels-data-model]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[ssd2-evaluation-conclusions]]"
  - "[[legal-limits-database]]"
  - "[[data-validation-and-acceptance]]"
  - "[[contaminant-reporting]]"
  - "[[baby-food-reporting]]"
source_pages:
  - "ChemMon 2026 pp. 12-16 (main changes introduced for the 2026 collection)"
  - "ChemMon 2026 p. 32 (sampling date and legal limits)"
  - "ChemMon 2026 pp. 38-40, 42 (FA/FF sample coding and examples)"
  - "ChemMon 2026 p. 51 (Table 4, F33)"
  - "ChemMon 2026 pp. 61, 63, 66, 70 (sums, paramText, LOD, exprResType)"
  - "ChemMon 2026 pp. 76, 78-79 (evalInfo.conclusion, evalInfo.restrictionException)"
  - "ChemMon 2026 p. 96 (Table 8, FA/FF occurrence)"
  - "ChemMon 2026 pp. 121, 133-135, 140-143 (Table 10)"
  - "ChemMon 2026 p. 144 (Table 11, CONCLUS)"
  - "No-presence 2026 pp. 4-5, 8-9, 11, 16 (Table 1), 19-21 (Table 3)"
  - "Use-levels 2026 pp. 4-5, 7, 9-10, 13, 18, 20 (Table 1), 24-28 (Table 3)"
last_updated: "2026-11-12"
---

# Food Additives and Flavourings Reporting

<!-- Source: Use-levels 2026 pp. 4-5; No-presence 2026 pp. 4-5 (both cite Commission Recommendation (EU) 2023/965) -->

## FA/FF data collection paths

FA/FF intake monitoring uses **three parallel data-collection paths**, all submitted through the EFSA DCF but with distinct data models and business rules. The supplied guidance, citing Commission Recommendation (EU) 2023/965, says MS should collect at least one of (a) analytical data or (b) use levels. MS may also collect (c) presence data, i.e. data on the presence or the absence of a specific FA/FF in a foodstuff: presence data alone is "not sufficient", but "it is recommended to also collect presence data". (No-presence 2026 p4; Use-levels 2026 p4) Pick the path by what you are reporting, not by the substance:

| Path | Granularity | Data model | Rule prefix | Wiki page |
|---|---|---|---|---|
| Analytical (measured concentrations) | Sample level | **SSD2** ChemMon | `CHEMON…`, `GBR…`, `LL_…FA_FF` | this page + [[business-rules-additives]] |
| Use levels (industry-reported min/typ/max) | Product-category level | Separate (**not** in SSD2) | `USE…`, `USE_LLDB…` | [[fa-ff-use-levels-data-model]] |
| No-presence (FA/FF not on label / not added) | Sample level | SSD2-*derived* but separate | `PRE…` | [[fa-ff-no-presence-data-model]] |

Key framing rules across the three paths:

- Positive presence with a measured concentration → SSD2 analytical (this page). The no-presence DM rejects a positive presence, `C19A` or `C05A` (PRE06, Error; No-presence 2026 p19).
- Category-level use levels reported by industry → use-levels DM. SSD2 cannot represent category-level aggregates, so use-levels is a parallel schema, not an SSD2 extension.
- Sample-level "FA/FF not used here" without an analytical measurement → no-presence DM. SSD2 cannot carry standalone negatives, so the no-presence DM was added to close that gap.
- The three paths share FA/FF catalogue families (`LEGREF`, `PARAM`, `ADDFOOD`, `CONCLUS`). `FUNC` (`functionOf`) is used only by the two parallel data models; the ChemMon guidance has no such element or catalogue. (No-presence 2026 p16; Use-levels 2026 p20) Preserve each collection’s hierarchy restrictions.
- Source discrepancy (CONCLUS hierarchy name): ChemMon p. 76 prints `fa_ff`, whereas ChemMon Table 11 (p. 144) and both parallel guides (No-presence p. 11; Use-levels p. 13) print `faff`. The matching `C19A`/`C20A`/`C05A` codes and examples establish the same concept family; do not infer software aliases from the spelling difference.

The remainder of this page covers the **analytical (SSD2)** path. For the other two, follow the links above.

## Shared rule anchors across the three FA/FF paths

Some rule families are shared in concept but not in severity or exact field placement. The important distinctions are:

| Topic | SSD2 analytical | No-presence DM | Use-levels DM |
| --- | --- | --- | --- |
| Presence / conclusion field | `evalInfo.conclusion` is highly recommended, Warning (`CHEMON87`) and uses the FA/FF CONCLUS codes (source spelling `fa_ff`; see [[ssd2-evaluation-conclusions]]) | `presenceAdded` is mandatory and fixed to `C20A` only (`PRE06`, `PRE10`) | `presenceAdded` is mandatory and accepts `C19A`, `C20A`, `C05A`, plus valid combinations (`USE09`, `USE18`, `USE19`) |
| Legislative class (`F33`) | Mandatory for FA/FF (`CHEMON39`) | Mandatory if not implicit (`PRE08`); explicit duplicate F33 only warns (`PRE15`) | Mandatory if not implicit (`USE16`); explicit duplicate F33 is an Error (`USE23`) |
| Physical state (`F03`) | Highly recommended, Warning (`CHEMON86`), for the ChemMon list, which names all of category 1 "Dairy products and analogues" | Required, Error (`PRE09`), for a narrower list: see below | Required, Error (`USE17`), for the same narrower list as `PRE09` |
| Target consumer (`F23`) | Highly recommended, Warning (`CHEMON89`), for category 13; "should be added" for infants (<12 months) (p. 39) | Required when F33 = 13 (`PRE02`) | Required when F33 = 13 (`USE03`) |
| Limit comparison date | Analytical legal-limit checks use the sampling date (ChemMon 2026 p32) | No separate LLDB layer in this DM | LLDB checks use the marketing date (`USE_LLDB01`, `USE_LLDB02`; Use-levels 2026 pp. 7, 18) |
| Authorisation of the substance in the category with the restriction/exception | Warning (`LL_03_FA_FF`) | No rule | Error (`USE_LLDB01`); the rule description is worded the same as `LL_03_FA_FF` |
| Value against the MPL | Warnings on the consistency of `evalCode` with `resVal` against the MPL (`LL_01_FA_FF`, `LL_02_FA_FF`); a `resVal` above the MPL is not itself rejected | No rule | Errors when the maximum use level is greater than the MPL: the MPL reported by the data provider (`USE27`) and the MPL from the LLDB (`USE_LLDB02`) |

(ChemMon 2026 Table 10 pp. 121, 133-135, 142-143; No-presence 2026 Table 3 pp. 19-21; Use-levels 2026 Table 3 pp. 24-28)

The F03 category lists are not the same. `CHEMON86` and ChemMon p. 38 list "1 - Dairy products and analogues" as a whole (list under "F03 physical state" below). `PRE09` and `USE17` list only these dairy subcategories: 01.5 Dehydrated milk, 01.6 Cream and cream powder, 01.8 Dairy analogues including beverage whiteners, 01.9 Edible caseinates, 01.10 Milk-based drinks and similar products intended for young children. Cheese (01.7), for example, is in the ChemMon list but not in the `PRE09`/`USE17` list. The other entries (06.3, 12.5, 12.6, 13, 14.1.2, 14.1.3, 14.1.4, 14.1.5, 17) are in all three lists. (ChemMon 2026 pp. 38, 133-134; No-presence 2026 p20; Use-levels 2026 p26)

Use [[controlled-terminology-catalogues]] for the shared catalogue layer, [[legal-limits-database]] for the date-driven limit logic, and [[data-validation-and-acceptance]] for the common DCF submission flow.

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 73, 148 -->
## Scope

- Food additives and flavourings form two of the five [[chemmon-overview|ChemMon]] reporting domains. (ChemMon 2026 p148)
- Food additives are regulated under Regulation (EC) No 1333/2008. (ChemMon 2026 p73)
- Food flavourings are regulated under Regulation (EC) No 1334/2008. (ChemMon 2026 p73)
- Matrix coding follows [[foodex2-in-chemmon]] rules. Validation is enforced by [[business-rules-additives]] and [[business-rules-cross-cutting]]. Some substances overlap with [[contaminant-reporting]] (e.g., naturally occurring substances with dual classification).

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 38-39, 42, 51, 96 -->
## Analytical (SSD2) path: matrix expectations

- **F33 (Legislative classes)**: "For food additives and flavourings, it is mandatory to report the legislative class facet code (F33)"; if it is not implicitly assigned it must be added. See [[foodex2-facets-legislative-descriptive]]. (ChemMon 2026 pp. 38, 42)
- Source discrepancy (F33 for flavourings): pp. 38 and 42 say mandatory for both domains, and CHEMON39 is an Error for food additives and food flavourings (Table 10 p. 121). Table 4 says "Required" for additives but "Recommended" for flavourings (p. 51). Table 8 gives the flavourings status as "Mandatory" yet says that if F33 is not implicitly assigned "it is recommended to add it" (p. 96). Validation enforces the Error.
- **F03 (Physical state)**: highly recommended, if not implicitly assigned, for the legislative categories listed below (CHEMON86, Warning). See [[foodex2-facets-state-process]]. (ChemMon 2026 pp. 38-39; Table 10 p. 133)
- **F23 (Target consumer)**: highly recommended when the sample refers to food category 13 (CHEMON89, Warning); if the sample is formulated for infants (<12 months), F23 "should be added" if it is not implicitly assigned. See [[foodex2-facets-packaging-consumer]] and [[baby-food-reporting]] for baby food classification and domain routing. (ChemMon 2026 p39; CHEMON89, Warning, Table 10 p. 135)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 38-39 -->
### F33 legislative class: implicit vs explicit

For additives and flavourings, the **legislative food category facet (F33) must always be present**. "In some cases" F33 is already pre-assigned in the reporting hierarchy of the FoodEx2 browser (p. 38; p. 42 says "in most of the cases"); if it is not implicitly assigned, it must be added explicitly. (ChemMon 2026 pp. 38, 42)

The legislative category **"All categories of foods" is not allowed** to be reported for additives/flavourings. (ChemMon 2026 p38)

<!-- Source: ChemMon 2026 pp. 38-39 -->
### F03 physical state: where it matters for additives/flavourings

If F03 is not implicitly assigned, it is highly recommended to add it (p. 39) for samples in these legislative food categories/subcategories (list on p. 38):

- 1 — Dairy products and analogues
- 6.3 — Breakfast cereals
- 12.5 — Soups and broths
- 12.6 — Sauces
- 13 — Foods intended for specific groups (Regulation (EU) No 609/2013)
- 14.1.2 — Fruit juices and vegetable juices (Directive 2001/112/EC)
- 14.1.3 — Fruit/vegetable nectars and similar products (Directive 2001/112/EC)
- 14.1.4 — Flavoured drinks
- 14.1.5 — Coffee/tea/herbal infusions and similar "hot beverages"
- 17 — Food supplements (Directive 2002/46/EC), excluding supplements for infants and young children

If the sample is formulated for **infants (<12 months)**, the target-consumer facet (F23) should be added if it is not implicitly assigned. (ChemMon 2026 p39)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 12, 61, 70 -->
## Expression Type

- `exprResType` should be reported for food additives and food flavourings, "as it became mandatory in 2025 and 2026 respectively"; if not reported, the system returns an error message (CHEMON84_a, Error). Source discrepancy: Table 1 says "From warning to error message in 2026" for additives and flavourings together (p. 12), while Table 10 says "It becomes an Error for food flavourings in 2026" (p. 133) and p. 70 says it became mandatory in 2025 for additives and 2026 for flavourings. (ChemMon 2026 pp. 12, 70, 133)
- For food additives, the analytical result for the individual substances must be reported expressed as specified in Regulation (EC) No 1333/2008, e.g. sorbic acid-sorbates expressed as the free acid. (ChemMon 2026 p61)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 61, 63, 66, 140 -->
## Result Reporting

- For food additives, `paramText` must be filled in as “Expressed as free acid” or “Expressed as salt” when the food additives are regulated as groups (e.g. sorbic acid and sorbates). If the information is not provided, the analytical value will be considered expressed as free acid. (ChemMon 2026 p63)
- CHEMON106 (Warning, Table 10 p. 140) checks this only for potassium sorbate (`RF-00000248-ADD`): `paramText` should specify “Expressed as free acid” or “Expressed as salt”. No rule checks the other grouped additives; see [[ssd2-analysis-parameter-coding]].
- The field prose p. 66 recommends LOD for FA/FF binary negative results generally. CHEMON107 (Table 10 p. 140) specifically warns for six named parameters, including potassium sorbate, when `resType=BIN` and `resQualValue=NEG`; see [[business-rules-additives]] for the complete list.
- Additionally, the sum should be reported if it complements the individual substance, as the maximum permitted levels (MPLs) are regulated at the sum level for the reported legislative category. (ChemMon 2026 p61)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 11-16, 121, 133, 140-141 -->
## Key Business Rules

| Rule | Description | Status |
| --- | --- | --- |
| CHEMON39 | `sampMatCode.legis` (F33) must carry the food category code under Regulations (EC) No 1333/2008 and 1334/2008 (Error, p. 121) | Merged 2026 |
| CHEMON84_a | `exprResType` (expression of result type) must be reported (Error, p. 133) | Amended 2026: becomes an Error for food flavourings (Table 10 p. 133); additives since 2025 (p. 70) |
| CHEMON86 | Physical-state facet (F03) highly recommended for the listed categories (Warning, p. 133) | Amended 2026 |
| CHEMON106 | Potassium sorbate `paramText` recommendation (Warning) | New 2026 |
| CHEMON107 | LOD recommendation for six named parameters with BIN/NEG | New 2026 |
| CHEMON108 | `A047N`, `A047Q`, `A047R`, `A047A`, `A047P` and `A0F3T` (the additive/colour/flavouring terms themselves) cannot be reported as `sampMatCode` (Warning, p. 140) | New 2026 |
| CHEMON109 | If `sampMatCode` has an implicit additive/flavouring F33, the explicit F33 is not needed (Warning, p. 141) | New 2026 |

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 16, 142-143 -->
## Legal Limit Rules (New 2026)

| Rule | Purpose |
| --- | --- |
| LL_01_FA_FF | If `resType` is `VAL`, `evalLimitType` is `W016A` (MPL) or not reported, and `resVal` is greater than the MPL, `evalCode` should be different from `J002A` or `J037A` |
| LL_02_FA_FF | Same conditions with `resVal` less than or equal to the MPL: `evalCode` should be different from `J003A` and `J038A` |
| LL_03_FA_FF | The substance (`paramCode`) should be authorised in this legislative category with this restriction/exception according to Regulations 1333/2008 and 1334/2008 |

All three are Warnings. (ChemMon 2026 Table 10 pp. 142-143)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 39-40 -->
## Worked Examples

| Product | FoodEx2 Code | Notes |
| --- | --- | --- |
| Soft-ripened cheese, sliced | `A02RH#F03.A06JA` | ChemMon 2026 p39 prints `A02RH#F03.A06JA$F33.A0C5F` as the correct code. Wiki note (not in the guidance): the code shown here drops the explicit F33 because F33.A0C5F (FA-01.7.2 Ripened cheese) is implicit in the locally checked MTX 17.2 snapshot, as the parallel guides also list it (No-presence 2026 p9; Use-levels 2026 p9); check your catalogue release before dropping the explicit F33. Add F03 only for the known sliced state. See version note below. |
| Wine, red | `A03MX` | Implicit F33=FA-14.2.2 Wine and products (ChemMon 2026 p39; also No-presence p8, Use-levels p9) |
| Omelette, plain | `A03YN#F33.A0C33` | Explicit F33=FA-10.2 Processed eggs and egg products (ChemMon 2026 p40, printed there as `A03YN# F33.A0C33`; also No-presence p9, Use-levels p9) |
| Infant formula milk/soya-based liquid | `A03QH` | Implicit F33=FA-13.1.1 Infant formulae (ChemMon 2026 p40; also No-presence p8, Use-levels p9) |
| Vitamin supplements syrup | `A03SL#F03.A1B1Y$F33.A0C15` | FA-17.2 supplements liquid form; A1B1Y is the syrup-type code (ChemMon 2026 p40; also Use-levels pp. 9-10; not in the No-presence guide) |
| Tea leaves, dry | `A04KK#F03.A0CEA` | Use-levels guide only: explicit F03 = Solid; implicit F33 = "14.1.5.2 Other" (Use-levels 2026 p9) |

**Cheese version note:** ChemMon p. 39 prints an explicit F33 for A02RH, while
both parallel FA/FF guides p. 9 list it as implicit. The cheese row above uses
the locally checked MTX 17.2 snapshot; [[foodex2-in-chemmon]] records the
discrepancy, query provenance and limits. Other rows reproduce the supplied
2026 guidance examples and are not a validation against every catalogue release.

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 78-79 -->
## Restriction/Exception

- `evalInfo.restrictionException` (N.06.4, optional) should be used to provide the restrictions/exceptions described in Regulation (EC) No 1333/2008 for each authorised food additive; it can also be used for food flavourings in line with Regulation (EC) No 1334/2008. (ChemMon 2026 p78)
- Codes need to be selected from the `ADDFOOD` catalogue; the most detailed code that defines the restriction/exception should be chosen. (ChemMon 2026 p78)
- The same substance can be authorised for the same legislative category at different MPLs depending on the restriction/exception, so the element helps identify the correct MPL. A warning is raised when the reported combination (substance, category, restriction/exception) is not authorised. (ChemMon 2026 p79)
- Examples: `ADD00197A` (mozzarella cheese analysed for lactic acid), `ADD00386A` (milk chocolate analysed for citric acid), `ADD00622A` (processed fish analysed for ascorbic acid), `ADD00881A` (no restrictions/exceptions to be reported). (ChemMon 2026 p79)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p. 76 -->
## Conclusion Reporting

- `evalInfo.conclusion` is highly recommended. (CHEMON87, Warning; ChemMon 2026 p76, Table 10 p. 134)
- Indicates whether the food additive or flavouring was on the label/added (`C19A`) or not (`C20A`), or is of natural occurrence (`C05A`). (ChemMon 2026 p76)
- Multiple conclusions may apply; for example, ascorbic acid added as a food additive and also naturally occurring: `C19A$C05A`. More examples are on [[ssd2-evaluation-conclusions]]. (ChemMon 2026 p76)
