---
title: "2026 Business Rule Changes"
type: "rule-reference"
domain: "all"
last_updated: "2026-04-10"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[business-rules]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-contaminant]]"
  - "[[business-rules-additives]]"
---

# 2026 Business Rule Changes

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->

## Overview

Annual delta of business rule changes for the 2026 ChemMon data collection. This file is a reference log of **what changed** — it does not contain canonical rule definitions. The definitive text of each rule lives in its respective slice file (referenced below each entry). Use this file to understand what's new, what's been tightened, and what's been retired since the 2025 guidance.

## Amended rules

- **CHEMMON08** -- `resVal`/`resLOQ` relationship updated: if `resVal` equals `resLOQ`, `resType` must be VAL. Defined in [[business-rules-cross-cutting]].
- **CHEMMON40** -- Result type validation expanded for qualitative results; replaces deactivated CHEMMON47. Defined in [[business-rules-cross-cutting]].
- **CHEMMON50** -- Programme type validation expanded; absorbs deactivated CHEMMON49. Defined in [[business-rules-cross-cutting]].
- **CHEMMON84_a** -- Food additive/flavouring `exprResType` requirement updated. Defined in [[business-rules-additives]].
- **CHEMMON84_b** -- Expression of result type recommended guidance revised for contaminants. Defined in [[business-rules-contaminant]].
- **CHEMMON86** -- Physical-state facet scope amended for food additives/flavourings. Defined in [[business-rules-additives]].
- **CHEMMON88** -- Restriction/exception reporting scope amended. Defined in [[business-rules-additives]].
- **CHEMMON94** -- Third-country import sampling point restriction tightened to require E010A for K038A. Defined in [[business-rules-cross-cutting]].
- **CHEMMON95** -- PPP non-compliant origin country validation revised; expanded list of excluded generic codes. Defined in [[business-rules-pesticide]].
- **CHEMMON96** -- VMPR sampling strategy for official programmes updated to include ST90A. Defined in [[business-rules-vmpr]].

## Merged rules

- **CHEMMON39_a/b** -- Previously separate food additive and flavouring legislative class rules consolidated into a single pair. Defined in [[business-rules-additives]].
- **CHEMMON79_a/b/c** -- Contaminant, additive, and flavouring analytical method validation rules consolidated. Method code cannot be Unknown/Unspecified/Classification not possible. Defined in [[business-rules-cross-cutting]].

## New rules

- **CHEMMON43_b** -- Sampling year validation for additives/flavourings (Warning; becomes Error 2027). Defined in [[business-rules-additives]].
- **CHEMMON90_a** -- Copper facet requirement for F20/F28. Defined in [[business-rules-pesticide]].
- **CHEMMON90_b** -- Measurement uncertainty mandatory for copper when `resType` = VAL. Defined in [[business-rules-pesticide]].
- **CHEMMON97** -- Multi-domain sampling strategy validation for K005A across PPP/CONT/ADD/FLAV. Defined in [[business-rules-cross-cutting]].
- **CHEMMON98** -- Programme type restriction for contaminants under N375A. Defined in [[business-rules-contaminant]].
- **CHEMMON99** -- Import origin validation: `origCountry` cannot equal `sampCountry` for import programmes. Defined in [[business-rules-cross-cutting]].
- **CHEMMON100** -- VMPR evaluation code restricted to five permitted codes. Defined in [[business-rules-vmpr]].
- **CHEMMON101** -- N422A regulation requires K019A programme type and ST30A strategy. Defined in [[business-rules-pesticide]].
- **CHEMMON102** -- VMPR geographic consistency check across `sampEventId` records. Defined in [[business-rules-vmpr]].
- **CHEMMON103** -- Organic/conventional production mutual exclusivity. Defined in [[business-rules-cross-cutting]].
- **CHEMMON104** -- N422A exclusive programme reference (no concatenation). Defined in [[business-rules-pesticide]].
- **CHEMMON105** -- N317A exclusive programme reference (no concatenation). Defined in [[business-rules-contaminant]].
- **CHEMMON106** -- Potassium sorbate `paramText` must specify free acid or salt form. Defined in [[business-rules-additives]].
- **CHEMMON107** -- LOD highly recommended for sorbic acid, BHT, coumarin, HCN, theobromine. Defined in [[business-rules-additives]].
- **CHEMMON108** -- Generic `sampMatCode` terms restricted for additives/flavourings. Defined in [[business-rules-additives]].
- **CHEMMON109** -- Implicit F33 makes explicit F33 unnecessary for additives/flavourings. Defined in [[business-rules-additives]].
- **LL_01_FA_FF** -- MPL comparison for food additives/flavourings. Defined in [[business-rules-legal-limits]].
- **LL_02_FA_FF** -- MPL threshold evaluation for food additives/flavourings. Defined in [[business-rules-legal-limits]].
- **LL_03_FA_FF** -- Substance authorisation check for food additives/flavourings. Defined in [[business-rules-legal-limits]].

## Deactivated rules

- **CHEMMON47** -- Replaced by CHEMMON40 (qualitative result value validation).
- **CHEMMON49** -- Included in CHEMMON50 (programme type validation).
- **CHEMMON53** -- Obsolete per 2025 update.
- **CHEMMON81** -- Replaced by CHEMMON40 (result type validation).
