---
title: "SSD2 Programme: Valid Table 2 Combinations"
type: "reference"
domain: "all"
last_updated: "2026-04-23"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 23-27 (Table 2 and worked examples)"
related:
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-elements-sampling]]"
  - "[[ssd2-elements-matrix]]"
  - "[[reporting-flags]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Programme: Valid Table 2 Combinations

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 23-27 -->

## Rule Summary (Rule-First)

- Table 2 defines the valid combinations of `progLegalRef`, `progType`, and `sampStrategy` across the reporting domains.
- Some combinations also depend on `sampPoint` (especially border control) or whether the sample is processed/unprocessed.
- The ChemMon business rules implement these combinations as accept/reject logic; treat any combination outside the listed patterns as invalid unless a rule explicitly allows it.

## How to read Table 2

The source guidance uses Table 2 to map programme metadata to reporting plans and downstream report eligibility. The business rules enforce the same logic, so this page is the durable interpretation layer for the combinations rather than a free-standing alternative to the rules. (ChemMon 2026 p22)

## VMPR plan flags

<!-- Source: ChemMon 2026 p25 -->

- **Plan 1** — national risk-based control plan for production in Member States:
  - `progType in {K005A, K018A}`
  - `sampStrategy = ST20A`
  - sample treated as unprocessed
- **Plan 2** — national randomised surveillance plan for production in Member States:
  - `progType in {K005A, K018A}`
  - `sampStrategy = ST10A`
  - sample treated as unprocessed
- **Plan 3** — national risk-based control plan for third-country imports:
  - `progType = K038A`
  - `sampStrategy = ST20A`
  - `sampPoint = E010A` (Border Control Posts)
- **Other** — suspect samples, `ST90A`, processed-product variants that do not count toward Plans 1/2, and any combination outside the formal plan logic.

## Contaminant control-plan flags

<!-- Source: ChemMon 2026 p25 -->

- **Food placed on the Union market**:
  - `progType in {K018A, K005A}`
  - `sampStrategy = ST20A`
- **Third-country imports**:
  - `progType = K038A`
  - `sampStrategy = ST20A`
  - `sampPoint = E010A`

## Pesticide control-plan flags

<!-- Source: ChemMon 2026 pp. 25-26 -->

- **EU MACP**:
  - `progType in {K009A, K018A}`
  - `sampStrategy in {ST10A, ST20A}`
  - sample is an EU MACP commodity (or relevant baby-food Annex II case)
- **MANCP**:
  - `progType = K005A` with `sampStrategy in {ST10A, ST20A, ST30A}`
  - or `progType = K018A` with the Table 2 cases for non-EU-MACP or targeted use
  - or `progType = K038A` with `sampStrategy in {ST10A, ST20A, ST30A}`
- **EU increased control programme on imported food**:
  - `progType = K019A`
  - `sampStrategy = ST30A`
  - `sampPoint = E010A`
  - matrix/origin covered by Regulation (EU) 2019/1793 annexes

## Worked examples

| Scenario | Combination |
| --- | --- |
| EU MACP pesticide sample on the Union market | `progLegalRef=N027A`, `progType=K009A`, `sampStrategy=ST10A` |
| VMPR Plan 1 sample | `progLegalRef=N371A`, `progType=K018A`, `sampStrategy=ST20A` |
| One sample used for both VMPR Plan 2 and pesticide MANCP | `progLegalRef=N027A$N371A`, `progType=K018A`, `sampStrategy=ST10A` |
| Contaminants control-plan sample on the Union market | `progLegalRef=N375A`, `progType=K018A`, `sampStrategy=ST20A` |
| Contaminants import-control sample | `progLegalRef=N375A`, `progType=K038A`, `sampStrategy=ST20A`, `sampPoint=E010A` |
| Third-country import sample relevant to VMPR, pesticides, and contaminants | `progLegalRef=N371A$N027A$N375A`, `progType=K038A`, `sampStrategy=ST20A`, `sampPoint=E010A` |

(ChemMon 2026 pp. 26-27)
