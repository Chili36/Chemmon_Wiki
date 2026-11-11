---
title: "SSD2 Elements: Sampling"
type: "reference"
domain: "all"
last_updated: "2026-11-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 27-32 (Section 2, sampling elements B.05-D.11)"
  - "p. 98 (Table 9, GBR2)"
related:
  - "[[ssd2-data-model]]"
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-sampling-method-and-point]]"
  - "[[ssd2-sampling-event-and-unit]]"
  - "[[ssd2-sample-identifiers]]"
  - "[[ssd2-sampling-country]]"
  - "[[ssd2-sampling-date]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Elements: Sampling

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 27-32 -->

## Overview

The sampling group identifies how the sample was selected, who took it, where in the chain it was taken, and the identifiers/date/country that connect analytical results back to the same physical sample. The original page had grown too broad, so it is now a short hub plus focused subpages.

## Rule Summary (Rule-First)

Use these as the fast path when debugging sampling-level records:

- If `sampMethod` indicates a pooled sample (`N002A` or `N031A`), then `sampUnitSize` and `sampUnitSizeUnit` become mandatory, and pooled samples must use `G005A` as the unit code. See [[ssd2-sampling-event-and-unit]]. (`CHEMON77`)
- `sampEventId` groups multiple samples from the same sampling unit/timepoint. If omitted, EFSA substitutes `sampId`. See [[ssd2-sampling-event-and-unit]].
- `sampId` is the stable identifier for the physical sample and must be reused across all results from that sample (ChemMon 2026 p30). `origSampId` is only for tracing back to an original sample in follow-up or feed-to-animal investigations. See [[ssd2-sample-identifiers]], which also covers the `GBR2` source discrepancy and `CHEMON22`.
- `sampCountry` is mandatory and uses ISO alpha-2 codes. For pesticides and VMPR it must equal the reporting organisation country. See [[ssd2-sampling-country]]. (`CHEMON58`)
- The Table 3 unspecific country codes "cannot be used" for non-compliant results (ChemMon 2026 p31); the paragraph opens on country of origin, the ban sentence itself names no element, and validation checks it only through `origCountry` (`CHEMON95`). See [[ssd2-sampling-country]].
- The full sampling date (`sampY`, `sampM`, `sampD`) is mandatory because legal-limit applicability and annual-report inclusion both depend on when the sample was taken. See [[ssd2-sampling-date]]. (`CHEMON43`, `CHEMON43_b`)

## Relevant Business Rules

The main constraints on this element group are:

- `GBR2` — sampling-event, local-organisation and sampling-programme descriptors (sections A, B, C) must be constant for records with the same `sampId` / `sampEventId`, except `progId` and `progLegalRef`, which Table 9 removed from the list. (ChemMon 2026 Table 9, p. 98)
- `CHEMON22` — `origSampId` follow-up samples should use suspect sampling.
- `CHEMON43` / `CHEMON43_b` — sampling-year reporting-window constraints.
- `CHEMON58` — pesticide and VMPR sampling-country consistency.
- `CHEMON77` — pooled-sample unit-size requirements.

See [[business-rules-gbr]], [[business-rules-cross-cutting]], [[business-rules-pesticide]], and [[business-rules-vmpr]].

## Subpages

- [[ssd2-sampling-method-and-point]] — `sampMethod`, `sampler`, `sampPoint`.
- [[ssd2-sampling-event-and-unit]] — `sampEventId`, `sampUnitType`, `sampUnitSize`, `sampUnitSizeUnit`.
- [[ssd2-sample-identifiers]] — `sampId`, `origSampId`.
- [[ssd2-sampling-country]] — `sampCountry` and the unspecific-country-code mapping.
- [[ssd2-sampling-date]] — `sampY`, `sampM`, `sampD` and reporting-window implications.
