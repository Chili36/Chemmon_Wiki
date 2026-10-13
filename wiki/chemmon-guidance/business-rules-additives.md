---
title: "Food Additives & Flavourings Business Rules"
select_when: "SSD2 FA/FF CHEMMON rule severity, implicit F33, F03/F23 recommendations and 2026 changes. PRE and USE belong to separate data-model pages."
type: "rule-reference"
domain: "additives"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Table 10, pp. 113-143"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-legal-limits]]"
  - "[[food-additives-reporting]]"
  - "[[fa-ff-no-presence-data-model]]"
  - "[[fa-ff-use-levels-data-model]]"
---

# Food Additives & Flavourings Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Table 10, pp. 113-143 -->

## Overview

CHEMMON rules that apply exclusively to the food additives and flavourings (FA/FF) reporting domain. These rules cover mandatory F33 legislative class facets, sampling year validation, expression-of-result type requirements, physical state reporting, target consumer facets, substance-specific `paramText` recommendations, and matrix code restrictions. Several rules are new or amended for 2026.

Rules that span additives *and* other domains (e.g. CHEMMON37, CHEMMON44, CHEMMON79, CHEMMON97) are in [[business-rules-cross-cutting]]. Legal limit rules for food additives/flavourings (LL_01/02/03 FA_FF) are in [[business-rules-legal-limits]]. For food additives reporting guidance including F33 coding, expression types, restrictions/exceptions, and worked examples, see [[food-additives-reporting]].

FA/FF reporting also has **two parallel data models** outside SSD2, each with its own rule namespace: `PRE…` rules on [[fa-ff-no-presence-data-model]] and `USE…` / `USE_LLDB…` rules on [[fa-ff-use-levels-data-model]]. Those rule IDs are not listed in this file because they validate different DCF submission paths; they do not overlap with the CHEMMON IDs below.

## Food Additives & Flavourings CHEMMON Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON39 | Error | For FA/FF (`is_add=1` or `is_flav=1`), `sampMatCode.legis` (F33) must provide the applicable food category under Regulations 1333/2008 and 1334/2008. An implicit F33 satisfies this; add it explicitly only if missing. | FA/FF | 121-122 |
| CHEMMON43_b | Warning | For FA/FF, `sampY` should be less than or equal to submission year minus 1. The source announces Error severity and merging with CHEMMON43 in 2027; the 2026 severity is Warning. | FA/FF | 123 |
| CHEMMON84_a | Error | `exprResType` (expression of result type) is mandatory for food additives and flavourings. (Amended 2026) | FA/FF | 133 |
| CHEMMON86 | Warning | For FA/FF, if F03 is not implicit, report it for legislative categories 1, 6.3, 12.5, 12.6, 13, 14.1.2, 14.1.3, 14.1.4, 14.1.5 and 17. These are the SSD2 categories; do not substitute the narrower PRE/USE dairy list. | FA/FF | 133-134 |
| CHEMMON87 | Warning | `evalInfo.conclusion` is highly recommended for food additives and flavourings. Evaluation conclusions aid data interpretation. | FA/FF | 134 |
| CHEMMON88 | Warning | For FA/FF, `evalInfo.restrictionException` is highly recommended. The source says it **might** become an Error in 2027 depending on the pilot; that is not the 2026 severity. | FA/FF | 134-135 |
| CHEMMON89 | Warning | For food category 13 (food for specific groups), F23 (target consumer) facet is recommended. | FA/FF | 135 |
| CHEMMON106 | Warning | For Potassium sorbate (RF-00000248-ADD), `paramText` should state “Expressed as free acid” or “Expressed as salt”. This row does not impose that text on all grouped additives. | Potassium sorbate | 140 |
| CHEMMON107 | Warning | For Sorbic acid (RF-00000304-ADD), Potassium sorbate (RF-00000248-ADD), BHT (RF-00000062-ADD), Coumarin (RF-00000370-TOX), Hydrocyanic acid (RF-00000333-TOX) or Theobromine (RF-00000334-TOX), **when `resType` is BIN AND `resQualValue` is NEG**, report `resLOD` (highly recommended). | Six named parameters; BIN + NEG | 140 |
| CHEMMON108 | Warning | For FA/FF, `sampMatCode` cannot use A047N (Food colours), A047Q (Artificial food colour), A047R (Food additives other than flavours, colours and artificial sweeteners), A047A (Food flavourings), A047P (Natural food colour) or A0F3T (Preparations for food flavouring). Severity remains Warning in 2026. | FA/FF | 140 |
| CHEMMON109 | Warning | If an implicit F33 (legislative class) facet is present via the `sampMatCode`, an explicit F33 is not needed for food additives/flavourings. Avoids duplication. (New 2026) | FA/FF | 141 |
