---
title: "Contaminant-Specific Business Rules"
type: "rule-reference"
domain: "contaminant"
last_updated: "2026-04-10"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Annex B"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[contaminant-reporting]]"
---

# Contaminant-Specific Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Annex B -->

## Overview

CHEMMON rules that apply exclusively to the chemical contaminant (CONT) reporting domain. These rules cover dioxin/PCB congener reporting, matrix-specific facet requirements (acrylamide, bisphenols, PAHs, mycotoxins, arsenic, chlorates, BFRs, fish origin, 3-MCPDs), expression-of-result defaults for feed, recovery correction reporting, and 2026 programme type restrictions.

Rules that span contaminants *and* other domains (e.g. CHEMMON37, CHEMMON44, CHEMMON79_a/b/c, CHEMMON97) are in [[business-rules-cross-cutting]]. For contaminant reporting guidance covering acrylamide, dioxins/PCBs, BFRs, arsenic, chlorates, bisphenol, PAHs, 3-MCPDs, mineral oils, mycotoxins, and nitrates, see [[contaminant-reporting]].

## Contaminant CHEMMON Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON09 | Warning | For dioxin/dl-PCB parameters, all 29 congeners must be reported per sample. Incomplete congener profiles prevent TEQ calculation. | CONT |
| CHEMMON10 | Warning | For non-dl-PCB parameters, six indicator congeners must be reported per sample. | CONT |
| CHEMMON11 | Warning | For mineral oils/mycotoxins, `moistPerc` should be reported to enable dry-weight conversions. | CONT |
| CHEMMON12 | Error | For acrylamide, F33 (legislative class) facet is mandatory. `sampMatCode.legis` must contain the specific product code per Commission Regulation (EU) 2017/2158 and Recommendation (EU) 2019/1888. See [[contaminant-reporting]]. | CONT |
| CHEMMON14 | Error | For bisphenol compounds, F19 (packaging material) facet is mandatory. Packaging material affects migration and exposure. | CONT |
| CHEMMON15 | Warning | For PAHs, F19 (packaging material) facet should be reported. | CONT |
| CHEMMON17 | Warning | For mycotoxins, F21 (production method) facet should be reported (e.g., organic vs. conventional). | CONT |
| CHEMMON18 | Warning | For arsenic in rice, F28 (process) facet should specify processed or unprocessed. Speciation depends on processing state. | CONT |
| CHEMMON19 | Warning | For chlorates/perchlorates/QACs, F28 (process) facet should be reported. | CONT |
| CHEMMON20 | Warning | For fish matrices with BFRs/dioxins/mercury, `origFishAreaCode` (fishing area) should be reported. | CONT |
| CHEMMON21 | Warning | For BFRs/dioxins/3-MCPDs, `fatPerc` should be reported to allow fat-weight expression. | CONT |
| CHEMMON54 | Error | For N317A (contaminant control programme), `progType` must be K019A (Monitoring) and `sampStrategy` must be ST30A (Suspect). | CONT |
| CHEMMON69 | Error | For contaminants in feed reported on whole weight basis, `moistPerc` is mandatory to allow dry-weight conversion. | CONT |
| CHEMMON71 | Error | For contaminants in feed, `exprResType` is mandatory. The basis of expression must be declared. | CONT |
| CHEMMON80 | Warning | For contaminants, `resValRecCorr` (recovery correction flag) should be reported to indicate whether the result was corrected for recovery. | CONT |
| CHEMMON83 | Warning | If `sampMatCode` = F10.A18PX, F19 (packaging) and F18 (contact surface) should NOT be reported. This matrix code already implies specific packaging. | CONT |
| CHEMMON84_b | Warning | `exprResType` is highly recommended for contaminants. (Amended 2026) | CONT |
| CHEMMON98 | Error | For contaminants with N375A (contaminant regulation), valid `progType` values are K005A, K018A, or K038A. (New 2026) | CONT |
| CHEMMON105 | Error | N317A is exclusive -- it cannot be concatenated with other `progLegalRef` values in the same record. (New 2026) | CONT |
