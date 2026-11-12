---
title: "ChemMon Matrix Classification Algorithms (VMPR, Pesticides)"
type: "reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 97 (Section 5)"
  - "pp. 41-42 (FoodEx2 mapping and general considerations)"
  - "p. 153 (correction of accepted data)"
related:
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-matrix-sampled-matrix]]"
  - "[[ssd2-matrix-vmpr-coding]]"
  - "[[vmpr-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[reporting-flags]]"
  - "[[chemmon-reports]]"
---

# ChemMon Matrix Classification Algorithms (VMPR, Pesticides)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Section 5 -->

## Overview

For the **National and Annual Reports** in the VMPR and pesticide domains, EFSA applies domain-specific **matrix-classification algorithms** that interpret the reported FoodEx2 matrix code (`sampMatCode`) and group samples into the legislative/reportable matrix groups required by the sectoral legislation. This page is about the downstream grouping layer; for constructing the matrix code itself, start at [[ssd2-matrix-sampled-matrix]] or [[ssd2-matrix-vmpr-coding]]. (ChemMon 2026 p97)

The guidance notes these algorithms are published on EFSA Knowledge Junction alongside other supporting tools, and are intended to help data providers verify that samples/results will be classified as expected based on the FoodEx2 codes they submit. (ChemMon 2026 p97)

## Pesticides: FoodEx2 to MATRIX grouping

<!-- Source: ChemMon 2026 p41 -->

- EFSA maps the reported FoodEx2 term to a pesticide-legislation **MATRIX** grouping used for the pesticide residues reports.
- For raw primary commodities (RPC), the mappings are recorded in the FoodEx2 catalogue as attributes of each term.
- The mapping is applied automatically in EFSA processing; data providers primarily need to ensure the **FoodEx2 code is correct**.

## VMPR: FoodEx2 to VMPR legislative categories

<!-- Source: ChemMon 2026 p41-42 -->

- EFSA maps FoodEx2 codes to VMPR legislative categories used for VMPR reporting.
- The mapping is applied automatically in EFSA processing; data providers primarily need to ensure the **FoodEx2 code is correct**.
- The mapping has been updated to accommodate changes introduced with Regulations (EU) 2022/1644 and 2022/1646. (ChemMon 2026 p42)

## Practical advice: validate before acceptance

<!-- Source: ChemMon 2026 p41, p153 -->

For pesticides, the FoodEx2-to-MATRIX mapping "can be checked" in the validation dashboards, and EFSA highly recommends checking that samples have been flagged as EUCP in accordance with expectations **before accepting** the dataset(s) in the confirmation dashboards. (ChemMon 2026 p41) Once data are 'Accepted' in the sDWH, the only way to correct them is through the record 'Update procedure' described in the GDE2 guidance. (ChemMon 2026 p153)
