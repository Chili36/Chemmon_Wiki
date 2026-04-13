---
title: "SSD2 Elements: Analysis, Laboratory, Parameter, Method"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 57-64 (Section 2, elements E.06-L.04)"
related:
  - "[[ssd2-data-model]]"
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-elements-result]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Elements: Analysis, Laboratory, Parameter, Method

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 57-64 -->

## Overview

The analysis/laboratory/parameter/method group describes **who did the analysis, where, with which method, and for which substance**. These are the elements that link a physical sample to the chemistry performed on it. See [[ssd2-elements-matrix]] for what was sampled and [[ssd2-elements-result]] for the numeric results.

## origFishAreaCode — Area of origin for fisheries or aquaculture

<!-- Source: ChemMon 2026 pp. 57-58 -->

**Element code:** E.06 · **Name:** `origFishAreaCode` · **Catalogue:** FAREA · **Status:** optional

### Purpose

For **fish, seafood and other marine products** the Food and Agriculture Organization fishing area should be reported. Codes can be selected from the FAREA catalogue.

### Example

| Description | XML |
| --- | --- |
| Baltic herring caught in Skagerrak and Kattegat, tested for brominated flame retardants (percentage fat should always be reported, results reported for each congener) | `<origFishAreaCode>M27IIIa</origFishAreaCode>` with `<exprResPerc>fatPerc=45</exprResPerc><exprResType>B003A</exprResType>` |

### Related business rule

**CHEMMON20** — For fish matrices with BFRs/dioxins/mercury, `origFishAreaCode` should be reported. See [[business-rules-contaminant]].

## analysisY — Year of analysis

<!-- Source: ChemMon 2026 p58 -->

**Element code:** F.03 · **Name:** `analysisY` · **Status:** mandatory

### Purpose

The year of analysis must be reported for all results. Simple four-digit year.

| Description | XML |
| --- | --- |
| Sample analysed in 2017 | `<analysisY>2017</analysisY>` |

## anPortSeq — Sample analysed portion sequence

<!-- Source: ChemMon 2026 p58 -->

**Element code:** H.01 · **Name:** `anPortSeq` · **Status:** optional

### Purpose

This element contains a sequential number (e.g. 1, 2, 3) to be used when a laboratory sample is analysed for the same substance more than once.

### Scope of use

`anPortSeq` should only be used for **repeated analysis of the same sample with the same method** (i.e. under repeatable conditions) and only when legally required (e.g. aflatoxins in dried fruits where three laboratory samples belonging to the same original sample must be analysed per Regulation (EU) 2023/2782). If different methods are used for the same sample and parameter, only the most accurate and reliable result should be reported (irrespective of the existence of a legal limit). (ChemMon 2026 p58)

### Restriction against legal-limit evaluations

When reporting results which are subject to assessment against a legal limit, **`anPortSeq` must not be used**. Either:

- the result derived with the most accurate or reliable analysis must be reported; or
- when samples were analysed with equally accurate techniques, **the mean value should be reported**. In cases where a mean is calculated, the date of the last component result should be reported, and the most applicable analytical method should be reported. (ChemMon 2026 p58)

### Counter-analysis

The 'sample taken' could be analysed for the same parameter more than once to perform a counter-analysis and/or to confirm a positive sample. In these cases, the only result to be reported is the one for which the evaluation is performed and the 'sample analysed portion' should not be used. (ChemMon 2026 p58)

## labId — Laboratory identification

<!-- Source: ChemMon 2026 pp. 58-59 -->

**Element code:** J.01 · **Name:** `labId` · **Status:** mandatory

### Purpose

A unique code to identify each laboratory providing laboratory results must be reported here (e.g. the national laboratory code). This code must also be used when providing information on participation in proficiency tests in National Reports. The mapping between code and laboratory name is the reporting country's responsibility (i.e. the competent authority/organisation reporting data to EFSA). It should be updated in case of a request by the Commission, EURLs or EFSA. (ChemMon 2026 pp. 58-59)

| Description | XML |
| --- | --- |
| National Reference Laboratory of Poland | `<labId>PolandNRL</labId>` |

