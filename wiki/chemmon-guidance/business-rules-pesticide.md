---
title: "Pesticide-Specific Business Rules"
select_when: "Named pesticide CHEMON rules and their field conditions, including copper facets and uncertainty and N027A programme types. Use only when the question concerns pesticide reporting."
type: "rule-reference"
domain: "pesticide"
last_updated: "2026-11-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Table 10, pp. 126-137 (CHEMON52-CHEMON95); Table 8, p. 86 (copper)"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-legal-limits]]"
  - "[[pesticide-reporting]]"
---

# Pesticide-Specific Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Table 10, pp. 113-143 -->

## Overview

CHEMON rules whose condition is the pesticide flag (`is_pest=1`), the pesticide legal reference N027A, or the copper `paramCode`. These rules cover programme type restrictions, result type and expression constraints, evaluation codes and limit types, measurement uncertainty, copper-specific facet requirements, and non-compliant origin country validation. The Scope cell gives each rule's own trigger.

Rules that apply to PPP *and* other domains (e.g. CHEMON27, CHEMON43, CHEMON44, CHEMON58, CHEMON85, CHEMON94, CHEMON97) are in [[business-rules-cross-cutting]], as are the N027A sampling-strategy rules (CHEMON50, CHEMON51) and the N422A rules (CHEMON101, CHEMON104), which name no domain flag (ChemMon 2026 pp. 125, 138-139). Legal limit rules for pesticides are in [[business-rules-legal-limits]]. For pesticide reporting guidance, sampling strategies, copper facet coding, and worked examples, see [[pesticide-reporting]].

> **Source review (5 October 2026):** Table 10 contains CHEMON03 once, for the analytical method. The former country-consistency duplicate was a wiki attribution error and has been removed. The complete Table 10 rows, continuations, severity and comments were compared on 5 October 2026; source wording ambiguities are retained explicitly. This is an assistant review, not independent human sign-off.

## Pesticide CHEMON Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMON52 | Error | If `progLegalRef` contains N027A, `progType` can only be K005A (Official National), K009A (Official EU), K038A (Official National for Third Country Import) or K018A (Official National and EU). | N027A | 126 |
| CHEMON56 | Error | For pesticides, `exprResType` can only be B001A (Whole weight), B003A (Fat basis) or B007A (Reconstituted product). B007A is not dry weight. | PPP | 127 |
| CHEMON59 | Error | For pesticides, `evalLimitType` can only be W002A (MRL), W990A (National or local limit), or missing. | PPP | 128 |
| CHEMON60 | Error | For pesticides, `evalCode` can only be J002A (below/equal to maximum permissible quantities), J003A (above), J029A (Result not evaluated) or J031A (Compliant due to measurement uncertainty). | PPP | 128 |
| CHEMON61 | Error | For pesticides, `resType` can only be LOD, LOQ, BIN, or VAL. No other result types are accepted. | PPP | 128 |
| CHEMON70 | Error | For pesticides in egg/milk matrices, `exprResType` must be B001A (whole weight). Fat-weight or dry-weight expression is not accepted for these matrices. | PPP | 131 |
| CHEMON72 | Warning | For pesticides, `resValUncert` (measurement uncertainty) should be reported when `resType` = VAL. | PPP | 131 |
| CHEMON90_a | Warning | For copper (`paramCode` RF-0102-001-PPP), the use of facet F20 (part-consumed-analysed) and/or facet F28 (process) is needed to describe sample preparation. | `paramCode` RF-0102-001-PPP trigger; no domain condition | 135 |
| CHEMON90_b | Error | For copper (`paramCode` RF-0102-001-PPP), `resValUncert` is mandatory when `resType` = VAL. | `paramCode` RF-0102-001-PPP trigger; no domain condition | 135 |
| CHEMON95 | Warning | For PPP with `evalCode` = J003A (non-compliant), `origCountry` must be reported and must not be XX, AA, EU, XC, XD, or XE. Non-compliant results require a specific country of origin. (Amended 2026) | PPP | 137 |

The two copper rules are triggered by the `paramCode` alone; neither names a domain flag (ChemMon 2026 p135). Table 8, "Specific reporting requirements for certain contaminants, food additives and food flavourings", also lists copper with CHEMON90_a (F20 and/or F28) and CHEMON90_b (`resValUncert`) (ChemMon 2026 p86).
