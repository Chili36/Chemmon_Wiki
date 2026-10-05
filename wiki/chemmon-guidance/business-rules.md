---
title: "ChemMon Business Rules"
type: "hub"
domain: "all"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
related:
  - "[[business-rules-gbr]]"
  - "[[business-rules-gbr-consistency]]"
  - "[[business-rules-gbr-results]]"
  - "[[business-rules-gbr-dates]]"
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
  - "[[fa-ff-no-presence-data-model]]"
  - "[[fa-ff-use-levels-data-model]]"
---

# ChemMon Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->

## Overview

- Business rules validate [[ssd2-data-model|SSD2]] submissions before acceptance into the EFSA data warehouse as part of the [[chemmon-overview|ChemMon]] data collection.
- Two severity levels: **Error** (blocks submission) and **Warning** (flags for review but does not block).
- Per the guidance, there are three groups of business rules: **GBR** (all DCF submissions), **CHEMMON** (ChemMon-wide rules), and **subset-specific rules** (e.g. pesticides, VMPR, additives/flavourings, or specific contaminants). (ChemMon 2026 p97)
- **Business rules take precedence** when they conflict with prose sections of the guidance.
- Matrix coding rules reference [[foodex2-in-chemmon]] for FoodEx2 usage.

This page is a **hub**: the canonical rule definitions live in the topic and domain references below. Use the rule's conditions and domain column to determine applicability; a page containing cross-domain rules does not mean every row applies to every submission.

<!-- Source: ChemMon 2026 pp. 97-143 (Tables 9-10) -->

The source guidance also provides troubleshooting tips alongside the GBR and CHEMMON rule lists (Tables 9 and 10). This wiki focuses on the rule definitions and how they relate to ChemMon reporting; troubleshooting text is not fully transcribed.

## Rule Index

### By tier

- **[[business-rules-gbr]]** — General Business Rules index and 16 core definitions: sample/event consistency, sampling/origin geography, result shape, units and uniqueness.
- **[[business-rules-gbr-consistency]]** — 12 GBR definitions: shared identifiers, processing geography, matrix/method text and sample-size units.
- **[[business-rules-gbr-results]]** — 20 GBR definitions: percentages, evaluation limits, decision thresholds, recovery and uncertainty, including Warning rules GBR22/42.
- **[[business-rules-gbr-dates]]** — 35 GBR definitions: calendar validity, day/month ranges, current date/year and chronological order.
- **[[business-rules-cross-cutting]]** — CHEMMON rules marked "All" or applying to multiple domains: analytical method, result value & type, sampling & programme, cross-domain matrix rules, evaluation & action, FoodEx2 validation.
- **[[business-rules-legal-limits]]** — Legal Limit rules comparing reported values to MRLs/MLs/MPLs across VMPR, pesticide, and food additive domains.

### By reporting domain

- **[[business-rules-vmpr]]** — VMPR-specific rules: accreditation, feed/water facets, species/breed consistency, VMPR evaluation codes, 2026 geographic consistency.
- **[[business-rules-pesticide]]** — Pesticide-specific rules: country of sampling, expression of results, copper facets, non-compliant origin, 2026 N422A exclusivity.
- **[[business-rules-contaminant]]** — Contaminant-specific rules: dioxin/PCB congeners, matrix facets (acrylamide, bisphenol, PAHs, arsenic, BFRs, mycotoxins), feed expression, 2026 programme restrictions.
- **[[business-rules-additives]]** — Food additives & flavourings rules: F33 legislative classes, expression type, physical state, 2026 substance-specific `paramText` and matrix restrictions.
- **[[business-rules-baby-food]]** — Baby food exclusion rules (CHEMMON55, CHEMMON63): matrix coding consistency for baby food programmes and VMPR legal framework exclusion. See [[baby-food-reporting]].

### Annual delta

- **[[business-rules-2026-changes]]** — Reference log of amended, merged, new, and deactivated rules for the 2026 data collection. Change notes only — canonical text lives in the slice files above.

## Parallel rule families (FA/FF data collections)

<!-- Source: No-presence 2026 Table 3; Use-levels 2026 Table 3 -->

The GBR/CHEMMON/LL catalogue above validates **SSD2** ChemMon submissions. FA/FF reporting also has two parallel data collections, each with its own rule namespace that does **not** overlap with the CHEMMON IDs:

- **`PRE01`–`PRE17`** — no-presence DM (17 rules; 16 Errors, 1 Warning). See [[fa-ff-no-presence-data-model]].
- **`USE01`–`USE27`** plus **`USE_LLDB01`/`USE_LLDB02`** — use-levels DM (29 rules, all Error). See [[fa-ff-use-levels-data-model]].

PRE and USE rules are not listed in the slice files because they validate different data models on different DCF submission paths. They are catalogued on the respective DM reference pages. See [[food-additives-reporting]] for the three-path overview.

## Coverage status

The source-derived inventory records **92 GBR, 104 CHEMON, 11 LL, 17 PRE and
29 USE IDs**, including inactive rows. Source CHEMON IDs are mapped to the
wiki's CHEMMON spelling. All **83 active, non-biological GBR definitions** have
been compared with the full Table 9 rows and are covered once across four pages;
the two inactive and seven biological-only GBR IDs remain in the source inventory.
All **100 active CHEMON rules**, the four inactive CHEMON rows, **17 PRE rules**,
**29 USE/USE_LLDB rules** and **49 PRE/USE fields** have now been compared with
the complete source rows and field sections. Canonical tables show source pages
and severity. A further contextual reading resolved the three content findings:
CHEMON grouping is explicit, USE19 requires at least one positive level under
the documented interpretation, and CONCLUS has a naming discrepancy for the
same concept family. Source notes and the supporting rationale remain visible.
This assistant source comparison does not certify an executable validator or
prove valid submissions.

See [[SOURCE_REVIEW]] and [[MAINTENANCE_WORKFLOW]] for findings, review scope
and the procedure for checking source drift. Independent human review is
unavailable; the review record distinguishes direct source statements from contextual interpretation.
