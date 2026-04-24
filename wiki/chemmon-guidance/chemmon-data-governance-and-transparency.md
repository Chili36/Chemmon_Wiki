---
title: "ChemMon Data Governance and Transparency"
type: "overview"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 9-10 (compound elements, catalogue conversion, Open Data, Knowledge Junction, residue definition)"
related:
  - "[[chemmon-background]]"
  - "[[ssd2-data-model]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[data-validation-and-acceptance]]"
  - "[[foodex2-in-chemmon]]"
  - "[[business-rules]]"
---

# ChemMon Data Governance and Transparency

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 9-10 -->

## Rule Summary

- SSD2 now allows either separate reporting of listed data elements or historical compound-element strings.
- Mapping national values to EFSA catalogues is a central data-quality risk.
- EFSA reduces free text because ChemMon data is increasingly published under Open by Default and transparency rules.
- Source resources such as structural metadata, catalogues, business rules, and schema definitions are expected to be published in machine-readable and human-readable formats.
- In this guidance, "residue" is a broad reporting concept covering both added substances and unintentionally present substances.

## Compound Element Flexibility

Some data providers reported that creating strings for compound elements introduced technical overhead. The SSD2 XSD schema now allows both:

- reporting each data element listed in the SSD2 specification separately
- reporting as compound elements, which is the historical format

Data providers can choose the approach that fits their systems without loss of information. (ChemMon 2026 p9)

For the logical SSD2 concept of compound elements, see [[ssd2-data-model]]. For the main FoodEx2 compound elements in ChemMon, see [[foodex2-in-chemmon]].

## Conversion to EFSA Catalogues

SSD2 requires mapping to EFSA-coded terminologies. FoodEx2 requires mapping to both base terms and facets to fully classify and describe samples. Differences in granularity or terminology philosophy between national systems and EFSA catalogues create a risk of mis-mapping and downstream data-quality issues. (ChemMon 2026 p9)

EFSA provides a catalogue browser application linked to the latest catalogue version and web services to support conversion. Use [[controlled-terminology-catalogues]] for the wiki catalogue overview. (ChemMon 2026 p9)

## Open Data and Free-Text Reduction

EFSA has moved toward an Open by Default approach for data in the Scientific Data Warehouse. This supports transparency and reuse, but it also requires protection of sensitive information such as personal data and commercially sensitive data. (ChemMon 2026 pp. 9-10)

For that reason, the use of free-text fields in ChemMon submissions has been reduced. Only free-text fields where the expected content is clearly specified remain. Geographical identifiers below country level and unique identifiers for business partners should be linked to public registers and used only where needed for risk assessment. (ChemMon 2026 p10)

The Transparency Regulation (EU) 2019/1381 introduced provisions on publication of data and information supporting requests from the Commission for scientific outputs. These apply to ChemMon data collected from 27 March 2021. (ChemMon 2026 p10)

Under Article 38(1)(c) of Regulation (EC) No 178/2002, proactive transparency applies to documents, studies, and data submitted to EFSA to support application dossiers or mandates received from 27 March 2021. Under Article 38(1)(a), Member States submit data on behalf of natural or legal persons and may submit confidentiality requests under Articles 39-39e. (ChemMon 2026 p10)

## Machine-Readable Resources

Resources linked to the ChemMon guidance, including structural metadata, catalogues, business rules, and schema definitions, are published in the EFSA Knowledge Junction in machine-readable and human-readable formats where appropriate. (ChemMon 2026 p10)

## The Concept of Residue

The guidance uses the general concept of "residue" to cover:

- residues coming from added substances, such as pesticides
- residues of substances present unintentionally in food, such as environmental contaminants

This broad definition lets intentional inputs and unintentional contaminants sit under the same reporting concept. (ChemMon 2026 p10)

## Navigation

- Use [[controlled-terminology-catalogues]] for catalogue-specific routing and hierarchy details.
- Use [[data-validation-and-acceptance]] for the DCF submission and correction workflow.
- Use [[business-rules]] for the validation rules that enforce catalogue, element, and cross-field constraints.
