---
title: "SSD2 Data Model"
select_when: "SSD2 structure and field families; use for orientation or general data-model questions, then select field-specific pages for exact constraints."
type: "reference"
domain: "all"
sources:
  - "EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf"
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[chemmon-single-ssd2-collection]]"
  - "[[chemmon-data-governance-and-transparency]]"
  - "[[business-rules]]"
  - "[[foodex2-in-chemmon]]"
  - "[[ssd2-element-reference]]"
source_pages:
  - "SSD2 2013 pp. 8-12 (Introduction; data elements, controlled terminologies, business rules)"
  - "SSD2 2013 pp. 16-19 (Section 5, data structure, Figure 3)"
  - "SSD2 2013 p. 22 (Table 4, list of elements)"
  - "SSD2 2013 pp. 78-79 (controlled terminology maintenance and versioning)"
  - "ChemMon 2026 pp. 80-84 (Table 7, mandatory/optional elements)"
last_updated: "2026-11-11"
---

# SSD2 Data Model

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf p8 -->
## Purpose

- The Standard Sample Description version 2 (SSD2) specifies the data elements and the data structure to describe several types of samples and results coming from laboratory analytical measurements. It extends the scope of SSD1 from food and feed samples to include samples of animal origin and environmental samples (for zoonoses, zoonotic agents and antimicrobial resistance). (SSD2 p8)
- SSD2 defines a logical model that is independent of the file format; it is composed of data element definitions and structure, controlled terminologies, and business rules. (SSD2 pp. 8-9)
- The ChemMon guidance tells data providers how to report the chemical monitoring domains using SSD2. See [[chemmon-overview]] for how the domains are organised and [[chemmon-single-ssd2-collection]] for the consolidation rationale.

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf pp. 16-19 -->
## Main Entities

SSD2 takes into account the logical relationships between these key entities, each a section of the element list:

| Section | Entity | Role |
| --- | --- | --- |
| A | Local organisation | The organisation (local/regional/National Competent Authority) that initially requested or performed the sampling and is responsible for the implementation of the sampling programme. |
| B | Sampling programme | The criteria, purpose, method or legislative reference used to generate a sampling event. |
| C | Sampling event | The sampling unit extracted at a certain time from the sampled population (e.g. an animal, a flock/herd, a batch or lot of products sampled at a certain time). |
| D | Sample taken | One or more samples taken from the sampling unit at a certain time. |
| E | Matrix sampled | The item sampled and its relevant characteristics available before the analysis (`sampMatCode`). See [[foodex2-in-chemmon]]. |
| F | Sample analysed | The sample as it is analysed by the laboratory; usually, but not always, identical to the sample taken. |
| G | Matrix analysed | The matrix analysed and its relevant characteristics (`anMatCode`); often the same as the matrix sampled. |
| H | Sample analysed portion | A replicate ("test portion") achieved by subdividing the sample analysed; only needed when a data collection domain explicitly requires replicate results. |
| I | Isolate | A culture of a biological agent isolated from a specific sample taken. |
| J | Laboratory | The laboratory in which the analysis was performed or that is responsible for the results. |
| K | Parameter | The parameter (analyte) determined in the matrix analysed (`paramCode`). |
| L | Analytical method | The laboratory method of analysis and diagnostic method used to generate the result. |
| M | Result | The result of the laboratory tests, as a quantitative or qualitative outcome value, with accreditation procedure and limits of detection and quantification. |
| N | Evaluation | Assessment of the result, evaluating its compliance with a defined limit (`evalCode`). |

(SSD2 pp. 16-17)

Figure 3 shows the relationships between the entities, but the structure "is implemented in the SSD in denormalised format": "no nested elements are included", the structure is similar to a spreadsheet table, and the values of the upper-level entities (e.g. the sample taken identifier) are repeated. (SSD2 pp. 18-19)

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf pp. 9-11 -->
## Element Types

SSD2 supports three types of data elements:

- **Simple elements**: can contain only one instance of an element value, which may be a text value, a numeric value or a catalogue value. These were the only type available in SSD1. (SSD2 p9)
- **Repeatable elements**: may contain one or many instances of an element value. The source example is "Action taken" (N.05), e.g. `A$R` for "Administrative consequences" and "Rapid alert notification". (SSD2 p9)
- **Compound elements**: may contain one or many simple elements, named "attributes"; both the attribute name and its value are included. Either all attributes are at the same level and independent (`element1=value1$element2=value2`), or one attribute is the default "base term" and the others are "facets" that further describe it (`baseTerm#facet1=value1$…`), as in "matrix analysed", which follows FoodEx2 (e.g. `A01TX#F01.A057E$F02.A069J`). (SSD2 p10) For the ChemMon rationale behind compound-element flexibility, see [[chemmon-data-governance-and-transparency]].

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 80-84 (Table 7) -->
## Key Mandatory Elements

