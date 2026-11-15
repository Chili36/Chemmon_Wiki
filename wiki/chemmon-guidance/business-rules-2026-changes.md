---
title: "2026 Business Rule Changes"
select_when: "Changes effective for the 2026 collection, merged or deactivated IDs and future transition notes. Use canonical rule pages for the operative conditions."
type: "rule-reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 11-16 (Table 1: main changes introduced with the 2026 data collection)"
  - "pp. 113-143 (Table 10 comment column for introduction years and announced changes)"
  - "p. 70 (M.13/M.14: years exprResType became mandatory for food additives and food flavourings)"
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

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 11-16 (Table 1), pp. 113-143 (Table 10 comments) -->

## Overview

Annual delta of business rule changes for the 2026 ChemMon data collection. This file is a reference log of **what changed** — it does not contain canonical rule definitions. The definitive text of each rule lives in its respective slice file (referenced below each entry). Use this file to understand what's new, what's been tightened, and what's been retired since the 2025 guidance. For the revision cadence and why ordinary rule changes usually lag by one sampling cycle, see [[chemmon-change-management]].

Each entry below states what Table 1 says changed (ChemMon 2026 pp. 11-16). "Type" is Table 1's "Type of change" cell, which for rules is the 2026 severity.

## Amended rules

- **CHEMON08** (Error) -- If `resVal` equals `resLOQ`, `resType` must be VAL. (p11) Defined in [[business-rules-cross-cutting]].
- **CHEMON40** (Error) -- If `resType` is BIN, LOQ or LOD, `resVal` must be empty. CHEMON47 is inactivated because CHEMON40 "is more complete". (p11-12) Defined in [[business-rules-cross-cutting]].
- **CHEMON50** (Error) -- If `progType` is K018A or K009A and `progLegalRef` contains N027A, `sampStrategy` can only be ST10A or ST20A. Its updated description includes CHEMON49. (p12) Defined in [[business-rules-cross-cutting]].
- **CHEMON84_a** (Error) -- For food additives or food flavourings, `exprResType` must be reported. "From warning to error message in 2026." (p12) The Table 10 comment says "It becomes an Error for food flavourings in 2026" (p133); M.13/M.14 says `exprResType` "became mandatory in 2025 and 2026 respectively" for food additives and food flavourings (p70). Defined in [[business-rules-additives]].
- **CHEMON84_b** (Warning) -- For contaminants in food, `exprResType` is highly recommended. "Business rule remains a warning message for contaminants." (p12) Defined in [[business-rules-contaminant]].
- **CHEMON86** (Warning) -- For food additives or food flavourings, F03 is highly recommended, if not implicit, for categories 1, 6.3, 12.5, 12.6, 13, 14.1.2, 14.1.3, 14.1.4, 14.1.5 and 17. "From warning to error message in 2027" for categories 12.5, 13, 14.1.4, 14.1.5 and 17. (p12-13) Defined in [[business-rules-additives]].
- **CHEMON88** (Warning) -- For food additives or food flavourings, `evalInfo.restrictionException` is highly recommended. "This business rule might become an error in 2027." (p13) Defined in [[business-rules-additives]].
- **CHEMON90_a** (Warning) -- If copper (`RF-0102-001-PPP`) is reported, facet F20 and/or F28 is needed. "Business rule remains a warning"; "From warning to error message in 2027." Introduced in 2025. (p13, p135) Defined in [[business-rules-pesticide]].
- **CHEMON90_b** (Error) -- If copper (`RF-0102-001-PPP`) is reported, `resValUncert` must be reported if `resType` = VAL. "From Warning to Error message in 2026." Introduced in 2025. (p13, p135) Defined in [[business-rules-pesticide]].
- **CHEMON94** (Error) -- If `progType` is K038A, `sampPoint` can only be E010A (Border Control Posts). "From warning to error message in 2026." (p13) Introduced in 2025 (Table 10 p136). Defined in [[business-rules-cross-cutting]].
- **CHEMON95** (Warning) -- For pesticides (`is_pest=1`) with `evalCode` J003A, a country of origin different from XX, AA, EU, XC, XD and XE must be reported. "It remains a warning in 2026." Introduced in 2025. (p13, p137) Defined in [[business-rules-pesticide]].
- **CHEMON96** (Error) -- For VMPR with `progType` K005A, `sampStrategy` can only be ST10A, ST20A, ST30A or ST90A. "From warning to error message in 2026." Introduced in 2025. (p13, p137) Defined in [[business-rules-vmpr]].
- **CHEMON97** (Error) -- For pesticides, contaminants, additives or flavourings with `progType` K005A, `sampStrategy` can only be ST10A, ST20A or ST30A. "From warning to error message in 2026." Introduced in 2025. (p14, p137) Defined in [[business-rules-cross-cutting]].
- **CHEMON98** (Error) -- For contaminants related to control plans (`progLegalRef` N375A), `progType` can only be K005A, K018A or K038A. "From warning to error message in 2026." Introduced in 2025. (p14, p137-138) Defined in [[business-rules-contaminant]].

