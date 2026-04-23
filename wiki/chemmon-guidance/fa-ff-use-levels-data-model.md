---
title: "FA/FF Use-levels Data Model"
type: "reference"
domain: "additives"
last_updated: "2026-04-22"
sources:
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
source_pages:
  - "pp. 4-30 (Sections 1-4, Tables 1-3)"
related:
  - "[[food-additives-reporting]]"
  - "[[fa-ff-no-presence-data-model]]"
  - "[[business-rules-additives]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[legal-limits-database]]"
  - "[[data-validation-and-acceptance]]"
  - "[[foodex2-in-chemmon]]"
---

# FA/FF Use-levels Data Model

<!-- Source: EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf, Section 2 -->

## What this DM is for

The **use-levels DM** collects FA/FF use levels (minimum / typical / maximum concentrations) reported by industry or by MS aggregating industry data, at **food-category** level rather than sample level. Commission Recommendation (EU) 2023/965 accepts either analytical data (SSD2) or use levels as the primary FA/FF intake data source; this DM carries the latter. (Use-levels 2026 pp. 4-5)

- Use levels may be reported as actual/exact (in which case `minLevel`, `typicalLevel`, and `maxLevel` all equal the same value) or as a range. If the substance is not used in the category, all three levels must be 0 (USE09). (Use-levels 2026 pp. 14-15)
- Data is submitted via the EFSA DCF using the Excel reporting tool (Zenodo DOI 10.5281/zenodo.14893177), exported to XML. Validation and acceptance mirror [[data-validation-and-acceptance]]: ack → BR validation → submit to sDWH → accept/reject via MicroStrategy. (Use-levels 2026 p17, Figure 1)

## Fast routing

- Use this DM when the statement is: "for this product category / food on this market date, the substance is used at these min/typical/max levels".
- Do **not** use this DM for a measured sample result. That belongs in the SSD2 analytical path ([[food-additives-reporting]]).
- Do **not** use this DM for a pure negative sample-level statement without levels. That belongs in [[fa-ff-no-presence-data-model]].
- If the question is about `prodId`, `marketCountry`, marketing date, `minLevel` / `typicalLevel` / `maxLevel`, or LLDB checks at marketing date, this is the right FA/FF parallel page.

## Why a separate DM

<!-- Source: Use-levels 2026 p5 -->

- The use-levels DM is **not implemented in SSD2.** SSD2 is designed for sample-level analytical data; the use-levels DM collects category-level aggregates and introduces elements (e.g. `marketCountry`, `minLevel`/`typicalLevel`/`maxLevel`, `conversionOrDilutionFactor`, `maxPermittedLevel`) that have no SSD2 equivalent.
- Terminology and controlled vocabularies are aligned with SSD2 where applicable (`LEGREF`, `PARAM`, `MTX`, `CONCLUS`, `ADDFOOD`, `EXPRRES`, `FUNC`, `UNIT`), so downstream joins with analytical data remain coherent.
- The DM is piloted annually and the 2026 version reflects changes incorporated from 2025 pilot feedback.

## Fast constraints

The highest-signal constraints for retrieval are:

- This is a **product-category** model keyed by `prodId`, not a sample-level model keyed by `sampId`.
- `presenceAdded` accepts `C19A`, `C20A`, and `C05A`, including meaningful combinations such as `C19A$C05A` and `C20A$C05A`. `C19A` and `C20A` cannot coexist. (`USE09`, `USE18`, `USE19`)
- `F33` is always required on `matCode`; `F03` and `F23` become conditional requirements from the reported legislative category. (`USE03`, `USE16`, `USE17`, `USE23`, `USE24`)
- `functionOf` is required only for additive-domain records (`progLegalRef=N112A`). (`USE10`)
- `weight`, `fatPerc`, `moistPerc`, `unit`, `conversionOrDilutionFactor`, and the three level fields are the part of this DM that has no SSD2 equivalent. (`USE11`-`USE15`, `USE25`)
- LLDB checks here are driven by the **marketing date**, not sampling date. (`USE_LLDB01`, `USE_LLDB02`)

## Data elements

<!-- Source: Use-levels 2026 Section 2 (pp. 6-16); Table 1 (pp. 19-21) -->

Twenty-nine elements, reported per product category × substance. The combination `(paramCode, prodId)` must be unique (USE20); sample-identifying fields must stay constant per `prodId` (USE01).

### Programme identification

