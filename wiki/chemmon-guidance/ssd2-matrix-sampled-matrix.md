---
title: "SSD2 Matrix: Sampled Matrix Code and Text"
type: "reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 32-33 (Section 2, E.02)"
  - "p. 42 (drinking water note)"
  - "p. 56 (Section 2, E.03)"
  - "p. 101 (Table 9: GBR15)"
related:
  - "[[ssd2-elements-matrix]]"
  - "[[foodex2-in-chemmon]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[controlled-terminology-catalogues]]"
---

# SSD2 Matrix: Sampled Matrix Code and Text

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 32-33, 42, 56 -->

## Rule Summary (Rule-First)

- `sampMatCode` is mandatory; the highest-detail suitable FoodEx2 term from the MTX reporting hierarchy is normally used. (ChemMon 2026 p32)
- If implicit facets already characterise the matrix sufficiently, do not restate them explicitly.
- If a suitable FoodEx2 term is missing, ask EFSA for support or code addition rather than forcing a broad or incorrect term.
- `sampMatText` is optional (ChemMon 2026 p56), but must be reported if `sampMatCode.gen` is 'Other' (`A07XE`) (`GBR15`, Error; ChemMon 2026 p101). It supplements the code for description and cross-checking; it should not contain brand names. (ChemMon 2026 p56)

## sampMatCode — Coded description of the matrix of the sample taken

<!-- Source: ChemMon 2026 p32 -->

**Element code:** E.02 · **Name:** `sampMatCode` · **Catalogue:** `MTX` (FoodEx2) · **Status:** mandatory

### Purpose

`sampMatCode` is the FoodEx2-coded description of the sampled matrix. Data providers should normally use the most detailed suitable code available, for example a commodity-level term rather than a broad botanical or matrix group. (ChemMon 2026 p32)

### Reporting hierarchy and downstream classification

FoodEx2 codes are selected from the MTX catalogue reporting hierarchy, which includes food, feed, and non-food animal matrices. If the sample is not yet declared or intended as food or feed, it must be reported as food. EFSA then applies legislative/reporting hierarchies and algorithms to `sampMatCode` for annual-report grouping and legal-limit classification. (ChemMon 2026 p32)

### Base terms and facets

A FoodEx2 base term is always required. If the chosen base term already contains the needed implicit facets, report only the base term. Explicit facets should be added only when they supply additional information not already implicit in the term. For the general FoodEx2 facet logic, see [[foodex2-in-chemmon]]. (ChemMon 2026 p33)

## Drinking water intended for human consumption (`A03DK`)

<!-- Source: ChemMon 2026 p42 -->

EFSA encourages reporting available pesticide and contaminant results for drinking water intended for human consumption using the FoodEx2 base term `A03DK` ("Drinking water") and its children. This is distinct from water given to farmed animals under VMPR/feed-style coding, which is handled separately in [[ssd2-matrix-vmpr-coding]]. (ChemMon 2026 p42)

## sampMatText — Text description of the matrix of the sample taken

<!-- Source: ChemMon 2026 p56 -->

**Element code:** E.03 · **Name:** `sampMatText` · **Status:** optional

### Purpose

After encoding the sampled matrix in `sampMatCode`, `sampMatText` can be used to give a fuller textual description of the sampled product or add relevant context that helps with quality checks and later analysis. (ChemMon 2026 p56)

### When FoodEx2 is not enough

If a suitable FoodEx2 term cannot be found, the guidance recommends contacting EFSA for support or for the addition of codes rather than relying on text alone. `sampMatText` is not a substitute for correct FoodEx2 coding. (ChemMon 2026 p56)

### What not to include

Brand names do not belong in `sampMatText`; they can be reported in element E.10 (`sampMatInfo`). (ChemMon 2026 p56)
