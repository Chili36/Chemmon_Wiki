---
title: "GBR: Identifier Consistency, Matrix Text and Size Units"
select_when: "Generic SSD2 rules for shared sample portions, organisation/laboratory/method identifiers, processing country, Other matrix text, unclassifiable method text, sample-size units and analysed-sample ID. GBR5/7/10/11/14/15/16/18/24/25/26/103."
type: "rule-reference"
domain: "all"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 99-102, 112 (Table 9)"
related:
  - "[[business-rules-gbr]]"
  - "[[ssd2-analysis-context]]"
  - "[[ssd2-analysis-laboratory]]"
  - "[[ssd2-analysis-methods]]"
  - "[[ssd2-matrix-sampled-matrix]]"
  - "[[ssd2-matrix-analysed-sample]]"
  - "[[ssd2-sampling-event-and-unit]]"
---

# GBR: Identifier Consistency, Matrix Text and Size Units

<!-- Source: ChemMon 2026 Table 9, pp. 99-102, 112 -->

These 12 rules are **Active, Error** in the 2026 source table. They apply to
SSD2 fields; they are not PRE or USE rules for the parallel FA/FF collections.
The broader GBR index, sample/event consistency rules and result uniqueness
rule are in [[business-rules-gbr]].

## Shared identifiers and portion descriptors

| Rule ID | Severity | Condition and requirement | Source page |
| --- | --- | --- | --- |
| GBR5 | Error | When both `sampAnId` and `anPortSeq` are reported, records with the same pair must have identical portion descriptors: `anPortSeq`, `anPortSize`, `anPortSizeUnit`, `anPortInfo` (SSD2 Section H). | 99 |
| GBR7 | Error | When `localOrgId` is reported, `localOrgCountry` must be constant for all records sharing that `localOrgId`. | 100 |
| GBR10 | Error | `labCountry` must be constant for all records sharing the same `labId`. | 100 |
| GBR11 | Error | `anMethRefCode`, `anMethCode`, `anMethText` and `anMethInfo` must be constant for all records sharing the same `anMethRefId`. | 100 |
| GBR103 | Error | If `anMatCode` is reported, report `sampAnId` as well. The source description says it “should” be reported, but the published validation severity for a missing value is Error. | 112 |

Do not merge these keys: a portion is identified by `sampAnId` **and**
`anPortSeq`; a laboratory is grouped by `labId`, and a method by `anMethRefId`.
The result-uniqueness rule GBR101 has its own four-field key and “Not in list”
exception, documented in [[business-rules-gbr]].

## Processing location and explanatory text

| Rule ID | Severity | Condition and requirement | Source page |
| --- | --- | --- | --- |
| GBR14 | Error | `procArea` must be within `procCountry`. | 101 |
| GBR15 | Error | If the generic-term facet `sampMatCode.gen` is A07XE (Other), `sampMatText` must be supplied. | 101 |
| GBR16 | Error | If the generic-term facet `anMatCode.gen` is A07XE (Other), `anMatText` must be supplied. | 101 |
| GBR18 | Error | If `anMethCode.base` is F001A (Classification not possible), `anMethText` must be supplied. | 101 |

GBR18 describes a text requirement; it does **not** authorise F001A in a domain
that separately forbids that method code. Check CHEMMON79 for contaminants,
additives and flavourings in [[business-rules-cross-cutting]]. Likewise, GBR15
and GBR16 concern the generic-term facet, not every base term whose label
happens to contain the word “other”.

## Units paired with sample-size values

| Rule ID | Severity | Condition and requirement | Source page |
| --- | --- | --- | --- |
| GBR24 | Error | If `sampUnitSize` is reported, `sampUnitSizeUnit` must be reported. | 102 |
| GBR25 | Error | If `sampSize` is reported, `sampSizeUnit` must be reported. | 102 |
| GBR26 | Error | If `anPortSize` is reported, `anPortSizeUnit` must be reported. | 102 |

These are three different size/unit pairs. Result concentration units use
`resUnit` and GBR27/29 instead; see [[ssd2-result-units-and-limits]].
