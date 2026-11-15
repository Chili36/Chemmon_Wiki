---
title: "FA/FF No-presence Data Model"
select_when: "No-presence FA/FF records: sampId/sampMatCode, presenceAdded, sampling date, PRE rules and PRE15 warning. Use for this collection, not SSD2 results or use levels."
type: "reference"
domain: "additives"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf"
source_pages:
  - "pp. 4-21 (Sections 1-3, Figure 1 p. 14, Tables 1-3 pp. 15-21)"
related:
  - "[[food-additives-reporting]]"
  - "[[fa-ff-use-levels-data-model]]"
  - "[[business-rules-additives]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[data-validation-and-acceptance]]"
  - "[[foodex2-in-chemmon]]"
---

# FA/FF No-presence Data Model

<!-- Source: EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf, Section 2 -->

## What this DM is for

The **no-presence DM** is a sample-level data model for reporting that a specific food additive or food flavouring (FA/FF) has **not** been used in a given sample. It is SSD2-*derived* — element names and catalogues align with SSD2 — but is **a separate data model** because standalone negative data cannot be represented in SSD2 itself. (No-presence 2026 pp. 4-5)

- Use this DM **only** for negative reports ("FA/FF not on label / not added"). Positive presence is not accepted here (PRE06, PRE10) and "should always be submitted together with analytical/use levels". (No-presence 2026 p11; Table 1 p16; PRE06 pp. 19-20)
  - **Source discrepancy:** p5 names one route only — positive presence "should be submitted to EFSA using the SSD2 format together with an analytical measurement" — while p11, Table 1 (p16) and PRE06 (pp. 19-20) say an analytical **or use-level** value in another data model. PRE06 enforces only that positive presence is not reported in this DM; it does not settle which other DM.
- Presence data alone are **not sufficient**. The guidance, citing Commission Recommendation (EU) 2023/965, says MS **should** collect at least one type of occurrence data — analytical data (SSD2) or use levels ([[fa-ff-use-levels-data-model]]) — and **may also** collect presence data; "it is **recommended** to also collect presence data to identify whether a FA/FF is used or not used in a particular foodstuff". (No-presence 2026 p4)
- **Who sends data:** national food authorities, research institutions, academia, food business operators and other interested stakeholders can designate experts. An expert is nominated as Data Provider (DP, sends data through the DCF with EFSA credentials) and/or Data Validator (DV, accepts or rejects the data in MicroStrategy); several experts from one stakeholder can be nominated. (No-presence 2026 p13)
- **Flow:** each DP shall compile the data in the Excel reporting tool for no-presence data (Zenodo DOI 10.5281/zenodo.14893698), export it to XML and upload it to the EFSA DCF. The DCF checks the schema and the business rules and shows a dataset status; only datasets in status 'Valid' or 'Valid with warnings' can be submitted to the sDWH; the DV then sets 'Accepted' or 'Rejected' in MicroStrategy and submits that final status. The dataset statuses and the ack, replace and acceptance steps are on [[data-validation-and-acceptance]]. (No-presence 2026 p13; Figure 1 p14)

## Fast routing

- Use this DM when the statement is: "for this sampled food, this FA/FF is **not** on the label / not added", and there is **no** analytical result to report.
- Do **not** use this DM for positive presence. A positive finding belongs either in the SSD2 analytical path ([[food-additives-reporting]]) or, if the report is category-level rather than sample-level, in the use-levels DM ([[fa-ff-use-levels-data-model]]).
- If the question is about sample-level identifiers, sampling date, or `sampMatCode`, this page is the right FA/FF parallel path. If it is about `prodId`, marketing date, or min/typical/max levels, it is the use-levels page instead.

## Why a separate DM

<!-- Source: No-presence 2026 pp. 4-5 -->

- SSD2 is structured around measured analytical values. A record that says "this FA/FF is not used here" without an accompanying analytical measurement cannot be represented.
- The no-presence DM fills that gap. The DM "is in accordance with the harmonised terminology of EFSA and, where applicable, with the terminology used in the EFSA Standard Sample Description (SSD2)" (No-presence 2026 p5). Wiki note (not in the guidance): element names such as `progLegalRef`, `sampMatCode`, `paramCode` and `resId` are shared with SSD2; others, such as `functionOf`, are not.
- The DM "has been already piloted in 2025, and it will be piloted in 2026". The element set in this page reflects the **2026** version, which was adjusted and improved after the result of the 2025 pilot was assessed. (No-presence 2026 pp. 4-5)

## Fast constraints

The highest-signal constraints for retrieval are:

