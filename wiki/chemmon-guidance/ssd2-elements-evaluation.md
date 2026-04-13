---
title: "SSD2 Elements: Evaluation, Action, Conclusion"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 73-76 (Section 2, elements N.01-N.06)"
related:
  - "[[ssd2-data-model]]"
  - "[[ssd2-elements-result]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-contaminant]]"
  - "[[business-rules-additives]]"
---

# SSD2 Elements: Evaluation, Action, Conclusion

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 73-76 -->

## Overview

The evaluation group captures how the analytical result is judged against legal limits and what enforcement or follow-up action was taken. These elements feed directly into EFSA's National and Annual Reports — the count of non-compliant samples and results in EU reports is based on `evalCode` in conjunction with `evalInfo.resAsses`. See [[ssd2-elements-result]] for the numeric result values being evaluated.

## evalLowLimit / evalLimitType — Limit for the result evaluation

<!-- Source: ChemMon 2026 pp. 73-74 -->

**Element codes:** N.01, N.03 · **Names:** `evalLowLimit`, `evalLimitType` · **Catalogue:** LMTTYP · **Status:** optional (required in specific cases)

### Purpose

These two elements are used to report the numerical value of the **legal maximum residue limit or maximum limit enforced** when assessing a laboratory result and the **type of legal limit**. (ChemMon 2026 p73)

### Processed product case

In case of a non-regulated processed product the maximum limit to be indicated is the one of the regulated unprocessed product (Article 3 of Regulation (EU) 2023/915). The transformation factor (see Art. 3 of Regulation (EU) 2023/915) could be indicated in `evalInfo.com` or in a `resInfo.com`. (ChemMon 2026 p73)

### When to report these elements

EFSA developed a harmonised database (**Legal Limit Database**) containing MRLs established for pesticides and veterinary medicine residues in Regulation (EC) No 396/2005 and Regulation (EC) No 37/2010. This database is used to validate the plausibility of the reported result evaluation (`evalCode`) with respect to the numerical comparison of result value (`resVal`) and the MRL when the reported sample is 'unprocessed'. Thus, the reporting of these elements would only be required in cases in which limits **other than those defined in the above-mentioned regulations or other than the official EU limits are in use**, e.g. national limits. (ChemMon 2026 p73)

The Legal Limit Database has also been developed for the food additives and flavourings domains, containing the maximum permitted levels (MPLs) established in Regulations (EC) No 1333/2008 and (EC) No 1334/2008.

### evalLimitType catalogue values

For pesticide monitoring the typically reported value for the type of limit for the result evaluation (`evalLimitType`) data element is `W002A` (MRL). If the national or local limit (`W990A`) is reported, the result will be disregarded from the report analysis. (ChemMon 2026 p74)

For VMPR monitoring the following limit types can be reported in `evalLimitType`:

| Code | Meaning |
| --- | --- |
| `W002A` | MRL |
| `W005A` | Minimum required performance limit |
| `W006A` | Reference point of action |
| `W012A` | Presence |
| `W001A` | Maximum limit (this applies only to coccidiostats, histomonostats and chemical elements) |
| `W007A` | Action level |
| `W008A` | Health-based guidance value |
| `W990A` | Other |

### Example

| Description | XML |
| --- | --- |
| Reporting of an EU MRL in place | `<evalLowLimit>0.003</evalLowLimit><evalLimitType>W002A</evalLimitType>` |

### Related business rules

- **CHEMMON35** — `evalLimitType` should be one of: W002A, W005A, W006A, W012A, W001A, W007A, W008A, or W990A.
- **CHEMMON46** — If `evalCode` = J003A (Above limit) and `evalLimitType` is not Presence-based, `resType` must be VAL.
- **CHEMMON48** — If `paramType` is not P002A and `resVal ≥ evalLowLimit`, `evalCode` should not be J029A.
- **CHEMMON59** — For pesticides, `evalLimitType` can only be W002A, W990A, or left empty.

See [[business-rules-cross-cutting]] and [[business-rules-pesticide]].

## evalCode — Evaluation of the result

<!-- Source: ChemMon 2026 pp. 74-75 -->

