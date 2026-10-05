---
title: "GBR: Percentages, Evaluation Limits and Decision Thresholds"
select_when: "Generic SSD2 percentage ranges, fat/dry-weight conditions, evaluation-limit comparisons, positive LOD/LOQ/recovery/uncertainty, CCalpha/CCbeta and the V999A exception. Includes Warning rules GBR22 and GBR42; core BIN/unit rules are on business-rules-gbr."
type: "rule-reference"
domain: "all"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 101-106 (Table 9)"
related:
  - "[[business-rules-gbr]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-legal-limits]]"
  - "[[ssd2-result-expression-basis]]"
  - "[[ssd2-result-method-accreditation]]"
  - "[[ssd2-result-recovery-correction]]"
  - "[[ssd2-result-uncertainty]]"
  - "[[ssd2-evaluation-limits]]"
---

# GBR: Percentages, Evaluation Limits and Decision Thresholds

<!-- Source: ChemMon 2026 Table 9, pp. 101-106 -->

These 20 rules are Active in the 2026 source. **GBR22 and GBR42 are Warnings**;
the other 18 are Errors. Read range and comparison rules together with field
presence requirements and domain-specific conditions. A numeric constraint
alone is not a complete specification of when a field must be supplied.

Core result shape, units, LOD/LOQ presence and result uniqueness are in
[[business-rules-gbr]]. These GBR rules concern SSD2, not the parallel PRE/USE
data models.

## Percentages and expression basis

| Rule ID | Severity | Condition and requirement | Source page |
| --- | --- | --- | --- |
| GBR19 | Error | `exprResPerc.fatPerc` must express a percentage between 0 and 100; report 40 for 40%, not 0.4. | 101 |
| GBR20 | Error | `exprResPerc.moistPerc` must express a percentage between 0 and 100. | 101-102 |
| GBR21 | Error | `exprResPerc.alcoholPerc` must express a percentage between 0 and 100. | 102 |
| GBR22 | Warning | If `exprResType` is B003A (Fat weight), `exprResPerc.fatPerc` should be reported. Omission triggers a Warning. | 102 |
| GBR23 | Error | If `exprResType` is B002A (Dry matter), `exprResPerc.moistPerc` must be reported. | 102 |

Do not apply the Warning severity of the fat-weight rule to the dry-matter
rule. See [[ssd2-result-expression-basis]] for the field descriptions and
[[business-rules-cross-cutting]] for additional CHEMMON plausibility checks.

## Evaluation limits and result comparison

| Rule ID | Severity | Condition and requirement | Source page |
| --- | --- | --- | --- |
| GBR30 | Error | If `evalLowLimit` is supplied, `evalLimitType` must be supplied. | 103 |
| GBR32 | Error | `evalHighLimit` must be strictly greater than `evalLowLimit`. | 103 |
| GBR33 | Error | If `resVal` is greater than `evalLowLimit`, `evalCode` must not be J002A (below or equal to the level of concern). | 103-104 |
| GBR34 | Error | If `evalCode` is J003A (above the level of concern) or J031A (compliant due to measurement uncertainty), and `evalLimitType` differs from W005A (MRPL), then `resVal` must be strictly greater than `evalLowLimit`. | 104 |
| GBR35 | Error | If `evalCode` is J002A, `resVal` must be less than or equal to `evalLowLimit`. | 104 |

For GBR34, the source description requires **greater than**; its shorter error
message mentions “lower than”. The wiki preserves the full description's
strict comparison, including the W005A exception, rather than inferring that
equality passes. Domain-specific LL rules have additional prerequisites;
see [[business-rules-legal-limits]].

## Detection and decision thresholds

| Rule ID | Severity | Condition and requirement | Source page |
| --- | --- | --- | --- |
| GBR38 | Error | `resLOD` must be greater than 0. | 104 |
| GBR40 | Error | `resLOQ` must be greater than 0. | 105 |
| GBR41 | Error | If `resType` is CCA and `accredProc` is not V999A (Not Validated), `CCalpha` must be supplied. Unvalidated methods are excluded from this presence condition. | 105 |
| GBR42 | Warning | `CCalpha` must be less than `CCbeta`. The source uses “must” in the description but assigns Warning severity to a failed comparison. | 105 |
| GBR43 | Error | `CCalpha` must be greater than 0. | 105 |
| GBR44 | Error | If `resType` is CCB and `accredProc` is not V999A (Not Validated), `CCbeta` must be supplied. Unvalidated methods are excluded from this presence condition. | 105 |
| GBR45 | Error | `CCbeta` must be greater than 0. | 105 |

The V999A exception belongs to the **presence** rules GBR41/44. It does not
remove the separate positivity constraints GBR43/45. For VMPR-specific method
and threshold guidance, use [[ssd2-result-method-accreditation]].

## Recovery and uncertainty values

| Rule ID | Severity | Condition and requirement | Source page |
| --- | --- | --- | --- |
| GBR49 | Error | `resValRec` must be greater than 0. | 106 |
| GBR50 | Error | `resValUncertSD` must be greater than 0. | 106 |
| GBR51 | Error | `resValUncert` must be greater than 0. | 106 |

Keep recovery rate, uncertainty standard deviation and uncertainty distinct.
Additional recovery ranges and recommendations are defined by CHEMMON rules;
these three GBR rows do not replace them.
