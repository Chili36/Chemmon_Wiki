---
title: "SSD2 Elements: Result Values (resId through resInfo)"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 64-73 (Section 2, elements M.01-M.20)"
related:
  - "[[ssd2-data-model]]"
  - "[[ssd2-elements-analysis]]"
  - "[[ssd2-elements-evaluation]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-gbr]]"
---

# SSD2 Elements: Result Values

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 64-73 -->

## Overview

The result group captures the numeric and qualitative outputs of the analysis: detection/quantification limits, the measured value, units, recovery, expression basis (whole/fat/dry weight), result type, and measurement uncertainty. See [[ssd2-elements-evaluation]] for how the result is compared against legal limits.

## resId — Result identification code

<!-- Source: ChemMon 2026 pp. 64-65 -->

**Element code:** M.01 · **Name:** `resId` · **Status:** mandatory

### Purpose

This element must be provided for every record in the dataset and **must be unique for an analytical result reported for a sample across all data collections from a data provider**. This identifier is also used for communication between EFSA and the data provider during the transmission and validation phases. When validating data, it is essential to be able to detect, which results are actually counted and to be able to identify which results may need to be amended. `resId` will be displayed in validation reports for non-compliant results (in aggregated tables by drill-down). (ChemMon 2026 p64)

### Naming convention

It is recommended that **certain prefixes or suffixes are included** to ensure the `resId` is unique within the country.

| Description | XML |
| --- | --- |
| Result reported by an Estonian veterinary laboratory in 2017 | `<resId>EEVetLab2017_0009435634</resId>` |
| Result reported by the Italian pesticides national reference laboratory in 2017 | `<resId>ITNRL2017_ADE0000456792</resId>` |
| Result reported by a Danish food testing laboratory in 2017 | `<resId>DKDTU2017_K0000034597X</resId>` |

(ChemMon 2026 p65)

## accredProc — Accreditation procedure for the analytical method

<!-- Source: ChemMon 2026 p65 -->

**Element code:** M.02 · **Name:** `accredProc` · **Catalogue:** MDACC · **Status:** mandatory

### Purpose

This code describes the validation/accreditation status of the method linked to `anMethRefId`. Codes can be selected from the MDACC catalogue.

### Key value

| Description | XML |
| --- | --- |
| Method accredited according to ISO/IEC 17025 and validated according to **Commission Implementing Regulation (EU) 2021/808** on the performance of analytical methods for veterinary medicine residue controls | `<accredProc>V007A</accredProc>` |

### Related business rules

- **CHEMMON31** — If `accredProc` = V007A and method is Confirmation, CCalpha is mandatory. See [[business-rules-vmpr]].
- **CHEMMON32** — If `accredProc` = V007A and method is Screening, CCbeta is mandatory.

## resUnit — Result unit

<!-- Source: ChemMon 2026 pp. 65-66 -->

**Element code:** M.03 · **Name:** `resUnit` · **Catalogue:** UNIT (chemUnit hierarchy) · **Status:** mandatory

### Purpose

This element indicates the **units of measurement** for the numerical values `resLOD`, `resLOQ`, `resVal`, `resLLWR`, `resULWR`, `resValUncert`, `resValUncertSD`, `CCalpha`, `CCbeta`, `evalLowLimit`, or `evalHighLimit`. Codes can be selected from the chemUnit hierarchy of the UNIT catalogue. This hierarchy reflects the standard International System of Units (SI) for concentrations: **grams, milligrams, micrograms, picograms or nanograms per kilogram, gram, or litre** (for liquids). (ChemMon 2026 p65)

### Unit conversion handling

EFSA converts results to a single unit type for consistent presentation in tables of reports or comparison in data analysis. Liquid samples will be converted by EFSA on the assumption that **one litre corresponds to one kilogram**, irrespective of the density. (ChemMon 2026 p65)

### Typical units by residue domain

