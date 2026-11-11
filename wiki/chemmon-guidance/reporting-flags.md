---
title: "Reporting Flags in the EFSA Scientific Data Warehouse"
type: "reference"
domain: "all"
last_updated: "2026-11-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 148-149 (Section 9, flag-value table and example table); pp. 150-151 (Table 13 flag names)"
related:
  - "[[controlled-terminology-catalogues]]"
  - "[[chemmon-reports]]"
  - "[[business-rules]]"
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-programme-legal-reference]]"
  - "[[ssd2-analysis-parameter-coding]]"
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
- Food flavourings (`is_flav`) (ChemMon 2026 p148-149)

The flags are created when the records are received into the DCF, which lets a specific business rule apply only to the records it is relevant for. (ChemMon 2026 p148)

Source discrepancy: the VMPR flag is `is_vet` in Section 9 and in Table 10 (ChemMon 2026 p149, p118), `is_vmpr` in Table 13 (ChemMon 2026 p150-151) and "VMPR=1" in one sentence (ChemMon 2026 p149). They are the same flag; business rules use `is_vet`.

## Flagging algorithm (as described in guidance)

<!-- Source: ChemMon 2026 p148-149 -->

EFSA describes the current flagging algorithm as based on:

- `progLegalRef` (LEGREF), and
- `paramCode` (PARAM).

EFSA notes matrix and reported unit can also affect flags, and the algorithm may be adjusted in future (including use of the Legal Limits Database). (ChemMon 2026 p148)

### What “in the domain” means

<!-- Source: ChemMon 2026 p149 -->

- `progLegalRef` is checked via the `ChemMonLegRef` hierarchy attributes (`VMPR`, `PEST`, `OCC`, `ADD`, `FLAV`) in the LEGREF catalogue. See [[controlled-terminology-catalogues]] and [[ssd2-programme-legal-reference]].
- `paramCode` is checked via domain analysis hierarchies in the PARAM catalogue (`vmprParam`, `pestParam`, `chemAnalysis`, `addAnalysis`, `flavAnalysis`). See [[ssd2-analysis-parameter-coding]].

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

Example table (ChemMon 2026 p149):

| Example | `is_vet` | `is_pest` | `is_occ` | `is_add` | `is_flav` |
| --- | --- | --- | --- | --- | --- |
| `progLegalRef`=VMPR records whose PARAM is only VMPR | 1 | 0 | 0 | 0 | 0 |
| `progLegalRef`=VMPR records whose PARAM is both VMPR and OCC (contaminants) | 1 | 0 | 2 | 0 | 0 |
| `progLegalRef`=VMPR records whose PARAM is both VMPR and pesticides | 1 | 2 | 0 | 0 | 0 |
| `progLegalRef`=VMPR and OCC (contaminants) records whose PARAM is both VMPR and OCC (contaminants) | 1 | 0 | 1 | 0 | 0 |
| `progLegalRef`=ADD records whose PARAM is both ADD and OCC | 0 | 0 | 1 | 1 | 0 |
| `progLegalRef`=FLAV records whose PARAM is only FLAV | 0 | 0 | 0 | 0 | 1 |

Source discrepancy: the ADD row prints `is_occ`=1 although only the PARAM, not the `progLegalRef`, is in the contaminants domain; by the flag-value table that case is 2, as the second row shows for VMPR with an OCC parameter (both ChemMon 2026 p149). The guidance does not explain the difference.

Two worked examples in the text (ChemMon 2026 p149):

- If `progLegalRef=N371A` (VMPR) and `paramCode=RF-00000411-VET` (Testosterone-17-Alpha; VMPR-only), EFSA describes the result as flagged `is_vet=1` and the other four flags as `0`.
- If `progLegalRef=N371A` (VMPR) and `paramCode=RF-0024-002-PPP` (Amitraz; in `vmprParam` and `pestParam`), EFSA describes the result as flagged `is_vet=1` and `is_pest=2` (other flags `0`).

## How flags are used

<!-- Source: ChemMon 2026 p149-150 -->

- Business rules can be applied according to flags (the guidance gives the example that CHEMON73 "will apply if VMPR=1"). (ChemMon 2026 p149)
- Validation dashboards and other downstream reports filter records using these flags (see [[chemmon-reports]]). (ChemMon 2026 p150)
