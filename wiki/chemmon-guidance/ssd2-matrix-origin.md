---
title: "SSD2 Matrix: Country of Origin (origCountry)"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 56 (Section 2, element E.04)"
related:
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-elements-sampling]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-gbr]]"
---

# SSD2 Matrix: Country of Origin (origCountry)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p56 -->

## Rule Summary (Rule-First)

- `origCountry` is mandatory and must be reported in ISO 3166-1 alpha-2 format.
- Use the country where the product underwent its last substantial, economically justified processing if the supply chain spans multiple countries.
- Unspecific country codes may be used when the true origin is unknown, but not in all reporting situations.
- For pesticide non-compliance and import-control cases, origin-country precision becomes stricter.

## origCountry — Country of origin on the sample taken

<!-- Source: ChemMon 2026 p56 -->

**Element code:** E.04 · **Name:** `origCountry` · **Catalogue:** `COUNTRY` · **Status:** mandatory

### Purpose

`origCountry` captures the country of origin for the sampled product. EFSA explicitly encourages reporting countries to identify origin for all samples, especially unprocessed products and cases where non-compliance is found. (ChemMon 2026 p56)

### Multi-country supply chains

When more than one country is involved in production, origin is assigned to the country where the product underwent its last substantial, economically justified processing. (ChemMon 2026 p56)

### Unspecific country codes

The guidance allows unspecific codes such as `AA`, `XC`, `XD`, `XE`, and `XX` when the true origin is unknown. However, these are not acceptable in every case; see the business rules below for the most important exceptions. (ChemMon 2026 p56)

## Related business rules

- `CHEMMON95` — for pesticide records with `evalCode = J003A` (non-compliant), `origCountry` must not be `XX`, `AA`, `EU`, `XC`, `XD`, or `XE`. See [[business-rules-pesticide]].
- `CHEMMON99` — for import programmes (`K038A` / `K019A` with border-control context), `origCountry` cannot equal `sampCountry`. See [[business-rules-cross-cutting]].
- `GBR13` — `origArea` must be geographically within `origCountry`. See [[business-rules-gbr]].