| Domain | Typical unit | Code |
| --- | --- | --- |
| Pesticide monitoring | milligram/kilogram | `G061A` |
| Testing for beta-agonists (VMPR) | microgram/kilogram | `G050A` |
| Mycotoxins | microgram/kilogram | `G050A` |
| Metals | milligram/kilogram | `G061A` |
| Dioxins and PCBs | picogram/gram | `G080A` |
| Polycyclic aromatic hydrocarbons (PAHs) | microgram/kilogram | `G050A` |

(ChemMon 2026 pp. 65-66)

### Related business rules

- **GBR27** — `resUnit` mandatory when `resType` = BIN.
- **GBR28** — `resUnit` mandatory when any LOD or LOQ value is reported.
- **GBR29** — `resUnit` mandatory when any `resVal` is reported.

See [[business-rules-gbr]].

## resLOD — Result limit of detection

<!-- Source: ChemMon 2026 p66 -->

**Element code:** M.04 · **Name:** `resLOD` · **Status:** optional (but mandatory when `resType=LOD`)

### Purpose

The **limit of detection (LOD)** is the lowest concentration that can be determined to be statistically different from a 'blank' analytical result. Results with the LOD reported may be used by EFSA to assess new scenarios when estimating the consumer's chronic exposure. `resLOD` must be reported if `resType = LOD`. (ChemMon 2026 p66)

### Recommendation for food additives and flavourings

For food additives and food flavourings, if `resType = BIN` is reported and `resQualValue` is `NEG`, **it is highly recommended to report the LOD**. Otherwise, the data cannot be used for dietary exposure estimations. (ChemMon 2026 p66)

### Example

| Description | XML |
| --- | --- |
| Result reported as LOD (i.e. `resType=LOD`) with a limit of detection = 0.001 | `<resLOD>0.001</resLOD>` |

### Related business rules

- **GBR36** — If `resType` = LOD, then `resLOD` must be reported.
- **GBR37** — `resLOD` must be less than or equal to `resLOQ`.
- **GBR47** — If `resType` = LOD, then `resVal` must be empty.
- **GBR102** — `resVal` must be greater than or equal to `resLOD`.

## resLOQ — Result limit of quantification

<!-- Source: ChemMon 2026 pp. 66-67 -->

**Element code:** M.05 · **Name:** `resLOQ` · **Status:** optional but usually required

### Purpose

The `resLOQ`, the numerical value of the **limit of quantification (LOQ)**, is the lowest validated residue concentration of the analyte which can be quantified and reported by routine monitoring with validated methods. (ChemMon 2026 p66)

### When resLOQ is required

This data element is **always required unless**:

- unvalidated methods are used (infrequent cases);
- the summed LOQ of the 'Multicomponent' pesticide residue definition/sum of contaminants cannot be calculated (where `resInfo.notSummed = Y`, see also Section M.20 below);
- the values for `resLOD`, `CCbeta` or `CCalpha` are reported for VMPR;
- `resType` = BIN, where `resLOD` should be reported. (ChemMon 2026 p66)

### Why LOQ matters

An LOQ is required for the following reasons:

1. **Uncertainty**: the LOQ is used by EFSA as a substitution method for the calculation of the middle and upper bound for the left-censored results on residue/contaminant concentrations.
2. **Sensitivity and method evaluation**: the LOQ is required to ensure the quality and comparability of analytical results, to ensure that acceptable accuracy is achieved and to ensure that false positives or false negatives are avoided.
3. **To apply quality criteria**: if a cut-off value is applied based on the LOQ, this will affect both quantified and left-censored data.

In cases where neither the LOD nor LOQ is provided, results cannot be used in exposure assessments and scientific reports. (ChemMon 2026 p67)

### VMPR rule

For veterinary monitoring, **one of `resLOD`, `resLOQ`, `CCalpha` and `CCbeta` must be reported for each result**. (ChemMon 2026 p67)

### Example

| Description | XML |
| --- | --- |
| LOQ = 0.005 milligram/kilogram | `<resLOQ>0.005</resLOQ>` |

### Related business rules

