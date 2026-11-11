---
title: "Pesticide Residues Reporting"
type: "domain-guide"
domain: "pesticide"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-in-chemmon]]"
  - "[[foodex2-facets-packaging-consumer]]"
  - "[[foodex2-facets-state-process]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[business-rules]]"
  - "[[contaminant-reporting]]"
  - "[[vmpr-reporting]]"
  - "[[baby-food-reporting]]"
  - "[[pesticide-residue-definition-by-matrix]]"
source_pages:
  - "pp. 11-15 (main changes introduced for the 2026 collection)"
  - "pp. 19-21 (progLegalRef examples, B.03 sampStrategy, B.04 progType)"
  - "pp. 23-27 (Table 2, pesticide flags, examples)"
  - "pp. 41-42 (copper coding, drinking water)"
  - "p. 86 (Table 8, copper)"
  - "pp. 135-139, 143 (Table 10: CHEMON90_a/b, CHEMON94, CHEMON95, CHEMON101, CHEMON104, CHEMON105, LL_04)"
  - "p. 146 (Table 12)"
last_updated: "2026-11-11"
---

# Pesticide Residues Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 19-21, 25-26, 148 -->
## Scope

- Pesticide residues is one of five [[chemmon-overview|ChemMon]] reporting domains, covering samples of food products defined in Annex I of Regulation (EC) No 396/2005 (processed and unprocessed). (ChemMon 2026 pp. 19, 148)
- Covers the EU-coordinated programme (EU MACP), national programmes under Regulation (EU) 2021/1355 (MANCP), and increased controls on imported food. EFSA flags a sample as EU MACP when `progType` is `K009A` or `K018A`, `sampStrategy` is `ST10A` or `ST20A`, and the sample is one of the 12 commodities in Annex I Part A, or baby food in Annex II, of Regulation (EU) 2024/989; the MANCP and import-control flag conditions are on [[ssd2-programme-valid-combinations]]. (ChemMon 2026 pp. 25-26)
- Matrix coding follows [[foodex2-in-chemmon]] rules. Copper reporting overlaps with [[contaminant-reporting]]; different `F20` and `F28` codes apply depending on domain, so use [[foodex2-facets-packaging-consumer]] and [[foodex2-facets-state-process]] for the facet definitions.
- Some pesticides have different residue definitions for different commodities, so the `paramCode` depends on the sampled matrix; LL_04 rejects mismatches (Error; ChemMon 2026 Table 10 p. 143). See [[pesticide-residue-definition-by-matrix]].

## Mandatory Legal References

Each pesticide submission must carry a `progLegalRef` code identifying the regulatory basis:

| Code | Regulation | Domain attributes (Table 12) |
| --- | --- | --- |
| N027A | Regulation (EC) No 396/2005; EU MACP under Reg. (EU) 2024/989, national programmes under Reg. (EU) 2021/1355 (Table 2) | PEST |
| N028A | Directive 2006/125/EC -- baby food. See [[baby-food-reporting]]. | PEST, OCC, ADD |
| N318A | Delegated Reg. (EU) 2016/127 and Reg. (EU) 2016/128 -- baby food. See [[baby-food-reporting]]. | PEST, OCC, ADD |
| N371A | Reg. (EU) 2022/1646 and 2022/1644 -- VMPR; concatenated with N027A for a sample used in both domains (p. 26). See [[vmpr-reporting]]. | VMPR |
| N375A | Reg. (EU) 2022/931 and 2022/932 -- contaminant control plans; concatenated with N027A in the p. 27 import example. | OCC |
| N317A | Reg. (EU) 2019/1793 -- increased controls on imported food of non-animal origin | PEST, OCC, ADD |
| N422A | Reg. (EU) 2019/1873 -- intensified official controls on products of animal origin (new 2026) | OCC, PEST, VMPR |

The full list of 31 codes is on [[ssd2-programme-legal-reference]]. (ChemMon 2026 pp. 19, 23-27, 146)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 11, 20-21 -->
## Sampling Strategies

| Code | Strategy |
| --- | --- |
| ST10A | Objective sampling (random surveillance), e.g. for the EU-coordinated pesticides monitoring programme |
| ST20A | Selective/targeted sampling (risk-based) -- "the code to be used when reporting samples taken under national programmes under Regulation (EU) 2021/1355 for pesticide residues"; in 2026 also added in combination with `K009A` and `K018A` for `N027A` (Table 1, p. 11) |
| ST30A | Suspect sampling (e.g. follow-up enforcement samples, samples after RASFF notifications, emergency measures at import); must be used for samples taken under Regulation (EU) 2019/1793 or Regulation (EU) 2019/1873; not considered in the EFSA exposure assessments |

(ChemMon 2026 p20)

- Samples falling under the EU MACP should be reported with `ST10A` or `ST20A`. (ChemMon 2026 p20)
- `progType`: EU MACP samples should use `K009A`; MANCP samples taken in the EU market `K005A`; `K018A` is for samples that are part of both an EU MACP and a national programme, should also be used when the analytical scope is wider than the EU MACP pesticide/crop combinations, and can be used if the same sample serves other domain programmes "as long as the sample strategy is used in accordance with Table 2"; at the border use `K019A` for the EU increased control programme under Regulation (EU) 2019/1793, otherwise `K038A`. (ChemMon 2026 p21) See [[ssd2-programme-strategy-and-type]].

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 13, 41, 86, 135 -->
## Copper-Specific Requirements

