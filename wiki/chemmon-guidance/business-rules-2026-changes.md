---
title: "2026 Business Rule Changes"
select_when: "Changes effective for the 2026 collection, merged or deactivated IDs and future transition notes. Use canonical rule pages for the operative conditions."
type: "rule-reference"
domain: "all"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-change-management]]"
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

Annual delta of business rule changes for the 2026 ChemMon data collection. This file is a reference log of **what changed** — it does not contain canonical rule definitions. The definitive text of each rule lives in its respective slice file (referenced below each entry). Use this file to understand what's new, what's been tightened, and what's been retired since the 2025 guidance. For the revision cadence and why ordinary rule changes usually lag by one sampling cycle, see [[chemmon-change-management]].

## Amended rules

- **CHEMON08** -- `resVal`/`resLOQ` relationship updated: if `resVal` equals `resLOQ`, `resType` must be VAL. Defined in [[business-rules-cross-cutting]].
- **CHEMON40** -- Result type validation expanded for qualitative results; replaces deactivated CHEMON47. Defined in [[business-rules-cross-cutting]].
- **CHEMON50** -- Programme type validation expanded; absorbs deactivated CHEMON49. Defined in [[business-rules-cross-cutting]].
- **CHEMON84_a** -- Food additive/flavouring `exprResType` requirement updated. Defined in [[business-rules-additives]].
- **CHEMON84_b** -- Expression of result type recommended guidance revised for contaminants. Defined in [[business-rules-contaminant]].
- **CHEMON86** -- Physical-state facet scope amended for food additives/flavourings. Defined in [[business-rules-additives]].
- **CHEMON88** -- Restriction/exception reporting scope amended. Defined in [[business-rules-additives]].
- **CHEMON94** -- Third-country import sampling point restriction tightened to require E010A for K038A. Defined in [[business-rules-cross-cutting]].
- **CHEMON95** -- PPP non-compliant origin country validation revised; expanded list of excluded generic codes. Defined in [[business-rules-pesticide]].
- **CHEMON96** -- VMPR sampling strategy for official programmes updated to include ST90A. Defined in [[business-rules-vmpr]].

## Merged rules

- **CHEMON39** -- Previous CHEMON39_a and CHEMON39_b rules are merged into CHEMON39 in 2026. Defined in [[business-rules-additives]].
- **CHEMON79** -- Previous CHEMON79_a, CHEMON79_b and CHEMON79_c rules are merged into CHEMON79 in 2026. Method code cannot be Unknown/Unspecified/Classification not possible. Defined in [[business-rules-cross-cutting]].

## New rules

- **CHEMON43_b** -- Sampling year validation for additives/flavourings (Warning; becomes Error 2027). Defined in [[business-rules-additives]].
- **CHEMON90_a** -- Copper facet requirement for F20/F28. Defined in [[business-rules-pesticide]].
- **CHEMON90_b** -- Measurement uncertainty mandatory for copper when `resType` = VAL. Defined in [[business-rules-pesticide]].
- **CHEMON97** -- Multi-domain sampling strategy validation for K005A across PPP/CONT/ADD/FLAV. Defined in [[business-rules-cross-cutting]].
- **CHEMON98** -- Programme type restriction for contaminants under N375A. Defined in [[business-rules-contaminant]].
- **CHEMON99** -- Import origin validation: `origCountry` cannot equal `sampCountry` for import programmes. Defined in [[business-rules-cross-cutting]].
- **CHEMON100** — VMPR evaluation restricted to six codes, including J041A (Detected). Warning in 2026. Defined in [[business-rules-vmpr]].
- **CHEMON101** -- N422A regulation requires K019A programme type and ST30A strategy. Defined in [[business-rules-pesticide]].
- **CHEMON102** -- VMPR geographic consistency check across `sampEventId` records. Defined in [[business-rules-vmpr]].
- **CHEMON103** -- Organic/conventional production mutual exclusivity. Defined in [[business-rules-cross-cutting]].
- **CHEMON104** -- N422A exclusive programme reference (no concatenation). Defined in [[business-rules-pesticide]].
- **CHEMON105** — N317A exclusive programme reference (no concatenation); not limited to contaminants. Defined in [[business-rules-cross-cutting]].
- **CHEMON106** -- Potassium sorbate `paramText` should specify free acid or salt form (Warning). Defined in [[business-rules-additives]].
- **CHEMON107** — LOD highly recommended for the six named parameters, including potassium sorbate, when `resType=BIN` and `resQualValue=NEG`. Defined in [[business-rules-additives]].
- **CHEMON108** -- Generic `sampMatCode` terms restricted for additives/flavourings. Defined in [[business-rules-additives]].
- **CHEMON109** -- Implicit F33 makes explicit F33 unnecessary for additives/flavourings. Defined in [[business-rules-additives]].
- **LL_01_FA_FF** -- MPL comparison for food additives/flavourings. Defined in [[business-rules-legal-limits]].
- **LL_02_FA_FF** -- MPL threshold evaluation for food additives/flavourings. Defined in [[business-rules-legal-limits]].
- **LL_03_FA_FF** -- Substance authorisation check for food additives/flavourings. Defined in [[business-rules-legal-limits]].

## Deactivated rules

- **CHEMON47** -- Replaced by CHEMON40 (qualitative result value validation).
- **CHEMON49** -- Included in CHEMON50 (programme type validation).
- **CHEMON53** -- Obsolete per 2025 update.
- **CHEMON81** -- Replaced by CHEMON40 (result type validation).
