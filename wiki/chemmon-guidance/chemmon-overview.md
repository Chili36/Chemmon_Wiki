---
title: "ChemMon Overview"
type: "overview"
domain: "all"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
related:
  - "[[chemmon-background]]"
  - "[[chemmon-scope-and-legal-basis]]"
  - "[[chemmon-single-ssd2-collection]]"
  - "[[chemmon-data-governance-and-transparency]]"
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
last_updated: "2026-11-12"
source_pages:
  - "ChemMon 2026 pp. 1, 5-10 (abstract; Section 1.1 Background); p. 32 (sampling date; E.02 sampMatCode); p. 97 (Section 6); p. 113 (Table 10, DOMAIN VALIDATION); p. 123 (Table 10, CHEMON43); p. 144 (Section 7); p. 148 (Section 9); pp. 149-151 (Section 10; Table 13); p. 152 (Section 11)"
  - "No-presence 2026 p. 4; Use-levels 2026 p. 5 (data that are not reported in SSD2)"
---

# ChemMon Overview

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p5, p8, p149-151 -->
## What ChemMon Is

- ChemMon (chemical monitoring) is the EFSA data collection to which data providers report datasets in SSD2 format containing results for chemical parameters "in relation to the occurrence of contaminants in food and feed, to food additives, to food flavourings, and to the monitoring of pesticide residues and veterinary medicinal product residue (VMPR) levels in food and feed". (ChemMon 2026 p5) For background scope and legal basis, see [[chemmon-scope-and-legal-basis]].
- Data submitted through ChemMon "will be used for EFSA scientific assessments", and EFSA produces reports from each calendar year of the data. (ChemMon 2026 p149) Statutory EU Annual Reports are generated only for pesticides and VMPR; National Reports are generated for VMPR and for chemical contaminants, food additives and flavourings; validation dashboard reports cover all five domains. (ChemMon 2026 Table 13 pp. 150-151) The SSD2 collection is meant to keep the data "fit for purpose for compliance and exposure assessments". (ChemMon 2026 p8) See [[chemmon-reports]].

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p1, p7-8 -->
## Relationship to SSD2 and GDE2

- This document does **not replace** the general EFSA Guidance on Standard Sample Description (SSD2) and Guidance on Data Exchange (GDE2) — it **complements and updates** some aspects of them. (ChemMon 2026 p1)
- It does replace earlier ChemMon reporting guidance: "It replaces all previous EFSA guidance on the reporting of chemical monitoring results from the contaminants, food additives, pesticide residues and VMPR domains." (ChemMon 2026 p8)
- This guidance **must be used in conjunction with** SSD2 and GDE2, which provide the details of the workflow, data validation, and the EFSA Data Collection Framework principles. See [[ssd2-data-model]] for the logical model. (ChemMon 2026 p8)
- **Precedence rule**: where divergence exists between the SSD2/GDE2 guidance publications and this document (e.g. in field size or mandatory status), **the details in this guidance must be followed**. (ChemMon 2026 p8)
- Documents to consult alongside this guidance: Standard Sample Description ver. 2.0 (EFSA, 2013), Guidance on Data Exchange version 2.0 (EFSA, 2014a), The food classification and description system FoodEx2 revision 2 (EFSA, 2015), the FoodEx2 classification webinar, the Catalogue Browser user guide, the FoodEx2 Interpreting and Checking Tool user guide, and the DCF User Manual. (ChemMon 2026 p8)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p5-9, p148; No-presence 2026 p4; Use-levels 2026 p5 -->
## Reporting Domains

ChemMon covers five distinct reporting domains, each with its own regulatory basis and scope:

| Domain | Scope |
| --- | --- |
| Pesticide residues | Monitoring of pesticide residues in food and feed under Regulation (EC) No 396/2005 on maximum residue levels of pesticides in or on food and feed of plant and animal origin (ChemMon 2026 p5). See [[pesticide-reporting]]. |
| Veterinary medicinal product residues (VMPR) | Official controls of VMPR in live animals and animal products under Regulations (EU) 2022/1644 and 2022/1646, which repealed Council Directive 96/23/EC (ChemMon 2026 p6, p8). See [[vmpr-reporting]]. |
| Chemical contaminants | Occurrence of contaminants in food and feed; the legislation listed includes Regulation (EU) 2023/915 on maximum levels for certain contaminants in food and Directive 2002/32/EC on undesirable substances in animal feed (ChemMon 2026 p5-6). See [[contaminant-reporting]]. |
| Food additives | Analytical results for food additives under Regulation (EC) No 1333/2008 (ChemMon 2026 p5). See [[food-additives-reporting]]. |
| Food flavourings | Analytical results for food flavourings under Regulation (EC) No 1334/2008 (ChemMon 2026 p5). See [[food-additives-reporting]]. |