- `progLegalRef` (mandatory, `LEGREF.faff`) — `N112A` (additives, Reg. 1333/2008) or `N113A` (flavourings, Reg. 1334/2008). (Use-levels 2026 p6)
- `prodId` (mandatory, ≤100 chars, no special characters) — unique identifier for the product category/food being reported. Multiple substances for the same category share a `prodId` across records. (USE20) (Use-levels 2026 p6)

### Provenance, market country, market date

- `repCountry` (optional, `COUNTRY`) — populated by EFSA from the reporting organisation if omitted. (Use-levels 2026 p6)
- `marketCountry` (mandatory, `COUNTRY`, **repeatable with `$` separator**) — list of countries where the product category is marketed. Example: `ES$IT` for Spain and Italy. Useful when industry directly reports products sold across multiple countries. (Use-levels 2026 pp. 6-7)
- `marketYear`, `marketMonth`, `marketDay` (all mandatory) — complete marketing date. Required to check the product against the Legal Limit Database at the applicable time (see [[legal-limits-database]]). Combined date must be valid (USE26). (Use-levels 2026 p7)
- `repYear` (**mandatory** here, unlike the no-presence DM) — must equal the current data collection year (USE02). (Use-levels 2026 p7)

### Matrix description

- `matCode` (mandatory, `MTX`/FoodEx2) — FoodEx2 base term plus required facets; see [[foodex2-in-chemmon]] for base-term rules.
  - **F33 (legislative class)** must always be present, implicitly or explicitly (USE16). **USE23 is an Error (not a Warning):** if F33 is implicit in the base term, do not add an explicit F33. (Use-levels 2026 pp. 7-8)
  - **F03 (physical state)** must be explicitly added if not implicit, for the same list of legislative categories as the no-presence DM (01.5, 01.6, 01.8, 01.9, 01.10, 06.3, 12.5, 12.6, 13, 14.1.2, 14.1.3, 14.1.4, 14.1.5, 17 excl. infants/young children). (USE17)
  - **F23 (target consumer)** required when F33 = 13 (foods for particular nutritional uses, Reg. 2009/39/EC). (USE03)
  - **Generic codes forbidden (USE24):** `A047N` ("Food colours"), `A047Q` ("Artificial food colour"), `A047R` ("Food additives other than flavours, colours and artificial sweeteners"), `A047A` ("Food flavourings"), `A047P` ("Natural food colour"), `A0F3T` ("Preparations for food flavouring") are too broad and cannot be used as `matCode` — pick a more specific product category. (Use-levels 2026 p27)
- `matText` (optional, ≤400 chars) — free-text description; defaults to the text associated with `matCode` if empty. (Use-levels 2026 p10)
- `brandName`, `manufacturer` (both optional, ≤250 chars) — brand and manufacturer of the product. (Use-levels 2026 p11)

### Industry / product attributes

- `foodIndustry` (mandatory, `YESNO`) — `Y` if the producer is a food industry manufacturer, `N` if the producer is a FA/FF producer. (USE06) (Use-levels 2026 p11)
- `widelyConsumed` (optional, `YESNO`) — `Y` if widely consumed, `N` if niche (e.g. gluten-free, infant/follow-on formula, sportsperson foods, regional products). (USE08) (Use-levels 2026 p12)

### Restriction / exception

- `restrictionException` (mandatory, `ADDFOOD`) — same rule as the no-presence DM: `FARestExc` when `progLegalRef=N112A` (USE04), `FFRestExc` when `progLegalRef=N113A` (USE05). Use the most detailed code; use `ADD00881A` if none applies. Worked examples: `ADD00197A` only mozzarella (lactic acid in 01.7.1), `ADD00386A` only milk chocolate (citric acid in 05.1), `ADD00622A` only tuna (ascorbic acid in 09.2). (Use-levels 2026 pp. 10-11)

### Parameter

- `paramCode` (mandatory, `PARAM`) — `addAnalysis` hierarchy when `progLegalRef=N112A` (USE21), `flavAnalysis` when `progLegalRef=N113A` (USE22); USE07 is the overall scope rule. Multiple substances for the same product category share `prodId` with different `recId`. (Use-levels 2026 p11)
- `paramText` (optional, ≤400 chars) — substance name; populated by EFSA from `paramCode` if empty. (Use-levels 2026 p12)

### Record identification

- `recId` (mandatory, ≤100 chars) — unique across all data collections from the same DP. The combination `(paramCode, prodId)` must also be unique (USE20). (Use-levels 2026 p12)

### Presence indication

