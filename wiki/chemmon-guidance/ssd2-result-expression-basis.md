---
title: "SSD2 Result: Expression Basis (exprResType, exprResPerc)"
type: "reference"
domain: "all"
last_updated: "2026-04-15"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 69-70 (Section 2, elements M.13-M.14)"
related:
  - "[[ssd2-elements-result]]"
  - "[[ssd2-result-value-and-type]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-contaminant]]"
  - "[[business-rules-additives]]"
---

# SSD2 Result: Expression Basis (exprResType, exprResPerc)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 69-70 -->

## Rule Summary (Rule-First)

- `exprResType` indicates the basis on which the concentration is expressed (e.g. whole weight, fat weight, dry matter).
- When `exprResType` is mandatory, `exprResPerc` becomes dependent-mandatory and must supply the relevant percentage(s) (fat/moisture).
- Domain-specific constraints apply (pesticides: limited code set and egg/milk rule; contaminants in feed: mandatory; additives/flavourings: mandatory).

## Relevant Business Rules

- **CHEMMON56/70** — Pesticide constraints for `exprResType`. See [[business-rules-pesticide]].
- **CHEMMON71** — Contaminants in feed: `exprResType` is mandatory. See [[business-rules-contaminant]].
- **CHEMMON84_a / CHEMMON84_b** — Additives/flavourings mandatory; contaminants recommended. See [[business-rules-additives]].

## exprResPerc / exprResType — Expression of result

<!-- Source: ChemMon 2026 pp. 69-70 -->

**Element codes:** M.13, M.14 · **Names:** `exprResPerc`, `exprResType` · **Catalogue:** EXPRRES · **Status:** mandatory for some domains

### Purpose

These elements are used to indicate when the concentration is **expressed as a percentage of a component** of the sample, for example, on a dry weight basis. In the cases where `exprResType` should be reported (mandatory), `exprResPerc` should be also reported (dependent mandatory). (ChemMon 2026 p69)

### Pesticide residues — whole-product vs fat basis

For pesticide residues, the MRLs for eggs and milk apply to the whole product. However, fat-soluble pesticides tend to concentrate in the fat. Therefore, when reporting pesticides in eggs or milk it is necessary to report if the result is expressed as:

- **whole weight** (code `B001A`): whole egg (after removal of the shell) or whole milk (based on a fat content of 4% by weight)
- **fat weight** (code `B003A`): fat phase separated and result provided on the fat part. (ChemMon 2026 p69)

This information allows EFSA to correctly check the consistency of result evaluation for exposure assessment.

### Mandatory for food additives and flavourings

For food additives and food flavourings, `exprResType` should be reported, **as it became mandatory in 2025 and 2026 respectively**. If not reported, the system returns an error message. (ChemMon 2026 p70)

### Contaminants: dry matter basis

In Regulation (EU) 2023/915, where the maximum levels for certain contaminants in food are established, there are specific remarks on the matrix to which the maximum levels apply. For example, the established maximum levels for aflatoxin B1, ochratoxin A, deoxynivalenol, zearalenone, fumonisins apply to the **dry matter** of baby food and processed cereal-based foods for infants and young children. (ChemMon 2026 p70)

### Fat weight for meat

For animal-origin products concerning meat, MRLs apply to the muscle or to the fat. If a fat-soluble pesticide is analysed in a meat sample and `exprResType` is "fat weight" (`B003A`), results will be checked against the MRL for fat. If `exprResType` is "whole weight" (`B001A`), the fat percentage under `exprResPerc` should be reported; if it is not reported, EFSA will consider default values whenever possible. If the pesticide analysed is not fat soluble, it is highly recommended to express the result as whole weight so it is checked against the MRLs for muscle. (ChemMon 2026 p70)

### Feed contaminants — dry-matter basis

Directive (EC) 2002/32 describes maximum levels of undesirable substances in mg/kg in feedstuffs with a moisture content of 12% (88% dry matter); to check compliance and derive exposure-assessment-usable concentrations it is recommended to report feed contaminants expressed on **88% dry matter** (code `B004A`). The `exprResType` has to be reported for feed; if analysis was performed on whole weight this should be indicated with `exprResType = B001A` and the moisture percentage of the sample in `exprResPerc.moistPerc` must be reported. If moisture percentage is not available but dry matter is, EFSA recommends calculating moisture as `100 − dry matter`. (ChemMon 2026 p70)

### Examples

| Description | XML |
| --- | --- |
| Fat-soluble pesticide in butter expressed on fat-weight basis | `<exprResPerc>fatPerc=80</exprResPerc><exprResType>B003A</exprResType>` or `<exprResPerc.fatPerc>80</exprResPerc.fatPerc><exprResType>B003A</exprResType>` |
| Moisture percentage for heavy metals in seaweed expressed on whole-weight basis | `<exprResPerc>moistPerc=40</exprResPerc><exprResType>B001A</exprResType>` |
| Moisture and fat percentages for heavy metals in seaweed (whole weight) | `<exprResPerc>moistPerc=40$fatPerc=5</exprResPerc><exprResType>B001A</exprResType>` |

(ChemMon 2026 p70)

### Related business rules

- **CHEMMON56** — For pesticides, `exprResType` can only be B001A, B003A, or B007A. See [[business-rules-pesticide]].
- **CHEMMON70** — For pesticides in egg/milk matrices, `exprResType` must be B001A.
- **CHEMMON71** — For contaminants in feed, `exprResType` is mandatory. See [[business-rules-contaminant]].
- **CHEMMON84_a** — `exprResType` is mandatory for food additives and flavourings. See [[business-rules-additives]].
- **CHEMMON84_b** — `exprResType` is highly recommended for contaminants.

