---
title: "Cross-Cutting CHEMMON Business Rules"
select_when: "Named cross-domain CHEMMON rules: analytical methods, result shape, sample/programme consistency, action-taken warnings, domain routing. Select when their conditions are relevant."
type: "rule-reference"
domain: "cross-cutting"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Table 10, pp. 113-143"
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

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Table 10, pp. 113-143 -->

## Overview

This page groups CHEMMON rules shared by multiple reporting domains. Read each rule's domain and trigger conditions before applying it. Select relevant rules alongside domain guidance when the question needs them.

Rules are grouped here by topic; the source definitions are in Table 10, pp. 113-143. Domain-specific rules live in [[business-rules-vmpr]], [[business-rules-pesticide]], [[business-rules-contaminant]], [[business-rules-additives]], and [[business-rules-baby-food]]. General Business Rules (GBR) are in [[business-rules-gbr]].

> **Source review (5 October 2026):** Table 10 contains CHEMON03 once, for the analytical method. The former country-consistency duplicate was a wiki attribution error and has been removed. The wiki spelling CHEMMON maps to CHEMON in this source. The complete Table 10 rows, continuations, severity and comments were compared on 5 October 2026; source wording ambiguities are retained explicitly. This is an assistant review, not independent human sign-off.

## Analytical Method Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON03 | Error | `anMethCode.base` is mandatory. The base term for the analytical method must be reported. | All | 113 |
| CHEMMON23 | Error | `anMethType` must be Screening (AT06A) or Confirmation (AT08A). No other method types are accepted. | All | 118 |
| CHEMMON30 | Error | If `evalCode` = J003A (Above the level of concern), `anMethType` must be Confirmation (AT08A). Non-compliant findings require a confirmatory method. | All | 119 |
| CHEMMON33 | Error | If `resType` is BIN, `anMethType` must be AT06A (Screening). The description says “should”, but the published severity is Error. | All | 120 |
| CHEMMON34 | Warning | If `anMethType` is AT08A (Confirmation), `resType` should not be BIN AND `resQualValue` should be empty. | All | 120 |
| CHEMMON79 | Error | For contaminants, additives or flavourings, `anMethCode` must differ from F500A (Unknown), F598A (Unspecified) and F001A (Classification not possible). Merged CHEMON79_a/b/c; the row's stated scope remains these three domains. | CONT/FA/FF | 132 |

## Result Value & Type Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON04 | Warning | `resValRec` should be at least 1; percentages use 85 for 85%, not 0.85. | All | 113 |
| CHEMMON05 | Warning | `resValRec` should be between 50 and 150. | All | 113 |
| CHEMMON08 | Error | If `resVal` equals `resLOQ`, `resType` must be VAL (quantified value). (Amended 2026) | All | 114 |
| CHEMMON24 | Error | `resQualValue` must be NEG (negative/absent), except when `paramCode` is specifically RF-00011484-PAR (MOAHs 3 to 7 ring). This is not an exception for every MOAH parameter. | All; specific parameter exception | 118 |
| CHEMMON40 | Error | If `resType` is BIN, LOQ or LOD, `resVal` must be empty. This includes below-LOQ/LOD results, not just binary results. | All | 122 |
| CHEMMON41 | Warning | If `resType` is VAL, `resLOQ` should not exceed `resVal`. | All | 122 |
| CHEMMON42 | Warning | If `resValRecCorr` is Y, `resValRec` should be reported. The error-message text mentions mean recovery of 70–120%; the rule description itself specifies the presence condition, not an additional numeric-range predicate. | All | 122 |
| CHEMMON44 | Error | `resLOQ` must be reported unless the method is unvalidated, `resInfo.notSummed` = Y, the domain is VMPR, or `resType` = BIN. | PPP/CONT/FA/FF | 123 |
| CHEMMON45 | Error | If `accredProc` is not Not validated AND `resInfo.notSummed` is not Y, report at least one of `resLOQ`, `resLOD`, `CCbeta` or `CCalpha`. | All; validation/notSummed exceptions | 123-124 |
| CHEMMON46 | Error | If `evalCode` is J003A OR J031A, AND `evalLimitType` is not W012A (Presence), `resType` must be VAL. | All | 124 |
| CHEMMON48 | Warning | If `paramType` is not P002A (Part of a sum) AND `resVal` is greater than or equal to `evalLowLimit`, `evalCode` should differ from J029A (Result not evaluated). | All | 124 |
| CHEMMON57 | Error | The pair (`paramCode`, `sampId`) must be unique, **except for analyses on aflatoxins**. This is distinct from GBR101's four-field key and parameter exception. | All; aflatoxin exception | 127 |
| CHEMMON62 | Error | If `resInfo.notSummed` is Y, the result must concern a multicomponent/sum and at least one component's LOQ must be reported. | All | 128 |
| CHEMMON78 | Error | If `resType` = BIN (binary), `resLOQ` must be empty. Binary results do not carry an LOQ. | All | 132 |
| CHEMMON82 | Error | `resLOQ` cannot be a placeholder value (99999, 999, 9999, 999999, 9999999). Real LOQ values must be reported. | All | 132 |

