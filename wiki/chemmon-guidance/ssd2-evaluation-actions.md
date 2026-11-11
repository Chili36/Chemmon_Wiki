---
title: "SSD2 Evaluation: Action Taken"
select_when: "Action taken after SSD2 results; distinguish CHEMON37 recommendations for contaminants/FA/FF from VMPR/pesticide CHEMON85 conditions."
type: "reference"
domain: "all"
last_updated: "2026-11-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 75-76 (Section 2, element N.05)"
related:
  - "[[ssd2-elements-evaluation]]"
  - "[[business-rules-cross-cutting]]"
---

# SSD2 Evaluation: Action Taken

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 75-76 -->

## Rule Summary (Rule-First)

- `actTakenCode` reports enforcement or follow-up action taken after a non-conformity or above-limit finding.
- Multiple actions may be reported.
- For VMPR/pesticides, CHEMON85 requires action reporting for J038A assessment, or empty assessment with detected/above-limit evaluation; see the complete rule and its source-wording note.
- For contaminants, additives and flavourings with `evalCode` J041A or J003A, action reporting is recommended; CHEMON37 is a Warning.

## actTakenCode — Action taken

<!-- Source: ChemMon 2026 pp. 75-76 -->

**Element code:** N.05 · **Name:** `actTakenCode` · **Catalogue:** `ACTION`

### Purpose

Action taken should be reported when a non-conformity is identified during the control activities or a measured substance is found above the level of concern. Multiple actions can be reported. For pesticide samples found non-compliant this shows whether the product was placed on the EU market and consumed, withdrawn without reaching the consumer, or destroyed. (ChemMon 2026 p75)

Codes come from the `ACTION` catalogue. The guidance examples use `I` (follow-up investigation) and `R` (rapid alert notification in RASFF); see the worked examples on [[ssd2-evaluation-conclusions]]. (ChemMon 2026 pp. 76-77)

### Requirements and recommendations

- VMPR/pesticides: CHEMON85 uses both `evalCode` and `evalInfo.resAsses`; do not reduce it to a numerical exceedance alone.
- Contaminants/additives/flavourings: recommended when `evalCode` is J041A or J003A; `CHEMON37` is a Warning (Table 10, p. 121).

## Related business rules

- `CHEMON37` — for contaminants/additives/flavourings, `evalCode` J041A or J003A should have `actTakenCode`; missing values trigger a Warning (Table 10, p. 121). See [[business-rules-cross-cutting]].
- `CHEMON85` — for VMPR/PPP, `actTakenCode` is mandatory for J038A assessment, or empty assessment with J041A/J003A evaluation. The surrounding assessment guidance and Table 10 p. 133 support this grouping; [[business-rules-cross-cutting]] gives the explicit conditions and rationale.
