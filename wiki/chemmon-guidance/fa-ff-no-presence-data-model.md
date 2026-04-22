---
title: "FA/FF No-presence Data Model"
type: "reference"
domain: "additives"
last_updated: "2026-04-22"
sources:
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf"
source_pages:
  - "pp. 4-23 (Sections 1-3, Tables 1-3)"
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

- Use this DM **only** for negative reports ("FA/FF not on label / not added"). Positive presence must go through SSD2 analytical reporting together with a measured level. (PRE06, PRE10)
- No-presence reporting is **optional**. Commission Recommendation (EU) 2023/965 requires MS to collect at least analytical data (SSD2) or use levels ([[fa-ff-use-levels-data-model]]); no-presence may be added to identify foodstuffs where a FA/FF is specifically not used. (No-presence 2026 p4)
- Data is submitted via the EFSA DCF using the Excel reporting tool (Zenodo DOI 10.5281/zenodo.14893698), exported to XML. Validation and acceptance follow the same flow as [[data-validation-and-acceptance]]: ack → BR validation → submit to sDWH → accept/reject via MicroStrategy. (No-presence 2026 p13, Figure 1)

## Why a separate DM

<!-- Source: No-presence 2026 pp. 4-5 -->

- SSD2 is structured around measured analytical values. A record that says "this FA/FF is not used here" without an accompanying analytical measurement cannot be represented.
- The no-presence DM fills that gap. Element naming (`progLegalRef`, `sampMatCode`, `paramCode`, `resId`, …) and controlled-terminology catalogues match SSD2 so downstream joins and dietary-exposure calculations remain coherent across both models.
- The DM is piloted annually: the element set in this page reflects the **2026** version, which incorporates changes from 2025 pilot feedback.

## Data elements

<!-- Source: No-presence 2026 Section 2 (pp. 6-12); Table 1 (pp. 15-16) -->

Sixteen elements, all submitted at sample level. A single `sampId` may carry multiple records (different substances), but the sample-identifying fields below must stay constant per `sampId` (PRE11).

### Programme identification

- `progLegalRef` (mandatory, `LEGREF.faff`) — legal framework. Only two codes allowed: `N112A` for food additives (Reg. 1333/2008), `N113A` for food flavourings (Reg. 1334/2008). (No-presence 2026 p6)
- `sampId` (mandatory, ≤100 chars, no special characters) — sample identifier. The same `sampId` must appear on every record that describes the same physical sample (e.g. one record per substance). (PRE11) (No-presence 2026 p6)

### Provenance and timing

- `repCountry` (optional, `COUNTRY`) — reporting country; populated by EFSA from the reporting organisation if omitted. (No-presence 2026 p6)
- `sampCountry` (mandatory, `COUNTRY`) — ISO 3166-1 alpha-2 country where the sample was taken. (No-presence 2026 p6)
- `repYear` (optional) — if reported, must equal the current data collection year (PRE16). (No-presence 2026 p7)
- `sampY`, `sampM`, `sampD` (all mandatory) — sampling year/month/day. `sampY` must equal the data collection year minus one (PRE01). The combined date must be valid (PRE17). If sampling spans a period, report the start date. (No-presence 2026 p7)

### Matrix description

- `sampMatCode` (mandatory, `MTX`/FoodEx2) — FoodEx2 base term plus required facets; see [[foodex2-in-chemmon]] for base-term selection and the full facet list.
  - **F33 (legislative class)** must always be present, implicitly or explicitly (PRE08). PRE15 warns if both implicit and explicit F33 are given — drop the explicit one. The category "All categories of foods" must not be reported. (No-presence 2026 p7)
  - **F03 (physical state)** must be explicitly added if not implicitly assigned, for legislative categories: 01.5 dehydrated milk, 01.6 cream and cream powder, 01.8 dairy analogues (incl. beverage whiteners), 01.9 edible caseinates, 01.10 milk-based drinks for young children, 06.3 breakfast cereals, 12.5 soups and broths, 12.6 sauces, 13 foods for specific groups, 14.1.2 fruit/vegetable juices, 14.1.3 fruit/vegetable nectars, 14.1.4 flavoured drinks, 14.1.5 coffee/tea/herbal infusions, 17 food supplements (excluding supplements for infants and young children). (PRE09) (No-presence 2026 pp. 7-8)
  - **F23 (target consumer)** must be added if the product is formulated for infants (<12 months) in legislative category 13 (Reg. 2009/39/EC). (PRE02) (No-presence 2026 p8)
- `sampMatText` (optional, ≤400 chars) — free-text matrix description; defaults to the text associated with `sampMatCode` if empty. (No-presence 2026 p9)
- `sampMatInfo.brandName`, `sampMatInfo.manuf` (both optional, ≤250 chars) — brand and manufacturer of the sample. (No-presence 2026 p10)

### Restriction / exception

