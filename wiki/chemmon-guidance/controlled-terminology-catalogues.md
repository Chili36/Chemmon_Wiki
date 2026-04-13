---
title: "Controlled Terminology Catalogues"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 144-147 (Section 7; Tables 11-12)"
related:
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-elements-matrix]]"
  - "[[reporting-flags]]"
  - "[[chemmon-matrix-classification-algorithms]]"
---

# Controlled Terminology Catalogues

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Section 7 -->

## Overview

ChemMon submissions use EFSA **controlled terminologies** (catalogues): code lists (and their hierarchies) that constrain allowed values for many SSD2 elements (e.g. `progLegalRef`, `paramCode`, `resUnit`). EFSA publishes these catalogues for reference and download via Knowledge Junction / Zenodo. (ChemMon 2026 p144)

## How catalogues are used in validation

<!-- Source: ChemMon 2026 pp. 144-145 (Table 11 notes) -->

- Every reported code is validated against a **reporting hierarchy** for its catalogue.
- Some catalogues also define one or more **analysis hierarchies** used for legislative/reporting groupings; values in analysis hierarchies are also present in the catalogue’s reporting hierarchy.
- Some “hierarchies” used for reporting are dedicated catalogues derived from MTX (FoodEx2), used for legislative mapping (e.g. VMPR matrix classes and pesticide MATRIX groupings). (ChemMon 2026 pp. 144-145)

## ChemMon-critical catalogues (high signal)

<!-- Source: ChemMon 2026 p144-145 (Table 11) -->

| Catalogue | Where it shows up | ChemMon hierarchy / attributes |
| --- | --- | --- |
| `LEGREF` | `progLegalRef` | Reporting hierarchy: `ChemMonLegRef` with domain attributes (`VMPR`, `PEST`, `OCC`, `ADD`, `FLAV`). See [[reporting-flags]]. |
| `PARAM` | `paramCode` | Reporting hierarchy: `ChemMonRep`; analysis hierarchies: `vmprParam`, `pestParam`, `chemAnalysis`, `addAnalysis`, `flavAnalysis`. See [[reporting-flags]]. |
| `MTX` (FoodEx2) | `sampMatCode`, `anMatCode` | Reporting hierarchy (food/feed/non-food matrices). Legislative mappings are derived from MTX for domain-specific reporting (see [[chemmon-matrix-classification-algorithms]]). |
| `UNIT` | `resUnit`, limits/values units | Reporting hierarchy: `chemUnit`. |
| `SAMPSTR` | `sampStrategy` | Reporting hierarchy: `chemSampStr`. |
| `VALTYP` | `resType` / validation-type concepts | Reporting hierarchy: `chemValTyp`. |
| `ADDFOOD` | additives restrictions/exceptions | Used for some additives-specific codes (e.g. restrictions/exceptions). |

## Choosing `progLegalRef` (LEGREF) for correct reuse

<!-- Source: ChemMon 2026 pp. 146-147 (Table 12 + guidance text) -->

- Use the **most specific** LEGREF term available, to ensure correct inclusion in the intended reports and downstream reuse.
- Reporting the generic term `N129A` (Regulation (EC) No 178/2002) will still flag records for occurrence-style reuse (see [[reporting-flags]]), but may not align with inclusion criteria for the statutory EU Annual Reports. (ChemMon 2026 p147)
- If a needed piece of legislation is missing from `LEGREF` / `ChemMonLegRef`, contact EFSA with a suggested term during the major release consultation period (typically October–November), or earlier if there is an urgent need. (ChemMon 2026 p147)

