---
title: "Food Additives & Flavourings Business Rules"
type: "rule-reference"
domain: "additives"
last_updated: "2026-04-10"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Annex B"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-legal-limits]]"
  - "[[food-additives-reporting]]"
---

# Food Additives & Flavourings Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Annex B -->

## Overview

CHEMMON rules that apply exclusively to the food additives and flavourings (FA/FF) reporting domain. These rules cover MRL evaluation code restrictions, mandatory F33 legislative class facets, sampling year validation, expression-of-result type requirements, physical state reporting, target consumer facets, substance-specific `paramText` requirements, and matrix code restrictions. Several rules are new or amended for 2026.

Rules that span additives *and* other domains (e.g. CHEMMON37, CHEMMON44, CHEMMON79_a/b/c, CHEMMON97) are in [[business-rules-cross-cutting]]. Legal limit rules for food additives/flavourings (LL_01/02/03 FA_FF) are in [[business-rules-legal-limits]]. For food additives reporting guidance including F33 coding, expression types, restrictions/exceptions, and worked examples, see [[food-additives-reporting]].

## Food Additives & Flavourings CHEMMON Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON36 | Warning | When `evalLimitType` = MRL, `evalCode` must be one of J002A, J003A, J031A, or J029A. Other evaluation codes are not valid for MRL-based assessments. | FA/FF |
| CHEMMON39_a/b | Error | F33 (legislative classes) facet is mandatory for food additives and flavourings. The applicable food category legislation must be declared. (Merged 2026) | FA/FF |
| CHEMMON43_b | Warning | For additives/flavourings, `sampY` must be < submission year minus 1. (New 2026; becomes Error in 2027) | FA/FF |
| CHEMMON84_a | Error | `exprResType` (expression of result type) is mandatory for food additives and flavourings. (Amended 2026) | FA/FF |
| CHEMMON86 | Warning | F03 (physical state) facet is recommended for specific food categories where physical state affects legal limits. (Amended 2026) | FA/FF |
| CHEMMON87 | Warning | `evalInfo.conclusion` is highly recommended for food additives and flavourings. Evaluation conclusions aid data interpretation. | FA/FF |
| CHEMMON88 | Warning | `evalInfo.restrictionException` is highly recommended for food additives and flavourings. Restriction or exception context should be documented. (Amended 2026) | FA/FF |
| CHEMMON89 | Warning | For food category 13 (food for specific groups), F23 (target consumer) facet is recommended. | FA/FF |
| CHEMMON106 | Warning | For potassium sorbate, `paramText` should specify whether the result relates to free acid or the salt form. (New 2026) | FA/FF |
| CHEMMON107 | Warning | For sorbic acid, BHT, coumarin, HCN, and theobromine, reporting `resLOD` is highly recommended to support data quality assessment. (New 2026) | FA/FF |
| CHEMMON108 | Warning | For food additives and flavourings, certain generic `sampMatCode` terms (broad classifications) are not allowed. More specific matrix codes must be used. (New 2026) | FA/FF |
| CHEMMON109 | Warning | If an implicit F33 (legislative class) facet is present via the `sampMatCode`, an explicit F33 is not needed for food additives/flavourings. Avoids duplication. (New 2026) | FA/FF |
