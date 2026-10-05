---
title: "SSD2 Evaluation: Result Evaluation Code"
type: "reference"
domain: "all"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 74-75 (Section 2, element N.04)"
  - "pp. 77-78 (element N.06.3)"
related:
  - "[[ssd2-elements-evaluation]]"
  - "[[ssd2-elements-result]]"
  - "[[ssd2-analysis-methods]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Evaluation: Result Evaluation Code

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 74-75 -->

## Rule Summary (Rule-First)

- `evalCode` is mandatory and expresses the reporting authority's judgement of the result.
- The core pattern is simple: `J003A` for clearly above the level of concern, `J002A` for below/equal, `J029A` for not evaluated, and narrower codes for special situations.
- `paramType = P002A` usually pushes individual components toward `J029A`.
- Some domains restrict the allowed code set more tightly than the general catalogue does.

## evalCode — Evaluation of the result

<!-- Source: ChemMon 2026 pp. 74-75 -->

**Element code:** N.04 · **Name:** `evalCode` · **Catalogue:** `RESEVAL` · **Status:** mandatory

### Purpose

`evalCode` is the reporting country's judgement on whether the result exceeds the relevant legal limit or otherwise represents a non-compliant or noteworthy finding. It is applied at the level of each residue or marker within the analytical method. (ChemMon 2026 p74)

### Main codes

| Code | Meaning |
| --- | --- |
| `J003A` | Above the level of concern |
| `J002A` | Below or equal to the level of concern |
| `J029A` | Not evaluated |
| `J031A` | Above the limit but compliant when measurement uncertainty is taken into account |
| `J041A` | Detected illegal/prohibited VMPR or unauthorised food additive |

(ChemMon 2026 p75)

### Multicomponent handling

For individual components of a multicomponent residue definition or contaminant group (`paramType = P002A`), the expected code is usually `J029A` because the individual component is not itself the final evaluated residue definition. (ChemMon 2026 p74)

### VMPR detected case

For VMPR, `J041A` together with `evalLimitType = W012A` ("Presence") can be used and is counted as non-compliant, although the guidance notes that `J003A` could also be used. (ChemMon 2026 p74)

## Overall result assessment

`evalInfo.resAsses` (N.06.3) is optional and accepts only J037A (Compliant) or
J038A (Non-compliant). Preserve this field spelling. It records the authority's
overall assessment, which can differ from the numerical `evalCode` judgement.
The source's examples are:

| evalCode | evalInfo.resAsses | General counting outcome |
| --- | --- | --- |
| J003A | omitted | Non-compliant |
| J003A | J037A | Compliant |
| J002A | J038A | Non-compliant |

The **pesticide EU Annual Report is an exception**: its compliance counts use
`evalCode` only. Additional `resAsses` information does not change those counts.
Where assessment and evaluation differ, the field guidance calls for a reason
in `evalInfo.conclusion`; CHEMMON66_a/b are the narrower Warning conditions.
See [[ssd2-evaluation-conclusions]] and [[business-rules-cross-cutting]] for the
source's ambiguous Boolean wording. The source also says `sampEventAsses`,
`sampTkAsses` and `sampAnAsses` are not used for these non-compliance counts.
(ChemMon 2026 pp. 77–78)

## Related business rules

- `CHEMMON30` — if `evalCode = J003A`, `anMethType` must be confirmation. See [[business-rules-cross-cutting]].
- `CHEMMON36` — Warning: when the limit type is MRL, J002A/J003A/J031A/J029A are recommended. See [[business-rules-cross-cutting]].
- `CHEMMON60` — pesticide results are restricted to `J002A`, `J003A`, `J029A`, or `J031A`. See [[business-rules-pesticide]].
- `CHEMMON100` — VMPR permits J002A/J003A/J029A/J031A/J041A/J040A; this is a Warning in 2026. See [[business-rules-vmpr]].
