---
title: "ChemMon Business Rules"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[vmpr-reporting]]"
  - "[[baby-food-reporting]]"
  - "[[ssd2-data-model]]"
last_updated: "2026-04-07"
---

# ChemMon Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Overview

- Business rules validate SSD2 submissions before acceptance into the EFSA data warehouse.
- Two severity levels: **Error** (blocks submission) and **Warning** (flags for review but does not block).
- Rules are domain-specific. Not all rules apply to all reporting domains (pesticides, contaminants, veterinary medicinal product residues, food additives/flavourings).
- Business rules take precedence when they conflict with prose sections of the guidance.
- Rules are organised into three tiers: General Business Rules (GBR) that apply across all EFSA data collections, ChemMon-specific rules (CHEMMON) that apply to the chemical monitoring domain, and Legal Limit rules (LL) that compare reported values against regulatory thresholds.

---

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Annex B -->
## General Business Rules (GBR)

General Business Rules apply across all EFSA SSD2 data collections, not only ChemMon. The following GBR rules are the most relevant to chemical monitoring submissions.

### Sampling Event & Sample Consistency

| Rule ID | Severity | Description |
| --- | --- | --- |
| GBR2 | Error | Sampling event consistency -- sections A, B, C must be constant for the same `sampId`/`sampEventId`. All rows sharing a sampling event must report identical sampling-level fields. |
| GBR3 | Error | Sample taken / matrix sampled consistency -- `sampMatCode` and related fields must be consistent for the same `sampId`. |
| GBR4 | Error | Sample analysed / matrix analysed consistency -- `anMatCode` and related fields must be consistent for the same `sampAnId`. |

### Geographic Validation

| Rule ID | Severity | Description |
| --- | --- | --- |
| GBR12 | Error | `sampArea` must be geographically within `sampCountry`. A NUTS code or region must belong to the declared sampling country. |
| GBR13 | Error | `origArea` must be geographically within `origCountry`. The origin area must belong to the declared country of origin. |

### Result Value & Unit Rules

| Rule ID | Severity | Description |
| --- | --- | --- |
| GBR27 | Error | Result unit (`resUnit`) mandatory when binary results are reported (`resType` = BIN). |
| GBR28 | Error | Result unit (`resUnit`) mandatory when any LOD or LOQ value is reported. |
| GBR29 | Error | Result unit (`resUnit`) mandatory when any result value (`resVal`) is reported. |
| GBR36 | Error | If `resType` = LOD, then `resLOD` must be reported. |
| GBR37 | Error | `resLOD` must be less than or equal to `resLOQ`. |
| GBR39 | Error | If `resType` = LOQ and `notSummed` is not 'Y', then `resLOQ` must be reported. |
| GBR46 | Error | If `resType` = VAL, then `resVal` must be reported. |
| GBR47 | Error | If `resType` = LOD, then `resVal` must be empty. |
| GBR48 | Error | `resVal` must be greater than 0 when reported. |
| GBR101 | Error | Only one result per parameter per sample analysed portion is permitted. Duplicate `paramCode`/`sampAnId` combinations are rejected. |
| GBR102 | Error | `resVal` must be greater than or equal to `resLOD`. A detected value cannot be below the limit of detection. |

---

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Annex B -->
## ChemMon Business Rules (CHEMMON)

### Analytical Method Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON03 | Error | `anMethCode.base` is mandatory. The base term for the analytical method must be reported. | All |
| CHEMMON23 | Error | `anMethType` must be Screening (AT06A) or Confirmation (AT08A). No other method types are accepted. | All |
| CHEMMON30 | Error | If `evalCode` = J003A (Above MRL/ML), `anMethType` must be Confirmation (AT08A). Non-compliant findings require a confirmatory method. | All |
| CHEMMON33 | Warning | If `resType` = BIN (binary), `anMethType` should be Screening (AT06A). Binary results are expected from screening methods. | All |
| CHEMMON34 | Warning | If `anMethType` = Confirmation (AT08A), `resType` should not be BIN. Confirmation methods should provide quantitative results. | All |
| CHEMMON79_a/b/c | Error | Contaminant/additive/flavouring analytical method code cannot be Unknown, Unspecified, or Classification not possible. A specific method must be declared. (Merged 2026) | CONT/FA/FF |

