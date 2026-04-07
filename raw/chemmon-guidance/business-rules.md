---
title: "ChemMon Business Rules"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
last_updated: "2026-04-07"
---

# ChemMon Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Overview

- Business rules validate SSD2 submissions before acceptance into the EFSA data warehouse.
- Two severity levels: **Error** (blocks submission) and **Warning** (flags for review but does not block).
- Rules are domain-specific. Not all rules apply to all reporting domains (pesticides, contaminants, veterinary medicinal product residues, food additives/flavourings).
- Business rules take precedence when they conflict with prose sections of the guidance.

## Key Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON01 | Error | Unique `sampId` per sample | All |
| CHEMMON02 | Error | Country of sampling must equal reporting organisation country for pesticides | PPP |
| CHEMMON03 | Error | `sampCountry`/`origCountry` consistency for PPP domain | PPP |
| CHEMMON08 | Error | `resVal` = `resLOQ` relationship (amended 2026) | All |
| CHEMMON12 | Error | Acrylamide F33 mandatory -- `sampMatCode.legis` must contain specific product code when `paramCode` is acrylamide per Commission Regulation (EU) 2017/2158 and Recommendation (EU) 2019/1888 | CONT |
| CHEMMON39_a/b | Error | Food additive/flavouring legislative classes (merged 2026) | FA/FF |
| CHEMMON40 | Error | Result type validation (amended 2026; replaces CHEMMON47) | All |
| CHEMMON43_b | Warning | `sampY` less than submission year for additives/flavourings (new 2026) | FA/FF |
| CHEMMON50 | Error | Programme type validation (amended 2026; absorbs CHEMMON49) | All |
| CHEMMON79_a/b/c | Error | Contaminant analytical method validation (merged 2026) | CONT |
| CHEMMON84_a | Error | Food additive/flavouring result type (amended 2026) | FA/FF |
| CHEMMON84_b | Warning | Expression of result type recommended (amended 2026) | FA/FF |
| CHEMMON86 | Warning | Physical-state facet for additives/flavourings (amended 2026) | FA/FF |
| CHEMMON88 | Warning | Restriction/exception reporting (amended 2026) | All |
| CHEMMON90_a | Warning | Copper facet requirement (new 2026) | PPP |
| CHEMMON90_b | Error | Result value uncertainty for copper (new 2026) | PPP |
| CHEMMON94 | Error | Third-country import sampling point restriction (amended 2026) | All |
| CHEMMON95 | Warning | PPP sampling country validation (amended 2026) | PPP |
| CHEMMON96 | Error | VMPR sampling strategy for official programmes (amended 2026) | VMPR |
| CHEMMON97 | Error | Multi-domain sampling strategy validation (new 2026) | Multi |
| CHEMMON98 | Error | Control plan programme type restriction (new 2026) | Multi |
| CHEMMON99 | Warning | Third-country import origin validation (new 2026) | All |
| CHEMMON100 | Warning | VMPR evaluation code restrictions (new 2026) | VMPR |
| CHEMMON101 | Error | N422A regulation programme type (new 2026) | PPP |
| CHEMMON102 | Warning | VMPR consistency check for `sampleEventId` records (new 2026) | VMPR |
| CHEMMON103 | Warning | Organic/conventional production mutual exclusivity (new 2026) | All |
| CHEMMON104 | Error | N422A regulation exclusive programme reference (new 2026) | PPP |
| CHEMMON105 | Error | N317A regulation exclusive programme reference (new 2026) | CONT |
| CHEMMON106 | Warning | Potassium sorbate `paramText` requirement (new 2026) | FA/FF |
| CHEMMON107 | Warning | Sorbic acid derivative LOD reporting (new 2026) | FA/FF |
| CHEMMON108 | Warning | Food colour/additive classification codes (new 2026) | FA/FF |
| CHEMMON109 | Warning | Implicit additive/flavouring legislative category (new 2026) | FA/FF |

## 2026 Changes

### Amended rules

- **CHEMMON08** -- `resVal`/`resLOQ` relationship updated.
- **CHEMMON40** -- Result type validation expanded; replaces deactivated CHEMMON47.
- **CHEMMON50** -- Programme type validation expanded; absorbs deactivated CHEMMON49.
- **CHEMMON84_a** -- Food additive/flavouring result type updated.
- **CHEMMON84_b** -- Expression of result type recommended guidance revised.
- **CHEMMON86** -- Physical-state facet scope amended.
- **CHEMMON88** -- Restriction/exception reporting scope amended.
- **CHEMMON94** -- Third-country import sampling point restriction tightened.
- **CHEMMON95** -- PPP sampling country validation revised.
- **CHEMMON96** -- VMPR sampling strategy for official programmes updated.

### Merged rules

- **CHEMMON39_a/b** -- Previously separate food additive and flavouring legislative class rules consolidated into a single pair.
- **CHEMMON79_a/b/c** -- Contaminant analytical method validation rules consolidated.

### New rules

- CHEMMON43_b, CHEMMON90_a, CHEMMON90_b, CHEMMON97, CHEMMON98, CHEMMON99, CHEMMON100, CHEMMON101, CHEMMON102, CHEMMON103, CHEMMON104, CHEMMON105, CHEMMON106, CHEMMON107, CHEMMON108, CHEMMON109.

### Deactivated rules

- **CHEMMON47** -- Replaced by CHEMMON40.
- **CHEMMON49** -- Included in CHEMMON50.

## Legal Limit Rules

These rules compare reported result values against Maximum Permitted Levels. All are new in 2026 and apply to the food additives/flavourings domain.

| Rule ID | Severity | Description |
| --- | --- | --- |
| LL_01_FA_FF | Warning | Maximum Permitted Level comparison |
| LL_02_FA_FF | Warning | MPL threshold evaluation |
| LL_03_FA_FF | Warning | Legislative category substance authorization |
