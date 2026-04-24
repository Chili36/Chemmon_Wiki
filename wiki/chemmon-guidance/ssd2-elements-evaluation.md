---
title: "SSD2 Elements: Evaluation, Action, Conclusion"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 73-76 (Section 2, elements N.01-N.06)"
related:
  - "[[ssd2-data-model]]"
  - "[[ssd2-elements-result]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-contaminant]]"
  - "[[business-rules-additives]]"
  - "[[ssd2-evaluation-limits]]"
  - "[[ssd2-evaluation-code]]"
  - "[[ssd2-evaluation-actions]]"
  - "[[ssd2-evaluation-conclusions]]"
---

# SSD2 Elements: Evaluation, Action, Conclusion

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 73-76 -->

## Overview

The evaluation group captures how the reported analytical result is judged against a legal limit or level of concern, what action followed from that judgement, and how special cases or follow-up conclusions are explained. These fields feed directly into EFSA reporting, especially the counting of compliant and non-compliant results.

This page is intentionally short and acts as a hub plus a fast-path summary. Detailed evaluation guidance is split into narrower pages so retrieval can pull the right slice instead of a single mixed file.

## Rule Summary (Rule-First)

- `evalCode` is mandatory and is the primary result judgement field.
- `evalLowLimit` / `evalLimitType` are usually only needed when the official EU limit is not already implied by EFSA's legal-limit logic or when a different limit must be declared.
- `actTakenCode` becomes important when non-compliance or detection triggers enforcement or follow-up.
- `evalInfo.conclusion` and `evalInfo.com` explain exceptions, follow-up investigations, additive/flavouring presence logic, and compliant outcomes despite elevated results.

## Relevant Business Rules

- `CHEMMON35`, `CHEMMON46`, `CHEMMON48`, `CHEMMON59` — limit-type / limit-value logic. See [[business-rules-cross-cutting]] and [[business-rules-pesticide]].
- `CHEMMON30`, `CHEMMON36`, `CHEMMON60`, `CHEMMON100` — allowed evaluation-code logic and interactions with result/method fields. See [[business-rules-cross-cutting]], [[business-rules-pesticide]], and [[business-rules-vmpr]].
- `CHEMMON37`, `CHEMMON85` — action-taken requirements. See [[business-rules-cross-cutting]].
- `CHEMMON26`, `CHEMMON66_a`, `CHEMMON66_b`, `CHEMMON87`, `CHEMMON88` — conclusion/comment recommendations and exception handling. See [[business-rules-cross-cutting]] and [[business-rules-additives]].

## Relevant Policy

- Keep numeric result reporting in [[ssd2-elements-result]] and use this page for the regulatory judgement layer that sits on top of those numbers.
- For additives/flavourings, the analytical-path use of `evalInfo.conclusion` is a distinct concept from the parallel-DM `presenceAdded` field; do not flatten those into one rule.

## Subpages

- [[ssd2-evaluation-limits]] — `evalLowLimit` and `evalLimitType`.
- [[ssd2-evaluation-code]] — `evalCode` meanings and allowed patterns.
- [[ssd2-evaluation-actions]] — `actTakenCode` and mandatory action cases.
- [[ssd2-evaluation-conclusions]] — `evalInfo.conclusion` and `evalInfo.com`.
