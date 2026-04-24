---
title: "Controlled Terminology Catalogues"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
source_pages:
  - "ChemMon 2026 pp. 144-147 (Section 7; Tables 11-12); No-presence 2026 Table 1 pp. 15-16; Use-levels 2026 Table 1 pp. 19-21"
related:
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-programme-legal-reference]]"
  - "[[ssd2-programme-strategy-and-type]]"
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-matrix-sampled-matrix]]"
  - "[[ssd2-analysis-parameter-coding]]"
  - "[[ssd2-evaluation-conclusions]]"
  - "[[reporting-flags]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[fa-ff-no-presence-data-model]]"
  - "[[fa-ff-use-levels-data-model]]"
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
| `LEGREF` | `progLegalRef` | Reporting hierarchy: `ChemMonLegRef` with domain attributes (`VMPR`, `PEST`, `OCC`, `ADD`, `FLAV`). The FA/FF parallel DMs use the sub-hierarchy **`faff`** directly (only `N112A` and `N113A` allowed). See [[ssd2-programme-legal-reference]] and [[reporting-flags]]. |
| `PARAM` | `paramCode` | Reporting hierarchy: `ChemMonRep`; analysis hierarchies: `vmprParam`, `pestParam`, `chemAnalysis`, `addAnalysis` (FA), `flavAnalysis` (FF). See [[ssd2-analysis-parameter-coding]] and [[reporting-flags]]. |
| `MTX` (FoodEx2) | `sampMatCode`, `anMatCode`, `matCode` (use-levels) | Reporting hierarchy (food/feed/non-food matrices). Legislative mappings are derived from MTX for domain-specific reporting (see [[chemmon-matrix-classification-algorithms]]); for SSD2 matrix-element behaviour see [[ssd2-matrix-sampled-matrix]]. |
| `UNIT` | `resUnit`, `unit` (use-levels), limits/values units | Reporting hierarchy: `chemUnit`. |
| `SAMPSTR` | `sampStrategy` | Reporting hierarchy: `chemSampStr`. See [[ssd2-programme-strategy-and-type]]. |
| `VALTYP` | `resType` / validation-type concepts | Reporting hierarchy: `chemValTyp`. |
| `ADDFOOD` | `restrictionException` (FA/FF) | FA restrictions/exceptions: hierarchy **`FARestExc`** (used with `progLegalRef=N112A`). FF restrictions/exceptions: hierarchy **`FFRestExc`** (used with `progLegalRef=N113A`). Report `ADD00881A` ("No restriction/exception to report") when nothing applies. |

## Catalogue usages surfaced by the FA/FF parallel data models

<!-- Source: No-presence 2026 Table 1 pp. 15-16; Use-levels 2026 Table 1 pp. 19-21 -->

The [[fa-ff-no-presence-data-model]] and [[fa-ff-use-levels-data-model]] make some catalogue usages more explicit than the ordinary SSD2 analytical path. Some are shared with SSD2 analytical reporting, while others are specific to the parallel FA/FF data models:

| Catalogue | Where it shows up | Hierarchy / usage |
| --- | --- | --- |
| `CONCLUS` | `presenceAdded` (both FA/FF DMs); `evalInfo.conclusion` on SSD2 analytical submissions | Hierarchy: **`faff`**. Codes: `C19A` (Yes, present on label/added), `C20A` (No, not present on label/not added), `C05A` (Natural occurrence). No-presence DM accepts `C20A` only; use-levels DM accepts all three plus combinations like `C19A$C05A`; SSD2 analytical additives/flavourings also use the same `faff` conclusion codes in `evalInfo.conclusion`. See [[ssd2-evaluation-conclusions]]. |
| `FUNC` | `functionOf` (both FA/FF DMs) | Functional class of the additive per Reg. 1333/2008 Annex I — 28 classes (sweeteners, colours, preservatives, antioxidants, carriers, acids, …) plus 5 Annex III classes. Required when `progLegalRef=N112A` in the parallel DMs. |
| `EXPRRES` | `weight` (use-levels DM only) | Hierarchy: **`WDFat`** — whole weight / dry matter / fat weight. Drives whether `fatPerc` or `moistPerc` must also be reported. |
| `YESNO` | `foodIndustry`, `widelyConsumed`, `maxPermittedLevelDefined` (use-levels DM) | Two-value catalogue: `Y` / `N`. |

All catalogue-value validations in the FA/FF parallel DMs are enforced via `PRE…` (no-presence) and `USE…` / `USE_LLDB…` (use-levels) business rules rather than the CHEMMON catalogue. See the DM pages for the rule tables.

## Choosing `progLegalRef` (LEGREF) for correct reuse

<!-- Source: ChemMon 2026 pp. 146-147 (Table 12 + guidance text) -->

- Use the **most specific** LEGREF term available, to ensure correct inclusion in the intended reports and downstream reuse.
- Reporting the generic term `N129A` (Regulation (EC) No 178/2002) will still flag records for occurrence-style reuse (see [[reporting-flags]]), but may not align with inclusion criteria for the statutory EU Annual Reports. (ChemMon 2026 p147)
- If a needed piece of legislation is missing from `LEGREF` / `ChemMonLegRef`, contact EFSA with a suggested term during the major release consultation period (typically October–November), or earlier if there is an urgent need. (ChemMon 2026 p147)