Mandatory/optional status for chemical monitoring is set by ChemMon Table 7 (full list on [[ssd2-element-reference]]). Examples of elements marked Mandatory there:

| Element | Description |
| --- | --- |
| `sampId` | Sample taken identification code (D.01); each sample must be identified by a unique sample identification reference (ChemMon 2026 p30). |
| `sampMatCode` | Coded description of the matrix of the sample taken (E.02; FoodEx2 compound element). |
| `analysisY` | Year of analysis (F.03). |
| `paramCode` | Coded description of the parameter (K.02). |
| `resType` | Type of result (M.16). |
| `evalCode` | Evaluation of the result (N.04). |

(ChemMon 2026 Table 7 pp. 80-84)

`resVal` (M.10) is **Optional** in Table 7 (p. 83): when `resType` is `LOQ`, `LOD` or `BIN`, `resVal` must be empty. (ChemMon 2026 p71) Additional elements become mandatory depending on the reporting domain and the specific business rules that apply. See [[business-rules]].

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf pp. 12, 78-79 -->
## Controlled Terminologies

- A controlled terminology is a finite and enumerated set of terms intended to convey information unambiguously; controlled terminologies have been applied extensively in the SSD. (SSD2 p12)
- Controlled terminologies are language independent: only the code needs to be transmitted, since the description in any language can be linked to the code. (SSD2 p12)
- For some elements an additional companion free-text element is included; the pair takes the suffixes `Code` and `Text`. (SSD2 p12)
- Versioning: after a term is published its code cannot be changed; terms are deprecated (logically removed) rather than deleted. In validation, reported terms are checked against the controlled terminology active at the time of the data transmission ("Valid from" <= transmission date < "Valid to"). (SSD2 p78)

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf p12 -->
## Validation Levels

SSD2 business rules validate data at three levels (SSD2 p12):

1. **Single data element validation**: checks on specific data elements, e.g. whether the code reported in a field constrained to a controlled terminology is correct, or whether the value is within an acceptance range.
2. **Inter-dependent data element validation**: checks on two or more data elements, e.g. whether LOQ was supplied if the result was reported below LOQ.
3. **Repeatable and compound data element validation**: checks on the whole element as well as on the individual elements of the list, e.g. for "analysed matrix", its consistency throughout the same sample and the presence/absence of required/deprecated facets or facet descriptors.

GDE2 addresses only the business rules applicable to all data collection domains; domain-specific rules are addressed in separate documents describing the data collections. (SSD2 p12) For chemical monitoring those are the ChemMon business rules. See [[business-rules]] for the rule families and source-derived inventory; rule numbering is not continuous.

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf pp. 8, 12, 22 -->
## Relationship to GDE2

- The supported file formats, the actual implementation of the logical model and a detailed definition of the business rules are left to a separate guidance, "Guidance on Data Exchange ver. 2.0" (GDE2); the syntax for repeatable and compound elements is also defined there. (SSD2 pp. 8-10)
- The data elements themselves (code, name, label, data type, single/repeatable/compound) are listed in SSD2 Table 4 and defined in SSD2 section 6. (SSD2 p22)
- This page covers the logical model and high-level structure. For element-level details in chemical monitoring, use the pages below.

## ChemMon-focused element reference pages (this wiki)

In addition to the SSD2 logical-model overview, this wiki maintains ChemMon-focused SSD2 element reference pages derived from the annual guidance (e.g. conditional mandatory rules, ChemMon-specific conventions, and the business rules that constrain each element group):

- [[ssd2-elements-programme]] — programme hub; see also [[ssd2-programme-legal-reference]] and [[ssd2-programme-valid-combinations]]
- [[ssd2-elements-sampling]] — sampling event and sample identification/date/location
- [[ssd2-elements-matrix]] — matrix hub; see also [[ssd2-matrix-sampled-matrix]] and [[ssd2-matrix-vmpr-coding]]
- [[ssd2-elements-analysis]] — analysis hub; see also [[ssd2-analysis-parameter-coding]] and [[ssd2-analysis-methods]]
- [[ssd2-elements-result]] — result limits/values/types/expression/uncertainty
- [[ssd2-elements-evaluation]] — evaluation hub; see also [[ssd2-evaluation-code]] and [[ssd2-evaluation-conclusions]]
- [[ssd2-element-reference]] — every SSD2 element in one list (ChemMon Table 7: type, catalogue, mandatory status), with links to the page that explains it