- `presenceAdded` is fixed to **`C20A` only** in this DM. `C19A` and `C05A` are out of scope here and must move to another reporting path. (`PRE06`, `PRE10`)
- `sampId` identifies the sampled food across multiple FA/FF records; `(paramCode, sampId)` must stay unique. (`PRE11`, `PRE12`)
- `F33` is always required on `sampMatCode`; `F03` and `F23` become conditional requirements from the reported legislative category. (`PRE02`, `PRE08`, `PRE09`)
- `functionOf` is required only for the additive domain (`progLegalRef=N112A`). (`PRE07`)
- `paramCode` and `restrictionException` are domain-routed: additive records must use `addAnalysis` + `FARestExc`; flavouring records must use `flavAnalysis` + `FFRestExc`. (`PRE03`, `PRE04`, `PRE13`, `PRE14`)

## Data elements

<!-- Source: No-presence 2026 Section 2 (pp. 6-12); Table 1 (pp. 15-16) -->

Table 1 contains **18 named elements**, described in 16 field sections because
the three date components share §2.6. They are submitted at sample level. A
single `sampId` may carry multiple records (different substances), but the
sample-identifying fields below must stay constant per `sampId` (PRE11).

### Programme identification

- `progLegalRef` (mandatory, `LEGREF.faff`) — legal framework. Only two codes allowed: `N112A` for food additives (Reg. 1333/2008), `N113A` for food flavourings (Reg. 1334/2008). (No-presence 2026 p6)
- `sampId` (mandatory, ≤100 chars, no special characters) — sample identifier. The same `sampId` must appear on every record that describes the same physical sample (e.g. one record per substance). Example: `IT_2026_mozzarella`. (PRE11) (No-presence 2026 p6)

### Provenance and timing

- `repCountry` (optional, `COUNTRY`, 2 chars) — reporting country; populated by EFSA from the reporting organisation if omitted. (No-presence 2026 p6; Table 1 p15)
- `sampCountry` (mandatory, `COUNTRY`, 2 chars) — ISO 3166-1 alpha-2 country where the sample was taken, e.g. `ES`. (No-presence 2026 p6; Table 1 p15)
- `repYear` (optional, integer, 4 digits) — if reported, must equal the current data collection year (PRE16), e.g. `2026` during the 2026 data collection. (No-presence 2026 p7; Table 1 p15)
- `sampY`, `sampM`, `sampD` (all mandatory; integers of 4, 2 and 2 digits) — sampling year/month/day. `sampY` must equal the data collection year minus one (PRE01), e.g. `2025` in the 2026 pilot. The combined date must be valid (PRE17). If sampling spans a period, report the start date. (No-presence 2026 p7; Table 1 p15)

### Matrix description

- `sampMatCode` (mandatory, `MTX`/FoodEx2, type `xs:compoundType`) — FoodEx2 base term plus required facets; see [[foodex2-in-chemmon]] for base-term selection and the full facet list. (No-presence 2026 p7; Table 1 p15)
  - **F33 (legislative class)** must always be present, implicitly or explicitly (PRE08), and "must be reported for both domains, additives and flavourings". PRE15 warns if both implicit and explicit F33 are given — drop the explicit one. The category "All categories of foods" must not be reported. Example with an explicit F33: `A03YN#F33.A0C33` (Omelette, plain; FA-10.2 Processed eggs and egg products); examples where the base term alone is correct because F33 is implicit: `A03QH`, `A03MX`, `A02RH`. (No-presence 2026 pp. 7-9)
  - **F03 (physical state)** must be explicitly added if not implicitly assigned, for legislative categories: 01.5 dehydrated milk, 01.6 cream and cream powder, 01.8 dairy analogues (incl. beverage whiteners), 01.9 edible caseinates, 01.10 milk-based drinks for young children, 06.3 breakfast cereals, 12.5 soups and broths, 12.6 sauces, 13 foods for specific groups, 14.1.2 fruit/vegetable juices, 14.1.3 fruit/vegetable nectars, 14.1.4 flavoured drinks, 14.1.5 coffee/tea/herbal infusions, 17 food supplements (excluding supplements for infants and young children). (PRE09) (No-presence 2026 pp. 7-8)
  - **F23 (target consumer)** must be added when the reported legislative category is **13** (foods intended for particular nutritional uses under Directive 2009/39/EC). (PRE02) (No-presence 2026 p8; Table 3 p19)
- `sampMatText` (optional, ≤400 chars) — free-text matrix description; defaults to the text associated with `sampMatCode` if empty. (No-presence 2026 p9)
- `sampMatInfo.brandName`, `sampMatInfo.manuf` (both optional, ≤250 chars) — brand and manufacturer of the sample. (No-presence 2026 p10)

### Restriction / exception

