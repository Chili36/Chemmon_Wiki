---
title: "ChemMon Background and Rationale"
type: "overview"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 5-10 (Section 1.1 Background)"
related:
  - "[[chemmon-overview]]"
  - "[[ssd2-data-model]]"
  - "[[business-rules]]"
  - "[[business-rules-2026-changes]]"
---

# ChemMon Background and Rationale

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 5-8 (Section 1.1 Background) -->

## Purpose and Audience

- This guidance is intended for the use of **data providers reporting datasets (files) to EFSA in SSD2 format** that contain results for chemical parameters in relation to:
  - the occurrence of contaminants in food and feed,
  - food additives,
  - food flavourings,
  - the monitoring of pesticide residues, and
  - veterinary medicinal product residue (VMPR) levels in food and feed. (ChemMon 2026 p5)
- Except for the statutory EU Annual Report domain (pesticide residues and VMPR), samples taken in any year can be transmitted to the EFSA Scientific Data Warehouse (sDWH) whenever the data provider has the data ready. **Only samples taken in the specific calendar year will be included in each year's national and Annual Report.** (ChemMon 2026 p5)

## Legal Framework

- EFSA receives monitoring results from laboratories in food and feed under a defined set of EU regulations, including but not limited to:
  - Regulation (EC) No 396/2005 — maximum residue levels of pesticides in or on food and feed of plant and animal origin (ChemMon 2026 p5)
  - Regulation (EU) No 1881/2006, replaced by Regulation (EU) 2023/915 — maximum levels for certain contaminants in food (ChemMon 2026 p5)
  - Regulations (EU) 2024/989, 2022/1644, 2022/1646 — multiannual national control programmes for residues of veterinary medicinal products (ChemMon 2026 p5-6)
  - Regulation (EU) 2017/625 — official controls and associated delegated acts (ChemMon 2026 p5)
  - Regulation (EC) No 1333/2008 — food additives (ChemMon 2026 p5)
  - Regulation (EC) No 1334/2008 — food flavourings (ChemMon 2026 p5)
  - Commission Implementing Regulation (EU) 2019/1873 — intensified official controls at border control posts on products of animal origin (new for 2026, corresponds to `progLegalRef` N422A) (ChemMon 2026 p11)
- Additionally, results on the presence of chemicals in food not covered by the above legislation can also be reported to EFSA. (ChemMon 2026 p6)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p7-8 (SSD2 history and consolidation) -->

## Why a Single SSD2 Data Collection

- In 2013, EFSA published a revision of the Standard Sample Description (EFSA, 2013) — **SSD2** — which provides the data specification for submitting laboratory results in samples from the food chain. This revision incorporates FoodEx2 (EFSA, 2014b), a food classification system compatible with the EU menu food consumption surveys. (ChemMon 2026 p8)
- Data providers are now requested to transmit all chemical monitoring data in the SSD2 format. This **offers the opportunity to collect all chemical monitoring data in a single mechanism**, reducing duplicate reporting and conflicting requirements. (ChemMon 2026 p8)
- Some modifications have been made that may reduce the reporting burden for data providers and ensure that the data received are fit for purpose for compliance and exposure assessments and potentially re-usable for other scientific purposes. (ChemMon 2026 p8)

### Resolving overlapping domains

- The inclusion of data under Regulations (EU) 2022/1644 and 2022/1646 (veterinary medicinal product residues) highlighted the problem of **duplicate reporting** and uncertainty about which data collection a sample should be submitted to, since the same substance could legitimately appear in more than one domain. (ChemMon 2026 p9)
- The single SSD2 collection addresses this by applying a programme legal reference (`progLegalRef`) to select data for inclusion in the Annual Reports for European monitoring programmes. This approach **simplifies reporting from Member States** and allows a more holistic assessment of specific hazards of concern for EFSA. (ChemMon 2026 p9)
- **This document no longer addresses Food Contact Materials (FCM)**. FCM substances belonged to the chemical contaminant's domain in ChemMon 2022 and ChemMon 2023, but have been removed from the 2026 guidance. (ChemMon 2026 p9)
- When substances fall into more than one domain, **business rules of all applicable domains will be applied**. This means a data element defined as optional in general ChemMon transmissions may still be mandatory for a specific domain or substance via a domain-specific business rule (see Table 8 in the source PDF). See [[business-rules]] and the domain-specific slice files. (ChemMon 2026 p9)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p9 (Technical simplifications) -->

## Compound Element Flexibility

- Some data providers reported that creating the strings required to report compound elements (base term plus facets) introduced additional technical overhead. (ChemMon 2026 p9)
- The **SSD2 XSD schema definition now allows both**:
  - reporting of each data element listed in the SSD2 specification **separately**, or
  - reporting as **compound elements** (the historical format). (ChemMon 2026 p9)
- Data providers can choose the approach that fits their existing systems without loss of information.