### Result Value & Type Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON04 | Warning | `resValRec` (recovery rate) should be >= 1%. Recovery rates below 1% are implausible. | All |
| CHEMMON05 | Warning | `resValRec` should be between 50% and 150%. Values outside this range suggest analytical problems. | All |
| CHEMMON08 | Error | If `resVal` equals `resLOQ`, `resType` must be VAL (quantified value). (Amended 2026) | All |
| CHEMMON24 | Error | `resQualValue` must equal NEG (negative) unless the parameter is MOAHs (mineral oil aromatic hydrocarbons). | All |
| CHEMMON40 | Error | For qualitative results, `resVal` must be empty. Qualitative result types do not carry numeric values. (Amended 2026; replaces CHEMMON47) | All |
| CHEMMON41 | Warning | `resLOQ` should not exceed `resVal` for positive detections. A quantified value below the LOQ is inconsistent. | All |
| CHEMMON42 | Warning | If `resValRecCorr` = Yes (recovery-corrected), `resValRec` must be reported and should be in the range 70--120%. | All |
| CHEMMON44 | Error | `resLOQ` must be reported unless the method is unvalidated, `notSummed` = Y, the domain is VMPR, or `resType` = BIN. | PPP/CONT/FA/FF |
| CHEMMON45 | Error | At least one of `resLOQ`, `resLOD`, `CCbeta`, or `CCalpha` must be reported. Every result needs a sensitivity indicator. | All |
| CHEMMON46 | Error | If `evalCode` = J003A (Above limit) and `evalLimitType` is not Presence-based, `resType` must be VAL. Non-compliance with a numeric limit requires a quantified value. | All |
| CHEMMON48 | Warning | If `paramType` is not P002A (individual substance) and `resVal` >= `evalLowLimit`, `evalCode` should not be J029A (Below LOQ). | All |
| CHEMMON56 | Error | For pesticides, `exprResType` can only be B001A (whole weight), B003A (fat weight), or B007A (dry weight). | PPP |
| CHEMMON57 | Error | `paramCode` + `sampId` combination must be unique per sample. Duplicate substance/sample pairs are rejected. | All |
| CHEMMON61 | Error | For pesticides, `resType` can only be LOD, LOQ, BIN, or VAL. No other result types are accepted. | PPP |
| CHEMMON62 | Error | If `notSummed` = Y, the LOQ of at least one component in the sum must be reported elsewhere in the submission. | All |
| CHEMMON72 | Warning | For pesticides, `resValUncert` (measurement uncertainty) should be reported when `resType` = VAL. | PPP |
| CHEMMON78 | Error | If `resType` = BIN (binary), `resLOQ` must be empty. Binary results do not carry an LOQ. | All |
| CHEMMON82 | Error | `resLOQ` cannot be a placeholder value (99999, 999, 9999, 999999, 9999999). Real LOQ values must be reported. | All |

