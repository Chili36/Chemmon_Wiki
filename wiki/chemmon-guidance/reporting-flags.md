---
title: "Reporting Flags in the EFSA Scientific Data Warehouse"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 148-149 (Section 9)"
related:
  - "[[controlled-terminology-catalogues]]"
  - "[[chemmon-reports]]"
  - "[[business-rules]]"
  - "[[ssd2-elements-programme]]"
---

# Reporting Flags in the EFSA Scientific Data Warehouse

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Section 9 -->

## Why flags exist

Since ChemMon merges multiple chemical-monitoring domains into one data collection, EFSA records **domain relevance per result** to avoid double reporting and to support reuse across domains (e.g. substances that are both pesticides and VMPR, or both contaminants and food additives). (ChemMon 2026 p148)

EFSA stores five flags per result record:

- VMPR (`is_vet`)
- Pesticides (`is_pest`)
- Contaminants (`is_occ`)
- Food additives (`is_add`)
- Food flavourings (`is_flav`) (ChemMon 2026 p148)

## Flagging algorithm (as described in guidance)

<!-- Source: ChemMon 2026 p148-149 -->

EFSA describes the current flagging algorithm as based on:

- `progLegalRef` (LEGREF), and
- `paramCode` (PARAM).

EFSA notes matrix and reported unit can also affect flags, and the algorithm may be adjusted in future (including use of the Legal Limits Database). (ChemMon 2026 p148)

### What “in the domain” means

<!-- Source: ChemMon 2026 p149 -->

- `progLegalRef` is checked via the `ChemMonLegRef` hierarchy attributes (`VMPR`, `PEST`, `OCC`, `ADD`, `FLAV`) in the LEGREF catalogue. See [[controlled-terminology-catalogues]].
- `paramCode` is checked via domain analysis hierarchies in the PARAM catalogue (`vmprParam`, `pestParam`, `chemAnalysis`, `addAnalysis`, `flavAnalysis`).

### Flag values (0–3)

<!-- Source: ChemMon 2026 p149 -->

| Flag value | Meaning for a given domain flag (e.g. `is_pest`) |
| --- | --- |
| 0 | Neither `progLegalRef` nor `paramCode` are in the domain |
| 1 | Both `progLegalRef` and `paramCode` are in the domain |
| 2 | Only `paramCode` is in the domain |
| 3 | Only `progLegalRef` is in the domain |

## Examples

<!-- Source: ChemMon 2026 p149 -->

- If `progLegalRef=N371A` (VMPR) and `paramCode=RF-00000411-VET` (Testosterone-17-Alpha; VMPR-only), EFSA describes the result as flagged `is_vet=1` and the other four flags as `0`.
- If `progLegalRef=N371A` (VMPR) and `paramCode=RF-0024-002-PPP` (Amitraz; in `vmprParam` and `pestParam`), EFSA describes the result as flagged `is_vet=1` and `is_pest=2` (other flags `0`).

## How flags are used

<!-- Source: ChemMon 2026 p149-150 -->

- Business rules can be applied according to flags (the guidance gives the example that CHEMMON73 applies if `VMPR=1`). (ChemMon 2026 p149)
- Validation dashboards and other downstream reports filter records using these flags (see [[chemmon-reports]]). (ChemMon 2026 p150)