Copper (`paramCode` `RF-0102-001-PPP`) can be reported under pesticides or contaminants, and the sample-preparation facets differ between the two. The two copper rules are triggered by the `paramCode`; their Table 10 rows carry no domain condition, and Table 8 lists the same two requirements for copper under contaminants. (ChemMon 2026 pp. 41, 86, 135)

- **CHEMON90_a** (Warning; "becomes an error in 2027"): if copper is reported, the use of facet F20 (part-consumed-analysed) and/or F28 (process) is needed. (ChemMon 2026 Table 10 p. 135)
- **CHEMON90_b** (Error from 2026): if copper is reported, result value uncertainty (`resValUncert`) must be reported if `resType=VAL`. (ChemMon 2026 Table 10 p. 135)
- Source discrepancy: Table 8 gives the F20/F28 status as "Highly Recommended" ("It is recommended that ... are provided") and says they "will become mandatory" from next year (p. 86); CHEMON90_a says the facets are "needed" but only raises a Warning in 2026 (pp. 13, 135).

<!-- Source: ChemMon 2026 p. 41 (Coding of copper samples under pesticides or contaminants) -->

### Copper sample-preparation facets (F20/F28)

For copper, data providers are requested to include any facet that describes sample preparation, i.e. whether it was done in accordance with the contaminant or the pesticide domain. Depending on the commodity (ChemMon 2026 p41):

- **Pesticide residues**: use the facet/code that matches pesticide preparation.
- **Contaminants** (for reference): use the facet/code that matches contaminant preparation.

| Commodity group | Pesticide residues coding | Contaminants coding (reference) |
| --- | --- | --- |
| Citrus fruits, misc fruits with inedible peel, cucurbits with inedible peel, potatoes | With peel: `F20.A07QE` | Without peel: `F20.A07QF` |
| Chestnuts | With shell: `F20.A07QC` | Without shell: `F20.A07QD` |
| Stone fruits | With stone: `F20.A07QJ` | Without stone: `F20.A07QK` |
| Sweet corn | Kernels with cob: `F20.A07RE` | Kernels without cob: `F20.A07RF` |
| Products of animal origin (muscle) | After removal of trimmable fat: `F20.A0F4V` | With fat: `F20.A0F4T` |
| Fruits, root and tuber vegetables, bulb vegetables, fruiting vegetables, Brassica vegetables, leafy vegetables, legume vegetables, stem vegetables and fungi | Not washed (no code) | Washed: `F28.A07JG` |

For coffee beans specifically: contaminants use roasted beans (`F28.A07GY`), while pesticide residues use green beans (no code given). (ChemMon 2026 p41)

### Measurement uncertainty (resValUncert)

When reporting copper with `resType=VAL`, `resValUncert` must be reported (CHEMON90_b, Error; ChemMon 2026 Table 10 p. 135). Table 8 adds that the range is to be given in the same units as `resVal`. (ChemMon 2026 p86)

<!-- Source: ChemMon 2026 p42 (Drinking water recommendation) -->
## Drinking Water (A03DK)

EFSA encourages data providers to collect and submit available information for pesticides (and contaminants) in **drinking water intended for human consumption**, using FoodEx2 base term `A03DK` ("Drinking water") and its children. (ChemMon 2026 p42)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 13-15, 135-139 -->
## Business Rules Relevant to Pesticide Reporting

Only CHEMON95 has a pesticide condition in its Table 10 row; the others are triggered by a `paramCode`, `progType` or `progLegalRef` and are not limited to one domain.

| Rule | Severity | Description | Trigger (Table 10) | Page |
| --- | --- | --- | --- | --- |
| CHEMON90_a | Warning | Copper: use of facet F20 and/or F28 is needed | `paramCode` `RF-0102-001-PPP` | 135 |
| CHEMON90_b | Error | Copper: `resValUncert` must be reported if `resType=VAL` | `paramCode` `RF-0102-001-PPP` | 135 |
| CHEMON94 | Error | `sampPoint` can only be `E010A` (Border Control Posts) (Error from 2026) | `progType` `K038A` | 136-137 |
| CHEMON95 | Warning | A country of origin different from `XX`, `AA`, `EU`, `XC`, `XD`, `XE` must be reported (remains a Warning in 2026) | PPP result (`is_pest=1`) with `evalCode` `J003A` | 137 |
| CHEMON101 | Error | `progType` is `K019A` and `sampStrategy` can only be `ST30A` (new 2026) | `progLegalRef` `N422A` | 138-139 |
| CHEMON104 | Error | No other `progLegalRef` can be concatenated (new 2026) | `progLegalRef` `N422A` | 139 |
| CHEMON105 | Error | No other `progLegalRef` can be used (new 2026) | `progLegalRef` `N317A` | 139 |

See [[business-rules-pesticide]] for the pesticide rules, [[business-rules-cross-cutting]] for CHEMON94, CHEMON101, CHEMON104 and CHEMON105, and [[business-rules]] for the full rule catalogue.
