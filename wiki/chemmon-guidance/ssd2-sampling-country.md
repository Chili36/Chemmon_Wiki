---
title: "SSD2 Sampling: Country of Sampling"
type: "reference"
domain: "all"
last_updated: "2026-11-10"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 31 (Section 2, element D.03; Table 3)"
  - "p. 127 (Table 10, CHEMON58)"
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
- For pesticides **and VMPR**, `sampCountry` must match the reporting organisation country. (`CHEMON58`; Table 10 p. 127)
- EFSA defines a small set of unspecific country codes (`AA`, `XC`, `XD`, `XE`, `XX`) for recoding in annual reports, but these cannot be used for non-compliant results.
- For bulk samples where origin is unavailable, EFSA recommends also reporting the processing country.

## sampCountry — Country of sampling

<!-- Source: ChemMon 2026 p31 -->

**Element code:** D.03 · **Name:** `sampCountry` · **Catalogue:** COUNTRY · **Status:** mandatory

### Purpose

`sampCountry` is reported using ISO 3166-1 alpha-2 codes for the country where the sample was taken. It is needed to connect results correctly to the sampling country when analysis happens elsewhere.

### Pesticide and VMPR constraint (CHEMON58)

`sampCountry` must equal the country of the reporting organisation when the result is reported for pesticides (`is_pest=1`) **or for VMPR** (`is_vet=1`); otherwise CHEMON58 raises an Error. (ChemMon 2026 Table 10, p. 127)

The D.03 text on p. 31 names only pesticide residues, but the rule DCF runs is wider, so VMPR records with a different sampling country are also rejected. The guidance does not reconcile the two texts; the rule shows what validation enforces. See [[business-rules-cross-cutting]].

For pesticides, the Annual Report will include records with `sampCountry` set to an EU country, Norway, or Iceland. Samples taken in overseas territories of EU countries must be reported as the corresponding EU country.

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
