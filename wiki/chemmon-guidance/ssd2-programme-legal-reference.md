---
title: "SSD2 Programme: Legal Reference (progLegalRef)"
type: "reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 18-19 (Section 2, element B.02)"
  - "ChemMon 2026 pp. 146-147 (Table 12)"
  - "pp. 11, 20, 23-24 (N422A change note, ST30A example, Table 2 header and N317A column)"
  - "pp. 126, 138-139 (Table 10, CHEMON54, CHEMON101, CHEMON104, CHEMON105)"
related:
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-programme-valid-combinations]]"
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

- if the record is validated according to the pesticide domain, use `N371A$N027A`; the combination of `sampStrategy` and `progType` "should be the one that reflects the VMPR National Control Plan as reflected in Table 2"
- if it is validated according to VMPR only, use `N371A`; the result is then reported only to VMPR, with the Table 2 `sampStrategy` and `progType` combinations

See [[ssd2-programme-valid-combinations]] for Table 2. The choice changes whether the result is also routed into pesticide reporting. (ChemMon 2026 pp. 18-19)

### LEGREF values and domain attributes (Table 12)

<!-- Source: ChemMon 2026 p. 146 (Table 12); main-use notes from p. 19, Table 2 (p. 23) and p. 11 -->

Table 12 lists the `progLegalRef` codes in the `ChemMonLegRef` hierarchy and the domains each is applicable to. These attributes decide the legislation half of the domain flags (see [[reporting-flags]]). Attributes: `PEST` pesticides, `VMPR` veterinary medicinal residues, `OCC` contaminants, `ADD` food additives, `FLAV` food flavourings. "Main use" is not a Table 12 column: it summarises the B.02 examples (p. 19) and, where a cell says so, the Table 2 header (p. 23) or the 2026 change list (p. 11); it is given only for the codes those pages name. (ChemMon 2026 p146)

| Code | Legal reference (as printed in Table 12) | Domain attributes | Main use |
| --- | --- | --- | --- |
| `N023A` | Commission Regulation (EC) No 2073/2005 (amended) | OCC |  |
| `N027A` | Regulation (EC) No 396/2005 (amended) | PEST | Pesticide residues, EU-coordinated programme; p. 19 says `N027A` also covers Reg. (EU) 2021/1355; the Table 2 header (p. 23) adds Reg. (EU) 2024/989 |
| `N028A` | Directive 2006/125/EC | PEST, OCC, ADD | Baby food; each `paramCode` falls under its own domain (pesticide and/or contaminant outputs), p. 19 |
| `N101A` | Regulation (EC) No 767/2009 (amended) | OCC |  |
| `N112A` | Regulation (EC) No 1333/2008 (amended) | ADD | Food additives |
| `N113A` | Regulation (EC) No 1334/2008 (amended) | FLAV | Food flavourings |
| `N129A` | Regulation (EC) No 178/2002 (amended) | OCC |  |
| `N139A` | Regulation (EC) No 853/2004 (amended) | OCC |  |
| `N154A` | Commission Directive (EC) No 40/2003 | OCC |  |
| `N208A` | Commission Recommendation No 196/2007 | OCC |  |
| `N211A` | Commission Recommendation No 161/2010 | OCC |  |
| `N252A` | Directive 2002/32/EC | OCC |  |
| `N302A` | Commission Recommendation 2015/682 | OCC |  |
| `N304A` | Commission Recommendation (EU) 2017/84 | OCC |  |
| `N310A` | Commission Regulation (EU) 2017/2158 | OCC |  |
| `N312A` | Commission Recommendation (EU) 2014/118 | OCC |  |
| `N313A` | Commission Recommendation (EU) 2013/165 | OCC |  |
| `N317A` | Commission Implementing Regulation (EU) 2019/1793 | PEST, OCC, ADD | "Suspect or targeted samples taken at border inspection" (p. 19); see the `N317A` note below |
| `N318A` | Commission Delegated Regulation (EU) 2016/127 and Regulation (EU) 2016/128 | PEST, OCC, ADD | Baby food; each `paramCode` falls under its own domain (pesticide and/or contaminant outputs), p. 19 |
| `N319A` | Commission Recommendation 2006/576/EC | OCC |  |
| `N320A` | Commission Recommendation 2013/711/EU amended | OCC |  |
| `N323A` | Regulation (EU) No 2017/625 | OCC, ADD |  |
| `N324A` | Commission Recommendation (EU) 2019/1888 | OCC |  |
| `N371A` | Commission Implementing Regulation (EU) 2022/1646 and Commission Delegated Regulation (EU) 2022/1644 | VMPR | VMPR |
| `N372A` | Commission Recommendation (EU) 2022/495 | OCC |  |
| `N374A` | Commission Recommendation (EU) 2016/2115 | OCC |  |
| `N375A` | Commission Delegated Regulation (EU) 2022/931 and Implementing Regulation (EU) 2022/932 | OCC | Contaminants, control plans |
| `N376A` | Commission Recommendation (EU) 2022/553 | OCC |  |
| `N377A` | Commission Recommendation (EU) 2022/561 | OCC |  |
| `N379A` | Commission Regulation (EU) 2023/915 | OCC | Contaminants, maximum levels |
| `N422A` | Commission Implementing Regulation (EU) 2022/1873 (sic; see note) | OCC, PEST, VMPR | Intensified official controls at border control posts on products of animal origin (new for 2026; p. 11, not named on p. 19) |