- **CHEMMON44** — `resLOQ` must be reported unless method is unvalidated, `notSummed = Y`, domain is VMPR, or `resType` = BIN.
- **CHEMMON45** — At least one of `resLOQ`, `resLOD`, `CCbeta`, or `CCalpha` must be reported.
- **CHEMMON78** — If `resType` = BIN, `resLOQ` must be empty.
- **CHEMMON82** — `resLOQ` cannot be a placeholder value (99999, 999, 9999, 999999, 9999999).

## CCalpha and CCbeta

<!-- Source: ChemMon 2026 pp. 67-68 -->

**Element codes:** M.08, M.09 · **Names:** `CCalpha`, `CCbeta` · **Status:** optional (mandatory for VMPR in some cases)

### Definitions

- **Decision limit (CCalpha)** — the limit at and above which it can be concluded with an error probability of α that a sample is non-compliant. Since CCalpha accounts for measurement uncertainty, this value must be reported for **confirmatory results** where the result is evaluated for compliance. (ChemMon 2026 p67)
- **Detection capability (CCbeta)** — the smallest content of the substance that may be detected, identified and/or quantified in a sample with an error probability of β. For substances for which no permitted limit has been established, CCbeta is the lowest concentration at which a method is able to detect truly contaminated samples with a statistical certainty of 1 − β. For substances with an established permitted limit, CCbeta is the concentration at which the method can detect permitted limit concentrations with a statistical certainty of 1 − β. CCbeta must be reported for **screening methods for veterinary medicinal residues**. (ChemMon 2026 p67)

### Multicomponent rules

- For multicomponent residue definitions/marker compounds for MRL, where one or more of the components is quantified, it is sufficient to report the CCalpha of the substance used for the evaluation of compliance.
- In cases of multicomponent residue definitions/marker compounds for MRL where no component can be quantified, the CCalpha of the usual main component should be reported as 'representative' for confirmatory tests.
- For screening tests, it is sufficient to report the CCbeta for the individual components. (ChemMon 2026 p67)

### VMPR accreditation requirement

For veterinary medicinal residues, when the analytical method is validated according to Commission Implementing Regulation (EU) 2021/808 the reporting of either CCalpha or CCbeta is required. **For A3b and B1b substances when the validation is done according to the Pesticides domain CCalpha and CCbeta are not required.** The use of CCalpha and CCbeta is also permitted for certain mycotoxins in food of animal origin (for instance AFM1 in milk or OTA A in pig meats). (ChemMon 2026 p68)

### Examples

| Description | XML |
| --- | --- |
| CCalpha reported for a confirmatory test | `<CCalpha>20</CCalpha>` |
| CCbeta reported for a screening test | `<CCbeta>350</CCbeta>` |

## resVal — Result value

<!-- Source: ChemMon 2026 p68 -->

**Element code:** M.10 · **Name:** `resVal` · **Status:** mandatory if `resType=VAL` and > 0

### Purpose

The `resVal` must be used to report the **measured concentration of the substance in the product** expressed in the unit reported in `resUnit`. `resVal` is mandatory if `resType = VAL` and must be greater than 0. If a sample was analysed using (qualitative) screening methods, the data element `resVal` must be left blank. See also the paragraph on M.16 Type of results (`resType`). (ChemMon 2026 p68)

### Processed products — important caveat for pesticides

For processed products in general, the results must be reported **for the sample analysed, i.e. the processed product, without any recalculation of the result to the unprocessed product**. If the pesticide residues domain and results expressed on fruits have stones (e.g. peaches, mangoes, avocados), the analytical result should be recalculated back to the whole fruit when checking for MRL compliance. However, when exposure assessments are undergone the pulp (without the stone) will be mapped with the consumption data. Therefore, when reporting either options the use of facet F20 is recommended to indicate if the analytical result is expressed with stone (`A07QJ`) or without stone (`A07QK`). (ChemMon 2026 p68)

### MRL validation scope

The MRL will only be validated considering the processed pesticide residue and VMPR samples, as MRL are set for fresh/unprocessed samples in both legal frameworks, i.e. the MRL will not be used to validate the plausibility of `resVal`, `resType` and `evalCode` reported if the sample is 'processed'. Further, MRL will not be validated for 'Wild' game samples analysed for VMPR substances. (ChemMon 2026 p68)

### Example

