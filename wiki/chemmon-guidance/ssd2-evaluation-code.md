---
title: "SSD2 Evaluation: Result Evaluation Code"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 74-75 (Section 2, element N.04)"
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

## Related business rules

- `CHEMMON30` — if `evalCode = J003A`, `anMethType` must be confirmation. See [[business-rules-cross-cutting]].
- `CHEMMON36` — when the limit type is MRL, only a narrow code set is allowed. See [[business-rules-cross-cutting]].
- `CHEMMON60` — pesticide results are restricted to `J002A`, `J003A`, `J029A`, or `J031A`. See [[business-rules-pesticide]].
- `CHEMMON100` — VMPR has its own restricted allowed set. See [[business-rules-vmpr]].
