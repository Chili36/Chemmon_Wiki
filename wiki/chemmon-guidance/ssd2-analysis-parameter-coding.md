---
title: "SSD2 Analysis: Parameter Type, Code, and Text"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 59-63 (Section 2, elements K.01-K.03)"
related:
  - "[[ssd2-elements-analysis]]"
  - "[[ssd2-elements-programme]]"
  - "[[reporting-flags]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[food-additives-reporting]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Analysis: Parameter Type, Code, and Text

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 59-63 -->

## Rule Summary (Rule-First)

- `paramCode` is mandatory and must come from the `ChemMonRep` reporting hierarchy.
- `paramType` is optional only when EFSA can pre-assign it unambiguously; it matters most for multicomponent or summed parameters.
- For domain-sensitive reporting, the real control point is whether the `paramCode` belongs to the correct analysis hierarchy (`vmprParam`, `pestParam`, `chemAnalysis`, `addAnalysis`, `flavAnalysis`).
- `paramText` is usually optional free text, but some food-additives cases require specific wording about free-acid vs salt expression.

## paramType — Type of parameter

<!-- Source: ChemMon 2026 pp. 59-61 -->

**Element code:** K.01 · **Name:** `paramType` · **Catalogue:** `PARAMTYP` · **Status:** optional when EFSA can pre-assign it

### Purpose

`paramType` indicates whether the reported parameter was analysed in full or only in part, especially for multicomponent residue definitions or summed parameters such as dioxin TEQ-style groupings. (ChemMon 2026 p59)

### Main values

| Code | Meaning |
| --- | --- |
| `P002A` | Part of a sum |
| `P004A` | Sum based on subset |
| `P005A` | `paramCode` fully analysed |

`P001A` and `P003A` are not used. (ChemMon 2026 p60)

### Practical assignment

- Use `P002A` for an individual component that contributes to a reported sum.
- Use `P005A` when the full parameter described by `paramCode` has been analysed.
- Use `P004A` when the reported sum/complex parameter is based on only a subset of the expected components. (ChemMon 2026 p60)

### Domain-specific notes

- Pesticides: for legal-limit compliance, the full residue definition should be analysed; individual `P002A` components are still useful as supporting data.
- VMPR: for negative screening results, reporting only the single components (`P002A`) can be sufficient; EFSA may generate the corresponding complex parameter internally.
- Contaminants: individual substance/congener data are important in addition to any group/sum.
- Food additives: individual substances must be reported as expressed by the legislation, and the sum should also be reported when MPLs are regulated at the sum level. (ChemMon 2026 pp. 60-61)

## paramCode — Parameter code

<!-- Source: ChemMon 2026 pp. 62-63 -->

**Element code:** K.02 · **Name:** `paramCode` · **Catalogue:** `PARAM` (`ChemMonRep`) · **Status:** mandatory

### Purpose

`paramCode` identifies the analyte or parameter measured in the laboratory. Only codes present in the `ChemMonRep` reporting hierarchy can be transmitted, even if the wider PARAM catalogue contains other codes. (ChemMon 2026 p62)

### Domain routing

EFSA uses analysis hierarchies under PARAM to route results into the right legal-limit and reporting domains:

| Domain | Analysis hierarchy |
| --- | --- |
| VMPR | `vmprParam` |
| Pesticides | `pestParam` |
| Contaminants | `chemAnalysis` |
| Food additives | `addAnalysis` |
| Food flavourings | `flavAnalysis` |

This routing is what feeds downstream flagging and reportability, so data providers must ensure the chosen `paramCode` lives in the hierarchy for the intended domain. See [[reporting-flags]]. (ChemMon 2026 pp. 62-63)

## paramText — Parameter text

<!-- Source: ChemMon 2026 p63 -->

**Element code:** K.03 · **Name:** `paramText` · **Status:** optional

### General rule

Avoid using the ampersand character (`&`) when preparing XML. (ChemMon 2026 p63)

### Food-additives specific rule

For food additives regulated as groups, `paramText` must state whether the result is expressed as **free acid** or **salt** when that distinction is relevant, for example with sorbic acid and sorbates. If no such text is supplied, EFSA treats the result as expressed as free acid. See [[food-additives-reporting]]. (ChemMon 2026 p63)

## Related business rules

- `CHEMMON68` — `progLegalRef` domain must match `paramCode` domain. See [[business-rules-cross-cutting]].
- `CHEMMON92` — in VMPR, the base term of `paramCode` must belong to `vetDrugRes`. See [[business-rules-vmpr]].
- `CHEMMON106` — potassium sorbate `paramText` should specify free-acid vs salt expression. See [[business-rules-additives]].