## labAccred — Laboratory accreditation

<!-- Source: ChemMon 2026 p59 -->

**Element code:** J.02 · **Name:** `labAccred` · **Catalogue:** LABACC · **Status:** mandatory

### Purpose

This element indicates whether the laboratory performing the analysis has been **accredited as required by Article 37 of Regulation (EU) No 2017/625**. (ChemMon 2026 p59)

### Values

For pesticide monitoring only two codes from the LABACC catalogue may be used:

| Code | Meaning | XML |
| --- | --- | --- |
| `L001A` | Accredited according to **ISO/IEC 17025** | `<labAccred>L001A</labAccred>` |
| `L003A` | For results generated by laboratories not or not yet accredited according to ISO/IEC 17025 (e.g. when the laboratory is awaiting the final audit from the accreditation body) | `<labAccred>L003A</labAccred>` |

## labCountry — Laboratory country

<!-- Source: ChemMon 2026 p59 -->

**Element code:** J.03 · **Name:** `labCountry` · **Catalogue:** COUNTRY · **Status:** mandatory

### Purpose

Indicate using **ISO 3166-1-alpha-2 country codes** the country where the laboratory is located. The country code must be unique for each `labId` provided.

| Description | XML |
| --- | --- |
| Germany | `<labCountry>DE</labCountry>` |

## paramType — Type of parameter

<!-- Source: ChemMon 2026 pp. 59-61 -->

**Element code:** K.01 · **Name:** `paramType` · **Catalogue:** PARAMTYP · **Status:** optional (pre-assigned by EFSA where unambiguous)

### Purpose

This data element indicates whether the parameter (`paramCode` K.02) reported has been analysed in full or partially; it also makes it possible to indicate that the selected `paramCode` refers to the **analysis of a single component** of 'Multicomponent' residue definitions (VMPR and pesticide residues) or of an **individual parameter of a 'summed' parameter** (e.g. dioxins TEQ). (ChemMon 2026 p59)

### Simple vs multicomponent substances

A substance's residue definitions or marker compound used for VMPR and pesticide residue MRLs can be broadly split into two types:

- **'Simple'**: Compounds that can be analysed using one single calibration substance (in terms of identity: same substance or same substance mix of isomers, etc.).
- **'Multicomponent'**: Compounds that can be analysed using several different calibration substances (e.g. the parent compound and one or more metabolites). (ChemMon 2026 p59)

### paramType catalogue values (Table 5)

Starting from the 2021 data collection this data element has been made optional, and the use and meaning of `paramType` were revised according to definitions reported in Table 5, with the aim of making data reporting easier. EFSA automatically pre-assigns the `paramType` in those cases in which the `paramCode`/`paramType` combination is unambiguous. However, in case of multicomponent `paramCode` calculated from measurements of individual components or the sum of individual parameters, the `paramType` should still be reported to indicate if all the expected parts as described by the parameter name have been analysed and summed up or not. (ChemMon 2026 p60)

| Code | Code interpretation | Note |
| --- | --- | --- |
| `P002A` | Part of a sum | Result from analysis of a component that is part of a calculated result reported for a `paramCode` (either P004A or P005A) |
| `P004A` | Sum based on subset | Result for which the full analysis has not been performed, and one or more components are not part of the calculated result for the `paramCode` |
| `P005A` | `paramCode` fully analysed | Result for which the full analysis has been performed, and all components are part of the calculated result for the `paramCode` |

**P001A and P003A are not to be used.** (ChemMon 2026 p60)

### Assignment rules

- Individual components of a multicomponent/sum `paramCode`: `paramType = P002A`.
- `paramCode` measured with one calibration compound (or a mix of compounds), covering the full description of the `paramCode`: `paramType = P005A`.
- Multicomponent/sum `paramCode` calculated from measurements of individual components: `paramType = P004A` / `P005A`.

In the last case data providers are requested to report either `paramType = P005A` if all the expected parts have been analysed as specified by `paramCode`, or `P004A` otherwise. (ChemMon 2026 p60)

### Domain-specific rules

