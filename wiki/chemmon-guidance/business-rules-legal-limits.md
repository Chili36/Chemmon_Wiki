---
title: "Legal Limit Business Rules"
select_when: "LL rules: numeric result and unprocessed-sample prerequisites, MRL/MPL evaluation comparisons, legal parameter/matrix combinations and part-of-sum exception."
type: "rule-reference"
domain: "cross-cutting"
last_updated: "2026-10-13"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 141-143, Table 10"
related:
  - "[[business-rules]]"
  - "[[legal-limits-database]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-additives]]"
  - "[[business-rules-cross-cutting]]"
  - "[[pesticide-residue-definition-by-matrix]]"
---

# Legal Limit Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, pp. 141-143, Table 10 -->

## Overview

Legal limit rules compare reported result values against regulatory thresholds (MRLs, MLs, MPLs). They ensure that evaluation codes are consistent with the numeric comparison between result values and applicable limits, and that parameter/matrix combinations match the legal limits database.

Apply each rule only within its stated domain and conditions; see [[business-rules-vmpr]], [[business-rules-pesticide]], and [[business-rules-additives]] for the underlying CHEMMON rules they interact with.

## VMPR & Pesticide Legal Limits

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| LL_01_VMPR | Warning | For VMPR, when `resType` = VAL, the sample is unprocessed, and `evalLimitType` is W002A (MRL) or empty: if `resVal` > MRL, `evalCode` must differ from J002A. | VMPR |
| LL_01_PPP | Error | Same conditions as LL_01_VMPR, for pesticides: if `resVal` > MRL, `evalCode` must differ from J002A. | PPP |
| LL_02_VMPR | Warning | For VMPR, when `resType` = VAL, the sample is unprocessed, and `evalLimitType` is W002A or empty: if `resVal` <= MRL, `evalCode` must differ from J003A and J031A. | VMPR |
| LL_02_PPP | Error | Same conditions as LL_02_VMPR, for pesticides: if `resVal` <= MRL, `evalCode` must differ from J003A and J031A. | PPP |

## Food Additives & Flavourings Legal Limits

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| LL_01_FA_FF | Warning | When `resType` = VAL and `evalLimitType` is W016A (MPL) or empty: if `resVal` > MPL, `evalCode` should differ from J002A and J037A. | FA/FF |
| LL_02_FA_FF | Warning | When `resType` = VAL and `evalLimitType` is W016A or empty: if `resVal` <= MPL, `evalCode` should differ from J003A and J038A. | FA/FF |
| LL_03_FA_FF | Warning | The reported substance should be authorised for the legislative category and restriction/exception under Regulations 1333/2008 and 1334/2008. | FA/FF |

## General Legal Limit Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| LL_03 | Error | `paramType` must be reported for multi-component or sum parameters. The parameter type (individual, sum, complex) must be declared to enable correct limit comparison. | All |
| LL_03_b | Warning | `paramType` should equal the pre-assigned `paramType` (p. 143). | All |
| LL_04 | Error | For pesticides, where `paramCode` is in the legal limits database, the sampled matrix and `paramCode.base` must match a plausible legal combination (`PlausibleCombinationPPP=1`), unless the result is a part of sum. The source groups LL_04/LL_04_b in one row. | PPP |
| LL_04_b | Error | Same grouped source definition and part-of-sum exception as LL_04. Table 10 does not define a separate `anMatCode` condition for this ID. | PPP |

LL_04 fails when a pesticide's residue definition differs by commodity and the reported `paramCode` belongs to another commodity's definition. See [[pesticide-residue-definition-by-matrix]] for choosing the code.