Notes:

- `N028A` / `N318A`: "Each paramCode reported will fall under its corresponding domain. If a given paramCode belongs to pesticide and contaminant domains, that result will be taken for the pesticide Annual Report output, as well as for contaminant covering baby food outputs." (ChemMon 2026 p19)
- `N317A` — Source discrepancy: the B.02 example describes "Suspect or targeted samples" (ChemMon 2026 p19), but the B.03 example says `ST30A` (suspect sampling) "Must be used when reporting samples taken under Regulation (EU) 2019/1793 or Regulation (EU) 2019/1873" (ChemMon 2026 p20), and Table 2 lists only `ST30A` for `N317A` (ChemMon 2026 p24). Selective/targeted sampling (`ST20A`) is not a listed combination. Validation settles it: `CHEMON54` (Error) requires `progType` `K019A` and `sampStrategy` `ST30A` for `N317A` (ChemMon 2026 Table 10, p. 126).
- `N371A`: "This is the only code to be selected (alone or in combination with other codes, e.g. in combination with code N027A for the pesticide residue monitoring activities) in order to flag that the sample was taken according to the three different plans" of Regulation (EU) 2022/1646. (ChemMon 2026 p19)
- `N422A`: Table 12 prints "2022/1873"; every other mention in the guidance (pp. 6, 11, 23-24 and CHEMON104 on p. 139) gives Regulation (EU) **2019/1873**, the regulation on intensified controls on products of animal origin. Treat 2022/1873 as a typo in Table 12.
- Source discrepancy: Table 1 says `N422A` "has been flagged for contaminants, pesticides, VMPR, food additives and food flavourings" (ChemMon 2026 p11), while Table 12 gives only `OCC, PEST, VMPR` (ChemMon 2026 p146). The guidance does not reconcile the two.
- Codes with several attributes (`N028A`, `N317A`, `N318A`, `N323A`, `N422A`) put the legislation in each of those domains; whether a result is flagged 1 or 3 then depends on whether its `paramCode` is in that domain's analysis hierarchy (pp. 148-149). See [[reporting-flags]].
- Use the most specific code. `N129A` (Regulation (EC) No 178/2002) flags records `is_occ=1`, so they are used for exposure assessment but not necessarily in EU Annual Reports. (ChemMon 2026 p147)

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

- `CHEMON68` — `progLegalRef` domain must match `paramCode`. See [[business-rules-cross-cutting]].
- `CHEMON101` — for `N422A`, `progType` must be `K019A` and `sampStrategy` must be `ST30A`. See [[business-rules-cross-cutting]]. (ChemMon 2026 pp. 138-139)
- `CHEMON104` — `N422A` is exclusive. See [[business-rules-cross-cutting]]. (ChemMon 2026 p139)
- `CHEMON54` — for `N317A`, `progType` must be `K019A` and `sampStrategy` must be `ST30A` (Error). See [[business-rules-cross-cutting]]. (ChemMon 2026 p126)
- `CHEMON105` (Error) — if `progLegalRef` is `N317A`, no other `progLegalRef` can be used. See [[business-rules-cross-cutting]]. (ChemMon 2026 p139)
