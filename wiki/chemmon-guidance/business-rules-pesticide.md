---
title: "Pesticide-Specific Business Rules"
select_when: "Named pesticide CHEMMON rules and their field conditions, including copper uncertainty and programme constraints. Use only when the question concerns pesticide reporting."
type: "rule-reference"
domain: "pesticide"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Tables 9-10, pp. 98-143"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-legal-limits]]"
  - "[[pesticide-reporting]]"
---

# Pesticide-Specific Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Tables 9-10, pp. 98-143 -->

## Overview

CHEMMON rules that apply exclusively to the pesticide residues (PPP) reporting domain. These rules cover country-of-sampling requirements, sampling year validation, programme type restrictions, result type and expression constraints, measurement uncertainty, copper-specific facet requirements, non-compliant origin country validation, and 2026 programme reference exclusivity rules.

Rules that apply to PPP *and* other domains (e.g. CHEMMON27, CHEMMON43, CHEMMON44, CHEMMON58, CHEMMON85, CHEMMON94, CHEMMON97) are in [[business-rules-cross-cutting]]. Legal limit rules for pesticides are in [[business-rules-legal-limits]]. For pesticide reporting guidance, sampling strategies, copper facet coding, and worked examples, see [[pesticide-reporting]].

> **Source review (5 October 2026):** Table 10 contains CHEMON03 once, for the analytical method. The former country-consistency duplicate was a wiki attribution error and has been removed. The wiki spelling CHEMMON maps to CHEMON in this source. Full semantic review of the remaining rule descriptions is still open.

## Pesticide CHEMMON Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON52 | Error | For pesticides with N027A, valid `progType` values are K005A (Official/National), K009A (EU coordinated), K038A (Import control), or K018A (Other official). | PPP |
| CHEMMON56 | Error | For pesticides, `exprResType` can only be B001A (whole weight), B003A (fat weight), or B007A (dry weight). | PPP |
| CHEMMON59 | Error | For pesticides, `evalLimitType` can only be W002A (MRL), W990A (Other), or left empty. | PPP |
| CHEMMON60 | Error | For pesticides, `evalCode` must be J002A (Below MRL), J003A (Above MRL), J029A (Below LOQ), or J031A (At or about MRL). | PPP |
| CHEMMON61 | Error | For pesticides, `resType` can only be LOD, LOQ, BIN, or VAL. No other result types are accepted. | PPP |
| CHEMMON70 | Error | For pesticides in egg/milk matrices, `exprResType` must be B001A (whole weight). Fat-weight or dry-weight expression is not accepted for these matrices. | PPP |
| CHEMMON72 | Warning | For pesticides, `resValUncert` (measurement uncertainty) should be reported when `resType` = VAL. | PPP |
| CHEMMON90_a | Warning | For copper (`paramCode` RF-0102-001-PPP), the use of facet F20 (part-consumed-analysed) and/or facet F28 (process) is needed to describe sample preparation. | PPP |
| CHEMMON90_b | Error | For copper (`paramCode` RF-0102-001-PPP), `resValUncert` is mandatory when `resType` = VAL. | PPP |
| CHEMMON95 | Warning | For PPP with `evalCode` = J003A (non-compliant), `origCountry` must not be XX, AA, EU, XC, XD, or XE. Non-compliant results require a specific country of origin. (Amended 2026) | PPP |
| CHEMMON101 | Error | For N422A (new regulation reference), `progType` must be K019A and `sampStrategy` must be ST30A. (New 2026) | PPP |
| CHEMMON104 | Error | N422A is exclusive -- it cannot be concatenated with other `progLegalRef` values in the same record. (New 2026) | PPP |
