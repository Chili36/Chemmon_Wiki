---
title: "VMPR-Specific Business Rules"
select_when: "Named VMPR CHEMMON rules: method accreditation, matrix facets, evaluation and geographic consistency. Check scope and collection year."
type: "rule-reference"
domain: "vmpr"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Table 10, pp. 113-143"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-baby-food]]"
  - "[[business-rules-legal-limits]]"
  - "[[vmpr-reporting]]"
---

# VMPR-Specific Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Table 10, pp. 113-143 -->

## Overview

CHEMMON rules for VMPR (Veterinary Medicinal Product Residues) reporting and V007A-accredited methods. Each row retains its exact trigger. These rules cover accreditation procedures, feed/water matrix facets, species/breed consistency, sampled/analysed matrix hierarchy validation, sampling strategy constraints for VMPR plans, evaluation code restrictions, and geographic consistency across sampling events.

Rules that apply to VMPR *and* other domains (e.g. CHEMMON27, CHEMMON43, CHEMMON58, CHEMMON85) are in [[business-rules-cross-cutting]]. Baby food exclusion rules that affect VMPR are in [[business-rules-baby-food]]. Legal limit rules for veterinary residues are in [[business-rules-legal-limits]]. For VMPR reporting guidance, sampling strategies, and worked examples, see [[vmpr-reporting]].

## VMPR CHEMMON Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON28 | Warning | For VMPR, only the recommended `sampPoint` codes from the guidance should be used. | VMPR | 119 |
| CHEMMON31 | Error | If `accredProc` is V007A (accredited and validated according to Regulation (EU) 2021/808), `anMethType` is AT08A (Confirmation), AND `paramType` is not P002A (Part of a sum), report `CCalpha`. | V007A methods | 119 |
| CHEMMON32 | Error | If `accredProc` is V007A (Regulation (EU) 2021/808) AND `anMethType` is AT06A (Screening), report `CCbeta`. The source does not give this rule the P002A exception from CHEMMON31. | V007A methods | 119-120 |
| CHEMMON73 | Warning | For VMPR feed/water matrices, F23 (target consumer/animal species) facet should be reported. | VMPR | 131 |
| CHEMMON76 | Error | For VMPR results for two or more samples (`sampId`) sharing `sampEventId`, each sample's `sampMatCode` F01 facet code must be the same. | VMPR | 131 |
| CHEMMON91 | Warning | For VMPR, only one F33 facet under A1ANN (Veterinary Medicinal Product Residues Classes) should be reported for `sampMatCode` and for `anMatCode`. | VMPR | 135 |
| CHEMMON92 | Error | For VMPR, the base terms of **`sampMatCode` and `anMatCode`** must belong to the VetDrugRes matrix hierarchy. This rule is about matrices, not `paramCode`. | VMPR | 136 |
| CHEMMON93 | Warning | For VMPR, with `progType` other than K038A and origin country equal to the reporting organisation's country, report at least one of `sampArea`, `origArea`, `origFishAreaCode`, `procArea` for J038A assessment, or empty assessment with J041A/J003A evaluation. See the parenthesized contextual reading in [[business-rules-cross-cutting]]. | VMPR; domestic origin; excludes K038A | 136 |
| CHEMMON96 | Error | For VMPR with K005A (official programme), valid sampling strategies are ST10A, ST20A, ST30A, or ST90A. (Amended 2026) | VMPR | 137 |
| CHEMMON100 | Warning | For VMPR, `evalCode` can only be J002A, J003A, J029A, J031A, **J041A (Detected)** or J040A (Not detected): six codes. The source announces Error severity in 2027; this table records 2026. | VMPR | 138 |
| CHEMMON102 | Warning | For VMPR records sharing `sampEventId`, keep `repCountry`, `sampCountry`, `sampArea`, `origCountry`, `origArea`, `origFishAreaCode`, `origFishAreaText`, `procCountry` and `procArea` constant. | VMPR | 139 |