- `presenceAdded` (mandatory, `CONCLUS.faff`, repeatable with `$`) — unlike the no-presence DM, **this DM accepts C19A, C20A, and C05A**, including combinations:
  - `C19A` — "Yes, present on label/added".
  - `C20A` — "No, not present on label/not added". Requires all levels to be 0 (USE09).
  - `C05A` — "Natural occurrence", used when the substance is naturally in the matrix.
  - Combinations such as `C19A$C05A` (added and also naturally present) or `C20A$C05A` (not added but naturally present) are allowed.
  - `C19A` and `C20A` cannot coexist on the same record (USE18 — same mutual-exclusion rule as PRE10 in the no-presence DM). (Use-levels 2026 pp. 12-13)

### Functional class

- `functionOf` (dependent mandatory, `FUNC`) — **required when `progLegalRef=N112A` (additive domain)** (USE10). Same catalogue and semantics as the no-presence DM's `functionOf`. The full list of 28 functional classes plus 5 Annex III classes is in `FUNC` and reproduced verbatim in the source PDF Table 2 (pp. 22-23). Not required for the flavouring domain. (Use-levels 2026 p14)

### Expression basis (weight)

- `weight` (mandatory, `EXPRRES.WDFat`) — whether use levels are expressed on **whole**, **dry matter**, or **fat weight** basis. (Use-levels 2026 p14)
- `fatPerc` (dependent mandatory, `xs:double`) — percentage of fat in the product; required when `weight = fat` (USE11). (Use-levels 2026 p14)
- `moistPerc` (dependent mandatory, `xs:double`) — percentage of moisture in the product; required when `weight = dry matter` (USE12). (Use-levels 2026 p15)
- `unit` (mandatory, `UNIT.chemUnit`) — unit for `minLevel`, `typicalLevel`, and `maxLevel`. All three values must be expressed in the same unit. (Use-levels 2026 p15)

### Level values

- `additionalInfo` (optional, ≤250 chars) — free-text notes on the reported product. (Use-levels 2026 p15)
- `minLevel` (optional, `xs:double`) — minimum use level. Must be `0` when `presenceAdded=C20A` (USE09). (Use-levels 2026 p15)
- `typicalLevel` (mandatory, `xs:double`) — typical use level. Must be `0` when `presenceAdded=C20A` (USE09); must be `> 0` when `presenceAdded=C19A` (USE19). If an exact level is known, `minLevel = typicalLevel = maxLevel`. (Use-levels 2026 p15)
- `maxLevel` (mandatory, `xs:double`) — maximum use level. Must be `0` when `presenceAdded=C20A` (USE09); must be `> 0` when `presenceAdded=C19A` (USE19). Enforced ordering: `maxLevel ≥ typicalLevel ≥ minLevel` (USE25). Must also be `≤` the MPL reported by the DP (USE27). (Use-levels 2026 pp. 15-16)
- `conversionOrDilutionFactor` (dependent mandatory, `xs:double`) — factor applied to minimum/typical/maximum levels to yield the product as consumed. The element description requires it for **food supplements** and for products that must be prepared before consumption (example: infant formula diluted 1:4 → factor 0.25). The published rule table explicitly enforces at least the food-supplement case via `USE13` (`matCode.F33 = 17`). In practice, use the field whenever the reported levels need a preparation/dilution step to express the product as consumed. (Use-levels 2026 p16; Table 3 p25)

### Maximum Permitted Level check

- `maxPermittedLevelDefined` (mandatory, `YESNO`) — `Y` if the regulation (or Quantum satis) defines an MPL for this substance-category-restriction combination; `N` otherwise. (USE14) (Use-levels 2026 p16)
- `maxPermittedLevel` (dependent mandatory, `xs:integer`, ≤10 digits) — numeric MPL value; required when `maxPermittedLevelDefined=Y` (USE15). Combined with the amount naturally present in the matrix where applicable. (Use-levels 2026 p16)

## Business rules

<!-- Source: Use-levels 2026 pp. 24-28, Table 3 -->

Twenty-seven operational rules (`USE01`–`USE27`) plus two LLDB-backed rules (`USE_LLDB01`, `USE_LLDB02`). All are **Active** and **Error** severity.