## Conversion of National Values to EFSA Catalogues

- SSD2 requires the mapping to EFSA-coded terminologies, and the FoodEx2 system requires a complex mapping to both base terms and facets to fully classify and describe the samples taken. (ChemMon 2026 p9)
- Where there are differences in granularity or philosophy of terminologies used in data provider systems there is a risk of mis-mapping with subsequent data quality issues. (ChemMon 2026 p9)
- **EFSA provides a catalogue browser application** (EFSA, online-b) which links to the latest version of the catalogue and web services to enable better conversion. (ChemMon 2026 p9)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p9-10 (Open Data and transparency) -->

## Open Data and Free-Text Field Reduction

- In recent years there have been many requests for access to datasets, largely under Regulation (EC) No 1049/2001 regarding public access to European Parliament, Council and Commission documents. (ChemMon 2026 p9)
- EFSA, in collaboration with Member States, has moved to an **"Open by Default" approach** for data in the Scientific Data Warehouse (EFSA, 2019a). (ChemMon 2026 p9)
- However, Open by Default requires that **sensitive information** — e.g. personal data and commercially sensitive data — is protected. (ChemMon 2026 p9-10)
- Therefore, **the use of free text fields in ChemMon data submissions has been reduced** and only those where the content is clearly specified remain. (ChemMon 2026 p10)
- **Geographical identifiers below country level** and **unique identifiers for business partners** should be linked to public registers of business partners and geographic units, required only when necessary to support risk assessment. (ChemMon 2026 p10)
- The **Transparency Regulation (EU) 2019/1381** introduced new legal provisions on the publication of data and information supporting requests from the Commission for a scientific output. These applied to data collected under the ChemMon data collection from 27/03/2021. (ChemMon 2026 p10)
- Under **Article 38(1)(c) of Regulation (EC) No 178/2002**, the proactive transparency requirements apply to documents, studies and data submitted to EFSA to support application dossiers or mandates for scientific output received by EFSA on/after 27/03/2021. (ChemMon 2026 p10)
- Similarly, pursuant to **Article 38(1)(a)** (proactive publication of documents), Member States submit data on behalf of natural or legal persons. In addition to the F28 mandate, Member States have the right to submit confidentiality requests for certain data in accordance with the provisions of Articles 39-39e of Regulation (EC) No 178/2002. (ChemMon 2026 p10)

## Machine-Readable Resources on EFSA Knowledge Junction

- All resources linked to this document — **structural metadata**, **catalogues**, **business rules**, **schema definitions** — will be published in the EFSA Knowledge Junction in a **machine-readable and human-readable format** where appropriate. (ChemMon 2026 p10)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p10 (Residue definition) -->

## The Concept of "Residue"

- For the sake of clarity, throughout the document the general concept of **'residue'** is used to indicate:
  - **residues coming from added substances** (e.g. pesticides), and
  - **residues of substances present in the food unintentionally** (e.g. environmental contaminants). (ChemMon 2026 p10)
- This broad definition covers both intentional inputs (pesticides, veterinary drugs) and unintentional contaminants (heavy metals, mycotoxins, process contaminants) under the same conceptual umbrella for reporting purposes.

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p10 (Revision cadence) -->

## Revision Cadence and Change Management

- It is acknowledged that for national annual monitoring, **any subsequent changes proposed to elements, catalogues or business rules in October-November of year X can only be applied to results reported in year X+2**. (ChemMon 2026 p10)
- This is because the changes must be known before the sampling officers collect the samples in year X+1 — you cannot apply a new facet requirement to samples that were already taken before the rule existed. (ChemMon 2026 p10)
- **Exception**: changes aimed at implementing new or amended legal requirements that cannot be anticipated by EFSA are applied as soon as legally required, regardless of the X+2 rule. (ChemMon 2026 p10)
- **Network members must contribute to and participate in the process of revision** on an ongoing basis, with emphasis on suggestions being submitted during the **last quarter of each year (September-November)**. (ChemMon 2026 p10)

## Main Changes for 2026

The major changes introduced for the 2026 ChemMon data collection compared with the previous year's data collection are listed in Table 1 of the source PDF. They fall into three categories of reason:

- **Legal requirement** — new or amended regulations (e.g. new `progLegalRef` N422A for Commission Implementing Regulation (EU) 2019/1873 on intensified official controls at border control posts). (ChemMon 2026 p11)
- **Quality requirement** — tightening or clarifying business rules to improve data quality (most amendments and new BRs in Table 1 fall here). (ChemMon 2026 pp. 11-16)
- **Sampling requirement** — additions to the permitted combinations of programme type, legal reference and sampling strategy (e.g. ST20A with K009A/K018A for pesticides). (ChemMon 2026 p11)

For the full catalogue of rule changes — amended, merged, new, and deactivated — see [[business-rules-2026-changes]].