- `restrictionException` (mandatory, `ADDFOOD`) — restriction or exception from Reg. 1333/2008 (additives) or 1334/2008 (flavourings). Select from `FARestExc` if `progLegalRef=N112A`, or `FFRestExc` if `progLegalRef=N113A`, per PRE03/PRE04. Use the **most detailed** code that applies. If none applies, report `ADD00881A` ("No restriction/exception to report"). Worked examples: `ADD00197A` only mozzarella (lactic acid no-presence in 01.7.1), `ADD00386A` only milk chocolate (citric acid in 05.1), `ADD00622A` only tuna (ascorbic acid in 09.2). (No-presence 2026 pp. 9-10)

### Parameter

- `paramCode` (mandatory, `PARAM`) — substance code. Must belong to `addAnalysis` when `progLegalRef=N112A` (PRE13), or `flavAnalysis` when `progLegalRef=N113A` (PRE14); PRE05 is the overall scope rule. To report multiple substances for the same physical sample, add new records with the same `sampId` but different `resId`. Examples: `RF-00000019-ADD` (acetic acid), `RF-00004837-PAR` (1-butanol). (No-presence 2026 p10)
- `paramText` (optional, ≤400 chars) — substance name; populated by EFSA from `paramCode` if empty. (No-presence 2026 p10)

### Result

- `resId` (mandatory, ≤100 chars) — must be provided for every record and be unique across all data collections from the same DP; it is also used for communication between EFSA and the DP during transmission and validation. It is **recommended** to include prefixes or suffixes so the `resId` is unique within a DP, e.g. `FI_FALab2026_0006754`. The combination `(paramCode, sampId)` must also be unique (PRE12). (No-presence 2026 p11)
- `presenceAdded` (mandatory, `CONCLUS.faff`) — **only `C20A` ("No, not present on label/not added") is accepted in this DM.** Report it when the FA/FF "is not reported on the label or there is evidence of not being used". Positive presence (`C19A` "Yes, present on label/added", or `C05A`) is not valid here (PRE06, PRE10) — it "should always be submitted together with analytical/use levels" in another data model (see the source discrepancy under "What this DM is for"). (No-presence 2026 p11; PRE06 pp. 19-20)
  - **Labelling caveat:** the use of a FA should by law be indicated on the label, **except** for FA without a technological role in the final product, e.g. carriers (Article 20 of Regulation 1169/2011), and FA with a nutritional purpose (Regulation 1925/2006); for FF there is **no** legal requirement on labelling. (No-presence 2026 p11)
- `functionOf` (dependent mandatory, `FUNC`) — **required when `progLegalRef=N112A` (additive domain)** (PRE07). Indicates the functional class of the FA; not required for the flavouring domain. Example: `emu` for a food additive belonging to the emulsifiers group. The allowed values are in the FUNC catalogue and those applicable for FA are listed in Table 2, which has **33 classes**: (No-presence 2026 p12; Table 2 pp. 17-18)
  - 27 classes printed with a definition: 1 sweeteners, 2 colours, 3 preservatives, 4 antioxidants, 5 carriers, 6 acids, 7 acidity regulators, 8 anti-caking agents, 9 anti-foaming agents, 10 bulking agents, 11 emulsifiers, 12 emulsifying salts, 13 firming agents, 14 flavour enhancers, 15 foaming agents, 16 gelling agents, 17 glazing agents (including lubricants), 18 humectants, 19 modified starches, 20 packaging gases, 21 propellants, 22 raising agents, 23 sequestrants, 24 stabilisers, 25 thickeners, 26 flour treatment agents, 27 contrast enhancers.
  - 28 "nutrient", printed without a definition.
  - Five Annex III classes: 29 carriers in food additives, 30 food additives other than carriers in food additives, 31 food additives including carriers in food enzymes, 32 food additives including carriers in food flavourings, 33 food additives in nutrients.
  - Table 2 prints class names, not `FUNC` codes; `emu` is the only code the document shows.

## Business rules

<!-- Source: No-presence 2026 pp. 19-21, Table 3 -->

All 17 rules in this DM are prefixed `PRE`. All are currently **Active**. Sixteen are **Error** severity (submission-blocking); PRE15 is the only **Warning**.

