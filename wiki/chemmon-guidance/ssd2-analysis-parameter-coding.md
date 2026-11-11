---
title: "SSD2 Analysis: Parameter Type, Code, and Text"
type: "reference"
domain: "all"
last_updated: "2026-11-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 59-63 (Section 2, elements K.01-K.03, Tables 5-6)"
  - "p. 140 (Table 10, CHEMON106)"
related:
  - "[[ssd2-elements-analysis]]"
  - "[[ssd2-elements-programme]]"
  - "[[reporting-flags]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[food-additives-reporting]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-vmpr]]"
  - "[[pesticide-residue-definition-by-matrix]]"
  - "[[pesticide-residue-definition-wording]]"
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

### Pre-assignment criteria

EFSA keeps a separate document with the full list of `paramCode`s and pre-assigned `paramType`, available in Knowledge Junction, built on these criteria (ChemMon 2026 p60):

| Case | Pre-assigned `paramType` |
| --- | --- |
| Individual components of a multicomponent/sum `paramCode` | `P002A` |
| `paramCode` measured with one calibration compound (or a mix of compounds), covering the full description of `paramCode` | `P005A` |
| Multicomponent/sum `paramCode` calculated from measurements of individual components | `P004A`/`P005A`: report `P005A` if all the expected parts have been analysed as specified by `paramCode`, or `P004A` otherwise |

### Worked examples

| Result | `paramCode` | `paramType` | Assigned by |
| --- | --- | --- | --- |
| Sum of malachite green and leucomalachite green in meat of aquaculture products (MRPL defined); both components analysed and summed | `RF-00004513-PAR` | `P005A` | Data provider (EFSA pre-assignment `P004A`/`P005A`) |
| Same sum, partial analysis; only leucomalachite green analysed | `RF-00004513-PAR` | `P004A` | Data provider (EFSA pre-assignment `P004A`/`P005A`) |
| Leucomalachite green, one of the components of the sum above | `RF-00001727-PAR` | `P002A` | Automatically assigned by EFSA |
| Permethrin (sum of isomers) (MRL defined) | `RF-0842-001-PPP` | `P005A` | Automatically assigned by EFSA |
| Aldicarb (sum of aldicarb, its sulfoxide and its sulfone, expressed as aldicarb) in plant commodities, all components analysed | `RF-0020-001-PPP` | `P005A` | Data provider (EFSA pre-assignment `P004A`/`P005A`) |
| Additionally for that aldicarb result: aldicarb, aldicarb sulfoxide, aldicarb sulfone | `RF-0020-002-PPP`, `RF-0020-003-PPP`, `RF-0020-004-PPP` | `P002A` each | — |
| Betamethasone in cow meat (MRL defined) | `RF-00000273-VET` | `P005A` | Automatically assigned by EFSA |
| Betamethasone in sheep meat (no MRL defined, not authorised use) | `RF-00000273-VET` | `P005A` | Automatically assigned by EFSA |
| Benzo-a-pyrene in smoked meat (ML defined) | `RF-00000046-ORG` | `P005A` | Automatically assigned by EFSA |
| Benzo-a-pyrene in smoked paprika (no ML defined) | `RF-00000046-ORG` | `P005A` | Automatically assigned by EFSA |
| Sum of 2 PAH indicators (benzo[a]pyrene and chrysene) in smoked paprika (no ML defined); both components analysed and summed | `RF-00004427-PAR` | `P005A` | Data provider (EFSA pre-assignment `P004A`/`P005A`) |
| Same sum; only chrysene analysed | `RF-00004427-PAR` | `P004A` | Data provider (EFSA pre-assignment `P004A`/`P005A`) |

(ChemMon 2026 pp. 61-62)

### Domain-specific notes

