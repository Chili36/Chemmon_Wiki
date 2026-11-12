---
title: "SSD2 Matrix: Country of Origin (origCountry)"
type: "reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 56-57 (Section 2, element E.04)"
  - "p. 31 (Table 3: unspecific country codes)"
  - "pp. 101, 137-138 (Tables 9-10: GBR13, CHEMON95, CHEMON99)"
related:
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-elements-sampling]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-gbr]]"
---

# SSD2 Matrix: Country of Origin (origCountry)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 31, 56-57 -->

## Rule Summary (Rule-First)

- `origCountry` is mandatory and must be reported in ISO 3166-1 alpha-2 format.
- Use the country where the product underwent its last substantial, economically justified processing if the supply chain spans multiple countries.
- Unspecific country codes may be used when the true origin is unknown, but not in all reporting situations.
- For non-compliant results (ChemMon 2026 p31, no domain named; validation checks this only for pesticides, `CHEMON95`, p137) and import-control cases (`CHEMON99`, p138), origin-country precision becomes stricter.

## origCountry — Country of origin on the sample taken

<!-- Source: ChemMon 2026 pp. 56-57 -->

**Element code:** E.04 · **Name:** `origCountry` · **Catalogue:** `COUNTRY` · **Status:** mandatory

### Purpose

`origCountry` captures the country of origin for the sampled product. EFSA explicitly encourages reporting countries to identify origin for all samples, especially unprocessed products and cases where non-compliance is found. (ChemMon 2026 p56)

### Multi-country supply chains

When more than one country is involved in production, origin is assigned to the country where the product underwent its last substantial, economically justified processing. A single country of origin must be reported, as described in the labelling requirements of Regulation (EU) No 1169/2011. Example: rice from Thailand packed in Iceland is `origCountry` = `TH`. (ChemMon 2026 p56-57)

### Unspecific country codes

When the exact country of origin is unknown but some information is available, the unspecific country codes of Table 3 (`AA`, `XC`, `XD`, `XE`, `XX`; the same as for `sampCountry`) can be used. In the case of non-compliant results, the Table 3 codes cannot be used. (ChemMon 2026 p31, p57)

Records with `origCountry` reported as an unspecific code (`XX`, `AA`, `EU`, `XC`, `XD`, `XE`) will be grouped as unknown (`XX`) for statutory reporting, e.g. the pesticides Annual Report. (ChemMon 2026 p57)

### Overseas territories (pesticide residues)

For pesticide residue annual reporting, samples taken in the overseas territories of EU countries must continue to be reported with their true `origCountry`; EFSA may reclassify them as domestic samples of the EU country for the Annual Report using the `moperRecodedCountry` attribute of the COUNTRY catalogue. (ChemMon 2026 p57)

### VMPR Plan 3

For VMPR Plan 3, the country of origin should not be equal to an EU country, including the country of the reporting organisation. Plan 3 results with an EU country as origin will be rejected from the report. (ChemMon 2026 p57)

## Related business rules

- `CHEMON95` — for pesticide records with `evalCode = J003A` (non-compliant), `origCountry` must not be `XX`, `AA`, `EU`, `XC`, `XD`, or `XE`. See [[business-rules-pesticide]].
- `CHEMON99` — for import/monitoring records at border-control context (`K038A` / `K019A` / `E010A`), `origCountry` cannot equal `sampCountry`. See [[business-rules-cross-cutting]].
- `GBR13` — `origArea` must be geographically within `origCountry`. See [[business-rules-gbr]].
