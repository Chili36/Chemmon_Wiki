---
title: "SSD2 Programme: Legal Reference (progLegalRef)"
type: "reference"
domain: "all"
last_updated: "2026-04-23"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 18-19 (Section 2, element B.02)"
related:
  - "[[ssd2-elements-programme]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[reporting-flags]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-vmpr]]"
  - "[[food-additives-reporting]]"
---

# SSD2 Programme: Legal Reference (progLegalRef)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 18-19 -->

## Rule Summary (Rule-First)

- `progLegalRef` is mandatory and may repeat when one record legitimately belongs to more than one reporting domain.
- Choose the most specific `LEGREF` code that matches the legal framework, because report inclusion and domain flags depend on it.
- `progLegalRef` must align with the domain of `paramCode`; mixed-domain combinations are allowed only when the sample/result genuinely belongs in multiple reports.
- `N317A` and `N422A` are special border-control references with stricter combination rules than ordinary control-plan codes.

## progLegalRef — Programme legal reference

<!-- Source: ChemMon 2026 pp. 18-19 -->

**Element code:** B.02 · **Name:** `progLegalRef` · **Catalogue:** `LEGREF` (`ChemMonLegRef`) · **Status:** mandatory · **Repeatable:** yes

### Purpose

`progLegalRef` specifies the legal framework under which the sample analysis was undertaken. It is one of the key routing fields in ChemMon because EFSA uses it to separate analytical results into the relevant national and annual reports. (ChemMon 2026 p18)

### Repeatability and multi-domain samples

This element is repeatable. Use multiple values when a result must be included in more than one annual or national report, or when the same sample/result is legitimately relevant to multiple residue domains. The guidance also allows the legal framework to be expressed at result level rather than sample level when different analyses on the same sample serve different purposes. (ChemMon 2026 p18)

### Catalogue and attribute-based routing

Codes are selected from the `LEGREF` catalogue using the `ChemMonLegRef` hierarchy. These terms carry domain attributes (`VMPR`, `PEST`, `OCC`, `ADD`, `FLAV`) that EFSA uses downstream for report inclusion and flagging. See [[controlled-terminology-catalogues]] and [[reporting-flags]]. (ChemMon 2026 p18)

### VMPR group A3b special case

For VMPR National Control Plan results in group A3b substances that are not authorised VMPs but do have an MRL or default MRL under pesticide legislation:

- if the record is validated according to the pesticide domain, use `N371A$N027A`
- if it is validated according to VMPR only, use `N371A`

The choice changes whether the result is also routed into pesticide reporting. (ChemMon 2026 pp. 18-19)

### Canonical values

| Code | Legal reference | Main use |
| --- | --- | --- |
| `N027A` | Regulation (EC) No 396/2005 + Reg. (EU) 2021/1355 / 2024/989 | Pesticide residues, EU-coordinated programme |
| `N028A` / `N318A` | Directive 2006/125/EC / Reg. (EU) 2016/127 and 2016/128 | Baby-food pesticide reporting |
| `N371A` | Reg. (EU) 2022/1646 and 2022/1644 | VMPR |
| `N112A` | Regulation (EC) No 1333/2008 | Food additives |
| `N113A` | Regulation (EC) No 1334/2008 | Food flavourings |
| `N379A` | Regulation (EU) 2023/915 | Contaminants, maximum levels |
| `N375A` | Regulation (EU) 2022/932 and 2022/931 | Contaminants, control plans |
| `N317A` | Regulation (EU) 2019/1793 | Suspect or targeted border samples |
| `N422A` | Regulation (EU) 2019/1873 | Increased official controls on products of animal origin (new for 2026) |

(ChemMon 2026 p19)

### Worked examples

| Scenario | XML |
| --- | --- |
| EU MACP pesticide sample | `<progLegalRef>N027A</progLegalRef>` |
| VMPR sample under Reg. 2022/1646 | `<progLegalRef>N371A</progLegalRef>` |
| Animal-origin sample relevant for both VMPR and contaminants | `<progLegalRef>N371A$N379A</progLegalRef>` |
| Food sample relevant for both VMPR and pesticides | `<progLegalRef>N371A$N027A</progLegalRef>` |
| Food flavourings sample | `<progLegalRef>N113A</progLegalRef>` |

(ChemMon 2026 p19)

## Related business rules

- `CHEMMON68` — `progLegalRef` domain must match `paramCode`. See [[business-rules-cross-cutting]].
- `CHEMMON101` — for `N422A`, `progType` must be `K019A` and `sampStrategy` must be `ST30A`. See [[business-rules-pesticide]].
- `CHEMMON104` — `N422A` is exclusive. See [[business-rules-pesticide]].
- `CHEMMON105` — `N317A` is exclusive. See [[business-rules-contaminant]].