The SSD2 collection carries analytical results. ChemMon p. 7 describes the pilot under Commission Recommendation 2023/965 as monitoring "the occurrence (use levels and analytical results)" of food additives and food flavourings, but use levels and stand-alone no-presence data are not reported in SSD2: "The current use levels DM is not implemented in SSD2" (Use-levels 2026 p5), and "the reporting of 'no-presence' data alone is not supported by the analytical data model (SSD2)" (No-presence 2026 p4). They go through the separate data models on [[fa-ff-use-levels-data-model]] and [[fa-ff-no-presence-data-model]].

The analytical results of all five domains are reported to **one single SSD2 data collection**; there is no separate dataset per domain. The results that go into each National and Annual Report are selected with analysis hierarchies on the PARAM and MTX catalogues "plus other catalogues where necessary"; a programme legal reference is also required to select data for the Annual Reports for European monitoring programmes (ChemMon 2026 p8-9), and EFSA stores a flag per domain on every result ([[reporting-flags]]; ChemMon 2026 p148). The rationale for the single SSD2 collection and overlapping-domain handling is in [[chemmon-single-ssd2-collection]].

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p8, p32, p144, p152 -->
## Data Submission

- Data is submitted electronically through EFSA's Data Collection Framework (DCF) in the Standard Sample Description version 2 (SSD2) format. See [[ssd2-data-model]] for the logical structure. (ChemMon 2026 p8, p152)
- Submissions are structured according to the SSD2 element definitions; the guidance shows its element examples as XML, e.g. `<sampY>2019</sampY>`. (ChemMon 2026 p32)
- Sample matrices are classified using FoodEx2 codes in the `sampMatCode` element, drawn from the reporting hierarchy of the MTX catalogue. See [[foodex2-in-chemmon]] for domain-specific coding rules. (ChemMon 2026 p32, p144)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p5, p32, p149, p152 -->
## Annual Cycle

1. **Sampling**: Samples are taken in a calendar year, "which runs from January to December"; the complete sampling date is mandatory and is used to select results for the Annual Reports. (ChemMon 2026 p32)
2. **Submission**: Data providers prepare SSD2-formatted files and transmit them to the DCF. Samples taken in any year can be transmitted when the data are ready, but the EU VMPR and pesticide reports only include samples taken in the specific calendar year and "submitted within agreed deadlines" (ChemMon 2026 p32); the guidance does not state the deadline dates. Source discrepancy: p. 5 allows any-year transmission "Except for the statutory EU Annual Report domain (pesticide residues and VMPR)" (ChemMon 2026 p5), while p. 32 states it without that exception and limits only what the reports include (ChemMon 2026 p32). Validation does not settle it: CHEMON43 (Error, pesticides and VMPR) only requires `sampY` to be lower than or equal to the submission year minus 1 (ChemMon 2026 p123). For contaminants, food additives and food flavourings, samples from previous years can be included, but "only samples in the specific calendar year (equal to the submission year minus 1) will be considered on the food additives/food flavourings report". (ChemMon 2026 p32)
3. **Validation**: The DCF returns the results of the business-rule validation; data providers correct and re-transmit. See [[business-rules]] and [[data-validation-and-acceptance]]. (ChemMon 2026 p152)
4. **Use**: Data submitted through ChemMon are used for EFSA scientific assessments and for the reports in [[chemmon-reports]]. (ChemMon 2026 p149) 'Submitted' data are visible in the validation reports before acceptance; the data validator's 'Accept' "ensures that data are in the EFSA sDWH and ready for use". (ChemMon 2026 p152)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p97, p152 -->
## Business Rules

- Business rules are provided to ensure the data submitted through the DCF are fit for purpose for EFSA's scientific assessments. There are three groups: general business rules (GBR), chemical monitoring rules (CHEMON), and specific rules for a subset of the data (pesticides, VMPR, food additives, food flavourings or specific contaminants). (ChemMon 2026 p97) Rule numbering has gaps; use the source-derived inventory in [[business-rules]] instead of inferring IDs from a numeric range.
- Rules that return a message are an Error or a Warning; the DOMAIN VALIDATION entry in Table 10 has type of error 'Not Applicable' and "does not generate any messages". (ChemMon 2026 p113) A dataset can be submitted to the sDWH once it has reached 'Valid' or 'Valid with Warning' status. (ChemMon 2026 p152) Wiki note (not in the guidance): the guidance does not say in so many words that an Error blocks submission; that follows from the two statuses.
- The full rule catalogue is maintained in [[business-rules]].

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p10 -->
## Transparency Regulation

- Regulation (EU) 2019/1381 on the transparency and sustainability of the EU risk assessment in the food chain became applicable on 27/03/2021; its provisions on publishing data and information that support requests for a scientific output "may also apply" to ChemMon data. (ChemMon 2026 p10)
- EFSA has moved to an Open by Default approach for data in the Scientific Data Warehouse, which requires that sensitive information (personal data, commercially sensitive data) is protected. See [[chemmon-data-governance-and-transparency]] for the background on Open Data, confidentiality requests and free-text reduction. (ChemMon 2026 p9-10)
