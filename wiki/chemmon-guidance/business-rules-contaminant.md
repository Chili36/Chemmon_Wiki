---
title: "Contaminant-Specific Business Rules"
select_when: "Named contaminant CHEMMON rules: substance-specific matrix facets and result reporting, including acrylamide, dioxins, arsenic and mineral oils."
type: "rule-reference"
domain: "contaminant"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Table 10, pp. 113-143"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[contaminant-reporting]]"
---

# Contaminant-Specific Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Table 10, pp. 113-143 -->

## Overview

CHEMMON rules for chemical contaminants, including rules triggered by named substances or matrices. Use each row’s scope rather than inferring a CONT flag requirement from this page title. These rules cover dioxin/PCB congener reporting, matrix-specific facet requirements (acrylamide, bisphenols, PAHs, mycotoxins, arsenic, chlorates, BFRs, fish origin, 3-MCPDs), expression-of-result defaults for feed, recovery correction reporting, and 2026 programme type restrictions.

Rules that span contaminants *and* other domains (e.g. CHEMMON37, CHEMMON44, CHEMMON79, CHEMMON97) are in [[business-rules-cross-cutting]]. For contaminant reporting guidance covering acrylamide, dioxins/PCBs, BFRs, arsenic, chlorates, bisphenol, PAHs, 3-MCPDs, mineral oils, mycotoxins, and nitrates, see [[contaminant-reporting]].

## Contaminant CHEMMON Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON09 | Warning | If `paramCode` is a dioxin or dioxin-like PCB, the full set of 29 congeners (17 PCDD/Fs and 12 dl-PCBs) should be reported, as listed in the Appendix to Annex I of Regulation (EU) 2023/915. | Dioxins/dl-PCBs | 114 |
| CHEMMON10 | Warning | If `paramCode` is a non-dioxin-like PCB, report the six indicator congeners PCB 28, 52, 101, 138, 153 and 180 listed in the Appendix to Annex I of Regulation (EU) 2023/915. | Non-dl-PCBs | 114 |
| CHEMMON11 | Warning | If `paramCode.base` has ancestor Mineral oils (RF-00000396-ORG) or Mycotoxins (RF-00000132-TOX), report `exprResPerc.moistPerc` regardless of whether results use whole weight, fat weight or dry matter. | Mineral oils/mycotoxins | 114-115 |
| CHEMMON12 | Error | If `paramCode.base` is Acrylamide (RF-00000410-ORG), `sampMatCode.legis` must include the additional product categories/subcategories under Regulation (EU) 2017/2158 and Recommendation (EU) 2019/1888. | Acrylamide | 115 |
| CHEMMON14 | Error | If `paramCode.base` has ancestor Bisphenol compounds (RF-00001240-PAR), report packaging material `sampMatCode.packmat` (F19). | Bisphenols | 115 |
| CHEMMON15 | Warning | If `paramCode.base` has ancestor Polycyclic aromatic hydrocarbons (RF-00000040-ORG), report packaging material `sampMatCode.packmat` (F19). | PAHs | 115 |
| CHEMMON17 | Warning | If `paramCode.base` has ancestor Mycotoxins (RF-00000132-TOX), report production method `sampMatCode.prod` (F21). | Mycotoxins | 116 |
| CHEMMON18 | Warning | For rice grains for human consumption, when `paramCode.base` has ancestor Arsenic and derivatives (RF-00000127-CHE), report `sampMatCode.process` (F28), at least processed/unprocessed. | Arsenic in rice grains | 116 |
| CHEMMON19 | Warning | If `paramCode.base` is Chlorates (RF-00000015-CHE), Perchlorate (RF-00001336-PAR), or Quaternary Ammonium Compounds (RF-1078-001-PPP) or a child thereof, report `sampMatCode.process` (F28), at least processed/unprocessed. | Chlorates/perchlorate/QACs | 116 |
| CHEMMON20 | Warning | If `sampMatCode.base` has ancestor A0BZ4 (Processed or preserved seafood) or A0BNJ (Fish, other aquatic animals and products derived thereof, feed), AND `paramCode.base` has ancestor RF-00000074-ORG (BFRs), RF-00000114-ORG (Dioxins and PCBs), or RF-00000169-CHE (Mercury and derivatives), report `origFishAreaCode`. | Specified matrix AND parameter ancestors | 117 |
| CHEMMON21 | Warning | If `paramCode.base` has ancestor RF-00000074-ORG (BFRs), RF-00000114-ORG (Dioxins and PCBs) or RF-00000376-ORG (3-MCPDs), report `exprResPerc.fatPerc` regardless of whole-weight, fat-weight or dry-matter expression. | BFRs/dioxins/PCBs/3-MCPDs | 117 |
| CHEMMON69 | Error | For contaminants in feed reported on whole weight basis, `moistPerc` is mandatory to allow dry-weight conversion. | CONT | 130 |
| CHEMMON71 | Error | For contaminants in feed, `exprResType` is mandatory. The basis of expression must be declared. | CONT | 131 |
| CHEMMON80 | Warning | For contaminants, `resValRecCorr` (recovery correction flag) should be reported to indicate whether the result was corrected for recovery. | CONT | 132 |
| CHEMMON84_b | Warning | For contaminants in **food**, `exprResType` is highly recommended. Contaminants in feed have the mandatory CHEMMON71 requirement. | CONT food | 133 |
| CHEMMON98 | Error | For contaminants with N375A (contaminant regulation), valid `progType` values are K005A, K018A, or K038A. (New 2026) | CONT | 137-138 |
