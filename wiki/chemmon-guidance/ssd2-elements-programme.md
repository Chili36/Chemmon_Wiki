---
title: "SSD2 Elements: Programme"
type: "reference"
domain: "all"
last_updated: "2026-04-23"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 17-26 (Section 2, elements B.01-B.04)"
related:
  - "[[ssd2-data-model]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[reporting-flags]]"
  - "[[ssd2-elements-sampling]]"
  - "[[ssd2-elements-matrix]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-vmpr]]"
  - "[[chemmon-overview]]"
  - "[[ssd2-programme-identification]]"
  - "[[ssd2-programme-legal-reference]]"
  - "[[ssd2-programme-strategy-and-type]]"
  - "[[ssd2-programme-valid-combinations]]"
---

# SSD2 Elements: Programme

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 17-26 -->

## Overview

The programme group identifies which monitoring programme the sample belongs to, which legal framework it is reported under, which sampling strategy was used, and whether the sample counts as EU, national, or import-control programme activity. These elements drive domain routing, report inclusion, and the valid combinations enforced by the ChemMon business rules.

This page is intentionally short and acts as a hub plus a fast-path summary. Detailed guidance is split into narrowly-scoped subpages so retrieval can pull the right slice instead of a 240-line mixed page.

See [[ssd2-data-model]] for the logical-model overview, [[ssd2-elements-sampling]] for sample event and sampling-point elements, and [[ssd2-elements-matrix]] for matrix coding.

## Rule Summary (Rule-First)

Use these as the fast path when coding or debugging programme metadata:

- `progLegalRef` is the primary legal-routing element. It is mandatory, repeatable, and must match the domain of `paramCode`.
- `progType` and `sampStrategy` are not free-form choices; valid combinations are constrained by `progLegalRef` and, in some cases, by `sampPoint` and sample state.
- Border-control references are special cases: `N317A` and `N422A` have strict exclusivity/combination rules, and `N422A` requires `progType=K019A` plus `sampStrategy=ST30A`.
- VMPR plan flags are derived from the combination of `progType`, `sampStrategy`, and sometimes `sampPoint` or whether the sample is unprocessed.
- `progId` is useful for national traceability and validation drill-down, but it does not drive EFSA annual reporting and can be a stable default value if a country does not use programme IDs.

## Relevant Business Rules

The most load-bearing rules for this group are:

- `CHEMMON68` — `progLegalRef` domain must match `paramCode`. See [[business-rules-cross-cutting]].
- `CHEMMON50`, `CHEMMON51` — pesticides `progType` / `sampStrategy` constraints with `N027A`. See [[business-rules-cross-cutting]] and [[business-rules-pesticide]].
- `CHEMMON96`, `CHEMMON97` — valid strategy combinations for VMPR and other domains with `K005A`. See [[business-rules-cross-cutting]].
- `CHEMMON101` — `N422A` requires `progType=K019A` and `sampStrategy=ST30A`. See [[business-rules-pesticide]].
- `CHEMMON104`, `CHEMMON105` — exclusivity rules for `N422A` and `N317A`. See [[business-rules-pesticide]] and [[business-rules-contaminant]].

## Relevant Policy

- Treat Table 2 combination logic as binding operational guidance, not as optional narrative background. If the chosen `progLegalRef` / `progType` / `sampStrategy` combination does not fit the Table 2 pattern, it is almost certainly wrong.
- Prefer the most specific `LEGREF` term that matches the actual legal framework, because report inclusion and downstream flags depend on it. See [[controlled-terminology-catalogues]] and [[reporting-flags]].

## Subpages

- [[ssd2-programme-identification]] — `progId` purpose, defaulting, and naming examples.
- [[ssd2-programme-legal-reference]] — `progLegalRef`, domain routing, repeatability, and canonical LEGREF codes.
- [[ssd2-programme-strategy-and-type]] — `sampStrategy` and `progType` values plus domain-specific usage.
- [[ssd2-programme-valid-combinations]] — Table 2 combination logic, VMPR plans, contaminants, pesticides, and worked examples.
