---
title: "ChemMon Overview"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[ssd2-data-model]]"
  - "[[business-rules]]"
  - "[[foodex2-in-chemmon]]"
last_updated: "2026-04-07"
---

# ChemMon Overview

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p6-10 -->
## What ChemMon Is

- ChemMon is EFSA's annual data collection exercise in which EU Member States and participating countries submit analytical results on chemical substances found in food and feed. (ChemMon 2026 p6-8)
- The data feeds EFSA's scientific outputs: annual reports on pesticide residues, veterinary medicinal product residues, contaminant occurrence, and dietary exposure assessments. (ChemMon 2026 p6-7)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p7-10 -->
## Reporting Domains

ChemMon covers five distinct reporting domains, each with its own regulatory basis and scope:

| Domain | Scope |
| --- | --- |
| Pesticide residues | Monitoring and enforcement samples under Regulation (EC) No 396/2005. |
| Veterinary medicinal product residues (VMPR) | National residue monitoring plans under Directive 96/23/EC and Regulation (EU) 2017/625. |
| Chemical contaminants | Occurrence data for contaminants such as heavy metals, mycotoxins, and process contaminants. |
| Food additives | Occurrence data on permitted food additives for re-evaluation exposure assessments. |
| Food flavourings | Occurrence data on flavouring substances used in or on food. |

Each domain routes to a dedicated Data Collection Framework (DCF) dataset. Not every parameter belongs in every domain, and routing rules determine the correct destination for each submission. (ChemMon 2026 p7-10)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p10-14 -->
## Data Submission

- Data is submitted electronically through EFSA's Data Collection Framework (DCF) in the Standard Sample Description version 2 (SSD2) format. See [[ssd2-data-model]] for the logical structure. (ChemMon 2026 p10-12)
- Each submission is an XML file containing sample, analytical, and result records structured according to SSD2 element definitions. (ChemMon 2026 p10)
- Sample matrices are classified using FoodEx2 codes in the `sampMatCode` element, drawn from the MTX reporting hierarchy. See [[foodex2-in-chemmon]] for domain-specific coding rules. (ChemMon 2026 p33-36)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p6-8 -->
## Annual Cycle

1. **Sampling**: Member States collect food and feed samples during the calendar year according to national monitoring and control plans.
2. **Submission**: Data providers prepare SSD2-formatted files and upload them to the appropriate DCF dataset, typically by 31 August of the following year for pesticide residues and by 30 June for VMPR.
3. **Validation**: EFSA runs automated business rules (CHEMMON01 onward) against the submitted data. Failing records are flagged for correction. See [[business-rules]].
4. **Publication**: Validated data is used in EFSA's annual scientific reports and supporting publications.

(ChemMon 2026 p6-8)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p14-16 -->
## Business Rules

- Submissions are validated by a numbered set of business rules (CHEMMON01 through CHEMMON109 and beyond) that check element presence, allowed values, inter-element consistency, and domain-specific constraints. (ChemMon 2026 p14-16)
- Rules are classified by severity: errors block acceptance, warnings flag potential issues but allow submission. (ChemMon 2026 p14)
- The full rule catalogue is maintained in [[business-rules]].

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p8 -->
## Transparency Regulation

- Regulation (EU) 2019/1381 on the transparency and sustainability of EU risk assessment in the food chain governs how ChemMon data is made available. (ChemMon 2026 p8)
- Under the Transparency Regulation, EFSA proactively publishes submitted data while protecting confidential business information and personal data in accordance with the regulation's provisions. (ChemMon 2026 p8)
