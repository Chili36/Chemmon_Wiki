---
title: "SSD2 Matrix: Analysed Sample and Analysed Matrix"
type: "reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 56 (Section 2, F.01, G.01-G.02)"
  - "p. 101 (Table 9: GBR16)"
related:
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-elements-sampling]]"
  - "[[ssd2-elements-result]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-gbr]]"
---

# SSD2 Matrix: Analysed Sample and Analysed Matrix

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p56 -->

## Rule Summary (Rule-First)

- `sampAnId`, `anMatCode`, and `anMatText` default to the sampled-sample values when left empty.
- There is no need to report these fields unless the analysed material differs from the sampled material. (ChemMon 2026 p56)
- `sampAnId` must stay stable for the same analysed sample across parameters and transmissions.
- In VMPR and pesticides, `sampMatCode` and `anMatCode` are usually expected to match.

## sampAnId / anMatCode / anMatText — Sample analysed identification

<!-- Source: ChemMon 2026 p56 -->

**Element codes:** F.01 (`sampAnId`), G.01 (`anMatCode`), G.02 (`anMatText`)

### Purpose

These elements describe the material as actually analysed, which may differ in nature from the sample taken. (ChemMon 2026 p56)

### Default inheritance

If left empty, EFSA assumes:

- `sampAnId <- sampId`
- `anMatCode <- sampMatCode`
- `anMatText <- sampMatText`

Therefore there is no need to report these fields unless the analysed material truly differs from the sampled material. (ChemMon 2026 p56)

### `sampAnId`

Each analysed sample must have a unique identifier no longer than 100 characters. When several parameters are reported for the same analysed sample, the same `sampAnId` must be maintained for that analysed sample in all transmissions. (ChemMon 2026 p56)

### `anMatCode` and `anMatText`

- `anMatCode` is the FoodEx2-coded description of the analysed matrix.
- `anMatText` describes the analysed matrix as free text and could be reported on a voluntary basis, e.g. if the `anMatCode` FoodEx2 codes are not sufficiently detailed (ChemMon 2026 p56). It must be reported if `anMatCode.gen` is 'Other' (`A07XE`) (`GBR16`, Error; ChemMon 2026 p101).

## Related business rules

- `CHEMON27` — in VMPR and pesticides, `sampMatCode` should equal `anMatCode`. See [[business-rules-cross-cutting]].
- `FOODEX2_ANMAT` — analysed matrix must be a valid FoodEx2 code. See [[business-rules-cross-cutting]].
- `GBR4` — analysed-sample / analysed-matrix consistency. See [[business-rules-gbr]].