### Sampling & Programme Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON01 | Error | Unique `sampId` per sample across all collections. Sample identifiers must not be reused. | All |
| CHEMMON02 | Error | Country of sampling must equal reporting organisation country for pesticides. Pesticide data must originate from the reporting country. | PPP |
| CHEMMON03 | Error | `sampCountry`/`origCountry` consistency for PPP domain. | PPP |
| CHEMMON22 | Warning | If `origSampId` is reported (follow-up sample), `sampStrategy` should be ST30A (Suspect sampling). Follow-up samples arise from targeted investigations. | All |
| CHEMMON43 | Error | For pesticides/VMPR, `sampY` (sampling year) must be <= submission year minus 1. Data must be submitted within the expected reporting window. | PPP/VMPR |
| CHEMMON43_b | Warning | For additives/flavourings, `sampY` must be < submission year minus 1. (New 2026; becomes Error in 2027) | FA/FF |
| CHEMMON50 | Error | Programme type validation for K018A/K009A with N027A. Specific programme types require matching legal references. (Amended 2026; absorbs CHEMMON49) | All |
| CHEMMON51 | Error | For N027A (coordinated control programme), valid sampling strategies are ST10A (Random), ST20A (Selective), or ST30A (Suspect). | All |
| CHEMMON52 | Error | For pesticides with N027A, valid `progType` values are K005A (Official/National), K009A (EU coordinated), K038A (Import control), or K018A (Other official). | PPP |
| CHEMMON54 | Error | For N317A (contaminant control programme), `progType` must be K019A (Monitoring) and `sampStrategy` must be ST30A (Suspect). | CONT |
| CHEMMON58 | Error | For pesticides/VMPR, `sampCountry` must equal `reportingOrgCountry`. Samples must originate in the reporting country. | PPP/VMPR |
| CHEMMON68 | Error | `progLegalRef` domain must match `paramCode` domain. The legal reference must correspond to the substance domain being reported. | All |
| CHEMMON77 | Error | For pooled samples (N002A/N031A), `sampUnitSizeUnit` must be G005A and `sampUnitSize` must equal the number of units pooled. | All |
| CHEMMON94 | Error | For K038A (import control), `sampPoint` can only be E010A (Border Control Posts). Import samples must be taken at the border. (Amended 2026) | All |
| CHEMMON95 | Warning | For PPP with `evalCode` = J003A (non-compliant), `origCountry` must not be XX, AA, EU, XC, XD, or XE. Non-compliant results require a specific country of origin. (Amended 2026) | PPP |
| CHEMMON96 | Error | For VMPR with K005A (official programme), valid sampling strategies are ST10A, ST20A, ST30A, or ST90A. (Amended 2026) | VMPR |
| CHEMMON97 | Error | For PPP/CONT/ADD/FLAV with K005A, valid sampling strategies are ST10A, ST20A, or ST30A. (New 2026) | PPP/CONT/FA/FF |
| CHEMMON98 | Error | For contaminants with N375A (contaminant regulation), valid `progType` values are K005A, K018A, or K038A. (New 2026) | CONT |
| CHEMMON99 | Warning | For K038A/K019A/E010A (import/monitoring at border), `origCountry` cannot equal `sampCountry`. Import samples must originate from a different country. (New 2026) | All |
| CHEMMON101 | Error | For N422A (new regulation reference), `progType` must be K019A and `sampStrategy` must be ST30A. (New 2026) | PPP |
| CHEMMON104 | Error | N422A is exclusive -- it cannot be concatenated with other `progLegalRef` values in the same record. (New 2026) | PPP |
| CHEMMON105 | Error | N317A is exclusive -- it cannot be concatenated with other `progLegalRef` values in the same record. (New 2026) | CONT |

### Baby Food & Sample Exclusion Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON55 | Error | For N028A/N318A (baby food programme references), `sampMatCode` parent term must be A03PV (Food products for young population). Baby food programme data must reference baby food matrices. See [[baby-food-reporting]]. | All |
| CHEMMON63 | Error | If `sampMatCode` falls under A03PZ (baby food), `progLegalRef` cannot be N371A. Baby food is excluded from the VMPR legal framework. See [[baby-food-reporting]] and [[vmpr-reporting]]. | VMPR |

