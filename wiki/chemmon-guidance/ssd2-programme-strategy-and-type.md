---
title: "SSD2 Programme: Sampling Strategy and Programme Type"
type: "reference"
domain: "all"
last_updated: "2026-04-23"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 20-21 (Section 2, elements B.03-B.04)"
related:
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-elements-sampling]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Programme: Sampling Strategy and Programme Type

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 20-21 -->

## Rule Summary (Rule-First)

- `sampStrategy` and `progType` are both mandatory.
- Their meaning depends on domain context; the same code does not automatically imply the same reporting role across pesticides, VMPR, and contaminants.
- `ST30A` is the suspect-sampling route and is mandatory for some border-control regimes.
- `K019A` is reserved for the EU increased control programme on imported food; `K038A` is the national import-control path used in VMPR, pesticides, and contaminants where applicable.
- The final validity check is not done on either field in isolation. Use them together with `progLegalRef` and, when needed, `sampPoint`.

## sampStrategy — Sampling strategy

<!-- Source: ChemMon 2026 pp. 20-21 -->

**Element code:** B.03 · **Name:** `sampStrategy` · **Catalogue:** `SAMPSTR` · **Status:** mandatory

### Purpose

`sampStrategy` describes the sampling methodology applied. It is important because random, targeted, and suspect samples serve different purposes in compliance assessment and exposure estimation and must not be analysed as if they were equivalent. (ChemMon 2026 p20)

### Catalogue values

| Code | Label | Main use |
| --- | --- | --- |
| `ST10A` | Objective (random) sampling | Surveillance / random samples, including EU MACP and VMPR randomised surveillance |
| `ST20A` | Selective / targeted sampling | Risk-based controls for compliance or targeted monitoring |
| `ST30A` | Suspect sampling | Follow-up, suspicion, enhanced surveillance, some import-control regimes |
| `ST90A` | Other | VMPR samples outside the Regulation (EU) 2022/1646 control-plan structure |

(ChemMon 2026 pp. 20-21)

### Domain-specific highlights

- VMPR annual reporting uses `Objective`, `Target sampling`, and `Suspect sampling` for the formal plans; `Other` is for VMPR records outside those plans. (ChemMon 2026 p20)
- In pesticides, EU MACP samples use `ST10A` or `ST20A`. (ChemMon 2026 p20)
- For samples taken under Regulations (EU) 2019/1793 or 2019/1873, `ST30A` is the required suspect-sampling route. (ChemMon 2026 p20)

## progType — Programme type

<!-- Source: ChemMon 2026 p21 -->

**Element code:** B.04 · **Name:** `progType` · **Catalogue:** `PRGTYP` · **Status:** mandatory

### Purpose

`progType` distinguishes whether the sample belongs to an EU-level programme, a national programme, a combined EU/national programme, or an import-control pathway. (ChemMon 2026 p21)

### Catalogue values

| Code | Label | Main use |
| --- | --- | --- |
| `K009A` | Official (EU) programme | EU-coordinated programme, e.g. EU MACP |
| `K005A` | Official (National) programme | National programme |
| `K018A` | Official (National and EU) programme | Combined or dual-use programme |
| `K019A` | EU increased control programme on imported food | EU increased import control |
| `K038A` | Official (National) programme for Third Country Import | National import-control path |
| `K010A` | Occurrence data produced in total diet study | Total Diet Study reporting |

(ChemMon 2026 p21)

### Domain-specific highlights

- Pesticides: EU MACP samples use `K009A`; MANCP samples on the EU market use `K005A`; `K018A` is also valid in the mixed-use cases defined in Table 2. (ChemMon 2026 p21)
- Border samples use `K019A` only for the EU increased control programme on imported food; otherwise use `K038A` for national import-control pathways. (ChemMon 2026 p21)

## Related business rules

- `CHEMMON50`, `CHEMMON51` — valid pesticide combinations for `N027A`. See [[business-rules-cross-cutting]] and [[business-rules-pesticide]].
- `CHEMMON96`, `CHEMMON97` — valid strategy combinations for `K005A`. See [[business-rules-cross-cutting]].
- `CHEMMON101` — `N422A` requires `K019A` plus `ST30A`. See [[business-rules-pesticide]].
