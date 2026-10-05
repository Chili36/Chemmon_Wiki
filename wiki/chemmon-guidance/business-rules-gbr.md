---
title: "General Business Rules (GBR)"
select_when: "Exact generic SSD2 rule conditions including GBR27-29 units/BIN and GBR101 uniqueness. This is a selected subset; do not assume every GBR is covered."
type: "rule-reference"
domain: "all"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 98-112, Table 9"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[ssd2-data-model]]"
---

# General Business Rules (GBR)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, pp. 98-112, Table 9 -->

## Overview

General Business Rules (GBR) apply across all EFSA SSD2 data collections, not only ChemMon. They validate sampling event consistency, geographic fields, and result value/unit reporting at the data-model level. This page documents a selected subset. The source table contains 92 GBR IDs, including inactive and biological-only entries; omitted active rules are tracked in the source review. It is not a complete validation specification.

See [[business-rules]] for the hub and [[business-rules-cross-cutting]] for CHEMMON-level rules that apply to every reporting domain.

## Sampling Event & Sample Consistency

| Rule ID | Severity | Description |
| --- | --- | --- |
| GBR2 | Error | Sampling-event, local-organisation and sampling-programme descriptors listed in Table 9 must be consistent for the same `sampId` / `sampEventId`. `progId` and `progLegalRef` are excluded from this consistency list (p. 98). |
| GBR3 | Error | Sample taken / matrix sampled consistency -- `sampMatCode` and related fields must be consistent for the same `sampId`. |
| GBR4 | Error | Sample analysed / matrix analysed consistency -- `anMatCode` and related fields must be consistent for the same `sampAnId`. |

## Geographic Validation

| Rule ID | Severity | Description |
| --- | --- | --- |
| GBR12 | Error | `sampArea` must be geographically within `sampCountry`. A NUTS code or region must belong to the declared sampling country. |
| GBR13 | Error | `origArea` must be geographically within `origCountry`. The origin area must belong to the declared country of origin. |

## Result Value & Unit Rules

| Rule ID | Severity | Description |
| --- | --- | --- |
| GBR27 | Error | `resUnit` must be reported when `resType` is different from BIN (p. 102). |
| GBR28 | Error | `resQualValue` must be reported when `resType` = BIN (p. 103). |
| GBR29 | Error | `resUnit` must be reported if any of `resLOD`, `resLOQ`, `resLLWR`, `resULWR`, `CCalpha`, `CCbeta`, `resVal`, `resValUncert`, `resValUncertSD`, `evalLowLimit` or `evalHighLimit` is reported (p. 103). |
| GBR36 | Error | If `resType` = LOD, then `resLOD` must be reported. |
| GBR37 | Error | `resLOD` must be less than or equal to `resLOQ`. |
| GBR39 | Error | If `resType` = LOQ and `notSummed` is not 'Y', then `resLOQ` must be reported. |
| GBR46 | Error | If `resType` = VAL, then `resVal` must be reported. |
| GBR47 | Error | If `resType` = LOD, then `resVal` must be empty. |
| GBR48 | Error | `resVal` must be greater than 0 when reported. |
| GBR101 | Error | Unless `paramCode.base` is RF-XXXX-XXX-XXX (Not in list), the combination of `paramCode.base`, `sampId`, `sampAnId` and `anPortSeq` must be unique (p. 112). |
| GBR102 | Error | `resVal` must be greater than or equal to `resLOD`. A detected value cannot be below the limit of detection. |
