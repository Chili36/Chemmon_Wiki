---
title: "VMPR-Specific Business Rules"
type: "rule-reference"
domain: "vmpr"
last_updated: "2026-04-10"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Annex B"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-baby-food]]"
  - "[[business-rules-legal-limits]]"
  - "[[vmpr-reporting]]"
---

# VMPR-Specific Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Annex B -->

## Overview

CHEMMON rules that apply exclusively to the VMPR (Veterinary Medicinal Product Residues) reporting domain. These rules cover accreditation procedures, feed/water matrix facets, species/breed consistency, paramCode hierarchy validation, sampling strategy constraints for VMPR plans, evaluation code restrictions, and geographic consistency across sampling events.

Rules that apply to VMPR *and* other domains (e.g. CHEMMON27, CHEMMON43, CHEMMON58, CHEMMON85, CHEMMON27) are in [[business-rules-cross-cutting]]. Baby food exclusion rules that affect VMPR are in [[business-rules-baby-food]]. Legal limit rules for veterinary residues are in [[business-rules-legal-limits]]. For VMPR reporting guidance, sampling strategies, and worked examples, see [[vmpr-reporting]].

## VMPR CHEMMON Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON28 | Warning | For VMPR, only the recommended `sampPoint` codes from the guidance should be used. | VMPR |
| CHEMMON31 | Error | If `accredProc` = V007A (Decision 2002/657/EC) and method is Confirmation, CCalpha (decision limit) is mandatory. | VMPR |
| CHEMMON32 | Error | If `accredProc` = V007A and method is Screening, CCbeta (detection capability) is mandatory. | VMPR |
| CHEMMON73 | Warning | For VMPR feed/water matrices, F23 (target consumer/animal species) facet should be reported. | VMPR |
| CHEMMON76 | Error | For VMPR with the same `sampEventId`, the F01 (species/breed) facet must be identical across all samples in the event. | VMPR |
| CHEMMON91 | Warning | For VMPR, only one F33 (legislative class) facet under VR classes should be reported per sample. Multiple VR classes per sample are discouraged. | VMPR |
| CHEMMON92 | Error | For VMPR, the base term of `paramCode` must belong to the vetDrugRes hierarchy. Only recognised veterinary drug residue parameters are accepted. | VMPR |
| CHEMMON93 | Warning | For non-compliant VMPR Plan 1/2 results, `sampArea` (geographic area) reporting is required to enable traceability. | VMPR |
| CHEMMON96 | Error | For VMPR with K005A (official programme), valid sampling strategies are ST10A, ST20A, ST30A, or ST90A. (Amended 2026) | VMPR |
| CHEMMON100 | Warning | For VMPR, `evalCode` is restricted to J002A, J003A, J029A, J031A, or J040A. Other evaluation codes are not valid for veterinary residue data. (New 2026) | VMPR |
| CHEMMON102 | Warning | For VMPR with the same `sampEventId`, geographic fields (`sampCountry`, `sampArea`, `origCountry`, `origArea`) must be constant across all records in the event. (New 2026) | VMPR |
