---
title: "General Business Rules (GBR)"
select_when: "Core generic SSD2 rules: sample/event consistency, sampling/origin geography, GBR27-29 units/BIN, result shape and GBR101 uniqueness. Links to separate date, descriptor-consistency and numeric-threshold GBR pages."
type: "rule-reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
source_pages:
  - "ChemMon 2026 p. 97 (GBR scope)"
  - "ChemMon 2026 pp. 98-112 (Table 9)"
  - "ChemMon 2026 pp. 80-81 (element table, sections C and D)"
  - "No-presence 2026 p. 13 (DCF upload), pp. 19-21 (Table 3)"
  - "Use-levels 2026 p. 17 (DCF upload), pp. 24-28 (Table 3)"
related:
  - "[[business-rules]]"
  - "[[business-rules-gbr-consistency]]"
  - "[[business-rules-gbr-results]]"
  - "[[business-rules-gbr-dates]]"
  - "[[business-rules-cross-cutting]]"
  - "[[ssd2-data-model]]"
---

# General Business Rules (GBR)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, pp. 98-112, Table 9 -->

## Overview

General business rules (GBR) "apply to all data submitted to EFSA through the
DCF, including microbiological data as well as chemical" (ChemMon 2026 p97).
Table 9 is written against SSD2 data elements. Table 9 of the
2026 ChemMon guidance lists 92 IDs: 83 active rules not marked biological-only,
seven biological-only rules, and two inactive rules. The 83 applicable active
definitions are covered once each across this page and three focused references:

- This page: 16 core rules for sample consistency, geography and result shape.
- [[business-rules-gbr-consistency]]: 12 rules for identifiers, matrix/method text,
  processing geography and sample-size units.
- [[business-rules-gbr-results]]: 20 rules for percentages, evaluation limits,
  decision thresholds, recovery and uncertainty, including the two Warnings.
- [[business-rules-gbr-dates]]: 35 rules for valid dates, ranges and chronology.

This covers Table 9's applicable active GBR definitions, not every rule needed
for a valid ChemMon submission. CHEMON/LL rules, field specifications and
collection-specific conditions still apply.

The No-presence and Use-levels guides list only PRE and USE rules in their
Table 3, "List of the business rules applicable" (No-presence pp. 19-21;
Use-levels pp. 24-28), and no GBR. Source discrepancy: ChemMon says GBRs "apply
to all data submitted to EFSA through the DCF" (ChemMon 2026 p97), and both
guides have their XML file uploaded in the DCF (No-presence p13; Use-levels
p17), yet their Table 3 lists no GBR. No source says which holds for those
submissions. Wiki note (not in the guidance): PRE and USE use their own data
models, so Table 9's SSD2 element names do not map directly onto them.

See [[business-rules]] for the hub and [[business-rules-cross-cutting]] for CHEMON rules spanning multiple domains; check each row's applicability.

## Sampling Event & Sample Consistency

| Rule ID | Severity | Description |
| --- | --- | --- |
| GBR2 | Error | Sampling-event, local-organisation and sampling-programme descriptors listed in Table 9 must be consistent for the same `sampId` / `sampEventId`. `progId` and `progLegalRef` are excluded from this consistency list (p. 98). |
| GBR3 | Error | For records sharing `sampId`, sample-taken and sampled-matrix descriptors (Sections D/E) **and `sampEventId`** must be constant (pp. 98-99). |
| GBR4 | Error | For records sharing `sampAnId`, analysed-sample and analysed-matrix descriptors (Sections F/G) **and `sampId`** must be constant (p. 99). |

The descriptor lists in the source are:

- **GBR2:** `localOrgId`, `localOrgCountry`, `localOrgInfo`, `sampStrategy`,
  `progType`, `sampMethod`, `sampler`, `sampPoint`, `progInfo`, `sampUnitType`,
  `sampUnitSize`, `sampUnitSizeUnit`, `sampUnitIds`, `sampEventInfo` (p. 98).
- **GBR3:** `sampId`, `repCountry`, `sampCountry`, `sampArea`, `sampY`, `sampM`,
  `sampD`, `sampSize`, `sampUnitSize`, `sampInfo`, `sampMatType`, `sampMatCode`,
  `sampMatText`, `origCountry`, `origArea`, `origFishAreaCode`, `origFishAreaText`,
  `procCountry`, `procArea`, `sampMatInfo`, together with `sampEventId` (pp. 98-99).
- **GBR4:** `sampAnId`, `sampAnRefTime`, `analysisY`, `analysisM`, `analysisD`,
  `sampAnInfo`, `anMatCode`, `anMatText`, `anMatInfo`, together with `sampId` (p. 99).

These section letters refer to the 2013 SSD2 model, as Table 9 footnote 75
states. Preserve the named identifiers as well as the descriptor fields.

**Source discrepancy:** GBR3's list of "data elements in the sections D and E"
(ChemMon 2026 pp. 98-99) does not match the element table. It includes
`sampUnitSize`, which is element C.03 and is already in GBR2's list (ChemMon
2026 p80), and it omits two Section D elements, `repYear` (D.05, p80) and
`sampSizeUnit` (D.10, p81). The guidance does not say which list validation
uses; the list above is Table 9's, unchanged.

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
| GBR39 | Error | If `resType` = LOQ and `resInfo.notSummed` is not 'Y', then `resLOQ` must be reported. |
| GBR46 | Error | If `resType` = VAL, then `resVal` must be reported. |
| GBR47 | Error | If `resType` = LOD, then `resVal` must be empty. |
| GBR48 | Error | `resVal` must be greater than 0 when reported. |
| GBR101 | Error | Unless `paramCode.base` is RF-XXXX-XXX-XXX (Not in list), the combination of `paramCode.base`, `sampId`, `sampAnId` and `anPortSeq` must be unique (p. 112). |
| GBR102 | Error | `resVal` must be greater than or equal to `resLOD`. A detected value cannot be below the limit of detection. |

The result rows above are in Table 9 pp. 102-106 and 112. Read complete rows
across page breaks: GBR47 continues from p. 105 to p. 106. Positivity and
additional threshold comparisons are in [[business-rules-gbr-results]].

## Inactive and biological-only rows

**GBR1 is inactive** (p. 98): the former `resId` uniqueness/database-key rule
is handled by the DCF schema. Inactive does not mean duplicate identifiers are
permitted by that schema.

**GBR8 is inactive** (p. 100): `progLegalRef` need not be constant merely because
records share `progId`. The source explains its deactivation allows different
legal references at result level for the same sample. This is consistent with
the `progId` / `progLegalRef` exclusion from GBR2's consistency list.

The source explicitly marks GBR6, GBR60, GBR69, GBR77, GBR85, GBR93 and GBR99
as biological-data rules (isolate consistency and isolation dates). Their IDs
are retained in the source inventory but are not presented as active chemical
monitoring requirements here. Numbering gaps are preserved; missing numbers
must not be filled with invented rules.
