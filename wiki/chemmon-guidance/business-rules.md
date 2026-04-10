---
title: "ChemMon Business Rules"
type: "hub"
domain: "all"
last_updated: "2026-04-10"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[business-rules-gbr]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-contaminant]]"
  - "[[business-rules-additives]]"
  - "[[business-rules-baby-food]]"
  - "[[business-rules-legal-limits]]"
  - "[[business-rules-2026-changes]]"
  - "[[chemmon-overview]]"
  - "[[ssd2-data-model]]"
  - "[[foodex2-in-chemmon]]"
---

# ChemMon Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->

## Overview

- Business rules validate [[ssd2-data-model|SSD2]] submissions before acceptance into the EFSA data warehouse as part of the [[chemmon-overview|ChemMon]] data collection.
- Two severity levels: **Error** (blocks submission) and **Warning** (flags for review but does not block).
- Rules are organised into three tiers: General Business Rules (GBR), ChemMon-specific rules (CHEMMON), and Legal Limit rules (LL).
- **Business rules take precedence** when they conflict with prose sections of the guidance.
- Matrix coding rules reference [[foodex2-in-chemmon]] for FoodEx2 usage.

This page is a **hub**: the canonical rule definitions live in the nine slice files below, grouped by applicability so the selector can inject just what a query actually needs. When in doubt, start with [[business-rules-cross-cutting]] — it applies to every domain.

## Rule Index

### By tier

- **[[business-rules-gbr]]** — General Business Rules (16 rules) that apply across all EFSA SSD2 data collections: sampling event consistency, geographic validation, result value/unit rules.
- **[[business-rules-cross-cutting]]** — CHEMMON rules (46 rules) marked "All" or applying to multiple domains: analytical method, result value & type, sampling & programme, cross-domain matrix rules, evaluation & action, FoodEx2 validation.
- **[[business-rules-legal-limits]]** — Legal Limit rules (11 rules) comparing reported values to MRLs/MLs/MPLs across VMPR, pesticide, and food additive domains.

### By reporting domain

- **[[business-rules-vmpr]]** — VMPR-specific rules (11 CHEMMON rules): accreditation, feed/water facets, species/breed consistency, VMPR evaluation codes, 2026 geographic consistency.
- **[[business-rules-pesticide]]** — Pesticide-specific rules (14 CHEMMON rules): country of sampling, expression of results, copper facets, non-compliant origin, 2026 N422A exclusivity.
- **[[business-rules-contaminant]]** — Contaminant-specific rules (19 CHEMMON rules): dioxin/PCB congeners, matrix facets (acrylamide, bisphenol, PAHs, arsenic, BFRs, mycotoxins), feed expression, 2026 programme restrictions.
- **[[business-rules-additives]]** — Food additives & flavourings rules (12 CHEMMON rules): F33 legislative classes, expression type, physical state, 2026 substance-specific `paramText` and matrix restrictions.
- **[[business-rules-baby-food]]** — Baby food exclusion rules (CHEMMON55, CHEMMON63): matrix coding consistency for baby food programmes and VMPR legal framework exclusion. See [[baby-food-reporting]].

### Annual delta

- **[[business-rules-2026-changes]]** — Reference log of amended, merged, new, and deactivated rules for the 2026 data collection. Change notes only — canonical text lives in the slice files above.

## Totals

131 rule definitions across the nine slices: 16 GBR + 104 CHEMMON + 11 LL. Every `CHEMMON\d+` rule ID appears exactly once in the slice files (see `tools/health_check.py` for verification).