| Rule | Severity | What it enforces | Source page |
|---|---|---|---|
| PRE01 | Error | `sampY` = data collection year − 1 | 19 |
| PRE02 | Error | F23 (target consumer) mandatory if F33 is category 13 (foods intended for particular nutritional uses as defined by Directive 2009/39/EC) | 19 |
| PRE03 | Error | If `progLegalRef=N112A`, `restrictionException` ∈ `FARestExc` (or use `ADD00881A`) | 19 |
| PRE04 | Error | If `progLegalRef=N113A`, `restrictionException` ∈ `FFRestExc` (or use `ADD00881A`) | 19 |
| PRE05 | Error | `paramCode` ∈ `addAnalysis` ∪ `flavAnalysis` (PARAM) | 19 |
| PRE06 | Error | Only `C20A` (no-presence) can be reported; positive presence belongs in another DM | 19–20 |
| PRE07 | Error | `functionOf` mandatory when `progLegalRef=N112A` | 20 |
| PRE08 | Error | F33 mandatory on `sampMatCode` if not implicitly assigned | 20 |
| PRE09 | Error | F03 mandatory for the specific legislative categories listed above | 20–21 |
| PRE10 | Error | `presenceAdded` values must be meaningful — `C19A` and `C20A` cannot coexist on one record | 21 |
| PRE11 | Error | `(repCountry, sampCountry, sampY, sampM, sampD, sampMatCode, sampMatInfo.brandName, sampMatInfo.manuf)` must be constant per `sampId` | 21 |
| PRE12 | Error | `(paramCode, sampId)` must be unique | 21 |
| PRE13 | Error | If `progLegalRef=N112A`, `paramCode` ∈ `addAnalysis` | 21 |
| PRE14 | Error | If `progLegalRef=N113A`, `paramCode` ∈ `flavAnalysis` | 21 |
| PRE15 | Warning | If `sampMatCode` has an implicit F33, do not add an explicit F33 | 21 |
| PRE16 | Error | `repYear`, if reported, = data collection year | 21 |
| PRE17 | Error | `(sampD, sampM, sampY)` must be a valid date | 21 |

## Source wording and field details

The complete field sections (§§2.1–2.16), Table 1 and all 17 PRE rows were
compared on 5 October 2026; the whole document (pp. 1–23) was audited again
on 11 November 2026. Catalogue restrictions and mandatory fields still
apply even when they have no separate PRE rule ID.

- **F23:** §2.7 p. 8 recommends it for infant products, while PRE02 p. 19
  makes it mandatory for legislative category 13. The rule reference above
  preserves PRE02's broader condition. Do not narrow it to infants only.
- **PRE17:** both source columns describe the invalid-date failure state.
  The expected passing condition is a valid sampling date, consistent with
  mandatory year/month/day in §2.6.
- `presenceAdded` and `functionOf` are repeatable types in Table 1. Repeatability
  does not permit C19A/C05A here: PRE06 still restricts presence to C20A.
- The source uses occasional shorthand `progLegRef` and `matCode.F33` in its
  rule prose; the declared fields in this model remain `progLegalRef` and
  `sampMatCode`. Do not introduce new submission fields from those spellings.
- Table 1 sizes include `progLegalRef` 5, `restrictionException` 9 and
  `paramCode` 400 characters, alongside the text/identifier sizes above.

## Version-sensitive cheese example

The source's p. 9 example uses `A02RH` (Soft-ripened cheese), with F33
'FA-01.7.2 Ripened cheese' implicit (No-presence 2026 p9). The checked local
MTX 17.2 snapshot agrees and gives the facet code F33.A0C5F. ChemMon's analytical
example p. 39 instead prints an explicit F33: do not copy that duplicate into
this path. PRE15 assigns Warning severity. See [[foodex2-in-chemmon]] for the
version-specific reconciliation and evidence; this does not establish the
catalogue release originally intended by the ChemMon example.

## Pilot substances

<!-- Source: No-presence 2026 p5, footnote 4 -->

The piloting involved three FA and two FF for 2025 and is going to involve two FA and three FF for 2026 (No-presence 2026 p5, footnote 4):

- **2025 pilot**: green S (E 142), tartrazine (E 102), ponceau 4R / cochineal red A (E 124), caffeine (16.016), pulegone (Annex III).
- **2026 pilot**: BHT (E 321), sorbic acid – sorbates (E 200–203), coumarin (Annex III), hydrocyanic acid (Annex III), theobromine (16.032).

Wiki note (not in the guidance): the source lists these two pilot years only and says nothing about later years; check the current EFSA reporting guidance before scoping a submission for another year.

## Relationship to other FA/FF reporting paths

- **SSD2 ChemMon analytical** ([[food-additives-reporting]]) — positive presence together with an analytical measurement goes here, not the no-presence DM. (No-presence 2026 p5)
- **[[fa-ff-use-levels-data-model]]** — category-level industry-reported use levels; parallel to, not a replacement for, sample-level no-presence data.
- Business-rule IDs in this DM (`PRE…`) are a separate namespace from the SSD2 CHEMON rules catalogued under [[business-rules]]; they do not overlap.