**Element code:** N.04 · **Name:** `evalCode` · **Catalogue:** RESEVAL · **Status:** mandatory

### Purpose

The evaluation (`evalCode`) must be applied **at the level of each residue or marker within the analytical method**. It provides the judgement of the reporting country on whether the result reported was considered to exceed the legal limit applicable to the sample or non-compliant due to, for example, the presence of forbidden/prohibited substances. (ChemMon 2026 p74)

### Simple rule

It is sufficient to report **'Above the level of concern'** (`evalCode = J003A`) for results that were found to clearly exceed the limit (taking into account the measurement uncertainty) or level of concern, or **'Below or equal the level of concern'** (`evalCode = J002A`) for results that are below the limit or level of concern.

### Multicomponent handling

The result evaluation for each of the single components of a multicomponent residue definition/marker compound or of a contaminants group (i.e. associated with the `paramType = P002A`) should be reported with the code `J029A = 'results not evaluated'`. (ChemMon 2026 p74)

### VMPR 'detected' case

For VMPR monitoring `evalCode = J041A` ('detected') in conjunction with `evalLimitType = W012A` ('Presence' code) can be reported and this will be counted as a non-compliant result, although it is not recommended since the code J003A could be used. (ChemMon 2026 p74)

### Catalogue values summary

| Code | Meaning |
| --- | --- |
| `J003A` | **The residue in the sample is considered to be above the level of concern.** For residues this code is selected if the numerical value of the quantified residues is clearly above the legal limit taking into account the analytical measurement uncertainty; thus, the result must be evaluated against the legal limit set under the relevant MRL/ML legislation. *Note*: J003A must not be used to indicate whether the measured residue in samples produced in the EU is not approved at EU level per Regulation 1107/2009 (on the approved uses of plant protection products), nor to assess the presence of a pesticide residue (within a legal limit) in organic products that is not permitted in organic farming. |
| `J002A` | The residue in the sample is considered to be **below the level of concern**. |
| `J029A` | The residue was **not evaluated** — e.g. when the substance is only part of the full residue definition/group (`paramType = Part of a sum (P002A)`), or when no legal limit applies to the substance or residue measured. |
| `J031A` | The result is above the limit, but the residue in the sample is considered to be **compliant, taking into account the analytical measurement uncertainty**. |
| `J041A` | The result indicates the **occurrence of an illegal/prohibited VMPR** included in Group A (no MRL set for these substances) or the detection of an unauthorised food additive. |

(ChemMon 2026 p75)

### Report count

The count of non-compliant samples and results in EU reports will be based on the values reported in this data element in conjunction with `evalInfo.resAsses` as explained in paragraph N.06.3. (ChemMon 2026 p74)

### Related business rules

- **CHEMMON30** — If `evalCode` = J003A (Above MRL/ML), `anMethType` must be Confirmation (AT08A).
- **CHEMMON36** — When `evalLimitType = MRL`, `evalCode` must be one of J002A, J003A, J031A, or J029A.
- **CHEMMON60** — For pesticides, `evalCode` must be J002A, J003A, J029A, or J031A.
- **CHEMMON65** — `evalInfo.resAsses` can only be J037A (Compliant) or J038A (Non-compliant).
- **CHEMMON100** — For VMPR, `evalCode` is restricted to J002A, J003A, J029A, J031A, or J040A. See [[business-rules-vmpr]].

See [[business-rules-cross-cutting]], [[business-rules-pesticide]], and [[business-rules-vmpr]].

## actTakenCode — Action taken

<!-- Source: ChemMon 2026 pp. 75-76 -->

**Element code:** N.05 · **Name:** `actTakenCode` · **Catalogue:** ACTION · **Status:** mandatory for non-compliant VMPR/PPP, recommended for contaminants/additives

### Purpose

Action taken should be reported **when a non-conformity is identified during the control activities** or if a measured substance is found above the level of concern. Multiple actions can be reported.

### Why it matters

This is important for the pesticide samples if found non-compliant, to understand whether the product has been placed on the EU market and consumed or withdrawn without reaching the consumer or destroyed. (ChemMon 2026 p75)

### Mandatory cases

