---
title: "SSD2 Elements: Sampling"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 27-32 (Section 2, sampling elements B.05-D.11)"
related:
  - "[[ssd2-data-model]]"
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-elements-matrix]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Elements: Sampling

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 27-32 -->

## Overview

The sampling group identifies *how* a sample was taken: the method, who took it, where in the food chain, when, and the unique identifiers that link multiple analytical results back to the same physical sample. These elements are shared across all reporting domains; see [[ssd2-elements-programme]] for the programme/legal-framework elements and [[ssd2-elements-matrix]] for matrix coding.

## sampMethod — Sampling method

<!-- Source: ChemMon 2026 p27 -->

**Element code:** B.05 · **Name:** `sampMethod` · **Catalogue:** SAMPMD · **Status:** optional

### Purpose

This element provides a reference to the legislation, protocol, or other documentation describing the method of selecting samples from the food chain. If reported, the sampling method codes are selected from the SAMPMD catalogue.

### Catalogue highlights

| Code | Meaning |
| --- | --- |
| `N040A` | Samples taken for the control of dioxins, dioxin-like PCBs and non-dioxin-like PCBs per Commission Regulation (EU) 2017/644 |
| `N009A` | Samples taken per Regulation (EC) No 396/2005 and Directive 2002/63/EC |
| `N042A` | VMPR samples analysed per Regulation (EU) 2022/1644 and 2021/808 |
| `N020A` | No standardised sampling methodology has been defined |
| `N031A` | Mercury samples from fish collected at different places (different batches) and put together before the analysis |
| `N011A` | Furan, 2-methylfuran and 3-methylfuran per part B of the Annex to Commission Regulation (EC) No 333/2007 |
| `N002A` or `N031A` | Analytical results referring to pooled samples, reported either as 'pooled/batch' or 'pooled' |

(ChemMon 2026 p27)

### Pooled samples rule

If the analytical result refers to pooled samples, the code `N002A` or `N031A` has to be selected. In these latter cases, it is **mandatory to report the two data elements `sampUnitSize` and `sampUnitSizeUnit`** (see sections C.03 and C.04). A business rule (**CHEMMON77**) has been implemented to verify if these directions are respected. Reporting these two data elements becomes mandatory from 2025 in case of pooled samples. (ChemMon 2026 p28)

## sampler — Sampler

<!-- Source: ChemMon 2026 p28 -->

**Element code:** B.06 · **Name:** `sampler` · **Catalogue:** SAMPLR · **Status:** mandatory

### Purpose

Identifies the person or persons responsible for taking the sample.

| Code | Meaning |
| --- | --- |
| `CX02A` | Samples taken in the context of an official control — this is the case for samples taken per Regulation 396/2005 and Regulation (EU) 2022/1646 for pesticides and VMPR residues or feed additives, respectively |
| `CX01A` | Samples taken by food business operators (FBOs) |

(ChemMon 2026 p28)

## sampPoint — Sampling point

<!-- Source: ChemMon 2026 p28 -->

**Element code:** B.07 · **Name:** `sampPoint` · **Catalogue:** SAMPNT · **Status:** mandatory

### Purpose

Describes the point in the food chain where the sample was taken. The catalogue is based on a list of terminology developed by Eurostat; it details the activities of establishments at different points in the food chain. The list of activities of the sampling points is subdivided into three hierarchy levels, the first of which is intended to identify the main stages in the production/consumption of food.

### Main stages

| Stage | Example | XML |
| --- | --- | --- |
| Primary production | Milk samples taken at a farm | `<sampPoint>E100A</sampPoint>` |
| Manufacturing | Milk samples taken at the level of the dairy industry before the bulk tanker has discharged | `<sampPoint>E301A</sampPoint>` |
| Distribution | Samples taken at wholesale and retail sale | `<sampPoint>E520A</sampPoint>` |
| Packaging | Eggs taken in the collection/packing centres (if possible to identify the source farm) | `<sampPoint>E600A</sampPoint>` |
| Border Control Posts | Samples classed as import samples; code used for reporting import sampling for VMPR Plan 3 and contaminants monitoring | `<sampPoint>E010A</sampPoint>` |

(ChemMon 2026 p28)

### VMPR-specific hierarchy

When EFSA generates the VMPR reports, the specific `SAMPNT.vmprClasses` hierarchy may be applied, which classifies the `sampPoint` codes into three main classes: **'Slaughter', 'Farm', and 'Other'**. (ChemMon 2026 p28)

### Online sales

In case of sample foodstuffs purchased directly by consumers via online platforms, the sampling point will depend on the origin i.e. Supermarket, Farm. (ChemMon 2026 p28)

## sampEventId — Sampling event identification code

<!-- Source: ChemMon 2026 p29 -->

**Element code:** C.01 · **Name:** `sampEventId` · **Status:** optional

### Purpose