## Sampling & Programme Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON22 | Warning | If `sampInfo.origSampId` is reported, `sampStrategy` should be ST30A (Suspect sampling). | All | 118 |
| CHEMMON43 | Error | For pesticides/VMPR, `sampY` (sampling year) must be <= submission year minus 1. Data must be submitted within the expected reporting window. | PPP/VMPR | 123 |
| CHEMMON50 | Error | If `progType` is K018A (Official National and EU) or K009A (Official EU), AND `progLegalRef` contains N027A (Regulation 396/2005), `sampStrategy` can only be ST10A (Objective) or ST20A (Selective). | N027A | 125 |
| CHEMMON51 | Error | If `progLegalRef` contains N027A (Regulation 396/2005), `sampStrategy` can only be ST10A (Objective), ST20A (Selective) or ST30A (Suspect). CHEMMON50 further narrows K018A/K009A cases. | N027A | 125 |
| CHEMMON54 | Error | If `progLegalRef` is N317A (Regulation (EU) 2019/1793), `progType` must be K019A (EU increased control programme on imported food) AND `sampStrategy` must be ST30A (Suspect). | N317A; no contaminant-only restriction | 126 |
| CHEMMON58 | Error | For pesticides/VMPR, `sampCountry` must equal `reportingOrgCountry`. This compares sampling and reporting countries; it does not require the product origin to match. | PPP/VMPR | 127 |
| CHEMMON68 | Error | `progLegalRef` domain must match `paramCode` domain. The legal reference must correspond to the substance domain being reported. | All | 130 |
| CHEMMON77 | Error | For pooled samples (`sampMethod` N002A/N031A), `sampUnitSizeUnit` must be G005A and `sampUnitSize` must equal the number of units pooled. | All | 131 |
| CHEMMON94 | Error | For K038A (import control), `sampPoint` can only be E010A (Border Control Posts). Import samples must be taken at the border. (Amended 2026) | All | 136-137 |
| CHEMMON97 | Error | For PPP/CONT/ADD/FLAV with K005A, valid sampling strategies are ST10A, ST20A, or ST30A. (New 2026) | PPP/CONT/FA/FF | 137 |
| CHEMMON99 | Warning | If `progType` is K038A or K019A OR `sampPoint` is E010A, `origCountry` must differ from `sampCountry`. K019A is EU increased control on imported food, not general monitoring. | Import-control triggers | 138 |

## Matrix & Facet Rules (cross-domain)

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON06 | Warning | `exprResPerc.fatPerc` should be at least 1; percentages use 85 for 85%. This is a plausibility warning, not a ban on genuinely low fat content. | All | 113 |
| CHEMMON07 | Warning | `exprResPerc.moistPerc` should be at least 1; percentages use 85 for 85%. | All | 113 |
| CHEMMON27 | Warning | For VMPR/pesticides, `sampMatCode` should equal `anMatCode`. The sampled and analysed matrices are usually the same. | VMPR/PPP | 118 |
| CHEMMON103 | Warning | Do not report both Organic production (A07SE) and Conventional non-organic production (A0C6Y) in `sampMatCode.prod`. The source says a sample with both will be considered organic; the inconsistency still warns. | All | 139 |
| CHEMMON83 | Warning | If `sampMatCode` contains facet F10.A18PX, F19 (packaging material) and F18 (packaging format) should not be reported. F10.A18PX is a facet, not a complete base-term code. | F10.A18PX trigger | 132 |