| Description | XML |
| --- | --- |
| Measured concentration of a residue in a sample is 5.6 milligrams/kilogram | `<resVal>5.6</resVal>` |

### Related business rules

- **GBR46** — If `resType` = VAL, then `resVal` must be reported.
- **GBR48** — `resVal` must be greater than 0 when reported.
- **GBR101** — Only one result per parameter per sample analysed portion is permitted.

## resValRec / resValRecCorr — Recovery and recovery correction

<!-- Source: ChemMon 2026 pp. 68-69 -->

**Element codes:** M.11, M.12 · **Names:** `resValRec`, `resValRecCorr` · **Status:** optional

### Purpose

The results from analytical methods which **do not include an extraction step** or analytical methods which use **certified reference material at a certified concentration** must be reported uncorrected for extraction recovery during the sample preparation. (ChemMon 2026 p68)

Calculated recovery corrections are typically used to assess the performance of the method. These should not be applied to adjust the numerical results of pesticide residue analysis.

### Mandatory recovery correction for specific contaminants

However, for the following the results must be **adjusted for recovery and the recovery rate reported** (unless specific conditions occur, e.g. for result significantly lower or higher than the maximum level):

- mycotoxins per Commission Regulation (EU) 2023/2782
- erucic acid per Commission Regulation (EU) 2023/2783
- nitrates per Commission Regulation (EC) No 1882/2006
- lead, cadmium, mercury, inorganic tin, 3-MCPD and benzo(a)pyrene per Commission Regulation 333/2007

(ChemMon 2026 p69)

### Expression format

The result value recovery rate (`resValRec`) associated with the concentration measurement is expressed as a percentage (%), i.e. 100 should be reported for a 100% rate.

### Default and reporting flag

Unless otherwise specified, the result expressed is considered by EFSA as **not corrected for recovery**. It is strongly recommended to report whether the analytical result has been or not corrected for recovery within the data element `resValRecCorr` (**'Yes' ('Y') or 'No' ('N')**). In case of an empty field in the data element `resValRecCorr`, the system will return a Warning message with respect to the chemical contaminants domain. If the data provider reports a result corrected for recovery, the data element `resValRecCorr` must be set to 'Yes' ('Y'). If reported, the results recovery must be greater than '0'. (ChemMon 2026 p69)

### Example

| Description | XML |
| --- | --- |
| The concentration of aflatoxin M1 was corrected for a recovery rate of 63% | `<resValRec>63</resValRec><resValRecCorr>Y</resValRecCorr>` |

### Related business rules

- **CHEMMON04** — `resValRec` should be ≥ 1%.
- **CHEMMON05** — `resValRec` should be between 50% and 150%.
- **CHEMMON42** — If `resValRecCorr` = Yes, `resValRec` must be reported and should be in 70-120% range.
- **CHEMMON80** — For contaminants, `resValRecCorr` should be reported. See [[business-rules-contaminant]].

## exprResPerc / exprResType — Expression of result

<!-- Source: ChemMon 2026 pp. 69-70 -->

**Element codes:** M.13, M.14 · **Names:** `exprResPerc`, `exprResType` · **Catalogue:** EXPRRES · **Status:** mandatory for some domains

### Purpose

These elements are used to indicate when the concentration is **expressed as a percentage of a component** of the sample, for example, on a dry weight basis. In the cases where `exprResType` should be reported (mandatory), `exprResPerc` should be also reported (dependent mandatory). (ChemMon 2026 p69)

### Pesticide residues — whole-product vs fat basis

For pesticide residues, the MRLs for eggs and milk apply to the whole product. However, the pesticides that are fat soluble tend to concentrate on the fat part of the product. Therefore, when reporting pesticides in eggs or milk it is necessary to report if the result is expressed as:

- **'whole weight'** (code `B001A`): the result is on the whole egg — after removal of the shell — or whole milk (based on a fat content of 4% by weight)
- **'fat weight'** (code `B003A`): the laboratory has separated the fat phase and the result is provided on the fat part. (ChemMon 2026 p69)

This information allows EFSA to correctly check the consistency of result evaluation in view of the exposure assessment.

