---
title: "SSD2 Elements: Analysis, Laboratory, Parameter, Method"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 57-64 (Section 2, elements E.06-L.04)"
related:
  - "[[ssd2-data-model]]"
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-elements-result]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-vmpr]]"
  - "[[ssd2-analysis-context]]"
  - "[[ssd2-analysis-laboratory]]"
  - "[[ssd2-analysis-parameter-coding]]"
  - "[[ssd2-analysis-methods]]"
---

# SSD2 Elements: Analysis, Laboratory, Parameter, Method

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 57-64 -->

## Overview

The analysis group describes where the analysis happened, which analyte or residue definition was reported, and how the method was identified and classified. These elements connect the sampled matrix to the analytical workflow and determine how EFSA routes the result through domain hierarchies, legal-limit checks, and downstream reporting.

This page is intentionally short and acts as a hub plus a fast-path summary. Detailed guidance is split into narrower pages so retrieval can pull the right slice instead of a 280-line mixed file.

## Rule Summary (Rule-First)

- `analysisY` is mandatory for every result.
- `origFishAreaCode` matters only for the fish/seafood cases where origin at FAO-area level is analytically or legally relevant.
- `anPortSeq` is a narrow exception for repeated analysis of the same sample under repeatable conditions; do not use it for ordinary legal-limit evaluation.
- `labId`, `labAccred`, and `labCountry` identify the analysing laboratory and its accreditation context.
- `paramCode` is the domain-routing analyte code; `paramType` matters most for multicomponent or summed parameters.
- `anMethRefId` ties records back to the same laboratory method; `anMethType` distinguishes screening from confirmation; `anMethCode` should be specific rather than generic.

## Relevant Business Rules

- `CHEMMON20` — fish matrices with BFRs/dioxins/mercury should report `origFishAreaCode`. See [[business-rules-contaminant]].
- `CHEMMON68` — `progLegalRef` domain must match `paramCode` domain. See [[business-rules-cross-cutting]].
- `CHEMMON23`, `CHEMMON30`, `CHEMMON33`, `CHEMMON34` — analytical-method type rules. See [[business-rules-cross-cutting]].
- `CHEMMON79_a/b/c` — contaminants/additives/flavourings cannot use generic fallback analytical-method codes. See [[business-rules-cross-cutting]].
- `CHEMMON92` — VMPR `paramCode` base term must be in `vetDrugRes`. See [[business-rules-vmpr]].

## Relevant Policy

- Keep matrix construction in [[ssd2-elements-matrix]] and result-shape logic in [[ssd2-elements-result]]. This page is about the analysis-side metadata and parameter/method decisions.
- For questions about domain flagging or parameter hierarchy routing, jump from here to [[reporting-flags]] once the parameter code itself is clear.

## Subpages

- [[ssd2-analysis-context]] — `origFishAreaCode`, `analysisY`, and `anPortSeq`.
- [[ssd2-analysis-laboratory]] — `labId`, `labAccred`, and `labCountry`.
- [[ssd2-analysis-parameter-coding]] — `paramType`, `paramCode`, and `paramText`.
- [[ssd2-analysis-methods]] — `anMethRefId`, `anMethType`, and `anMethCode`.