- **Pesticides**: to check for MRL compliance it is a legal requirement to analyse the full residue definitions as defined in Regulation (EC) No 396/2005 (i.e. all the components) and reflected in the correspondent `paramCode`. Results on those individual components associated with `P002A` are strongly recommended to be reported too. These will normally not be included in the data analysis presented in the EU Report on pesticide residues. (ChemMon 2026 p60)
- **VMPR**: for veterinary medicinal products, a similar approach is established. However, in case of negative screening results the reporting of the single components associated with `P002A` is sufficient and the multicomponent/sum `paramCode` does not need to be reported. In this case, EFSA will automatically generate the record related to the complex `paramCode` in the sDWH, which will be then accounted for and totalised in the summary results presented in both the National and EU VMPR Reports. (ChemMon 2026 p61)
- **Contaminants**: the single substances or congener-specific occurrence data must be reported, in addition to the sum (when required for assessment against maximum levels) or complex mixtures of occurrence. These data are essential for dietary exposure assessments since animal and human exposure estimates on food/feed required substance/congener-specific occurrence data. The sums of congener/substance groups reported alone are of very limited use for EFSA. (ChemMon 2026 p61)
- **Food additives**: the analytical result for the individual substances must be reported expressed as specified in the Regulation N°1333/2008 (e.g. sorbic acid-sorbates expressed as the free acid). Additionally, the sum should be reported if it complements the individual substance, as the maximum permitted levels (MPLs) are regulated at the sum level for the reported legislative category. (ChemMon 2026 p61)

## paramCode / paramText — Parameter code and text

<!-- Source: ChemMon 2026 pp. 62-63 -->

**Element codes:** K.02, K.03 · **Names:** `paramCode` (mandatory), `paramText` (optional) · **Catalogue:** PARAM (ChemMonRep hierarchy)

### Purpose

The parameter code is used to indicate the **substance identified in the laboratory analysis**. It should contain codes linked to the **ChemMonRep hierarchy of the PARAM catalogue**. This means that if a specific `paramCode` is in the PARAM catalogue but is not in the ChemMonRep hierarchy, it cannot be transmitted. (ChemMon 2026 p62)

### Examples

| Description | XML |
| --- | --- |
| Sum of aflatoxins B1, B2, G1 and G1 | `<paramCode>RF-00000435-TOX</paramCode>` |
| Aflatoxin B1 as a component of the sum of aflatoxins | `<paramCode>RF-00000150-TOX</paramCode>` |
| Cloxacillin (VMPR) | `<paramCode>RF-00000566-VET</paramCode>` |
| Sweetener saccharin | `<paramCode>RF-00000013-ADD</paramCode>` |
| Terbacil (PPP) | `<paramCode>RF-0912-001-PPP</paramCode>` |
| Flavouring caffeine | `<paramCode>RF-00000038-NTR</paramCode>` |

(ChemMon 2026 p62)

### Domain routing via analysis hierarchies (Table 6)

Each code of the ChemMonRep hierarchy is also present in one or more specific "analysis" hierarchies that are used in EFSA sDWH to classify data according to legal limits or legislation, to generate National and Annual Reports, and to include results in specific data analysis or exposure assessment. **Data providers should make sure that the `paramCode`s used for reporting results intended for a specific domain are included in the hierarchy of that domain.** This information can be found in the PARAM catalogue, in the EFSA Catalogue Browser, on the right-hand side under 'Reportability'. (ChemMon 2026 p62)

| Domain | Analysis hierarchy |
| --- | --- |
| VMPR | `vmprParam` |
| Pesticide residues | `pestParam` |
| Contaminants | `chemAnalysis` |
| Food additives | `addAnalysis` |
| Food flavourings | `flavAnalysis` |

(ChemMon 2026 p63)

### paramText rules

Regarding the `paramText`, please avoid the use of the ampersand character (`&`) when preparing the XML files.

**For food additives**, `paramText` must be filled in as **"Expressed as free acid"** or **"Expressed as salt"** when the food additives are regulated as groups (e.g. sorbic acid and sorbates). This information is mainly required when the reported substance can be expressed as the free acid or converted to the salt. If information is not provided, the analytical value will be considered expressed as free acid. (ChemMon 2026 p63)

