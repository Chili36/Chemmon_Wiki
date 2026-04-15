---
title: "SSD2 Result: Method Accreditation and Decision Thresholds (accredProc, CCalpha, CCbeta)"
type: "reference"
domain: "all"
last_updated: "2026-04-15"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 65 (Section 2, element M.02)"
  - "pp. 67-68 (Section 2, elements M.08-M.09)"
related:
  - "[[ssd2-elements-result]]"
  - "[[ssd2-elements-analysis]]"
  - "[[ssd2-result-units-and-limits]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Result: Method Accreditation and Decision Thresholds

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 65, 67-68 -->

## Rule Summary (Rule-First)

- `accredProc` is mandatory and describes the validation/accreditation status of the method linked to `anMethRefId`.
- For VMPR, decision-threshold fields `CCalpha` (confirmatory) and `CCbeta` (screening) may be required depending on method accreditation and method type.
- If `accredProc = V007A` (ISO/IEC 17025 + validated per Commission Implementing Regulation (EU) 2021/808):
  - **CHEMMON31**: for confirmation methods, `CCalpha` is mandatory.
  - **CHEMMON32**: for screening methods, `CCbeta` is mandatory.
- VMPR also has a general "report at least one limit/threshold" requirement; see [[ssd2-result-units-and-limits]].

## Relevant Business Rules

- **CHEMMON31** — If `accredProc` = V007A and method is Confirmation, CCalpha is mandatory.
- **CHEMMON32** — If `accredProc` = V007A and method is Screening, CCbeta is mandatory.

See [[business-rules-vmpr]].

## accredProc — Accreditation procedure for the analytical method

<!-- Source: ChemMon 2026 p65 -->

**Element code:** M.02 · **Name:** `accredProc` · **Catalogue:** MDACC · **Status:** mandatory

### Purpose

This code describes the validation/accreditation status of the method linked to `anMethRefId`. Codes can be selected from the MDACC catalogue.

### Key value

| Description | XML |
| --- | --- |
| Method accredited according to ISO/IEC 17025 and validated according to **Commission Implementing Regulation (EU) 2021/808** on the performance of analytical methods for veterinary medicine residue controls | `<accredProc>V007A</accredProc>` |

## CCalpha and CCbeta

<!-- Source: ChemMon 2026 pp. 67-68 -->

**Element codes:** M.08, M.09 · **Names:** `CCalpha`, `CCbeta` · **Status:** optional (mandatory for VMPR in some cases)

### Definitions

- **Decision limit (CCalpha)** — the limit at and above which it can be concluded with an error probability of α that a sample is non-compliant. Since CCalpha accounts for measurement uncertainty, this value must be reported for **confirmatory results** where the result is evaluated for compliance. (ChemMon 2026 p67)
- **Detection capability (CCbeta)** — the smallest content of the substance that may be detected, identified and/or quantified in a sample with an error probability of β. For substances for which no permitted limit has been established, CCbeta is the lowest concentration at which a method is able to detect truly contaminated samples with a statistical certainty of 1 − β. For substances with an established permitted limit, CCbeta is the concentration at which the method can detect permitted limit concentrations with a statistical certainty of 1 − β. CCbeta must be reported for **screening methods for veterinary medicinal residues**. (ChemMon 2026 p67)

### Multicomponent rules

- For multicomponent residue definitions/marker compounds for MRL, where one or more of the components is quantified, it is sufficient to report the CCalpha of the substance used for the evaluation of compliance.
- In cases of multicomponent residue definitions/marker compounds for MRL where no component can be quantified, the CCalpha of the usual main component should be reported as "representative" for confirmatory tests.
- For screening tests, it is sufficient to report the CCbeta for the individual components. (ChemMon 2026 p67)

### VMPR accreditation requirement

For veterinary medicinal residues, when the analytical method is validated according to Commission Implementing Regulation (EU) 2021/808 the reporting of either CCalpha or CCbeta is required. **For A3b and B1b substances when the validation is done according to the Pesticides domain CCalpha and CCbeta are not required.** The use of CCalpha and CCbeta is also permitted for certain mycotoxins in food of animal origin (for instance AFM1 in milk or OTA A in pig meats). (ChemMon 2026 p68)

### Examples

| Description | XML |
| --- | --- |
| CCalpha reported for a confirmatory test | `<CCalpha>20</CCalpha>` |
| CCbeta reported for a screening test | `<CCbeta>350</CCbeta>` |

