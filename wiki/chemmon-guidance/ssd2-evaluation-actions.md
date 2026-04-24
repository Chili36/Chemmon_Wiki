---
title: "SSD2 Evaluation: Action Taken"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
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
- For VMPR and pesticides, action reporting is mandatory when the result is non-compliant.
- For contaminants, additives, and flavourings, action reporting becomes mandatory in the positive/non-compliant cases defined by the business rules.

## actTakenCode — Action taken

<!-- Source: ChemMon 2026 pp. 75-76 -->

**Element code:** N.05 · **Name:** `actTakenCode` · **Catalogue:** `ACTION`

### Purpose

Report the action taken when a non-conformity is identified or the measured substance is found above the level of concern. This is especially important for understanding market consequences in pesticide and VMPR reporting. (ChemMon 2026 p75)

### Mandatory cases

- VMPR and pesticides: mandatory for non-compliant results.
- Contaminants/additives/flavourings: mandatory in the positive/non-compliant cases captured by `CHEMMON37`. (ChemMon 2026 p75)

## Related business rules

- `CHEMMON37` — for contaminants/additives/flavourings, positive or above-limit findings require `actTakenCode`. See [[business-rules-cross-cutting]].
- `CHEMMON85` — for VMPR and pesticides with non-compliant results, `actTakenCode` is mandatory. See [[business-rules-cross-cutting]].