### Related business rule

**CHEMMON68** — `progLegalRef` domain must match `paramCode` domain. See [[business-rules-cross-cutting]].

## anMethRefId — Analytical method reference

<!-- Source: ChemMon 2026 pp. 63-64 -->

**Element code:** L.01 · **Name:** `anMethRefId` · **Status:** mandatory (size ≤ 50)

### Purpose

This element should contain a code not longer than 50 characters to identify an analytical method used within the laboratory that links all results obtained from the same analytical method. (ChemMon 2026 p63)

### Examples

| Description | XML |
| --- | --- |
| Delvo test for antibacterial substances in bulk milk validated in 2017 | `<anMethRefId>BulkMilkAntibioticSCR2017</anMethRefId>` |
| Gas chromatography-mass spectrometry analysis for pesticide residues in honey used in the national reference laboratory | `<anMethRefId>NRLGC-MSHoney</anMethRefId>` |
| Liquid chromatography-mass spectrometry analysis for aspartame in soft drinks | `<anMethRefId>2020-LC-MS-E951</anMethRefId>` |
| Coupling liquid and gas chromatography with subsequent flame ionisation detection to analyse MOH in vegetable oils | `<anMethRefId>2019-LC-GC-FID-Veg-Oil</anMethRefId>` |

### Consistency rule

The `anMethRefCode`, `anMethCode`, `anMethText` and `anMethInfo` must be constant (the same) for all results with the same `anMethRefId`. (ChemMon 2026 p63)

## anMethType / anMethCode — Analytical method type and code

<!-- Source: ChemMon 2026 p64 -->

**Element codes:** L.03, L.04 · **Names:** `anMethType`, `anMethCode` · **Catalogues:** ANLYTYP, ANYLMD · **Status:** mandatory

### anMethType — method type

The analytical method type is used to indicate whether the analysis was performed to **detect the presence** of a substance/class of substances ('screening' `AT06A`) or to **quantify/unequivocally identify the substance** ('confirmation' `AT08A`). (ChemMon 2026 p64)

- **Screening (`AT06A`)** should only be selected when a qualitative method returns a negative result.
- **Confirmation (`AT08A`)** should be reported for quantitative/semi-quantitative analytical methods.

### anMethCode — specific analytical method

The analytical method code describes the type of analysis performed by the laboratory. It is strongly advised to report the **specific analytical method, instead of reporting the `anMethCode F001A` ('Classification not possible')**. For chemical contaminants, food additives and food flavourings, the system returns an error message if the `anMethCode` is reported as code `F001A` ('Classification not possible'); if the generic code `F001A` is reported, enter also `anMethText`. (ChemMon 2026 p64)

### Examples

| Description | XML |
| --- | --- |
| Charm II test to screen for tetracyclines in animal tissues | `<anMethType>AT06A</anMethType><anMethCode>F580A</anMethCode>` |
| Multiresidue method using gas chromatography with tandem mass spectrometry | `<anMethType>AT08A</anMethType><anMethCode>F049A</anMethCode>` |
| Liquid chromatography-tandem mass spectrometry used to quantify unauthorised residues in animal samples | `<anMethType>AT08A</anMethType><anMethCode>F027A</anMethCode>` |

(ChemMon 2026 p64)

### Related business rules

- **CHEMMON23** — `anMethType` must be Screening (AT06A) or Confirmation (AT08A).
- **CHEMMON30** — If `evalCode` = J003A (Above MRL/ML), `anMethType` must be Confirmation (AT08A).
- **CHEMMON33** — If `resType` = BIN, `anMethType` should be Screening (AT06A).
- **CHEMMON34** — If `anMethType` = Confirmation (AT08A), `resType` should not be BIN.
- **CHEMMON79_a/b/c** — Contaminant/additive/flavouring analytical method code cannot be F500A (Unknown), F598A (Unspecified), or F001A (Classification not possible).

See [[business-rules-cross-cutting]].
