---
title: "Cross-Cutting CHEMMON Business Rules"
type: "rule-reference"
domain: "cross-cutting"
last_updated: "2026-04-10"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Annex B"
related:
  - "[[business-rules]]"
  - "[[business-rules-gbr]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-contaminant]]"
  - "[[business-rules-additives]]"
  - "[[ssd2-data-model]]"
  - "[[foodex2-in-chemmon]]"
---

# Cross-Cutting CHEMMON Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Annex B -->

## Overview

CHEMMON rules that apply to **every reporting domain** (marked "All" in the source guidance) or to **multiple domains simultaneously** (e.g. PPP/VMPR, CONT/FA/FF, PPP/CONT/FA/FF). These are the rules that a deterministic selector should always inject alongside any domain-specific file, because they define the baseline validation every ChemMon submission is subject to.

Grouped by the same sub-sections as the source guidance so readers familiar with Annex B can navigate quickly. Domain-specific rules live in [[business-rules-vmpr]], [[business-rules-pesticide]], [[business-rules-contaminant]], [[business-rules-additives]], and [[business-rules-baby-food]]. General Business Rules (GBR) are in [[business-rules-gbr]].

> **Note on CHEMMON03**: The source guidance defines CHEMMON03 twice — once as an analytical method rule (below) and a second time as a PPP country-consistency rule in [[business-rules-pesticide]]. Both entries are preserved verbatim pending human review.

## Analytical Method Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON03 | Error | `anMethCode.base` is mandatory. The base term for the analytical method must be reported. | All |
| CHEMMON23 | Error | `anMethType` must be Screening (AT06A) or Confirmation (AT08A). No other method types are accepted. | All |
| CHEMMON30 | Error | If `evalCode` = J003A (Above MRL/ML), `anMethType` must be Confirmation (AT08A). Non-compliant findings require a confirmatory method. | All |
| CHEMMON33 | Warning | If `resType` = BIN (binary), `anMethType` should be Screening (AT06A). Binary results are expected from screening methods. | All |
| CHEMMON34 | Warning | If `anMethType` = Confirmation (AT08A), `resType` should not be BIN. Confirmation methods should provide quantitative results. | All |
| CHEMMON79_a/b/c | Error | Contaminant/additive/flavouring analytical method code cannot be Unknown, Unspecified, or Classification not possible. A specific method must be declared. (Merged 2026) | CONT/FA/FF |

## Result Value & Type Rules

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
| CHEMMON57 | Error | `paramCode` + `sampId` combination must be unique per sample. Duplicate substance/sample pairs are rejected. | All |
| CHEMMON62 | Error | If `notSummed` = Y, the LOQ of at least one component in the sum must be reported elsewhere in the submission. | All |
| CHEMMON78 | Error | If `resType` = BIN (binary), `resLOQ` must be empty. Binary results do not carry an LOQ. | All |
| CHEMMON82 | Error | `resLOQ` cannot be a placeholder value (99999, 999, 9999, 999999, 9999999). Real LOQ values must be reported. | All |

## Sampling & Programme Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON01 | Error | Unique `sampId` per sample across all collections. Sample identifiers must not be reused. | All |
| CHEMMON22 | Warning | If `origSampId` is reported (follow-up sample), `sampStrategy` should be ST30A (Suspect sampling). Follow-up samples arise from targeted investigations. | All |
| CHEMMON43 | Error | For pesticides/VMPR, `sampY` (sampling year) must be <= submission year minus 1. Data must be submitted within the expected reporting window. | PPP/VMPR |
| CHEMMON50 | Error | Programme type validation for K018A/K009A with N027A. Specific programme types require matching legal references. (Amended 2026; absorbs CHEMMON49) | All |
| CHEMMON51 | Error | For N027A (coordinated control programme), valid sampling strategies are ST10A (Random), ST20A (Selective), or ST30A (Suspect). | All |
| CHEMMON58 | Error | For pesticides/VMPR, `sampCountry` must equal `reportingOrgCountry`. Samples must originate in the reporting country. | PPP/VMPR |
| CHEMMON68 | Error | `progLegalRef` domain must match `paramCode` domain. The legal reference must correspond to the substance domain being reported. | All |
| CHEMMON77 | Error | For pooled samples (N002A/N031A), `sampUnitSizeUnit` must be G005A and `sampUnitSize` must equal the number of units pooled. | All |
| CHEMMON94 | Error | For K038A (import control), `sampPoint` can only be E010A (Border Control Posts). Import samples must be taken at the border. (Amended 2026) | All |
| CHEMMON97 | Error | For PPP/CONT/ADD/FLAV with K005A, valid sampling strategies are ST10A, ST20A, or ST30A. (New 2026) | PPP/CONT/FA/FF |
| CHEMMON99 | Warning | For K038A/K019A/E010A (import/monitoring at border), `origCountry` cannot equal `sampCountry`. Import samples must originate from a different country. (New 2026) | All |

## Matrix & Facet Rules (cross-domain)

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON06 | Warning | `fatPerc` (fat percentage) should be >= 1 when reported. Values below 1% are implausible for most matrices. | All |
| CHEMMON07 | Warning | `moistPerc` (moisture percentage) should be >= 1 when reported. | All |
| CHEMMON27 | Warning | For VMPR/pesticides, `sampMatCode` should equal `anMatCode`. The sampled and analysed matrices are usually the same. | VMPR/PPP |
| CHEMMON103 | Warning | Organic production (A07SE) and conventional production (A0C6Y) facets must not be reported together on the same record. They are mutually exclusive. (New 2026) | All |

## Evaluation & Action Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON26 | Error | If `actTakenCode` = Follow-up investigation, `evalInfo.conclusion` should be reported to explain the basis for the follow-up. | All |
| CHEMMON35 | Warning | `evalLimitType` should be one of: W002A (MRL), W005A (ML), W006A (Action level), W012A (Reference point for action), W001A (ADI), W007A (Benchmark dose), W008A (Health-based guidance value), or W990A (Other). | All |
| CHEMMON37 | Error | For CONT/ADD/FLAV domains, if `evalCode` = Detected or Above limit, `actTakenCode` is mandatory. An enforcement action must be recorded for positive/non-compliant findings. | CONT/FA/FF |
| CHEMMON65 | Error | `evalInfo.resAssess` can only be J037A (Compliant) or J038A (Non-compliant). No other assessment outcomes are accepted. | All |
| CHEMMON66_a | Warning | If `evalInfo.resAssess` = J037A (Compliant) but `evalCode` indicates Above or Detected, `evalInfo.conclusion` should be reported to explain the compliant assessment. | All |
| CHEMMON66_b | Warning | If `evalInfo.resAssess` = J038A (Non-compliant) but `evalCode` does not indicate Above or Detected, `evalInfo.conclusion` should be reported to explain the non-compliant assessment. | All |
| CHEMMON67 | Warning | `sampTkAsse` and `sampEventAsse` should NOT be reported. These legacy fields are deprecated in ChemMon. | All |
| CHEMMON85 | Error | For VMPR/PPP with non-compliant evaluation results, `actTakenCode` is mandatory. Enforcement actions must be recorded. | VMPR/PPP |

## FoodEx2 Validation Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| FOODEX2_SAMMAT | Error | `sampMatCode` must follow FoodEx2 coding rules. The sampled matrix must be a valid FoodEx2 term with correct facet usage. | All |
| FOODEX2_ANMAT | Error | `anMatCode` must follow FoodEx2 coding rules. The analysed matrix must be a valid FoodEx2 term with correct facet usage. | All |
