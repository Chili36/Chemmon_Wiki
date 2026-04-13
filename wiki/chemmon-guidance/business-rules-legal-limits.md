---
title: "Legal Limit Business Rules"
type: "rule-reference"
domain: "cross-cutting"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Annex B"
related:
  - "[[business-rules]]"
  - "[[legal-limits-database]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-additives]]"
  - "[[business-rules-cross-cutting]]"
---

# Legal Limit Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Annex B -->

## Overview

Legal limit rules compare reported result values against regulatory thresholds (MRLs, MLs, MPLs). They ensure that evaluation codes are consistent with the numeric comparison between result values and applicable limits, and that parameter/matrix combinations match the legal limits database.

These rules span all reporting domains; see [[business-rules-vmpr]], [[business-rules-pesticide]], and [[business-rules-additives]] for the underlying CHEMMON rules they interact with.

## VMPR & Pesticide Legal Limits

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| LL_01_VMPR | Warning | If `resVal` exceeds the MRL for veterinary residues, `evalCode` must reflect non-compliance. | VMPR |
| LL_01_PPP | Error | If `resVal` exceeds the MRL for pesticides, `evalCode` must reflect non-compliance. | PPP |
| LL_02_VMPR | Warning | If `resVal` <= MRL for veterinary residues, `evalCode` must not indicate non-compliance. | VMPR |
| LL_02_PPP | Error | If `resVal` <= MRL for pesticides, `evalCode` must not indicate non-compliance. | PPP |

## Food Additives & Flavourings Legal Limits

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| LL_01_FA_FF | Warning | Maximum Permitted Level (MPL) comparison -- if `resVal` exceeds the MPL, the evaluation should reflect this. (New 2026) | FA/FF |
| LL_02_FA_FF | Warning | MPL threshold evaluation -- if `resVal` <= MPL, the evaluation should not indicate exceedance. (New 2026) | FA/FF |
| LL_03_FA_FF | Warning | Substance authorisation check -- the reported substance must be authorised for the declared food category under the applicable regulation. (New 2026) | FA/FF |

## General Legal Limit Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| LL_03 | Error | `paramType` must be reported for multi-component or sum parameters. The parameter type (individual, sum, complex) must be declared to enable correct limit comparison. | All |
| LL_03_b | Warning | `paramType` should equal the pre-assigned `paramType` from the EFSA parameter catalogue. Deviations should be justified. | All |
| LL_04 | Error | For pesticides, the `sampMatCode`/`paramCode` combination must match entries in the legal limits database. Only valid matrix/substance pairs are accepted. | PPP |
| LL_04_b | Error | For pesticides, the `anMatCode`/`paramCode` combination must match entries in the legal limits database. | PPP |