### Domain-Specific Matrix Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON06 | Warning | `fatPerc` (fat percentage) should be >= 1 when reported. Values below 1% are implausible for most matrices. | All |
| CHEMMON07 | Warning | `moistPerc` (moisture percentage) should be >= 1 when reported. | All |
| CHEMMON09 | Warning | For dioxin/dl-PCB parameters, all 29 congeners must be reported per sample. Incomplete congener profiles prevent TEQ calculation. | CONT |
| CHEMMON10 | Warning | For non-dl-PCB parameters, six indicator congeners must be reported per sample. | CONT |
| CHEMMON11 | Warning | For mineral oils/mycotoxins, `moistPerc` should be reported to enable dry-weight conversions. | CONT |
| CHEMMON12 | Error | For acrylamide, F33 (legislative class) facet is mandatory. `sampMatCode.legis` must contain the specific product code per Commission Regulation (EU) 2017/2158 and Recommendation (EU) 2019/1888. See [[contaminant-reporting]]. | CONT |
| CHEMMON14 | Error | For bisphenol compounds, F19 (packaging material) facet is mandatory. Packaging material affects migration and exposure. | CONT |
| CHEMMON15 | Warning | For PAHs, F19 (packaging material) facet should be reported. | CONT |
| CHEMMON17 | Warning | For mycotoxins, F21 (production method) facet should be reported (e.g., organic vs. conventional). | CONT |
| CHEMMON18 | Warning | For arsenic in rice, F28 (process) facet should specify processed or unprocessed. Speciation depends on processing state. | CONT |
| CHEMMON19 | Warning | For chlorates/perchlorates/QACs, F28 (process) facet should be reported. | CONT |
| CHEMMON20 | Warning | For fish matrices with BFRs/dioxins/mercury, `origFishAreaCode` (fishing area) should be reported. | CONT |
| CHEMMON21 | Warning | For BFRs/dioxins/3-MCPDs, `fatPerc` should be reported to allow fat-weight expression. | CONT |
| CHEMMON27 | Warning | For VMPR/pesticides, `sampMatCode` should equal `anMatCode`. The sampled and analysed matrices are usually the same. | VMPR/PPP |
| CHEMMON28 | Warning | For VMPR, only the recommended `sampPoint` codes from the guidance should be used. | VMPR |
| CHEMMON69 | Error | For contaminants in feed reported on whole weight basis, `moistPerc` is mandatory to allow dry-weight conversion. | CONT |
| CHEMMON73 | Warning | For VMPR feed/water matrices, F23 (target consumer/animal species) facet should be reported. | VMPR |
| CHEMMON76 | Error | For VMPR with the same `sampEventId`, the F01 (species/breed) facet must be identical across all samples in the event. | VMPR |
| CHEMMON83 | Warning | If `sampMatCode` = F10.A18PX, F19 (packaging) and F18 (contact surface) should NOT be reported. This matrix code already implies specific packaging. | CONT |
| CHEMMON90_a | Warning | For copper parameters, F20 (geographical origin of production) and/or F28 (process) facets are needed. (New 2026) | PPP |
| CHEMMON90_b | Error | For copper parameters, `resValUncert` is mandatory when `resType` = VAL. (New 2026) | PPP |
| CHEMMON91 | Warning | For VMPR, only one F33 (legislative class) facet under VR classes should be reported per sample. Multiple VR classes per sample are discouraged. | VMPR |
| CHEMMON92 | Error | For VMPR, the base term of `paramCode` must belong to the vetDrugRes hierarchy. Only recognised veterinary drug residue parameters are accepted. | VMPR |
| CHEMMON103 | Warning | Organic production (A07SE) and conventional production (A0C6Y) facets must not be reported together on the same record. They are mutually exclusive. (New 2026) | All |

### Food Additives & Flavourings Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON36 | Warning | When `evalLimitType` = MRL, `evalCode` must be one of J002A, J003A, J031A, or J029A. Other evaluation codes are not valid for MRL-based assessments. | FA/FF |
| CHEMMON37 | Error | For CONT/ADD/FLAV domains, if `evalCode` = Detected or Above limit, `actTakenCode` is mandatory. An enforcement action must be recorded for positive/non-compliant findings. | CONT/FA/FF |
| CHEMMON39_a/b | Error | F33 (legislative classes) facet is mandatory for food additives and flavourings. The applicable food category legislation must be declared. (Merged 2026) | FA/FF |
| CHEMMON84_a | Error | `exprResType` (expression of result type) is mandatory for food additives and flavourings. (Amended 2026) | FA/FF |
| CHEMMON84_b | Warning | `exprResType` is highly recommended for contaminants. (Amended 2026) | CONT |
| CHEMMON85 | Error | For VMPR/PPP with non-compliant evaluation results, `actTakenCode` is mandatory. Enforcement actions must be recorded. | VMPR/PPP |
| CHEMMON86 | Warning | F03 (physical state) facet is recommended for specific food categories where physical state affects legal limits. (Amended 2026) | FA/FF |
| CHEMMON87 | Warning | `evalInfo.conclusion` is highly recommended for food additives and flavourings. Evaluation conclusions aid data interpretation. | FA/FF |
| CHEMMON88 | Warning | `evalInfo.restrictionException` is highly recommended for food additives and flavourings. Restriction or exception context should be documented. (Amended 2026) | FA/FF |
| CHEMMON89 | Warning | For food category 13 (food for specific groups), F23 (target consumer) facet is recommended. | FA/FF |
| CHEMMON100 | Warning | For VMPR, `evalCode` is restricted to J002A, J003A, J029A, J031A, or J040A. Other evaluation codes are not valid for veterinary residue data. (New 2026) | VMPR |
| CHEMMON102 | Warning | For VMPR with the same `sampEventId`, geographic fields (`sampCountry`, `sampArea`, `origCountry`, `origArea`) must be constant across all records in the event. (New 2026) | VMPR |
| CHEMMON106 | Warning | For potassium sorbate, `paramText` should specify whether the result relates to free acid or the salt form. (New 2026) | FA/FF |
| CHEMMON107 | Warning | For sorbic acid, BHT, coumarin, HCN, and theobromine, reporting `resLOD` is highly recommended to support data quality assessment. (New 2026) | FA/FF |
| CHEMMON108 | Warning | For food additives and flavourings, certain generic `sampMatCode` terms (broad classifications) are not allowed. More specific matrix codes must be used. (New 2026) | FA/FF |
| CHEMMON109 | Warning | If an implicit F33 (legislative class) facet is present via the `sampMatCode`, an explicit F33 is not needed for food additives/flavourings. Avoids duplication. (New 2026) | FA/FF |

