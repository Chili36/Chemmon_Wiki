---
title: "SSD2 Elements: Matrix"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 32-36 (Section 2, E.02 sampMatCode and related matrix guidance)"
  - "p. 56 (Section 2, E.03-E.04, F.01, G.01-G.02)"
related:
  - "[[ssd2-data-model]]"
  - "[[ssd2-elements-sampling]]"
  - "[[ssd2-sampling-country]]"
  - "[[foodex2-in-chemmon]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[vmpr-reporting]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-cross-cutting]]"
  - "[[ssd2-matrix-sampled-matrix]]"
  - "[[ssd2-matrix-vmpr-coding]]"
  - "[[ssd2-matrix-origin]]"
  - "[[ssd2-matrix-analysed-sample]]"
---

# SSD2 Elements: Matrix

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 32-36, 56 -->

## Overview

The matrix group describes what was sampled and, if different, what was analysed. The main decisions are:

- how to encode the sampled matrix with FoodEx2 (`sampMatCode`)
- how to handle VMPR-specific matrix coding rules
- how to report country of origin (`origCountry`)
- when to override the default analysed-matrix inheritance (`sampAnId`, `anMatCode`, `anMatText`)

This page is intentionally short and acts as a hub plus a fast-path summary. Detailed element guidance is split into narrower pages so retrieval can pull the right slice instead of a single mixed matrix file.

## Rule Summary (Rule-First)

- `sampMatCode` must use the most detailed suitable FoodEx2 term from the MTX reporting hierarchy; if the item is not yet intended as food or feed, report it as food.
- A base term is always required. Add explicit facets only when they contribute information not already implicit in the selected FoodEx2 term.
- VMPR has additional matrix rules beyond ordinary FoodEx2 use: `F01` / `F02` expectations, wild-game `F21`, feed/water `F23`, non-food matrices, and special product categories.
- `sampMatText` supplements `sampMatCode`; it is not where brand names belong.
- `origCountry` is mandatory. Unspecific country codes are sometimes allowed, but not for non-compliant pesticide results, and import-control samples cannot have `origCountry = sampCountry`.
- `sampAnId`, `anMatCode`, and `anMatText` inherit from the sampled-matrix elements unless the analysed material is genuinely different from the sampled material.

## Relevant Business Rules

- `FOODEX2_SAMMAT`, `FOODEX2_ANMAT` — `sampMatCode` / `anMatCode` must be valid FoodEx2 codes. See [[business-rules-cross-cutting]].
- `CHEMMON27` — for VMPR and pesticides, `sampMatCode` should usually equal `anMatCode`. See [[business-rules-cross-cutting]].
- `CHEMMON76` — VMPR event-level species consistency. See [[business-rules-vmpr]].
- `CHEMMON95`, `CHEMMON99`, `GBR13` — origin-country restrictions. See [[business-rules-pesticide]], [[business-rules-cross-cutting]], and [[business-rules-gbr]].
- `CHEMMON108`, `CHEMMON109` — additives/flavourings matrix specificity and implicit `F33` duplication. See [[business-rules-additives]].

## Relevant Policy

- Keep general FoodEx2 syntax and implicit/explicit-facet logic in [[foodex2-in-chemmon]]. Use this matrix group only for SSD2 element behaviour and ChemMon-specific matrix coding constraints.
- For questions about downstream legislative grouping rather than code construction, jump from this page to [[chemmon-matrix-classification-algorithms]].

## Subpages

- [[ssd2-matrix-sampled-matrix]] — `sampMatCode`, `sampMatText`, FoodEx2 detail level, and the drinking-water case.
- [[ssd2-matrix-vmpr-coding]] — VMPR-specific matrix coding: processed derivatives, wild game, feed, water, non-food matrices, insects, and edible casings.
- [[ssd2-matrix-origin]] — `origCountry` rules, unspecific codes, and import/non-compliance constraints.
- [[ssd2-matrix-analysed-sample]] — `sampAnId`, `anMatCode`, and `anMatText` inheritance and override logic.
