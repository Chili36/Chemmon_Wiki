---
title: "SSD2 Programme: Programme Identification (progId)"
type: "reference"
domain: "all"
last_updated: "2026-04-23"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 17-18 (Section 2, element B.01)"
related:
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-data-model]]"
  - "[[chemmon-overview]]"
---

# SSD2 Programme: Programme Identification (progId)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 17-18 -->

## Rule Summary (Rule-First)

- `progId` is reportable but not part of EFSA's annual report routing logic.
- Use one stable identifier for all samples that belong to the same national programme, project, or ad hoc monitoring exercise.
- If a country does not use programme IDs internally, a default value for all records is acceptable as long as it stays within the 100-character limit.

## progId — Sampling programme identification code

<!-- Source: ChemMon 2026 p17 -->

**Element code:** B.01 · **Name:** `progId` · **Status:** reportable · **Format:** free text, size <= 100

### Purpose

`progId` lets a reporting country identify the national sampling programme or project under which a sample was taken. All samples analysed for the same purpose or objective should be grouped under the same code so data providers and EFSA can retrieve them together during validation or follow-up. EFSA also exposes `progId` in the validation dashboard for filtering and drill-down. (ChemMon 2026 p17)

### Use in EFSA reports

This element is **not used in EFSA national or annual reports**. It is kept for traceability, communication during validation, and national/nodal analysis rather than report inclusion. (ChemMon 2026 p17)

### Default value when no national programme ID exists

A country that does not use programme identifiers can still report `progId` by sending a single default value for all records. The guidance places no restriction on the chosen text other than the maximum length of 100 characters. (ChemMon 2026 p17)

### Examples

| Scenario | XML |
| --- | --- |
| Lithuanian default programme identifier for VMPR monitoring | `<progId>LT_2019_VMPR</progId>` |
| Slovak total diet study in 2016 | `<progId>SK_2016_TDS</progId>` |
| Romanian VMPR National Plan 3 (third-country imports) | `<progId>RO_2023_VMPR_Plan3</progId>` |

(ChemMon 2026 p18)
