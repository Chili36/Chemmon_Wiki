---
title: "ChemMon Overview"
type: "overview"
domain: "all"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[ssd2-data-model]]"
  - "[[business-rules]]"
  - "[[reporting-flags]]"
  - "[[chemmon-reports]]"
  - "[[data-validation-and-acceptance]]"
  - "[[foodex2-in-chemmon]]"
  - "[[vmpr-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
last_updated: "2026-04-11"
---

# ChemMon Overview

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p6-10 -->
## What ChemMon Is

- ChemMon is EFSA's annual data collection exercise in which EU Member States and participating countries submit analytical results on chemical substances found in food and feed. (ChemMon 2026 p6-8)
- The data feeds EFSA's scientific outputs: annual reports on pesticide residues, veterinary medicinal product residues, contaminant occurrence, and dietary exposure assessments. (ChemMon 2026 p6-7)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p1, p7-8 -->
## Relationship to SSD2 and GDE2

- This document does **not replace** the general EFSA Guidance on Standard Sample Description (SSD2) and Guidance on Data Exchange (GDE2) — it **complements and updates** some aspects of them. (ChemMon 2026 p1)
- This guidance **must be used in conjunction with** SSD2 and GDE2, which provide the details of the workflow, data validation, and the EFSA Data Collection Framework principles. See [[ssd2-data-model]] for the logical model. (ChemMon 2026 p8)
- **Precedence rule**: where divergence exists between the SSD2/GDE2 guidance publications and this document (e.g. in field size or mandatory status), **the details in this guidance must be followed**. (ChemMon 2026 p8)
- Documents to consult alongside this guidance: Standard Sample Description ver. 2.0 (EFSA, 2013), Guidance on Data Exchange version 2.0 (EFSA, 2014a), The food classification and description system FoodEx2 revision 2 (EFSA, 2015), the FoodEx2 classification webinar, the Catalogue Browser user guide, the FoodEx2 Interpreting and Checking Tool user guide, and the DCF User Manual. (ChemMon 2026 p8)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p7-10 -->
## Reporting Domains

ChemMon covers five distinct reporting domains, each with its own regulatory basis and scope:

| Domain | Scope |
| --- | --- |
| Pesticide residues | Monitoring and enforcement samples under Regulation (EC) No 396/2005. See [[pesticide-reporting]]. |
| Veterinary medicinal product residues (VMPR) | National residue monitoring plans under Directive 96/23/EC and Regulation (EU) 2017/625. See [[vmpr-reporting]]. |
| Chemical contaminants | Occurrence data for contaminants such as heavy metals, mycotoxins, and process contaminants. See [[contaminant-reporting]]. |
| Food additives | Occurrence data on permitted food additives for re-evaluation exposure assessments. See [[food-additives-reporting]]. |
| Food flavourings | Occurrence data on flavouring substances used in or on food. See [[food-additives-reporting]]. |

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
