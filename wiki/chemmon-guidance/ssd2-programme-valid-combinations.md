---
title: "SSD2 Programme: Valid Table 2 Combinations"
select_when: "Which sampStrategy a progType allows for a progLegalRef (Table 2 grid, incl. baby food, contaminant codes, additives, N317A/N422A), and how VMPR, contaminant and pesticide plan flags are assigned."
type: "reference"
domain: "all"
last_updated: "2026-11-10"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 22-27 (Table 2 grid pp. 23-24, plan flags pp. 25-26, worked examples pp. 26-27)"
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

- Table 2 lists which `sampStrategy` values each `progType` allows for each `progLegalRef`, in the pesticide, VMPR, contaminant, food additive and food flavouring domains. The full grid is below.
- The constraints are implemented as business rules. **All other combinations are acceptable in the other domains.** (ChemMon 2026 p22)
- Plan flags also depend on `sampPoint` (border control posts, `E010A`), on processed/unprocessed status and, for pesticides, on whether the commodity is in the EU MACP list.
- An empty cell means Table 2 lists no sampling strategy for that `progType` under that legal reference.

## Table 2 grid

<!-- Source: ChemMon 2026 pp. 23-24, Table 2 -->

Table 2: combinations of `progLegalRef`, `progType` and `sampStrategy` for pesticide residues, VMPR, contaminants, food additives and food flavourings. The source prints programme columns across and `progType` rows down; here each source column is a row. Legal bases are as printed in the source. "—" means no combination listed. (ChemMon 2026 pp. 23-24)

| `progLegalRef` (legal basis) | Source column (`progType` description) | `K005A` Official (National) | `K009A` Official (EU) | `K018A` Official (National and EU) | `K019A` EU increased control on imported food | `K038A` Official (National) for Third Country Import |
| --- | --- | --- | --- | --- | --- | --- |
| `N027A` (Reg. 396/2005; Reg. (EU) 2024/989) | Pesticide residues: EU-coordinated programme | — | ST10A, ST20A | ST10A, ST20A | — | — |
| `N027A` (Reg. 396/2005; Reg. 2021/1355) | Pesticide residues: national programmes | ST10A, ST20A, ST30A | — | ST10A, ST20A | — | — |
| `N027A` (Reg. 396/2005; Reg. 2021/1355) | Pesticide residues: national programmes, control at borders (animal and non-animal origin) | — | — | — | — | ST10A, ST20A, ST30A |
| `N028A` / `N318A` (printed "Regulation 2016/125/EC", Reg. 2016/128 and Dir. 2006/125/EC) | Pesticide residues: baby food | ST10A, ST20A, ST30A | ST10A, ST20A | ST10A, ST20A | — | ST10A, ST20A, ST30A |
| `N371A` (Reg. 2022/1646 and 2022/1644) | VMPR Plan 1 | ST20A | — | ST20A | — | — |
| `N371A` (Reg. 2022/1646 and 2022/1644) | VMPR Plan 2 | ST10A | — | ST10A | — | — |
| `N371A` (Reg. 2022/1646 and 2022/1644) | VMPR Plan 3 | — | — | — | — | ST20A |
| `N371A` (Reg. 2022/1646 and 2022/1644) | VMPR Other control activities | ST30A, ST90A | — | ST30A, ST90A | — | ST30A, ST90A |
| `N129A`, `N379A`, `N323A`, etc. (Reg. 178/2002, 2023/915, (EU) 625/2017) | Contaminants | ST10A, ST20A, ST30A | ST10A, ST20A | ST10A, ST20A | — | ST10A, ST20A, ST30A |
| `N375A` (Reg. 2022/932 and 2022/931) | Contaminants: control plan for food placed on the Union market | ST10A, ST20A, ST30A | — | ST10A, ST20A | — | — |
| `N375A` (Reg. 2022/932 and 2022/931) | Contaminants: control plan for food of animal origin entering the Union | — | — | — | — | ST20A, ST30A |
| `N112A` (Reg. 1333/2008) | Food additives | ST10A, ST20A, ST30A | ST10A, ST20A | ST10A, ST20A | — | ST10A, ST20A, ST30A |
| `N113A` (Reg. 1334/2008) | Food flavourings | ST10A, ST20A, ST30A | ST10A, ST20A | ST10A, ST20A | — | ST10A, ST20A, ST30A |
| `N317A` (Reg. 2019/1793) | Increased control on imported food of non-animal origin | — | — | — | ST30A | — |
| `N422A` (Reg. 2019/1873) | Increased control on imported food of animal origin | — | — | — | ST30A | — |

Reading notes:

- `K019A` is listed only for `N317A` and `N422A`, and only with `ST30A`.
- `K009A` is never listed for VMPR, for `N375A`, or for the border, `N317A` and `N422A` columns.
- `ST90A` appears only in the VMPR Other column.

## How to read Table 2

The source uses Table 2 to map programme metadata to reporting plans and report eligibility; the flag definitions below say how EFSA assigns each plan. (ChemMon 2026 pp. 22, 25-26)

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
  - or `progType = K018A` with `sampStrategy = ST10A` and the commodity **not** one of the 12 listed in the EU MACP Regulation (EU) 2024/989, or with `sampStrategy = ST20A`
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
