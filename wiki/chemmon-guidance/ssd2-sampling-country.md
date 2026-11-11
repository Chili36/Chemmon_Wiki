---
title: "SSD2 Sampling: Country of Sampling"
type: "reference"
domain: "all"
last_updated: "2026-11-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 31 (Section 2, element D.03; Table 3)"
  - "p. 127 (Table 10, CHEMON58)"
  - "p. 137 (Table 10, CHEMON95)"
related:
  - "[[ssd2-elements-sampling]]"
  - "[[business-rules-pesticide]]"
  - "[[ssd2-elements-matrix]]"
  - "[[pesticide-reporting]]"
  - "[[business-rules-cross-cutting]]"
---

# SSD2 Sampling: Country of Sampling

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p31 -->

## Rule Summary (Rule-First)

- `sampCountry` is mandatory and uses ISO 3166-1 alpha-2 codes.
- For pesticides **and VMPR**, `sampCountry` must match the reporting organisation country. (`CHEMON58`; Table 10 p. 127)
- EFSA defines a small set of unspecific country codes (`AA`, `XC`, `XD`, `XE`, `XX`) and shows how they are recoded for pesticide residues Annual Reports; the guidance text says these cannot be used for non-compliant results (ChemMon 2026 p31). That text is about country of origin; see the discrepancy note below.
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

The paragraph that introduces Table 3 sits under D.03 but is about **country of origin**: "Country of origin cannot be unknown due to EU legislation where traceability of goods placed on the market is a must." EFSA stresses the importance of collecting and submitting this information; if a data provider cannot, Table 3 "will be used to recode unspecific country codes". "In the case of non-compliant results, codes listed in Table 3 cannot be used." (ChemMon 2026 p31)

Table 3 is titled "Reportable unspecific country codes for sampCountry and origCountry"; its two right-hand columns are headed "Use for pesticide residues reporting (Annual Reports)". (ChemMon 2026 p31)

| Code description | Code | `sampCountry` (pesticide residues Annual Reports) | `origCountry` (pesticide residues Annual Reports) |
| --- | --- | --- | --- |
| EEA (European Economic Area) | `AA` | Excluded | Unknown (`XX`) |
| Non-EEA | `XC` | Excluded | Unknown (`XX`) |
| Non-domestic, import | `XD` | Excluded | Unknown (`XX`) |
| Non-European Union | `XE` | Excluded | Unknown (`XX`) |
| Unknown | `XX` | Excluded | Unknown (`XX`) |

Source discrepancy: the p. 31 text bans the Table 3 codes for non-compliant results without naming a domain or an element. The only business rule on this is CHEMON95: if the result is reported for pesticides (`is_pest=1`) and `evalCode` is "greater than maximum permissible quantities" (`J003A`), then a country of origin different from `XX`, `AA`, `EU`, `XC`, `XD`, `XE` must be reported; it is a Warning ("It will remain a Warning in 2026") and its list also includes `EU`, which is not in Table 3 (ChemMon 2026 Table 10, p. 137). So validation checks `origCountry` for pesticides only, as a Warning; no rule applies the ban to `sampCountry`. See [[business-rules-pesticide]].

### Recommendation for bulk samples

EFSA recommends that the country of processing of the sample taken (E.08) is provided when bulk samples are reported and the country of origin is not available. (ChemMon 2026 p31)

### Examples

| Description | XML |
| --- | --- |
| Sample taken in Greece | `<sampCountry>GR</sampCountry>` |
| Sample taken in Northern Ireland (per Windsor Framework) | `<sampCountry>XI</sampCountry>` |
