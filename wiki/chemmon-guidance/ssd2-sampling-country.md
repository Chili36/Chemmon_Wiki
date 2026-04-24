---
title: "SSD2 Sampling: Country of Sampling"
type: "reference"
domain: "all"
last_updated: "2026-04-23"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 31 (Section 2, element D.03)"
related:
  - "[[ssd2-elements-sampling]]"
  - "[[ssd2-elements-matrix]]"
  - "[[pesticide-reporting]]"
  - "[[business-rules-cross-cutting]]"
---

# SSD2 Sampling: Country of Sampling

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p31 -->

## Rule Summary (Rule-First)

- `sampCountry` is mandatory and uses ISO 3166-1 alpha-2 codes.
- For pesticides, `sampCountry` must match the reporting organisation country. (`CHEMMON58`)
- EFSA defines a small set of unspecific country codes (`AA`, `XC`, `XD`, `XE`, `XX`) for recoding in annual reports, but these cannot be used for non-compliant results.
- For bulk samples where origin is unavailable, EFSA recommends also reporting the processing country.

## sampCountry — Country of sampling

<!-- Source: ChemMon 2026 p31 -->

**Element code:** D.03 · **Name:** `sampCountry` · **Catalogue:** COUNTRY · **Status:** mandatory

### Purpose

`sampCountry` is reported using ISO 3166-1 alpha-2 codes for the country where the sample was taken. It is needed to connect results correctly to the sampling country when analysis happens elsewhere.

### Pesticide residues constraint

For pesticide residues, `sampCountry` and the reporting organisation country must be the same. The pesticides Annual Report will include records with `sampCountry` set to an EU country, Norway, or Iceland. Samples taken in overseas territories of EU countries must be reported as the corresponding EU country.

### Reportable unspecific country codes

EFSA provides the following recoding table for cases where the real country cannot be reported. In the case of non-compliant results, these codes cannot be used.

| Code description | Code | `sampCountry` (Annual Reports) | `origCountry` (Annual Reports) |
| --- | --- | --- | --- |
| EEA (European Economic Area) | `AA` | Excluded | Unknown (`XX`) |
| Non-EEA | `XC` | Excluded | Unknown (`XX`) |
| Non-domestic, import | `XD` | Excluded | Unknown (`XX`) |
| Non-European Union | `XE` | Excluded | Unknown (`XX`) |
| Unknown | `XX` | Excluded | Unknown (`XX`) |

### Recommendation for bulk samples

EFSA recommends reporting the country of processing when bulk samples are reported and the country of origin is not available.

### Examples

| Description | XML |
| --- | --- |
| Sample taken in Greece | `<sampCountry>GR</sampCountry>` |
| Sample taken in Northern Ireland (per Windsor Framework) | `<sampCountry>XI</sampCountry>` |
