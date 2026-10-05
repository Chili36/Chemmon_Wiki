---
title: "Pesticide-Specific Business Rules"
select_when: "Named pesticide CHEMMON rules and their field conditions, including copper uncertainty and programme constraints. Use only when the question concerns pesticide reporting."
type: "rule-reference"
domain: "pesticide"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Table 10, pp. 113-143"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-legal-limits]]"
  - "[[pesticide-reporting]]"
---

# Pesticide-Specific Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Table 10, pp. 113-143 -->

## Overview

CHEMMON rules that apply exclusively to the pesticide residues (PPP) reporting domain. These rules cover country-of-sampling requirements, sampling year validation, programme type restrictions, result type and expression constraints, measurement uncertainty, copper-specific facet requirements, non-compliant origin country validation, and 2026 programme reference exclusivity rules.

Rules that apply to PPP *and* other domains (e.g. CHEMMON27, CHEMMON43, CHEMMON44, CHEMMON58, CHEMMON85, CHEMMON94, CHEMMON97) are in [[business-rules-cross-cutting]]. Legal limit rules for pesticides are in [[business-rules-legal-limits]]. For pesticide reporting guidance, sampling strategies, copper facet coding, and worked examples, see [[pesticide-reporting]].

> **Source review (5 October 2026):** Table 10 contains CHEMON03 once, for the analytical method. The former country-consistency duplicate was a wiki attribution error and has been removed. The wiki spelling CHEMMON maps to CHEMON in this source. The complete Table 10 rows, continuations, severity and comments were compared on 5 October 2026; source wording ambiguities are retained explicitly. This is an assistant review, not independent human sign-off.

## Pesticide CHEMMON Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON52 | Error | If `progLegalRef` contains N027A, `progType` can only be K005A (Official National), K009A (Official EU), K038A (Official National for Third Country Import) or K018A (Official National and EU). | N027A | 126 |
| CHEMMON56 | Error | For pesticides, `exprResType` can only be B001A (Whole weight), B003A (Fat basis) or B007A (Reconstituted product). B007A is not dry weight. | PPP | 127 |
| CHEMMON59 | Error | For pesticides, `evalLimitType` can only be W002A (MRL), W990A (National or local limit), or missing. | PPP | 128 |
| CHEMMON60 | Error | For pesticides, `evalCode` can only be J002A (below/equal to maximum permissible quantities), J003A (above), J029A (Result not evaluated) or J031A (Compliant due to measurement uncertainty). | PPP | 128 |
| CHEMMON61 | Error | For pesticides, `resType` can only be LOD, LOQ, BIN, or VAL. No other result types are accepted. | PPP | 128 |
| CHEMMON70 | Error | For pesticides in egg/milk matrices, `exprResType` must be B001A (whole weight). Fat-weight or dry-weight expression is not accepted for these matrices. | PPP | 131 |
| CHEMMON72 | Warning | For pesticides, `resValUncert` (measurement uncertainty) should be reported when `resType` = VAL. | PPP | 131 |
| CHEMMON90_a | Warning | For copper (`paramCode` RF-0102-001-PPP), the use of facet F20 (part-consumed-analysed) and/or facet F28 (process) is needed to describe sample preparation. | PPP | 135 |
| CHEMMON90_b | Error | For copper (`paramCode` RF-0102-001-PPP), `resValUncert` is mandatory when `resType` = VAL. | PPP | 135 |
| CHEMMON95 | Warning | For PPP with `evalCode` = J003A (non-compliant), `origCountry` must be reported and must not be XX, AA, EU, XC, XD, or XE. Non-compliant results require a specific country of origin. (Amended 2026) | PPP | 137 |
| CHEMMON101 | Error | If `progLegalRef` is N422A (Regulation (EU) 2019/1873), `progType` must be K019A (EU increased control programme on imported food) AND `sampStrategy` must be ST30A (Suspect). | N422A | 138-139 |
| CHEMMON104 | Error | If `progLegalRef` is N422A (Regulation (EU) 2019/1873), no other `progLegalRef` can be concatenated. | N422A | 139 |
