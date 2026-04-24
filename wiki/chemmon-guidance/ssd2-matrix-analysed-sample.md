---
title: "SSD2 Matrix: Analysed Sample and Analysed Matrix"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 56 (Section 2, F.01, G.01-G.02)"
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
- Only report these fields when the analysed material actually differs from the sampled material.
- `sampAnId` must stay stable for the same analysed sample across parameters and transmissions.
- In VMPR and pesticides, `sampMatCode` and `anMatCode` are usually expected to match.

## sampAnId / anMatCode / anMatText — Sample analysed identification

<!-- Source: ChemMon 2026 p56 -->

**Element codes:** F.01 (`sampAnId`), G.01 (`anMatCode`), G.02 (`anMatText`)

### Purpose

These elements describe the material as actually analysed, which can differ from the sampled matrix when only a portion or derived material was analysed. (ChemMon 2026 p56)

### Default inheritance

If left empty, EFSA assumes:

- `sampAnId <- sampId`
- `anMatCode <- sampMatCode`
- `anMatText <- sampMatText`

Therefore there is no need to report these fields unless the analysed material truly differs from the sampled material. (ChemMon 2026 p56)

### `sampAnId`

Each analysed sample must have a unique identifier no longer than 100 characters. When several parameters are reported for the same analysed sample, the same `sampAnId` should be preserved across those records and across later transmissions. (ChemMon 2026 p56)

### `anMatCode` and `anMatText`

- `anMatCode` is the FoodEx2-coded description of the analysed matrix.
- `anMatText` is the optional free-text supplement for the analysed matrix when the code alone is not sufficiently descriptive. (ChemMon 2026 p56)

## Related business rules

- `CHEMMON27` — in VMPR and pesticides, `sampMatCode` should equal `anMatCode`. See [[business-rules-cross-cutting]].
- `FOODEX2_ANMAT` — analysed matrix must be a valid FoodEx2 code. See [[business-rules-cross-cutting]].
- `GBR4` — analysed-sample / analysed-matrix consistency. See [[business-rules-gbr]].
