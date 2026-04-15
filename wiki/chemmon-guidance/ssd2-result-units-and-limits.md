---
title: "SSD2 Result: Units and Reporting Limits (resUnit, resLOD, resLOQ, resInfo.notSummed)"
type: "reference"
domain: "all"
last_updated: "2026-04-15"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 65-67 (Section 2, elements M.03-M.05)"
  - "pp. 72-73 (Section 2, element M.20)"
related:
  - "[[ssd2-elements-result]]"
  - "[[ssd2-result-method-accreditation]]"
  - "[[business-rules-gbr]]"
  - "[[business-rules-cross-cutting]]"
---

# SSD2 Result: Units and Reporting Limits

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 65-67, 72-73 -->

## Rule Summary (Rule-First)

- `resUnit` is mandatory when reporting any numeric result/limit fields (GBR27/28/29).
- `resLOD` must be reported when `resType = LOD` (GBR36) and must be ≤ `resLOQ` (GBR37).
- `resLOQ` is expected for most chemical-monitoring results and is required unless the guidance explicitly allows exceptions (unvalidated methods; `resInfo.notSummed = Y`; some VMPR cases where `resLOD`/`CCalpha`/`CCbeta` are used instead; `resType = BIN`).
- VMPR: at least one of `resLOD`, `resLOQ`, `CCalpha`, or `CCbeta` must be reported for each result (see also [[ssd2-result-method-accreditation]]).
- `resLOQ` must not use placeholder values like 99999/9999 (CHEMMON82). If a summed LOQ is not available, use `resInfo.notSummed = Y` and leave `resLOQ` NULL where allowed, rather than inventing a fake numeric LOQ.

## Relevant Business Rules

- Unit/limit presence and consistency: GBR27/28/29, GBR36/37/47, GBR102. See [[business-rules-gbr]].
- `resLOQ` rules/exceptions: CHEMMON44/45/78/82, CHEMMON62. See [[business-rules-cross-cutting]].

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

The **limit of detection (LOD)** is the lowest concentration that can be determined to be statistically different from a "blank" analytical result. Results with the LOD reported may be used by EFSA to assess new scenarios when estimating the consumer's chronic exposure. `resLOD` must be reported if `resType = LOD`. (ChemMon 2026 p66)

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
- the summed LOQ of a multicomponent pesticide residue definition or a sum of contaminants cannot be calculated (where `resInfo.notSummed = Y`, see also section M.20 below);
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

## resInfo.notSummed — Summing status

<!-- Source: ChemMon 2026 pp. 72-73 -->

**Element code:** M.20 · **Name:** `resInfo.notSummed` · **Status:** optional

### Purpose

In line with the European Commission (2015) document on pesticides, this element describes provisions for reporting `resLOQ` according to the residue definition type:

- For multicomponent pesticide residue definitions, EFSA requests that the individual LOQ for each component quantified is reported separately from that residue definition and a summed LOQ, which is calculated by the reporting country.
- If the reporting country does not report the summed LOQ, then `resLOQ` can be null for a given `paramCode` set with `paramType` equal to `P005A` or `P004A` and `resInfo.notSummed` equal to "Y". Thus, the `paramCode` of the multicomponent and the `resInfo.notSummed` set to Y must be reported. In this case, upon submission the individual component LOQs (for `paramType P002A` substances) will be calculated by EFSA based on the LOQs reported for the individual components associated with `paramType P002A`. For this reason, the individual component `resLOQ` associated to `paramType P002A` is mandatory. If no individual `resLOQ` is reported for at least one component for a given `paramCode` with `paramType` P005A/P004A, no "sum of LOQ" calculation will be done by EFSA. (ChemMon 2026 p73)

### Contaminant sum LOQ handling

For the calculated sum of contaminants, there are currently no standard guidelines on how to sum LOQs of individual substances. The reporting country can decide to report the LOQ by summing up the LOQs of all the individual substances to which the sum refers or to indicate `resInfo.notSummed = Y` and `resLOQ = null`, if the results for the single substances and corresponding LOQs are reported. This approach is to avoid storing a false value of "99999" in `resLOQ` when the summed LOQ was not possible. **Business rules apply to ensure that `resLOQ` can only be NULL where `resInfo.notSummed = Y`.** No value such as "99999" or similar (e.g. "999", "9999", "999999") shall be reported. (ChemMon 2026 p73)

### Related business rule

**CHEMMON62** — If `notSummed = Y`, the LOQ of at least one component in the sum must be reported elsewhere in the submission.

