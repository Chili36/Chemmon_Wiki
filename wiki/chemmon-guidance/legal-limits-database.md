---
title: "Legal Limits Database (MRLs and Other Limits)"
type: "reference"
domain: "all"
last_updated: "2026-04-22"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
source_pages:
  - "ChemMon 2026 p. 148 (Section 8); Use-levels 2026 p. 18 (Section 4)"
related:
  - "[[business-rules-legal-limits]]"
  - "[[ssd2-elements-result]]"
  - "[[chemmon-reports]]"
  - "[[fa-ff-use-levels-data-model]]"
  - "[[food-additives-reporting]]"
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
  - Directive (EC) No 141/2006 (veterinary residues). (ChemMon 2026 p148)
- If an MRL changes during the data-collection reference period, the database contains both limits with dates of applicability; EFSA determines which applies based on the **sampling date**.
- The applied legal limit only covers **raw, unprocessed** samples (per guidance text).

## Availability and authority

<!-- Source: ChemMon 2026 p148 -->

- An extraction is visible/downloadable through EFSA MicroStrategy and can support data providers.
- The database includes legal-limit history across years.
- Data providers must still rely on the legislation as the official source of legal limits. (ChemMon 2026 p148)

## Relationship to legal-limit business rules

See [[business-rules-legal-limits]] for the validation rules that compare reported results against legal limits as part of the ChemMon validation layer.

## FA/FF Maximum Permitted Levels — checked at the marketing date

<!-- Source: Use-levels 2026 p18 (Section 4); Use-levels 2026 pp. 24-28 (Table 3) -->

For the FA/FF **use-levels** data collection ([[fa-ff-use-levels-data-model]]), the LLDB also holds Maximum Permitted Levels (MPLs) established in:

- Regulation (EC) No 1333/2008 (food additives)
- Regulation (EC) No 1334/2008 (food flavourings)

The FA/FF check differs from the SSD2 analytical check above in **which date drives the lookup**:

- **SSD2 analytical submissions** → the legal limit that applies at the **sampling date** (`sampY/M/D`) is used. (ChemMon 2026 p148)
- **FA/FF use-levels submissions** → the MPL that applies at the **marketing date** (`marketYear/Month/Day`) is used. (Use-levels 2026 p18)

Two LLDB-backed rules enforce this in the use-levels DM:

- `USE_LLDB01` — the reported `paramCode` must be authorised for the reported legislative category × restriction combination per Reg. 1333/2008 / 1334/2008 at the marketing date.
- `USE_LLDB02` — the reported `maxLevel` must be `≤` the MPL from LLDB valid at the marketing date.

Both are **Error** severity. The in-record consistency check (`maxLevel ≤ maxPermittedLevel` as reported by the DP) is a separate rule (`USE27`); USE_LLDB02 is the authoritative cross-check against EFSA's centrally maintained MPL records.