The `sampEventId` is the **unique identifier that represents the sampling unit extracted at a certain time from the sampled population**. This identifier can be reported when multiple samples are taken from a single sampling unit at a point in time. The sampling unit could be a batch, an animal, a flock, a herd or a holding. The sampling unit type can optionally be reported in `sampUnitType` and `sampUnitIds`. (ChemMon 2026 p29)

### Default behaviour

If a value is not reported in `sampEventId`, this data element **will automatically be substituted by EFSA with the `sampId`** during the data submission process. (ChemMon 2026 p29)

### Domain-specific behaviour

- **Pesticide residues**: this element is not used when counting the number of samples for the creation of reports and can be left empty. (ChemMon 2026 p29)
- **VMPR (Regulation (EU) 2022/1646)**: if two samples are taken from a single pig at slaughter (one sample of kidney and one of muscle), the two samples should be reported with the same `sampEventId` and in the VMPR national sampling plan will correspond to **one pig**. (ChemMon 2026 p29)

### Consistency check

A business rule checks if two or more samples reported with different `sampId` but belonging to the same sample event (`sampEventId`) are referring to the same animal species. See [[business-rules-vmpr]] for CHEMMON76 and related rules.

## sampUnitType — Sampling unit type

<!-- Source: ChemMon 2026 pp. 29-30 -->

**Element code:** C.02 · **Name:** `sampUnitType` · **Catalogue:** SAMPUNTYP · **Status:** optional

### Purpose

Describes the sampling unit defined in the sampling method. Can be used to indicate whether the sample contains material from multiple individuals or lots. This is used in the `sampEventId` example to indicate that two samples were taken from one pig.

### Example

| Description | XML |
| --- | --- |
| Milk samples taken at the level of the dairy industry before the bulk tanker has discharged | `<sampUnitType>G202A</sampUnitType>` |
| Single samples (e.g. one animal or one fruit) which are not representative of a lot/batch | `<sampUnitType>G203A</sampUnitType>` |

(ChemMon 2026 p30)

## sampUnitSize and sampUnitSizeUnit — Sampling unit size

<!-- Source: ChemMon 2026 p30 -->

**Element codes:** C.03 and C.04 · **Names:** `sampUnitSize`, `sampUnitSizeUnit` · **Status:** optional

### Purpose

The size of the sampling unit and its unit of measurement can be reported using the optional fields `sampUnitSize` and `sampUnitSizeUnit`, respectively. These report how a sample is created before the analysis, providing information on the unit of measurement (e.g. 'Unit', 'Litre', etc.) and the amount (a number) linked to the unit provided.

### Example (standard individual sample)

| Description | XML |
| --- | --- |
| An individual rice sample made up of 300 grams that have been collected and analysed for mycotoxins | `<sampUnitSizeUnit>G148A</sampUnitSizeUnit><sampUnitSize>300</sampUnitSize>` |

### Pooled samples rule

**However, in the specific case of pooled samples** (see also sampMethod), the element `sampUnitSizeUnit` must be reported with the code `G005A` ('Unit'), while the element `sampUnitSize` must report the **number of single samples pooled**. The system returns an error message if this BR (CHEMMON77) is not followed. (ChemMon 2026 p30)

| Description | XML |
| --- | --- |
| A pooled sample made up of five units of fish collected at different points and combined before the sample is analysed for mercury levels | `<sampUnitSizeUnit>G005A</sampUnitSizeUnit><sampUnitSize>5</sampUnitSize>` |

## sampId — Sample taken identification code

<!-- Source: ChemMon 2026 pp. 30-31 -->

**Element code:** D.01 · **Name:** `sampId` · **Status:** mandatory (size ≤ 100)

### Purpose

Each sample must be identified by a **unique sample identification reference not longer than 100 characters**. Where multiple analytical results are reported for a sample (e.g. results for different residues analysed in the same sample using multiresidue methods and/or several single residue methods), **the same `sampId` must be used for all the results**. Business rule GBR2 applies to ensure that. (ChemMon 2026 p30)

### Role in compliance and reporting

- The sample identification code is used to **determine the overall status of the sample** (e.g. compliant/non-compliant against the MRL) based on all the results reported for the substances/marker residues measured in the sample.
- The sample identification code is used to **enforce the total number of samples taken by MS in accordance with the requirements set in different Regulations**. (ChemMon 2026 p30)

### Example

| Description | XML |
| --- | --- |
| Unique identifier for sample from 2021 in Italy | `<sampId>IT_2021_AS000023456</sampId>` |

### Related business rules

See **CHEMMON01** (unique `sampId` per sample across all collections) and **GBR2** (sampling event consistency) in [[business-rules-gbr]] and [[business-rules-cross-cutting]].

## sampCountry — Country of sampling

<!-- Source: ChemMon 2026 p31 -->

