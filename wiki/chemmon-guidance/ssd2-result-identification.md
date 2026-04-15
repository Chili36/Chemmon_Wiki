---
title: "SSD2 Result: Result Identification (resId)"
type: "reference"
domain: "all"
last_updated: "2026-04-15"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 64-65 (Section 2, element M.01)"
related:
  - "[[ssd2-elements-result]]"
  - "[[ssd2-data-model]]"
---

# SSD2 Result: Result Identification (resId)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 64-65 -->

## Rule Summary (Rule-First)

- `resId` is mandatory for every record.
- `resId` must be unique for an analytical result reported for a sample across all data collections from the same data provider.
- Use a naming convention (prefix/suffix) that guarantees uniqueness within a country; include stable context like lab/year/sequence if helpful.

## resId — Result identification code

<!-- Source: ChemMon 2026 pp. 64-65 -->

**Element code:** M.01 · **Name:** `resId` · **Status:** mandatory

### Purpose

This element must be provided for every record in the dataset and **must be unique for an analytical result reported for a sample across all data collections from a data provider**. This identifier is also used for communication between EFSA and the data provider during the transmission and validation phases. When validating data, it is essential to be able to detect which results are actually counted and to be able to identify which results may need to be amended. `resId` will be displayed in validation reports for non-compliant results (in aggregated tables by drill-down). (ChemMon 2026 p64)

### Naming convention

It is recommended that **certain prefixes or suffixes are included** to ensure the `resId` is unique within the country.

| Description | XML |
| --- | --- |
| Result reported by an Estonian veterinary laboratory in 2017 | `<resId>EEVetLab2017_0009435634</resId>` |
| Result reported by the Italian pesticides national reference laboratory in 2017 | `<resId>ITNRL2017_ADE0000456792</resId>` |
| Result reported by a Danish food testing laboratory in 2017 | `<resId>DKDTU2017_K0000034597X</resId>` |

(ChemMon 2026 p65)