| Rule | What it enforces |
|---|---|
| USE01 | `(matCode, repCountry, marketCountry, brandName, manufacturer, foodIndustry, widelyConsumed, marketYear, marketMonth, marketDay)` must be constant per `prodId` |
| USE02 | `repYear` = data collection year |
| USE03 | F23 mandatory if F33 = 13 (foods for specific groups) |
| USE04 | If `progLegalRef=N112A`, `restrictionException` ∈ `FARestExc` (or `ADD00881A`) |
| USE05 | If `progLegalRef=N113A`, `restrictionException` ∈ `FFRestExc` (or `ADD00881A`) |
| USE06 | `foodIndustry` ∈ allowed `YESNO` codes |
| USE07 | `paramCode` ∈ `addAnalysis` ∪ `flavAnalysis` (PARAM) |
| USE08 | `widelyConsumed` ∈ allowed `YESNO` codes |
| USE09 | If `presenceAdded=C20A`, `minLevel = typicalLevel = maxLevel = 0` |
| USE10 | `functionOf` mandatory when `progLegalRef=N112A` |
| USE11 | `fatPerc` mandatory when `weight = fat` |
| USE12 | `moistPerc` mandatory when `weight = dry matter` |
| USE13 | `conversionOrDilutionFactor` mandatory when `matCode.F33 = 17` (food supplements) |
| USE14 | `maxPermittedLevelDefined` ∈ allowed `YESNO` codes |
| USE15 | `maxPermittedLevel` mandatory when `maxPermittedLevelDefined=Y` |
| USE16 | F33 mandatory on `matCode` if not implicitly assigned |
| USE17 | F03 mandatory for the specific legislative categories (same list as PRE09) |
| USE18 | `C19A` and `C20A` cannot coexist on one record |
| USE19 | If `presenceAdded=C19A`, `typicalLevel` and `maxLevel` cannot be 0 |
| USE20 | `(paramCode, prodId)` must be unique |
| USE21 | If `progLegalRef=N112A`, `paramCode` ∈ `addAnalysis` |
| USE22 | If `progLegalRef=N113A`, `paramCode` ∈ `flavAnalysis` |
| USE23 | If F33 is implicit in `matCode`, an explicit F33 cannot be reported |
| USE24 | `matCode` must not be one of the forbidden generic codes (`A047N`, `A047Q`, `A047R`, `A047A`, `A047P`, `A0F3T`) |
| USE25 | `maxLevel ≥ typicalLevel ≥ minLevel` |
| USE26 | `(marketDay, marketMonth, marketYear)` must be a valid date |
| USE27 | `maxLevel ≤ MPL` reported by the DP (consistency between reported `maxLevel` and reported `maxPermittedLevel`) |
| USE_LLDB01 | `paramCode` must be authorised in this legislative category with this restriction/exception per Reg. 1333/2008 / 1334/2008 (cross-check against [[legal-limits-database]]) |
| USE_LLDB02 | `maxLevel ≤ MPL` from the Legal Limit Database at the marketing date (cross-check against [[legal-limits-database]]) |

## LLDB cross-check at marketing date

<!-- Source: Use-levels 2026 Section 4, p18 -->

EFSA maintains a Legal Limit Database (LLDB) holding MPLs from Regulation (EC) No 1333/2008 (additives) and Regulation (EC) No 1334/2008 (flavourings). For this DM the LLDB is consulted at the **marketing date** of the product (the `marketYear/Month/Day`), not the sampling date used for SSD2 analytical data. USE_LLDB01 confirms authorisation; USE_LLDB02 confirms `maxLevel` does not exceed the MPL valid on that date. See [[legal-limits-database]] for scope, authority, and the sampling-date counterpart.

## Pilot substance rotation

<!-- Source: Use-levels 2026 p5, footnote 4 -->

Like the no-presence DM, the use-levels DM is piloted on a rotating substance list:

- **2025 pilot**: green S (E 142), tartrazine (E 102), ponceau 4R / cochineal red A (E 124), caffeine (16.016), pulegone (Annex III).
- **2026 pilot**: BHT (E 321), sorbic acid – sorbates (E 200–203), coumarin (Annex III), hydrocyanic acid (Annex III), theobromine (16.032).

Verify the current year's pilot scope against the latest EFSA reporting guidance before scoping a submission.

## Relationship to other FA/FF reporting paths

- **SSD2 ChemMon analytical** ([[food-additives-reporting]]) — sample-level measured concentrations. Analytical data and use levels answer different exposure-assessment questions; both may be collected for the same substance.
- **[[fa-ff-no-presence-data-model]]** — sample-level negative reports. Uses `sampId`/`sampY`/`sampCountry` rather than `prodId`/`marketYear`/`marketCountry`.
- Rule IDs in this DM (`USE…`, `USE_LLDB…`) are a separate namespace from SSD2 CHEMMON rules catalogued under [[business-rules]]; they do not overlap.
