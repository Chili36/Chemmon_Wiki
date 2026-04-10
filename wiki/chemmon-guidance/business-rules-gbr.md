---
title: "General Business Rules (GBR)"
type: "rule-reference"
domain: "all"
last_updated: "2026-04-10"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Annex B"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[ssd2-data-model]]"
---

# General Business Rules (GBR)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Annex B -->

## Overview

General Business Rules (GBR) apply across all EFSA SSD2 data collections, not only ChemMon. They validate sampling event consistency, geographic fields, and result value/unit reporting at the data-model level. These rules run before any ChemMon-specific validation and reject non-conforming submissions early.

See [[business-rules]] for the hub and [[business-rules-cross-cutting]] for CHEMMON-level rules that apply to every reporting domain.

## Sampling Event & Sample Consistency

| Rule ID | Severity | Description |
| --- | --- | --- |
| GBR2 | Error | Sampling event consistency -- sections A, B, C must be constant for the same `sampId`/`sampEventId`. All rows sharing a sampling event must report identical sampling-level fields. |
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
