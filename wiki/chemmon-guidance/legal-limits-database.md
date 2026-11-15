---
title: "Legal Limits Database (MRLs and Other Limits)"
type: "reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
source_pages:
  - "ChemMon 2026 p. 148 (Section 8); ChemMon 2026 pp. 142-143 (Table 10, LL_01_FA_FF to LL_03_FA_FF, LL_04); Use-levels 2026 p. 18 (Section 4); Use-levels 2026 p. 28 (Table 3)"
related:
  - "[[business-rules-legal-limits]]"
  - "[[ssd2-elements-result]]"
  - "[[ssd2-evaluation-limits]]"
  - "[[chemmon-reports]]"
  - "[[fa-ff-use-levels-data-model]]"
  - "[[food-additives-reporting]]"
  - "[[pesticide-residue-definition-by-matrix]]"
---

# Legal Limits Database (MRLs and Other Limits)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Section 8 -->

## Overview

EFSA maintains a harmonised **Legal Limits Database** to support evaluation of numeric analytical results against applicable legal limits (e.g. MRLs) at result level. (ChemMon 2026 p148)

The guidance describes it as a resource intended to help data providers check exceedances and compliance evaluation, alongside the sectoral legislation. (ChemMon 2026 p148)

## What it covers (per guidance)

<!-- Source: ChemMon 2026 p148 -->

- Contains maximum residue limits (MRLs) from:
  - Regulation (EC) No 396/2005 (pesticides),
  - Regulation (EC) No 37/2010 (veterinary residues),
  - Directive (EC) No 141/2006 (the guidance lists it with the other two and does not say which residues it covers). (ChemMon 2026 p148)
- If an MRL changes during the data-collection reference period, the database contains both limits with dates of applicability; EFSA determines which applies based on the **sampling date**. (ChemMon 2026 p148)
- There is a small number of substances for which legal limits are not harmonised across the legislation that applies to chemical monitoring. (ChemMon 2026 p148)
- In the **ChemMon 2026 SSD2 analytical path**, the applied legal limit note is scoped to **raw, unprocessed** samples. The FA/FF use-levels path documented below is a separate LLDB use case with marketing-date applicability. (ChemMon 2026 p148; Use-levels 2026 p18)

## Availability and authority

<!-- Source: ChemMon 2026 p148 -->

- An extraction is visible/downloadable through EFSA MicroStrategy and can support data providers.
- The database includes legal-limit history across years.
- Data providers must still rely on the legislation as the official source of legal limits. (ChemMon 2026 p148)

## Relationship to legal-limit business rules

For pesticide results (`is_pest=1`) whose `paramCode` is part of the legal limits database, LL_04/LL_04_b (Error) uses the database's plausible matrix/`paramCode` combinations to check that the reported code matches the residue definition for the sampled matrix, "unless the result is reported for a part of sum"; see [[pesticide-residue-definition-by-matrix]]. (ChemMon 2026 p143)

See [[business-rules-legal-limits]] for the validation rules that compare reported results against legal limits as part of the ChemMon validation layer. For the SSD2 fields that explicitly carry a declared limit and limit type, see [[ssd2-evaluation-limits]].

## FA/FF Maximum Permitted Levels — checked at the marketing date

<!-- Source: Use-levels 2026 p18 (Section 4); Use-levels 2026 p28 (Table 3); ChemMon 2026 pp. 142-143 (Table 10) -->

For the FA/FF **use-levels** data collection ([[fa-ff-use-levels-data-model]]), the LLDB also holds Maximum Permitted Levels (MPLs) established in:

- Regulation (EC) No 1333/2008 (food additives)
- Regulation (EC) No 1334/2008 (food flavourings)

The FA/FF check differs from the SSD2 analytical check above in **which date drives the lookup**:

- **SSD2 analytical submissions** → the legal limit that applies at the **sampling date** (`sampY/M/D`) is used. (ChemMon 2026 p148)
- **FA/FF use-levels submissions** → the MPL that applies at the **marketing date** (`marketYear/Month/Day`) is used. (Use-levels 2026 p18)

Two LLDB-backed rules enforce this in the use-levels DM:

- `USE_LLDB01` — the reported `paramCode` must be authorised for the reported legislative category × restriction combination per Reg. 1333/2008 / 1334/2008 at the marketing date.
- `USE_LLDB02` — the reported `maxLevel` must be `≤` the MPL from LLDB valid at the marketing date.

Both are **Error** severity. The in-record consistency check (`maxLevel ≤ maxPermittedLevel` as reported by the DP) is a separate rule (`USE27`, Error); `USE_LLDB02` is the check against the MPL held in the LLDB. (Use-levels 2026 p28)

The SSD2 analytical path has its own FA/FF MPL rules, all Warnings: `LL_01_FA_FF` and `LL_02_FA_FF` check that `evalCode` is consistent with `resVal` against the MPL, and `LL_03_FA_FF` checks that the substance is authorised in the legislative category with the restriction/exception. `LL_03_FA_FF` and `USE_LLDB01` have the same rule description but different severity (Warning against Error). (ChemMon 2026 Table 10 pp. 142-143; Use-levels 2026 p28) See [[business-rules-legal-limits]].