### Evaluation & Action Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON26 | Error | If `actTakenCode` = Follow-up investigation, `evalInfo.conclusion` should be reported to explain the basis for the follow-up. | All |
| CHEMMON31 | Error | If `accredProc` = V007A (Decision 2002/657/EC) and method is Confirmation, CCalpha (decision limit) is mandatory. | VMPR |
| CHEMMON32 | Error | If `accredProc` = V007A and method is Screening, CCbeta (detection capability) is mandatory. | VMPR |
| CHEMMON35 | Warning | `evalLimitType` should be one of: W002A (MRL), W005A (ML), W006A (Action level), W012A (Reference point for action), W001A (ADI), W007A (Benchmark dose), W008A (Health-based guidance value), or W990A (Other). | All |
| CHEMMON59 | Error | For pesticides, `evalLimitType` can only be W002A (MRL), W990A (Other), or left empty. | PPP |
| CHEMMON60 | Error | For pesticides, `evalCode` must be J002A (Below MRL), J003A (Above MRL), J029A (Below LOQ), or J031A (At or about MRL). | PPP |
| CHEMMON65 | Error | `evalInfo.resAssess` can only be J037A (Compliant) or J038A (Non-compliant). No other assessment outcomes are accepted. | All |
| CHEMMON66_a | Warning | If `evalInfo.resAssess` = J037A (Compliant) but `evalCode` indicates Above or Detected, `evalInfo.conclusion` should be reported to explain the compliant assessment. | All |
| CHEMMON66_b | Warning | If `evalInfo.resAssess` = J038A (Non-compliant) but `evalCode` does not indicate Above or Detected, `evalInfo.conclusion` should be reported to explain the non-compliant assessment. | All |
| CHEMMON67 | Warning | `sampTkAsse` and `sampEventAsse` should NOT be reported. These legacy fields are deprecated in ChemMon. | All |
| CHEMMON70 | Error | For pesticides in egg/milk matrices, `exprResType` must be B001A (whole weight). Fat-weight or dry-weight expression is not accepted for these matrices. | PPP |
| CHEMMON71 | Error | For contaminants in feed, `exprResType` is mandatory. The basis of expression must be declared. | CONT |
| CHEMMON80 | Warning | For contaminants, `resValRecCorr` (recovery correction flag) should be reported to indicate whether the result was corrected for recovery. | CONT |
| CHEMMON93 | Warning | For non-compliant VMPR Plan 1/2 results, `sampArea` (geographic area) reporting is required to enable traceability. | VMPR |

### FoodEx2 Validation Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| FOODEX2_SAMMAT | Error | `sampMatCode` must follow FoodEx2 coding rules. The sampled matrix must be a valid FoodEx2 term with correct facet usage. | All |
| FOODEX2_ANMAT | Error | `anMatCode` must follow FoodEx2 coding rules. The analysed matrix must be a valid FoodEx2 term with correct facet usage. | All |

---

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Annex B -->
## Legal Limit Rules

Legal limit rules compare reported result values against regulatory thresholds (MRLs, MLs, MPLs). They ensure that evaluation codes are consistent with the numeric comparison between result values and applicable limits.

### VMPR & Pesticide Legal Limits

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| LL_01_VMPR | Warning | If `resVal` exceeds the MRL for veterinary residues, `evalCode` must reflect non-compliance. | VMPR |
| LL_01_PPP | Error | If `resVal` exceeds the MRL for pesticides, `evalCode` must reflect non-compliance. | PPP |
| LL_02_VMPR | Warning | If `resVal` <= MRL for veterinary residues, `evalCode` must not indicate non-compliance. | VMPR |
| LL_02_PPP | Error | If `resVal` <= MRL for pesticides, `evalCode` must not indicate non-compliance. | PPP |