## Evaluation & Action Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON26 | Warning | If `actTakenCode` is I (Follow-up investigation), `evalInfo.conclusion` should be reported. | All | 118 |
| CHEMMON35 | Warning | Recommended `evalLimitType` codes are W002A (MRL), W005A (MRPL), W006A (Reference point of action), W012A (Presence), W001A (Maximum limit), W007A (Action level), W008A (Target level), W990A (National or local limit). | All | 120 |
| CHEMMON36 | Warning | If `evalLimitType` is W002A (MRL), `evalCode` should be J002A (below/equal to limit), J003A (above limit), J031A (compliant due to measurement uncertainty), or J029A (result not evaluated). | All; W002A trigger | 121 |
| CHEMMON37 | Warning | For contaminants, additives or flavourings, when `evalCode` = J041A (Detected) or J003A (Above maximum permissible quantities), `actTakenCode` should be reported (Table 10, p. 121). | CONT/FA/FF | 121 |
| CHEMMON65 | Error | `evalInfo.resAsses` can only be J037A (Compliant) or J038A (Non-compliant). Preserve the source field spelling `resAsses`. | All | 129 |
| CHEMMON66_a | Warning | For a compliant assessment (`evalInfo.resAsses` J037A) conflicting with `evalCode` J003A, or with detected J041A and Presence limit W012A, report `evalInfo.conclusion`. See the source-wording note below before implementing Boolean logic. | All | 129 |
| CHEMMON66_b | Warning | If `evalInfo.resAsses` is J038A AND `evalCode` is not J003A AND `evalCode` is not J041A AND `evalLimitType` is not W012A, report `evalInfo.conclusion`. Keep all three negative conditions; this is not simply the negation of CHEMMON66_a. | All | 130 |
| CHEMMON67 | Warning | `evalInfo.sampTkAsses` and `evalInfo.sampEventAsses` should not be reported; the source says they will not be used for pesticide/VMPR report analysis. | All | 130 |
| CHEMMON85 | Error | For VMPR/PPP, report `actTakenCode` when result assessment is J038A (Non-compliant), or when assessment is empty and `evalCode` is J041A (Detected) or J003A (Above maximum permissible quantities). See the source-wording note below. | VMPR/PPP | 133 |

## FoodEx2 Validation Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| FOODEX2_SAMPMAT | Error | `sampMatCode` must follow FoodEx2 coding rules. The sampled matrix must be a valid FoodEx2 term with correct facet usage. | All | 141 |
| FOODEX2_ANMAT | Error | `anMatCode` must follow FoodEx2 coding rules. The analysed matrix must be a valid FoodEx2 term with correct facet usage. | All | 141 |

## Import-control matrix and origin

<!-- Source: ChemMon 2026 Table 10, p. 129 -->

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON64 | Error | For samples under Regulation (EU) 2019/1793 (`progLegalRef` N317A), `origCountry` and `sampMatCode` must be values listed in that regulation. | N317A | 129 |
| CHEMMON105 | Error | If `progLegalRef` is N317A (Regulation (EU) 2019/1793), no other `progLegalRef` can be used on that record. | N317A; no contaminant-only restriction | 139 |

## Source wording and inactive rows

The Table 10 descriptions mix “and” and “or” without parentheses in
CHEMON66_a (p. 129), CHEMON85 (p. 133) and CHEMON93 (p. 136). The summaries
above group the assessment/evaluation alternatives under the stated domain
and, for CHEMON93, origin/programme conditions. This is a contextual reading,
not a verified executable EFSA predicate. The error-message columns abbreviate
these conditions and are not a substitute for the full description. In
particular, keep the Presence condition in CHEMON66_a and the three separate
negative conditions in CHEMON66_b. Resolve exact Boolean precedence against
the collection's executable rules before implementing these as a validator.

CHEMON47 and CHEMON81 are inactive because CHEMON40 covers their result-value
cases; CHEMON49 is inactive because CHEMON50 incorporates it; CHEMON53 is
inactive following the 2025 Table 2 update (pp. 124-126, 132). They are retained
in the source inventory and annual-change notes, not active rule definitions.

**DOMAIN VALIDATION** (p. 113) flags incoming records using `progLegalRef` and
`paramCode.base`; it does not generate an Error or Warning. It and the two
FoodEx2 rules are additional named Table 10 rows outside the five-family
GBR/CHEMON/LL/PRE/USE ID inventory.