### Mandatory for food additives and flavourings

For food additives and food flavourings, `exprResType` should be reported, **as it became mandatory in 2025 and 2026 respectively**. If not reported, the system returns an error message. (ChemMon 2026 p70)

### Contaminants: dry matter basis

In Regulation (EU) 2023/915, where the maximum levels for certain contaminants in food are established, there are specific remarks on the matrix to which the maximum levels apply. For example, the established maximum levels for aflatoxin B1, ochratoxin A, deoxynivalenol, zearalenone, fumonisins apply to the **dry matter** of the baby food and processed cereal-based foods for infants and young children. (ChemMon 2026 p70)

### Fat weight for meat

For product of animal origin concerning meat, it is to be considered that the MRLs apply to the muscle or to the fat. If fat soluble pesticide is analysed in meat sample and `exprResType` is reported as 'fat weight' (code `B003A`), the results will be checked against the MRL for fat. While if `exprResType` is expressed as 'whole weight' (`B001A`) the fat percentage under `exprResPerc` should be reported. If it is not reported, EFSA will consider default values whenever possible. If the pesticide analysed is not fat soluble, it is highly recommended to express the result as whole weight so is checked against the MRLs for muscle. (ChemMon 2026 p70)

### Feed contaminants — dry-matter basis

Directive (EC) 2002/32 describes the maximum levels of undesirable substances in mg/kg in the feedstuffs with a moisture content of 12% (88% dry matter); in order to check compliance and to derive concentration levels usable in exposure assessment it is recommended to report feed contaminants data expressed on **88% dry matter** (code `B004A`). The `exprResType` has to be reported for feed; if the analysis has been performed on whole weight, this should be indicated in the `exprResType` with the code `B001A` and the moisture percentage of the sample in the `exprResPerc.moistPerc` field must be reported. The system will return an Error message if this BR is not followed. In cases where percentage of moisture is not available, but percentage of dry matter is instead, EFSA recommends calculation of the percentage of moisture by applying the calculation `100 − percentage of dry matter = percentage of moisture`. (ChemMon 2026 p70)

### Examples

| Description | XML |
| --- | --- |
| Results for a fat-soluble pesticide measured in a butter sample expressed on a fat weight basis | `<exprResPerc>fatPerc=80</exprResPerc><exprResType>B003A</exprResType>` or `<exprResPerc.fatPerc>80</exprResPerc.fatPerc><exprResType>B003A</exprResType>` |
| Moisture percentage for heavy metals in seaweed samples expressed on whole weight basis | `<exprResPerc>moistPerc=40</exprResPerc><exprResType>B001A</exprResType>` |
| Moisture and fat percentages for heavy metals in seaweed expressed on a whole weight basis | `<exprResPerc>moistPerc=40$fatPerc=5</exprResPerc><exprResType>B001A</exprResType>` |

(ChemMon 2026 p70)

### Related business rules

- **CHEMMON56** — For pesticides, `exprResType` can only be B001A, B003A, or B007A. See [[business-rules-pesticide]].
- **CHEMMON70** — For pesticides in egg/milk matrices, `exprResType` must be B001A.
- **CHEMMON71** — For contaminants in feed, `exprResType` is mandatory. See [[business-rules-contaminant]].
- **CHEMMON84_a** — `exprResType` is mandatory for food additives and flavourings. See [[business-rules-additives]].
- **CHEMMON84_b** — `exprResType` is highly recommended for contaminants.

## resQualValue — Result qualitative value

<!-- Source: ChemMon 2026 p71 -->

**Element code:** M.15 · **Name:** `resQualValue` · **Status:** optional

### Purpose

When qualitative screening results (for example, biological tests) are reported with `resType = BIN`, then `resQualValue` must be reported and the accepted value is **NEG**. For confirmatory results or quantifiable results, `resQualValue` must not be reported. (ChemMon 2026 p71)

### LOD recommendation

As mentioned also in section M.04, for food additives and food flavourings, if `resType = BIN` and `resQualValue = NEG`, then it is highly recommended to report the LOD. Otherwise, the data cannot be used for dietary exposure estimations.