It is **mandatory for VMPR and pesticides to report the action taken in case of non-compliant results**. (ChemMon 2026 p75)

### Related business rules

- **CHEMMON37** — For CONT/ADD/FLAV, if `evalCode` = Detected or Above limit, `actTakenCode` is mandatory. See [[business-rules-cross-cutting]].
- **CHEMMON85** — For VMPR/PPP with non-compliant evaluation results, `actTakenCode` is mandatory.

## evalInfo.conclusion / evalInfo.com — Conclusion and comment

<!-- Source: ChemMon 2026 p76 -->

**Element codes:** N.06.1, N.06.2 · **Names:** `evalInfo.conclusion`, `evalInfo.com` · **Catalogue:** CONCLUS · **Status:** optional (recommended in various cases)

### Purpose

- **`evalInfo.conclusion`** is used to classify the findings of follow-up investigations.
- **`evalInfo.com`** is a free-text comment element that allows reporting additional details on non-compliant results or non-conformities.

This element may be included in EFSA Annual Reports listing non-compliant results.

### When to use evalInfo.conclusion

`evalInfo.conclusion` and `evalInfo.com` can also be used to **indicate when results are above a residue legal limit, but the final evaluation is compliant** — e.g. cases of natural occurrence or environmental contamination. (ChemMon 2026 p76)

`evalInfo.conclusion` should be used for reporting a **long shelf-life product** (code `C08A = 'Long shelf-life product'` from CONCLUS catalogue) for which the MRL in place at the time of placing it on the market was different than the MRL applicable on the current data collection for the given pesticide/crop combination. The BRs checking against the MRLs will not be applicable. (ChemMon 2026 p76)

### Food additives and flavourings specific usage

For the additives and flavourings domains, `evalInfo.conclusion` is highly recommended to be used to indicate **whether the food additive or flavouring was specified on the label of the analysed sample, or the positive analytical result was due to natural occurrence**. (ChemMon 2026 p76)

The codes to be used are those from the CONCLUS catalogue selecting the `fa_ff` hierarchy. The two main options are:

| Code | Meaning |
| --- | --- |
| `C19A` | Yes, present on label/added |
| `C20A` | No, not present on label/not added |
| `C05A` | Natural occurrence (can also be used in cases when the substance is in the sample as part of the matrix selection) |

For example, `C05A` could be reported in combination with code `C20A` (`C20A$C05A`) if the substance is not listed on the label/added but occurs naturally. (ChemMon 2026 p76)

### Examples (additives/flavourings)

| Description | XML |
| --- | --- |
| Ascorbic acid added as FA and naturally occurring | `<evalInfo.conclusion>C19A$C05A</evalInfo.conclusion>` |
| Ascorbic acid added as ingredient and naturally occurring | `<evalInfo.conclusion>C19A$C05A</evalInfo.conclusion><evalInfo.com>Ascorbic acid added as ingredient</evalInfo.com>` |
| XXX added as carry-over, and not as FA | `<evalInfo.conclusion>C19A</evalInfo.conclusion><evalInfo.com>Carry-over</evalInfo.com>` |
| Caffeine added as flavouring and declared on the label | `<evalInfo.conclusion>C19A</evalInfo.conclusion>` |
| "Flavourings" is declared on the label, without specifying "ethyl vanillate" | `<evalInfo.conclusion>C20A</evalInfo.conclusion>` |

(ChemMon 2026 p76)

### Related business rules

- **CHEMMON26** — If `actTakenCode = Follow-up investigation`, `evalInfo.conclusion` should be reported.
- **CHEMMON66_a** — If `evalInfo.resAsses = J037A` (Compliant) but `evalCode` indicates Above or Detected, `evalInfo.conclusion` should be reported.
- **CHEMMON66_b** — If `evalInfo.resAsses = J038A` (Non-compliant) but `evalCode` does not indicate Above or Detected, `evalInfo.conclusion` should be reported.
- **CHEMMON87** — `evalInfo.conclusion` is highly recommended for food additives/flavourings. See [[business-rules-additives]].
- **CHEMMON88** — `evalInfo.restrictionException` is highly recommended for food additives/flavourings.

See [[business-rules-cross-cutting]] and [[business-rules-additives]].