**Element code:** D.03 · **Name:** `sampCountry` · **Catalogue:** COUNTRY · **Status:** mandatory

### Purpose

Reported using the **ISO 3166-1-alpha-2 codes** for the country where the sample was taken. Codes can be selected from the COUNTRY catalogue. Where samples are analysed in a different country than the country of sampling (e.g. where a lab is located outside of the sampling country) this element is needed to correctly connect the results to the sampling country.

### Pesticide residues constraint (CHEMMON58)

For pesticide residues, `sampCountry` and the reporting organisation country **must be the same** (CHEMMON58). The pesticides Annual Report will include records with `sampCountry` being one of the EU countries, Norway or Iceland. Samples taken in the overseas territories of EU countries must be reported as `sampCountry` of the corresponding EU country — e.g. samples taken in Guadeloupe must be reported as `sampCountry=France`. (ChemMon 2026 p31)

### Reportable unspecific country codes (Table 3)

Country of origin cannot be unknown due to EU legislation where traceability of goods placed on the market is a must. Therefore, EFSA stresses the importance of collecting this information and submitting it to EFSA. However, if some data providers are not capable to have this information, the following table will be used to recode unspecific country codes. **In the case of non-compliant results, codes listed in Table 3 cannot be used.** (ChemMon 2026 p31)

| Code description | Code | `sampCountry` (Annual Reports) | `origCountry` (Annual Reports) |
| --- | --- | --- | --- |
| EEA (European Economic Area) | `AA` | Excluded | Unknown (XX) |
| Non-EEA | `XC` | Excluded | Unknown (XX) |
| Non-domestic, import | `XD` | Excluded | Unknown (XX) |
| Non-European Union | `XE` | Excluded | Unknown (XX) |
| Unknown | `XX` | Excluded | Unknown (XX) |

### Recommendation for bulk samples

EFSA recommends that the country of processing (E.08) is provided when bulk samples are reported and the country of origin is not available. (ChemMon 2026 p31)

### Examples

| Description | XML |
| --- | --- |
| Sample taken in Greece | `<sampCountry>GR</sampCountry>` |
| Sample taken in Northern Ireland (per Windsor Framework) | `<sampCountry>XI</sampCountry>` |

## sampY / sampM / sampD — Date of sampling

<!-- Source: ChemMon 2026 p32 -->

**Element codes:** D.06, D.07, D.08 · **Names:** `sampY`, `sampM`, `sampD` · **Status:** mandatory

### Purpose

The complete date on when the sample was taken is mandatory. The information on the date of sampling is required to **check the sample compliance against legal limits applicable at the time of sampling** and to **select results for inclusion in the Annual Reports**. (ChemMon 2026 p32)

### Reporting window rules

- Samples taken in **any year** can be transmitted to the EFSA sDWH when the data provider has the data ready.
- However, in line with the European Commission (EC) interpretation, **each EU VMPR and pesticides report should only include samples taken in the specific calendar year**, which runs from January to December, and submitted within agreed deadlines.
- In relation to samples for **contaminants, food additives, and food flavourings**, reporting of historical data is possible. Therefore, data providers can include samples taken from previous years. However, **only samples in the specific calendar year (equal to the submission year minus 1)** will be considered on the food additives/food flavourings report. (ChemMon 2026 p32)

### Example

| Description | XML |
| --- | --- |
| Friday 16 February 2019 | `<sampY>2019</sampY><sampM>02</sampM><sampD>16</sampD>` |

### Related business rules

- **CHEMMON43** — For pesticides/VMPR, `sampY` must be ≤ submission year minus 1.
- **CHEMMON43_b** — For additives/flavourings, `sampY` must be < submission year minus 1 (new 2026, becomes error in 2027).

See [[business-rules-cross-cutting]] and [[business-rules-additives]].

## origSampId — Original sample identifier

<!-- Source: ChemMon 2026 p32 -->

**Element code:** D.11 · **Name:** `sampInfo.origSampId` · **Status:** optional

### Purpose

This element can be used to indicate that subsequent sampling and testing is **linked to an original non-compliant or contaminated sample** and offers the possibility to separate samples taken to support a specific investigation from routine monitoring samples. (ChemMon 2026 p32)

### Feed → animal chain tracking

In order to make explicit a connection between two samples where one is feed known to have been given to an animal and where the same animal is the source of a food sample, data providers must use `sampInfo.origSampId` to connect the two samples. This applies to **insects as food and the substrates they are fed** when both are analysed for chemicals. (ChemMon 2026 p32)

### Follow-up samples

Similarly, an explicit connection is relevant for follow-up samples, which originate from a positive control sample. (ChemMon 2026 p32)

### Related business rule

**CHEMMON22** — If `origSampId` is reported (follow-up sample), `sampStrategy` should be ST30A (Suspect sampling). See [[business-rules-cross-cutting]].
