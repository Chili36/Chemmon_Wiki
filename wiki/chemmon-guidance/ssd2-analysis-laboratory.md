---
title: "SSD2 Analysis: Laboratory Identification and Accreditation"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 58-59 (Section 2, elements J.01-J.03)"
related:
  - "[[ssd2-elements-analysis]]"
  - "[[ssd2-analysis-methods]]"
  - "[[ssd2-result-method-accreditation]]"
---

# SSD2 Analysis: Laboratory Identification and Accreditation

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 58-59 -->

## Rule Summary (Rule-First)

- `labId`, `labAccred`, and `labCountry` are all mandatory.
- `labId` is the national identifier for the laboratory and must stay stable enough to support validation and reporting.
- `labCountry` is the ISO country code for the laboratory and must be unique per `labId`.
- `labAccred` expresses the accreditation status of the laboratory; for pesticides the allowed value set is especially narrow.

## labId — Laboratory identification

<!-- Source: ChemMon 2026 pp. 58-59 -->

**Element code:** J.01 · **Name:** `labId` · **Status:** mandatory

### Purpose

`labId` is the unique code used to identify the laboratory providing the analytical result. The reporting country is responsible for maintaining the mapping between the code and the actual laboratory name and for updating it when required by EFSA, the Commission, or the EURLs. (ChemMon 2026 pp. 58-59)

## labAccred — Laboratory accreditation

<!-- Source: ChemMon 2026 p59 -->

**Element code:** J.02 · **Name:** `labAccred` · **Catalogue:** `LABACC` · **Status:** mandatory

### Purpose

`labAccred` indicates whether the laboratory performing the analysis has the accreditation status required under Regulation (EU) 2017/625. (ChemMon 2026 p59)

### Pesticide-specific values

For pesticide monitoring, only these two `LABACC` values are valid:

| Code | Meaning |
| --- | --- |
| `L001A` | Accredited according to ISO/IEC 17025 |
| `L003A` | Not yet accredited according to ISO/IEC 17025 |

(ChemMon 2026 p59)

## labCountry — Laboratory country

<!-- Source: ChemMon 2026 p59 -->

**Element code:** J.03 · **Name:** `labCountry` · **Catalogue:** `COUNTRY` · **Status:** mandatory

### Purpose

Report the country where the laboratory is located using ISO 3166-1 alpha-2 codes. Each `labId` should map to a unique `labCountry`. (ChemMon 2026 p59)