### Food Additives & Flavourings Legal Limits

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| LL_01_FA_FF | Warning | Maximum Permitted Level (MPL) comparison -- if `resVal` exceeds the MPL, the evaluation should reflect this. (New 2026) | FA/FF |
| LL_02_FA_FF | Warning | MPL threshold evaluation -- if `resVal` <= MPL, the evaluation should not indicate exceedance. (New 2026) | FA/FF |
| LL_03_FA_FF | Warning | Substance authorisation check -- the reported substance must be authorised for the declared food category under the applicable regulation. (New 2026) | FA/FF |

### General Legal Limit Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| LL_03 | Error | `paramType` must be reported for multi-component or sum parameters. The parameter type (individual, sum, complex) must be declared to enable correct limit comparison. | All |
| LL_03_b | Warning | `paramType` should equal the pre-assigned `paramType` from the EFSA parameter catalogue. Deviations should be justified. | All |
| LL_04 | Error | For pesticides, the `sampMatCode`/`paramCode` combination must match entries in the legal limits database. Only valid matrix/substance pairs are accepted. | PPP |
| LL_04_b | Error | For pesticides, the `anMatCode`/`paramCode` combination must match entries in the legal limits database. | PPP |

---

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## 2026 Changes

### Amended rules

- **CHEMMON08** -- `resVal`/`resLOQ` relationship updated: if `resVal` equals `resLOQ`, `resType` must be VAL.
- **CHEMMON40** -- Result type validation expanded for qualitative results; replaces deactivated CHEMMON47.
- **CHEMMON50** -- Programme type validation expanded; absorbs deactivated CHEMMON49.
- **CHEMMON84_a** -- Food additive/flavouring `exprResType` requirement updated.
- **CHEMMON84_b** -- Expression of result type recommended guidance revised for contaminants.
- **CHEMMON86** -- Physical-state facet scope amended for food additives/flavourings.
- **CHEMMON88** -- Restriction/exception reporting scope amended.
- **CHEMMON94** -- Third-country import sampling point restriction tightened to require E010A for K038A.
- **CHEMMON95** -- PPP non-compliant origin country validation revised; expanded list of excluded generic codes.
- **CHEMMON96** -- VMPR sampling strategy for official programmes updated to include ST90A.

### Merged rules

- **CHEMMON39_a/b** -- Previously separate food additive and flavouring legislative class rules consolidated into a single pair.
- **CHEMMON79_a/b/c** -- Contaminant, additive, and flavouring analytical method validation rules consolidated. Method code cannot be Unknown/Unspecified/Classification not possible.

### New rules

- **CHEMMON43_b** -- Sampling year validation for additives/flavourings (Warning; becomes Error 2027).
- **CHEMMON90_a** -- Copper facet requirement for F20/F28.
- **CHEMMON90_b** -- Measurement uncertainty mandatory for copper when `resType` = VAL.
- **CHEMMON97** -- Multi-domain sampling strategy validation for K005A across PPP/CONT/ADD/FLAV.
- **CHEMMON98** -- Programme type restriction for contaminants under N375A.
- **CHEMMON99** -- Import origin validation: `origCountry` cannot equal `sampCountry` for import programmes.
- **CHEMMON100** -- VMPR evaluation code restricted to five permitted codes.
- **CHEMMON101** -- N422A regulation requires K019A programme type and ST30A strategy.
- **CHEMMON102** -- VMPR geographic consistency check across `sampEventId` records.
- **CHEMMON103** -- Organic/conventional production mutual exclusivity.
- **CHEMMON104** -- N422A exclusive programme reference (no concatenation).
- **CHEMMON105** -- N317A exclusive programme reference (no concatenation).
- **CHEMMON106** -- Potassium sorbate `paramText` must specify free acid or salt form.
- **CHEMMON107** -- LOD highly recommended for sorbic acid, BHT, coumarin, HCN, theobromine.
- **CHEMMON108** -- Generic `sampMatCode` terms restricted for additives/flavourings.
- **CHEMMON109** -- Implicit F33 makes explicit F33 unnecessary for additives/flavourings.
- **LL_01_FA_FF** -- MPL comparison for food additives/flavourings.
- **LL_02_FA_FF** -- MPL threshold evaluation for food additives/flavourings.
- **LL_03_FA_FF** -- Substance authorisation check for food additives/flavourings.

### Deactivated rules

- **CHEMMON47** -- Replaced by CHEMMON40 (qualitative result value validation).
- **CHEMMON49** -- Included in CHEMMON50 (programme type validation).
- **CHEMMON53** -- Obsolete per 2025 update.
- **CHEMMON81** -- Replaced by CHEMMON40 (result type validation).