## Merged rules

- **CHEMON39** (Error) -- CHEMON39_a and CHEMON39_b are merged into CHEMON39. (p11) Defined in [[business-rules-additives]].
- **CHEMON79** (Error) -- CHEMON79_a, CHEMON79_b and CHEMON79_c are merged into CHEMON79: for contaminants, food additives or food flavourings, `anMethCode` should be different from Unknown (F500A), Unspecified (F598A) or Classification not possible (F001A). The Table 10 comment adds that it becomes an Error in 2026 for all domains. (p12, p132) Defined in [[business-rules-cross-cutting]].

## New rules

- **CHEMON43_b** (Warning) -- Sampling year validation for food additives and food flavourings. "From warning to error message in 2027"; CHEMON43 and CHEMON43_b will be merged in 2027. (p11) Defined in [[business-rules-additives]].
- **CHEMON99** (Warning) -- If `progType` is K038A or K019A, or `sampPoint` is E010A, `origCountry` cannot equal `sampCountry`. "From warning to error message in 2027." (p14) Defined in [[business-rules-cross-cutting]].
- **CHEMON100** (Warning) — VMPR `evalCode` restricted to six codes, including J041A (Detected). "From warning to error message in 2027." (p14) Defined in [[business-rules-vmpr]].
- **CHEMON101** (Error) -- If `progLegalRef` is N422A, `progType` is K019A and `sampStrategy` can only be ST30A. "Error message already in 2026." (p14) Defined in [[business-rules-cross-cutting]].
- **CHEMON102** (Warning) -- VMPR geographic elements should be constant across records with the same `sampEventId`. "From warning to error message in 2027." (p15) Defined in [[business-rules-vmpr]].
- **CHEMON103** (Warning) -- Organic (A07SE) and conventional (A0C6Y) production should not be reported together; in that case the sample will be considered organic. "From warning to error message in 2027." (p15) Defined in [[business-rules-cross-cutting]].
- **CHEMON104** (Error) -- If `progLegalRef` is N422A, no other `progLegalRef` can be used. "Error message already in 2026." (p15) Defined in [[business-rules-cross-cutting]].
- **CHEMON105** (Error) — If `progLegalRef` is N317A, no other `progLegalRef` can be used; not limited to contaminants. "Error message already in 2026." (p15) Defined in [[business-rules-cross-cutting]].
- **CHEMON106** (Warning) -- Potassium sorbate `paramText` should specify "Expressed as free acid" or "Expressed as salt". (p15) Defined in [[business-rules-additives]].
- **CHEMON107** (Warning) — LOD highly recommended for the six named parameters, including potassium sorbate, when `resType=BIN` and `resQualValue=NEG`. (p15) Defined in [[business-rules-additives]].
- **CHEMON108** (Warning) -- For additives or flavourings, six generic `sampMatCode` terms cannot be reported. "It might become an error in 2027." (p15) Defined in [[business-rules-additives]].
- **CHEMON109** (Warning) -- For additives or flavourings, if the `sampMatCode` contains an implicit F33, the explicit F33 is not needed. "It might become an error in 2027." (p16) Defined in [[business-rules-additives]].
- **LL_01_FA_FF** (Warning) -- MPL comparison for food additives/flavourings. (p16) Defined in [[business-rules-legal-limits]].
- **LL_02_FA_FF** (Warning) -- MPL threshold evaluation for food additives/flavourings. (p16) Defined in [[business-rules-legal-limits]].
- **LL_03_FA_FF** (Warning) -- Substance authorisation check for food additives/flavourings. (p16) Defined in [[business-rules-legal-limits]].

## Deactivated rules

Inactivated in 2026 according to Table 1 (p12):

- **CHEMON47** -- Inactivated "due to the BR CHEMON40 which is more complete".
- **CHEMON49** -- Included in the updated description of CHEMON50.

Inactive in Table 10 but not listed as a 2026 change in Table 1:

- **CHEMON53** -- "Due to the update of table 2 in 2025, the specific rule is not active any longer." (p126)
- **CHEMON81** -- "Due to the update of CHEMON40, the BR CHEMON81 is obsolete." (p132)

## Other Table 1 changes

- New `progLegalRef` N422A and the addition of ST20A with K009A/K018A for pesticides (N027A) are described on [[chemmon-change-management]]. (p11)