- Pesticides: to check for MRL compliance it is a legal requirement to analyse the full residue definitions as defined in Regulation (EC) No 396/2005 (i.e. all the components). Additionally, results on the individual components associated with `P002A` are strongly recommended to be reported too; these will normally not be included in the data analysis of the EU Report on pesticide residues, but EFSA might use them in later mandates on specific substances. (ChemMon 2026 p60) Some pesticides have different residue definitions, and so different `paramCode`s, for different commodities; see [[pesticide-residue-definition-by-matrix]]. To work out which parts a definition names (for example, whether the substance after "expressed as" must be analysed), see [[pesticide-residue-definition-wording]].
- VMPR: a similar approach applies. However, for negative screening results the reporting of the single components associated with `P002A` is sufficient and the multicomponent/sum `paramCode` does not need to be reported; EFSA will automatically generate the record for the complex `paramCode`, which is then counted in the National and EU VMPR Reports. "Negative" here means results reported with `resType` = `LOD`, `LOQ`, `CCB`, `BIN` or `CCA` and `evalCode` different from `J041A` (Detected). (ChemMon 2026 p61, footnote 47)
- Contaminants: the single substances or congener-specific occurrence data must be reported, in addition to the sum (when required for assessment against maximum levels) or complex mixtures. The sums of congener/substance groups reported alone are of very limited use for EFSA. (ChemMon 2026 p61)
- Food additives: the analytical result for the individual substances must be reported expressed as specified in Regulation (EC) No 1333/2008 (e.g. sorbic acid-sorbates expressed as the free acid). Additionally, the sum should be reported if it complements the individual substance, as the MPLs are regulated at the sum level for the reported legislative category. (ChemMon 2026 p61)

## paramCode — Parameter code

<!-- Source: ChemMon 2026 pp. 62-63 -->

**Element code:** K.02 · **Name:** `paramCode` · **Catalogue:** `PARAM` (`ChemMonRep`) · **Status:** mandatory

### Purpose

`paramCode` identifies the analyte or parameter measured in the laboratory. Only codes present in the `ChemMonRep` reporting hierarchy can be transmitted, even if the wider PARAM catalogue contains other codes. (ChemMon 2026 p62)

### Examples

| Result | `paramCode` |
| --- | --- |
| Aflatoxins sum of B1, B2, G1 and G2 | `RF-00000435-TOX` |
| Aflatoxin B1 alone as component of the sum of aflatoxins | `RF-00000150-TOX` |
| Cloxacillin | `RF-00000566-VET` |
| The sweetener saccharin | `RF-00000013-ADD` |
| Terbacil | `RF-0912-001-PPP` |
| The flavouring caffeine | `RF-00000038-NTR` |

(ChemMon 2026 p62)

### Domain routing

EFSA uses analysis hierarchies under PARAM to route results into the right legal-limit and reporting domains:

| Domain | Analysis hierarchy |
| --- | --- |
| VMPR | `vmprParam` |
| Pesticides | `pestParam` |
| Contaminants | `chemAnalysis` |
| Food additives | `addAnalysis` |
| Food flavourings | `flavAnalysis` |

This routing is what feeds downstream flagging and reportability, so data providers should make sure the chosen `paramCode` is included in the hierarchy for the intended domain. This can be checked in the PARAM catalogue in the EFSA Catalogue Browser, on the right-hand side under "Reportability". See [[reporting-flags]]. (ChemMon 2026 pp. 62-63)

## paramText — Parameter text

<!-- Source: ChemMon 2026 p63 -->

**Element code:** K.03 · **Name:** `paramText` · **Status:** optional

### General rule

Avoid using the ampersand character (`&`) when preparing XML. (ChemMon 2026 p63)

### Food-additives specific rule

For food additives regulated as groups (e.g. sorbic acid and sorbates), `paramText` must be filled in as `Expressed as free acid` or `Expressed as salt`. This is mainly required when the reported substance can be expressed as the free acid or converted to the salt. If the information is not provided, the analytical value will be considered expressed as free acid. See [[food-additives-reporting]]. (ChemMon 2026 p63)

## Related business rules

- `CHEMON68` — `progLegalRef` domain must match `paramCode` domain. See [[business-rules-cross-cutting]].
- `CHEMON92` validates the VMPR **matrix** base terms (`sampMatCode`, `anMatCode`) against VetDrugRes, not `paramCode`. See [[business-rules-vmpr]].
- `CHEMON106` (Warning) — if `paramCode` `RF-00000248-ADD` (Potassium sorbate) is reported, `paramText` should specify `Expressed as free acid` or `Expressed as salt` (ChemMon 2026 Table 10, p140). See [[business-rules-additives]].
