---
title: "SSD2 Sampling: Sample Identifiers"
type: "reference"
domain: "all"
last_updated: "2026-04-23"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 30-32 (Section 2, elements D.01 and D.11)"
related:
  - "[[ssd2-elements-sampling]]"
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-sampling-event-and-unit]]"
  - "[[business-rules-gbr]]"
  - "[[business-rules-cross-cutting]]"
---

# SSD2 Sampling: Sample Identifiers

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 30-32 -->

## Rule Summary (Rule-First)

- `sampId` is mandatory, maximum 100 characters, and must be reused across all analytical results from the same physical sample.
- `sampId` is used to determine overall sample compliance and to count samples for programme/reporting purposes.
- `origSampId` is optional and only used to tie a sample back to an original sample in a follow-up or feed-to-animal investigation.
- If `origSampId` is reported, the guidance expects suspect sampling (`sampStrategy = ST30A`). (`CHEMMON22`)

## sampId — Sample taken identification code

<!-- Source: ChemMon 2026 pp. 30-31 -->

**Element code:** D.01 · **Name:** `sampId` · **Status:** mandatory (size ≤ 100)

### Purpose

Each sample must be identified by a unique sample identification reference not longer than 100 characters. Where multiple analytical results are reported for a sample, the same `sampId` must be used for all results.

### Role in compliance and reporting

- `sampId` is used to determine the overall status of the sample based on all reported results.
- `sampId` is used to enforce total sample counts against the requirements set in different regulations.

### Example

| Description | XML |
| --- | --- |
| Unique identifier for a sample from 2021 in Italy | `<sampId>IT_2021_AS000023456</sampId>` |

### Related business rules

See `GBR2` for sampling-event consistency and `CHEMMON01` for unique sample identification across collections.

## origSampId — Original sample identifier

<!-- Source: ChemMon 2026 p32 -->

**Element code:** D.11 · **Name:** `sampInfo.origSampId` · **Status:** optional

### Purpose

This element can indicate that subsequent sampling and testing is linked to an original non-compliant or contaminated sample, separating follow-up investigations from routine monitoring.

### Feed to animal chain tracking

To make explicit a connection between a feed sample and the corresponding food sample from the animal that consumed it, data providers must use `sampInfo.origSampId` to connect the two samples. This also applies to insects as food and the substrates they are fed when both are analysed for chemicals.

### Follow-up samples

An explicit connection is also relevant for follow-up samples originating from a positive control sample.

### Related business rule

`CHEMMON22` — If `origSampId` is reported, `sampStrategy` should be `ST30A` (suspect sampling).