- `restrictionException` (mandatory, `ADDFOOD`) — restriction or exception from Reg. 1333/2008 (additives) or 1334/2008 (flavourings). Select from `FARestExc` if `progLegalRef=N112A`, or `FFRestExc` if `progLegalRef=N113A`, per PRE03/PRE04. Use the **most detailed** code that applies. If none applies, report `ADD00881A` ("No restriction/exception to report"). Worked examples: `ADD00197A` only mozzarella (lactic acid no-presence in 01.7.1), `ADD00386A` only milk chocolate (citric acid in 05.1), `ADD00622A` only tuna (ascorbic acid in 09.2). (No-presence 2026 pp. 9-10)

### Parameter

- `paramCode` (mandatory, `PARAM`) — substance code. Must belong to `addAnalysis` when `progLegalRef=N112A` (PRE13), or `flavAnalysis` when `progLegalRef=N113A` (PRE14); PRE05 is the overall scope rule. To report multiple substances for the same physical sample, add new records with the same `sampId` but different `resId`. (No-presence 2026 p10)
- `paramText` (optional, ≤400 chars) — substance name; populated by EFSA from `paramCode` if empty. (No-presence 2026 p10)

### Result

- `resId` (mandatory, ≤100 chars) — unique across all data collections from the same DP. The combination `(paramCode, sampId)` must also be unique (PRE12). (No-presence 2026 p11)
- `presenceAdded` (mandatory, `CONCLUS.faff`) — **only `C20A` ("No, not present on label/not added") is accepted in this DM.** Positive presence codes (`C19A` present/added, `C05A` natural occurrence) are not valid here (PRE06, PRE10) — report positive presence via the SSD2 analytical DM with an accompanying measured value. (No-presence 2026 p11)
- `functionOf` (dependent mandatory, `FUNC`) — **required when `progLegalRef=N112A` (additive domain)** (PRE07). Identifies the functional class of the additive (emulsifier, preservative, antioxidant, etc.) per Reg. 1333/2008 Annex I — the full list of 28 functional classes plus 5 Annex III carrier/enzyme/flavouring classes is in the FUNC catalogue and reproduced verbatim in the source PDF Table 2. Not required for the flavouring domain. (No-presence 2026 p12; Table 2 at pp. 17-18)

## Business rules

<!-- Source: No-presence 2026 pp. 19-21, Table 3 -->

All 17 rules in this DM are prefixed `PRE`. All are currently **Active**. Sixteen are **Error** severity (submission-blocking); PRE15 is the only **Warning**.

| Rule | Severity | What it enforces |
|---|---|---|
| PRE01 | Error | `sampY` = data collection year − 1 |
| PRE02 | Error | F23 (target consumer) mandatory if F33 is category 13 (foods for specific groups) |
| PRE03 | Error | If `progLegalRef=N112A`, `restrictionException` ∈ `FARestExc` (or use `ADD00881A`) |
| PRE04 | Error | If `progLegalRef=N113A`, `restrictionException` ∈ `FFRestExc` (or use `ADD00881A`) |
| PRE05 | Error | `paramCode` ∈ `addAnalysis` ∪ `flavAnalysis` (PARAM) |
| PRE06 | Error | Only `C20A` (no-presence) can be reported; positive presence belongs in another DM |
| PRE07 | Error | `functionOf` mandatory when `progLegalRef=N112A` |
| PRE08 | Error | F33 mandatory on `sampMatCode` if not implicitly assigned |
| PRE09 | Error | F03 mandatory for the specific legislative categories listed above |
| PRE10 | Error | `presenceAdded` values must be meaningful — `C19A` and `C20A` cannot coexist on one record |
| PRE11 | Error | `(repCountry, sampCountry, sampY, sampM, sampD, sampMatCode, sampMatInfo.brandName, sampMatInfo.manuf)` must be constant per `sampId` |
| PRE12 | Error | `(paramCode, sampId)` must be unique |
| PRE13 | Error | If `progLegalRef=N112A`, `paramCode` ∈ `addAnalysis` |
| PRE14 | Error | If `progLegalRef=N113A`, `paramCode` ∈ `flavAnalysis` |
| PRE15 | Warning | If `sampMatCode` has an implicit F33, do not add an explicit F33 |
| PRE16 | Error | `repYear`, if reported, = data collection year |
| PRE17 | Error | `(sampD, sampM, sampY)` must be a valid date |

## Pilot substance rotation

<!-- Source: No-presence 2026 p5, footnote 4 -->

The no-presence DM is piloted on a rotating substance list:

- **2025 pilot**: green S (E 142), tartrazine (E 102), ponceau 4R / cochineal red A (E 124), caffeine (16.016), pulegone (Annex III).
- **2026 pilot**: BHT (E 321), sorbic acid – sorbates (E 200–203), coumarin (Annex III), hydrocyanic acid (Annex III), theobromine (16.032).

The list rotates annually. Verify the current year's pilot scope against the latest EFSA reporting guidance before scoping a submission.

## Relationship to other FA/FF reporting paths

- **SSD2 ChemMon analytical** ([[food-additives-reporting]]) — mandatory positive presence with measured levels goes here, not the no-presence DM.
- **[[fa-ff-use-levels-data-model]]** — category-level industry-reported use levels; parallel to, not a replacement for, sample-level no-presence data.
- Business-rule IDs in this DM (`PRE…`) are a separate namespace from the SSD2 CHEMMON rules catalogued under [[business-rules]]; they do not overlap.
