---
title: "SSD2 Result: Reported Value and Result Type (resVal, resQualValue, resType)"
type: "reference"
domain: "all"
last_updated: "2026-04-15"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 68 (Section 2, element M.10)"
  - "pp. 71-72 (Section 2, elements M.15-M.16)"
related:
  - "[[ssd2-elements-result]]"
  - "[[ssd2-result-units-and-limits]]"
  - "[[ssd2-result-expression-basis]]"
  - "[[business-rules-gbr]]"
  - "[[business-rules-cross-cutting]]"
---

# SSD2 Result: Reported Value and Result Type

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 68, 71-72 -->

## Rule Summary (Rule-First)

- `resType` is mandatory and determines which value/limit fields are allowed or required.
- If `resType = VAL`, `resVal` is mandatory and must be > 0.
- If `resType` indicates a qualitative or below-threshold result (`BIN`, `LOD`, `LOQ`), `resVal` must be empty (CHEMMON40; GBR47 for `LOD`).
- If `resType = BIN`, report `resQualValue` (expected `NEG` in most cases) and leave `resVal` empty.
- Exceptional VMPR case: `resType = AWR` (above working range) is allowed only under strict conditions and still requires a numeric threshold (`CCalpha` or `resLOQ`) and `resVal`.

## Relevant Business Rules

- Result value presence: GBR46/48. See [[business-rules-gbr]].
- Result-type/value compatibility: CHEMMON08/24/40/41. See [[business-rules-cross-cutting]].

## resVal — Result value

<!-- Source: ChemMon 2026 p68 -->

**Element code:** M.10 · **Name:** `resVal` · **Status:** mandatory if `resType=VAL` and > 0

### Purpose

The `resVal` must be used to report the **measured concentration of the substance in the product** expressed in the unit reported in `resUnit`. `resVal` is mandatory if `resType = VAL` and must be greater than 0. If a sample was analysed using (qualitative) screening methods, the data element `resVal` must be left blank. See also the paragraph on M.16 Type of results (`resType`). (ChemMon 2026 p68)

### Processed products — important caveat for pesticides

For processed products in general, the results must be reported **for the sample analysed, i.e. the processed product, without any recalculation of the result to the unprocessed product**. If the pesticide residues domain and results expressed on fruits have stones (e.g. peaches, mangoes, avocados), the analytical result should be recalculated back to the whole fruit when checking for MRL compliance. However, when exposure assessments are undergone the pulp (without the stone) will be mapped with the consumption data. Therefore, when reporting either option the use of facet F20 is recommended to indicate if the analytical result is expressed with stone (`A07QJ`) or without stone (`A07QK`). (ChemMon 2026 p68)

### MRL validation scope

The MRL will only be validated considering the processed pesticide residue and VMPR samples, as MRL are set for fresh/unprocessed samples in both legal frameworks, i.e. the MRL will not be used to validate the plausibility of `resVal`, `resType` and `evalCode` reported if the sample is "processed". Further, MRL will not be validated for "Wild" game samples analysed for VMPR substances. (ChemMon 2026 p68)

### Example

| Description | XML |
| --- | --- |
| Measured concentration of a residue in a sample is 5.6 milligrams/kilogram | `<resVal>5.6</resVal>` |

### Related business rules

- **GBR46** — If `resType` = VAL, then `resVal` must be reported.
- **GBR48** — `resVal` must be greater than 0 when reported.
- **GBR101** — Only one result per parameter per sample analysed portion is permitted.

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

- In order to refine exposure assessments consistently across chemical domains, when `resType = LOQ`, `LOD` or `BIN`, `resVal` must be empty. The system will return an Error message. (ChemMon 2026 p71)
- When `resType = VAL`, then `resLOQ` must be numerically lower than `resVal`. For multicomponent `paramCode`s, `resInfo.notSummed = Y` can be reported to avoid a summed-LOQ mismatch. (ChemMon 2026 p71)
- For test results where the residue can be quantified at a validated level, `resType` must be `VAL` and `resVal` must be greater than 0; in that case it is expected that `anMethType = confirmation`. (ChemMon 2026 p71)
- VMPR specifics: if the residue cannot be quantified and `CCalpha` is reported then `resType = CCA` must be reported. If `resLOQ` is reported and it is below CCalpha, then `resType = LOQ` should be reported if the result is below `resLOQ`. For qualitative screening results, the expected values for `resType` are `BIN` (with `resQualValue = NEG` and `resVal` blank) with detection capability reported in `CCbeta`, or alternatively the LOD reported in `resLOD`. Positive screening results should be followed by confirmatory quantitative results rather than binary positive screening results. (ChemMon 2026 p71)
- Quantitative screening method results can be reported similarly to confirmatory results (with `CCbeta` reported in place of `CCalpha`). (ChemMon 2026 p72)

### AWR — Above working range (exceptional)

In exceptional cases, for the veterinary medicinal products domain, the code `AWR = Value above the upper limit of the working range` can be selected, but only when one of the standard codes would not be fit for purpose and when:

1. the identity of the residue has been analytically confirmed;
2. the laboratory is certain of the positive occurrence of the residue in the tested sample;
3. even though quantifiable, the residue was not quantified with a given precision/accuracy as the residue concentration was above the upper level of the validated/calibrated/working analytical method range for residue concentration. (ChemMon 2026 p72)

If `resType = AWR` is selected, a numerical value for `CCalpha` (or `resLOQ`) and `resVal` must be reported. EFSA considers `resType = AWR` as corresponding to `resType = VAL` for some downstream counting (e.g. counting "positive" detections). (ChemMon 2026 p72)

### Related business rules

- **CHEMMON08** — If `resVal = resLOQ`, `resType` must be VAL.
- **CHEMMON40** — For qualitative results (`resType` = BIN/LOQ/LOD), `resVal` must be empty.
- **CHEMMON41** — `resLOQ` should not exceed `resVal` for positive detections.
- **CHEMMON61** — For pesticides, `resType` can only be LOD, LOQ, BIN, or VAL.

