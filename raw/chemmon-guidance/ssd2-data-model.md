---
title: "SSD2 Data Model"
sources:
  - "EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf"
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[business-rules]]"
last_updated: "2026-04-07"
---

# SSD2 Data Model

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf p7-10 -->
## Purpose

- The Standard Sample Description version 2 (SSD2) is a harmonised data format for describing food and feed samples, the analytical methods applied to them, and the results obtained. (SSD2 p7-9)
- SSD2 provides a common language across EU Member States so that data submitted to EFSA can be aggregated, compared, and analysed consistently regardless of the originating country or laboratory. (SSD2 p7)
- All ChemMon reporting domains use SSD2 as the mandatory submission format through the Data Collection Framework. See [[chemmon-overview]] for how the domains are organised. (ChemMon 2026 p10-12)

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf p10-18 -->
## Main Entities

The SSD2 model is organised around a chain of entities that describe the journey from sampling programme through to evaluated result:

| Entity | Role |
| --- | --- |
| Local Organisation | The reporting organisation responsible for the data. |
| Sampling Programme | The monitoring or control programme under which samples are taken. |
| Sampling Event | A specific sampling occasion: where, when, and how the sample was obtained. |
| Sample Taken | The physical sample collected at the sampling event. |
| Matrix Sampled | What was sampled, coded using FoodEx2 (`sampMatCode`). |
| Sample Analysed | The portion of the sample that was actually analysed (may differ from what was sampled). |
| Matrix Analysed | What was analysed, again coded with FoodEx2 (`anMatCode`). |
| Laboratory | The laboratory that performed the analysis. |
| Parameter | The analyte or substance measured (`paramCode`). |
| Analytical Method | The method and technique used for detection and quantification. |
| Result | The measured or derived value (`resVal`), including units, LOD, and LOQ. |
| Evaluation | The regulatory assessment of the result (`evalCode`): compliant, non-compliant, etc. |

These entities are linked by foreign-key relationships: a sampling programme contains sampling events, each event produces samples taken, and so on down to individual results and their evaluations. (SSD2 p10-18)

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf p19-22 -->
## Element Types

SSD2 elements fall into three types:

- **Simple elements**: single-value fields such as `sampId` (sample identifier) or `analysisY` (analysis year). Each carries one value per record. (SSD2 p19)
- **Repeatable elements**: elements that may appear more than once within a record, such as multiple parameter codes for a screening result. (SSD2 p19-20)
- **Compound elements**: elements composed of a base term plus optional facets, following FoodEx2 encoding conventions. `sampMatCode` and `anMatCode` are the primary compound elements. The base term identifies the food category; facets add detail such as processing state, source animal, or production method. (SSD2 p20-22)

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf p22-30; EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p10-14 -->
## Key Mandatory Elements

The following elements are mandatory in most ChemMon submissions:

| Element | Description |
| --- | --- |
| `sampId` | Unique sample identifier within the reporting country. |
| `sampMatCode` | FoodEx2 code for the matrix sampled (compound element). |
| `analysisY` | Year the analysis was performed. |
| `paramCode` | SSD parameter code identifying the analyte measured. |
| `resVal` | Result value -- the numeric analytical finding. |
| `evalCode` | Evaluation code indicating the regulatory assessment of the result. |

Additional elements become mandatory depending on the reporting domain and the specific business rules that apply. See [[business-rules]]. (SSD2 p22-30; ChemMon 2026 p10-14)

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf p19, 37-40 -->
## Controlled Terminologies

- Most categorical elements draw their allowed values from controlled terminologies: finite, enumerated sets of codes maintained by EFSA. (SSD2 p19, p37-40)
- Codes are language-independent. A `paramCode` such as `RF-00000001-PAR` maps to a specific substance regardless of language or local naming. (SSD2 p37)
- Controlled terminologies are versioned and updated annually alongside the ChemMon guidance. Data providers must use the terminology version specified in the current year's call for data. (SSD2 p38-40; ChemMon 2026 p10)

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf p40-45 -->
## Validation Levels

SSD2 data undergoes three levels of validation:

1. **Single-element validation**: checks that each element conforms to its type, format, and allowed-value constraints individually (e.g., `analysisY` is a four-digit year, `evalCode` is from the permitted list). (SSD2 p40-41)
2. **Inter-dependent validation**: checks consistency between related elements (e.g., if `resType` indicates a quantified result then `resVal` must be present and greater than zero). (SSD2 p42-43)
3. **Compound-element validation**: checks that FoodEx2 compound codes are structurally valid, that the base term belongs to the correct hierarchy, and that facets are permitted for that base term. (SSD2 p44-45)

The ChemMon business rules (CHEMMON01 onward) implement and extend these validation levels for the specific requirements of chemical monitoring. See [[business-rules]].

<!-- Source: EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf p7 -->
## Relationship to GDE2

- Detailed element-by-element specifications, including data types, cardinalities, and allowed-value catalogues, are maintained in the Generic Data Exchange (GDE2) documentation rather than in the SSD2 logical model itself. (SSD2 p7)
- This page covers the logical model and high-level structure. For element-level details, refer to the GDE2 specifications and the annual ChemMon guidance annexes.