### Example

| Description | XML |
| --- | --- |
| Negative result for the presence of amoxicillin in a milk sample and using a Delvo test (screening) | `<resQualValue>NEG</resQualValue>` |

### Related business rule

**CHEMMON24** — `resQualValue` must equal NEG unless the parameter is MOAHs.

## resType — Type of result

<!-- Source: ChemMon 2026 pp. 71-72 -->

**Element code:** M.16 · **Name:** `resType` · **Catalogue:** VALTYP · **Status:** mandatory

### Purpose

The `resType` indicates the type of analytical result obtained for a substance in a product.

### Catalogue values

| Code | Meaning | Example use |
| --- | --- | --- |
| `VAL` | The result can be quantified at a validated level and `resVal` is reported | Quantified positive detection |
| `CCA` | The residue can be quantified but is below the reported value for CCalpha | VMPR confirmatory below decision limit |
| `LOQ` | The residue is below the LOQ | Below quantification threshold |
| `LOD` | The residue is below the LOD and `resLOD` is reported | Below detection threshold |
| `BIN` | The result of a qualitative screening test | Screening negative/positive |
| `CCB` | The residue cannot be detected and CCbeta is reported | Below detection capability |
| `AWR` | **Above the working range** — exceptional; only for VMPR in rare cases | Environmental sample above calibrated range |

(ChemMon 2026 p71)

### Important rules

- In some cases, a chromatographic peak below the LOQ may be seen. In order to refine exposure assessments in the most consistent approach among all chemical domains, when `resType = LOQ`, `LOD` or `BIN`, `resVal` must be empty. The system will return an Error message. (ChemMon 2026 p71)
- When `resType = VAL`, then `resLOQ` must be numerically lower than `resVal`. In the case of multicomponent paramCodes to overcome this rule, `resInfo.notSummed = Y` can be reported. (ChemMon 2026 p71)
- For test results in which the residue can be quantified at a validated level then the `resType` must be reported as `VAL` and the `resVal` must be greater than 0; in that case it is expected that the `anMethType = 'confirmation'`. (ChemMon 2026 p71)
- For VMPR monitoring, if the residue cannot be quantified and CCalpha is reported, then the `resType = CCA` must be reported. If, however, the `resLOQ` is reported and it is below CCalpha, then the `resType = LOQ` should be reported if the result is below the `resLOQ`. For qualitative screening method results, the expected values for `resType` are BIN (in association with `resQualValue = NEG` and `resVal = blank`) with detection capability reported in `CCbeta`, or alternatively the LOD reported in `resLOD`. For positive screening results, the quantitative confirmatory test results should be reported and not binary positive screening results. (ChemMon 2026 p71)
- Quantitative screening method results can be reported in a similar way to confirmatory results (with a value for CCbeta reported in place of a value for CCalpha). (ChemMon 2026 p72)

### AWR — Above working range (exceptional)

In exceptional cases, for the veterinary medicinal products domain, the code `AWR = 'Value above the upper limit of the working range'` can be selected, but only when one of the six above codes would not be fit for purpose and when:

1. the identity of the residue has been analytically confirmed;
2. the laboratory is certain of the 'positive' occurrence of the residue in the tested sample;
3. even though quantifiable, the residue was not quantified with a given precision/accuracy as the residue concentration was above the upper level of the validated/calibrated/working analytical method range for residue concentration. (ChemMon 2026 p72)

This specific code is expected to be selected only to report 'non-standard' samples, whose results are considered relevant at the national level for risk management reasons — for example, an 'environmental' sample consisting of a 'contaminated' syringe clearly containing a prohibited substance whose presence and identity could be confirmed, but its 'concentration' was well above the calibrated concentration curve. Thus, results coded with AWR can have sufficient information for risk management but will not be useful for risk assessment. **If the `resType` code = AWR is selected, then a numerical value for the data elements CCalpha (or resLOQ) and resVal must be reported.** If the `resType` code AWR is selected, EFSA would consider it as 'corresponding' to `resType = VAL` when e.g. counting the number of 'positive' detections. (ChemMon 2026 p72)

### Related business rules

- **CHEMMON08** — If `resVal = resLOQ`, `resType` must be VAL.
- **CHEMMON40** — For qualitative results (resType = BIN/LOQ/LOD), `resVal` must be empty.
- **CHEMMON41** — `resLOQ` should not exceed `resVal` for positive detections.
- **CHEMMON61** — For pesticides, `resType` can only be LOD, LOQ, BIN, or VAL.

## resValUncert — Result value uncertainty

<!-- Source: ChemMon 2026 p72 -->

**Element code:** M.17 · **Name:** `resValUncert` · **Status:** optional

### Purpose

The `resValUncert` indicates the **expanded measurement uncertainty value** (usually 95% confidence interval) associated with the measurement. This uncertainty is expressed in the same unit as the one reported in the field `resUnit`.

### Recommendation for pesticide residues

For pesticide residue monitoring, it is recommended to populate this field especially if single residue methods are used and/or if for a multiresidue method the expanded measurement uncertainty (MU) is different than 50%. The `resValUncert` is requested only when `resType = VAL`. (ChemMon 2026 p72)

### Scope of use

According to Regulation (EU) 2023/2782 (on mycotoxins), Regulation (EC) No 705/2015 (on erucic acid), Regulation (EC) No 333/2007, and Regulation (EC) No 644/2017, the condition for acceptance of a lot should also take into consideration measurement uncertainty. (ChemMon 2026 p72)

### Note on below-LOQ values

For results below the LOQ value, no MU is to be reported as it is 'a parameter characterising the dispersion of quantify values being attributed to a measurand' (International vocabulary of metrology, ISO-2007: ISO/IEC guide 99, VIM 3). (ChemMon 2026 p72)

### Related business rules

- **CHEMMON72** — For pesticides, `resValUncert` should be reported when `resType = VAL`.
- **CHEMMON90_b** — For copper parameters, `resValUncert` is mandatory when `resType = VAL`. See [[business-rules-pesticide]].

## resInfo.notSummed — Summing status

<!-- Source: ChemMon 2026 pp. 72-73 -->

**Element code:** M.20 · **Name:** `resInfo.notSummed` · **Status:** optional

### Purpose

In line with the European Commission (2015) document on pesticides, this element describes provisions for reporting `resLOQ` according to the residue definition type:

- For multicomponent pesticide residue definitions, EFSA requests that the individual LOQ for each component quantified is reported separately from that residue definition and a summed LOQ, which is calculated by the reporting country.
- If the reporting country does not report the summed LOQ, then `resLOQ` can be null for a given `paramCode` set with `paramType` equal to `P005A` or `P004A` and `resInfo.notSummed` equal to 'Y'. Thus, the `paramCode` of the multicomponent and the `resInfo.notSummed` set to Y, must be reported. In this case, upon submission of the individual component LOQs (for `paramType P002A` substances) will be calculated by EFSA based on the LOQs reported for the individual components associated with `paramType P002A`. For this reason, the individual component `resLOQ` associated to `paramType P002A` is mandatory. If no individual `resLOQ` is reported for at least one component for a given `paramCode` with `paramType` P005A/P004A, no 'sum of LOQ' calculation will be done by EFSA. (ChemMon 2026 p73)

### Contaminant sum LOQ handling

For the calculated sum of contaminants, there are currently no standard guidelines on how to sum LOQs of individual substances. The reporting country can decide to report the LOQ by summing up the LOQs of all the individual substances to which the sum refers or to indicate `resInfo.notSummed = Y` and `resLOQ = null`, if the results for the single substances and correspondent LOQs are reported. This approach is to avoid storing a false value of '99999' in `resLOQ` when the summed LOQ was not possible. **Business rules apply to ensure that `resLOQ` can only be NULL where `resInfo.notSummed = Y`.** No value such as '99999' or similar (e.g. '999', '9999', '999999') shall be reported. (ChemMon 2026 p73)

### Related business rule

**CHEMMON62** — If `notSummed = Y`, the LOQ of at least one component in the sum must be reported elsewhere in the submission.
