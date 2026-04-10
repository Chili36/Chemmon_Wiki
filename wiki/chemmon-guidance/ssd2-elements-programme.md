---
title: "SSD2 Elements: Programme"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 17-26 (Section 2, elements B.01-B.04)"
related:
  - "[[ssd2-data-model]]"
  - "[[ssd2-elements-sampling]]"
  - "[[ssd2-elements-matrix]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-pesticide]]"
  - "[[business-rules-vmpr]]"
  - "[[chemmon-overview]]"
---

# SSD2 Elements: Programme

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 17-26 (Section 2, programme elements) -->

## Overview

The programme group identifies the sampling programme, the legal framework it operates under, the sampling strategy applied, and the programme type. These four elements together determine how results are routed into EFSA's National and Annual Reports and which legislative regime applies.

See [[ssd2-data-model]] for the logical model overview, [[ssd2-elements-sampling]] for the sampling event / sample / date elements, and [[ssd2-elements-matrix]] for the matrix coding elements.

## progId — Sampling programme identification code

<!-- Source: ChemMon 2026 p17 -->

**Element code:** B.01 · **Name:** `progId` · **Catalogue:** (free text, size ≤ 100) · **Status:** reportable, with default value permitted

### Purpose

Reporting countries use this field to specify their own codes for national sampling programmes or projects under which the sample was taken. All samples analysed under a programme for a specific purpose or objective should be grouped under the same code. One or more of these codes can be used to group samples where there is a requirement to compare actual samples taken against national sampling plans, or where ad hoc studies have been performed to address a food safety issue.

### Use in EFSA reports

**This element is not used in national or EU Annual Reports issued by EFSA.** It is requested and considered useful mainly for data providers and national organisations. (ChemMon 2026 p17)

### Why it is still reported

- During data validation, if a specific `progId` was reported for a subset of samples, it makes it easier for EFSA and national data providers to collaboratively identify samples taken for the same purpose and retrieve them to check whether those results were correctly coded.
- Where specific risk-based monitoring schemas are defined under the implementing acts per the requirements of Regulation (EU) No 625/2017, `progId` makes it possible to identify the samples under these schemas.
- EFSA provides this element in the MicroStrategy validation dashboard so that the details of all samples reported with a given `progId` can be filtered and visualised. (ChemMon 2026 p17)

### Default value for countries that do not use progId

A country that does not use `progId` can **simply provide a default value for all records**, considering that there are no restrictions on the values used as long as they are within the size limit of **100 characters**. (ChemMon 2026 p17)

### Examples

| Description | XML |
| --- | --- |
| Default Lithuanian national programme identifier to group all samples intended for VMPR monitoring | `<progId>LT_2019_VMPR</progId>` |
| Total Diet Study conducted in Slovakia in 2016 | `<progId>SK_2016_TDS</progId>` |
| National pesticide monitoring programme in France in 2018 | `<progId>FR_2018_NPMP</progId>` |
| Ad hoc Italian national programme on fipronil residues in poultry products | `<progId>IT_2018_FIPRONIL_POULTRY</progId>` |
| Portuguese programme to identify all samples taken in 2020 to detect the presence of mineral oils | `<progId>PT_Mineral_oils_2020</progId>` |
| Finnish results on the occurrence of sweeteners in food | `<progId>FI_2021_sweeteners</progId>` |
| Romanian VMPR National Plan 3 (third country imports) | `<progId>RO_2023_VMPR_Plan3</progId>` |

(ChemMon 2026 p18)

## progLegalRef — Programme legal reference

<!-- Source: ChemMon 2026 pp. 18-19 -->

**Element code:** B.02 · **Name:** `progLegalRef` · **Catalogue:** LEGREF (ChemMonLegRef hierarchy) · **Status:** mandatory · **Repeatable:** yes

### Purpose

This mandatory data element is used to **specify the legal framework under which the sample analysis was undertaken**. It is also required in a harmonised data collection to support the **separation of analytical results into the relevant National and Annual Reports** prepared by EFSA. (ChemMon 2026 p18)

### Repeatability and multi-domain samples

`progLegalRef` is **repeatable** — it allows multiple values for reporting. In particular, results that should be included in more than one annual/national report, or addressed in EFSA data analysis related to results from different residue domains, should be reported with multiple `progLegalRef` values. (ChemMon 2026 p18)

It is also possible to report the legal framework at the result level rather than at the sample level whenever the sample contains analysis performed for different purposes.

### Catalogue and attribute-based routing

Codes to report `progLegalRef` can be selected from the **LEGREF catalogue** using the `ChemMonLegRef` hierarchy. Values in this catalogue are marked as being applicable to the different domains by attribute. This attribute is used to select results to be included in National and Annual Reports, or to be used for exposure assessment and data analysis. The full list is summarised in Table 12 of the source PDF. (ChemMon 2026 p18)

### VMPR National Control Plans group A3b special case

For the results reflecting the VMPR National Control Plans of substances in group A3b — which per Regulation (EU) 2022/1644 are not authorised as veterinary medicinal products but have a Maximum Residue Level (MRL) or default MRL of 0.01 mg/kg under the pesticide residue legislation — the following applies:

- **If validation is done according to the pesticide residue domain**, the `progLegalRef` to be used is the combination `N371A$N027A` for VMPR and pesticides respectively. The combination of sampling strategy and programme type should be the one that reflects the VMPR National Control Plan.
- **If validation is done according to the VMPR domain only**, the `progLegalRef` to be used is `N371A` and the sample is therefore only reported to VMPR per the Table 2 sampling strategy/programme type combinations.

(ChemMon 2026 pp. 18-19)

### Canonical values and what each represents

| Code | Legal reference | Domain / purpose |
| --- | --- | --- |
| `N027A` | Regulation (EC) No 396/2005 + Regulation (EU) 2021/1355 (and 2024/989) | Pesticide residues: EU-coordinated programme (EU MACP), applies to processed and unprocessed food defined in Annex I |
| `N028A` / `N318A` | Directive 2006/125/EC / Regulation (EU) 2016/127 and 2016/128 | Baby food: pesticide results for products intended for young populations |
| `N371A` | Regulation (EU) 2022/1646 and 2022/1644 | VMPR: legislative framework for veterinary medicinal product and other residues in samples of animal origin |
| `N112A` | Regulation (EC) No 1333/2008 | Food additives |
| `N113A` | Regulation (EC) No 1334/2008 | Food flavourings |
| `N379A` | Regulation (EU) 2023/915 | Contaminants: compliance against maximum levels |
| `N375A` | Regulation (EU) 2022/932 and 2022/931 | Contaminants: Member State control plans |
| `N317A` | Regulation (EU) 2019/1793 | Suspect or targeted samples taken at border inspection |
| `N422A` | Regulation (EU) 2019/1873 (**new for 2026**) | Increased official controls at border control posts on products of animal origin |

(ChemMon 2026 p19)

### Worked examples of multi-domain legal references

| Scenario | XML |
| --- | --- |
| Pesticide residues: sample of a product in Annex I of Regulation (EC) 396/2005, part of EU MACP | `<progLegalRef>N027A</progLegalRef>` |
| Baby food samples under Directive 2006/125/EC or Regulation 2016/127 — each `paramCode` routed by its own domain | `<progLegalRef>N028A</progLegalRef>` or `<progLegalRef>N318A</progLegalRef>` |
| VMPR samples under Regulation (EU) 2022/1646 — the only code selectable for the three control plans | `<progLegalRef>N371A</progLegalRef>` |
| Samples under Regulation (EC) 1333/2008 on food additives | `<progLegalRef>N112A</progLegalRef>` |
| Samples where results assess compliance against Regulation (EU) 2023/915 contaminants maximum levels | `<progLegalRef>N379A</progLegalRef>` |
| Samples assessing compliance with MS control plans per Regulations 2022/932 and 2022/931 | `<progLegalRef>N375A</progLegalRef>` |
| Chemical elements tested in animal organs that would be included in VMPR Annual Reports AND are relevant for reporting chemical contaminants | `<progLegalRef>N371A$N379A</progLegalRef>` |
| Food samples fulfilling legal requirements under both Regulation 2022/1646 and 396/2005 (e.g. milk, eggs, honey) — included in both VMPR and pesticide Annual Reports | `<progLegalRef>N371A$N027A</progLegalRef>` |
| Suspect or targeted samples at border per Regulation (EU) 2019/1793 | `<progLegalRef>N317A</progLegalRef>` |
| Samples under Regulation (EC) 1334/2008 on food flavourings | `<progLegalRef>N113A</progLegalRef>` |

(ChemMon 2026 p19)

### Related business rules

- **CHEMMON68** — `progLegalRef` domain must match `paramCode` domain. See [[business-rules-cross-cutting]].
- **CHEMMON50** — Programme type validation for K018A/K009A with N027A. See [[business-rules-cross-cutting]].
- **CHEMMON101** — For N422A, `progType` must be K019A and `sampStrategy` must be ST30A. See [[business-rules-pesticide]].
- **CHEMMON104** — N422A is exclusive (cannot be concatenated with other `progLegalRef` values). See [[business-rules-pesticide]].
- **CHEMMON105** — N317A is exclusive (cannot be concatenated with other `progLegalRef` values). See [[business-rules-contaminant]].

## sampStrategy — Sampling strategy

<!-- Source: ChemMon 2026 pp. 20-21 -->

**Element code:** B.03 · **Name:** `sampStrategy` · **Catalogue:** SAMPSTR · **Status:** mandatory

### Purpose

This element classifies samples according to the sampling methodology applied. **It is important that samples taken in a targeted or suspect way are analysed separately from those taken on a random basis** — they serve different purposes in compliance assessment and exposure estimation.

### Domain-specific requirements

- **VMPR National and Annual Reports**: all results should be reported with sampling strategies `Objective`, `Target sampling`, or `Suspect sampling`. The sampling strategy `Other` should be used to transmit results that are not considered in the VMPR National Control Plans as set up by Regulation (EU) 2022/1646. (ChemMon 2026 p20)
- **PPP (pesticides) domain**: samples falling under the EU MACP should be reported with sampling strategy `Objective sampling` (ST10A) or `Selective sampling` (ST20A). (ChemMon 2026 p20)

### Catalogue values

| Code | Label | Meaning and usage |
| --- | --- | --- |
| `ST10A` | Objective (random) sampling | Surveillance samples (random), e.g. EU-coordinated pesticides programme, or surveillance samples taken to fulfil requirements of the VMPR national randomised surveillance plan (Plan 2, Objective sampling) |
| `ST20A` | Selective/targeted sampling | Risk-based sampling designed to assess compliance with legislation (e.g. samples under national programmes aiming to detect unlawful use or controlling compliance against legal limits). Used under Regulation (EU) 2021/1355 for pesticide residues, for VMPR national risk-based control plan (Plan 1 and Plan 3 for third-country imports per Regulation (EC) No 2022/1646), and for official controls regarding contaminants in foods |
| `ST30A` | Suspect sampling | Risk-based sampling targeting specific producers repeatedly reporting non-compliance — e.g. samples taken after RASFF notifications, follow-up enforcement samples, samples for reasons of suspicion or enhanced surveillance, samples under emergency measures at import. **Must** be used when reporting samples taken under Regulation (EU) 2019/1793 or Regulation (EU) 2019/1873 |
| `ST90A` | Other | VMPR samples collected in the framework of monitoring programmes developed under national legislation that go beyond the programme per Regulation (EU) 2022/1646 |

(ChemMon 2026 pp. 20-21)

### Related business rules

- **CHEMMON51** — For N027A (coordinated control programme), valid sampling strategies are ST10A, ST20A, or ST30A.
- **CHEMMON96** — For VMPR with K005A, valid sampling strategies are ST10A, ST20A, ST30A, or ST90A.
- **CHEMMON97** — For PPP/CONT/ADD/FLAV with K005A, valid sampling strategies are ST10A, ST20A, or ST30A.
- **CHEMMON101** — For N422A, sampling strategy must be ST30A.

See [[business-rules-cross-cutting]] and the domain-specific slice files.

## progType — Programme type

<!-- Source: ChemMon 2026 p21 -->

**Element code:** B.04 · **Name:** `progType` · **Catalogue:** PRGTYP · **Status:** mandatory

### Purpose

This element distinguishes samples taken as part of EU control programmes and other sampling programmes.

### Domain-specific guidance

- **PPP (pesticides)**: samples falling under the EU MACP should be reported using `PRGTYP K009A`. When reporting samples falling under the MANCP and taken in the EU market, code the sample with `PRGTYP K005A`. If there is a need to use the same sample for other domain programmes, `PRGTYP K018A` can be used as long as the sample strategy is used in accordance with Table 2.
- **Border samples**: if the sample falls under the EU increased control programme on imported food of non-animal origin (Regulation (EU) 2019/1793) use `K019A`. Otherwise, use `K038A` for all other import controls. (ChemMon 2026 p21)

### Catalogue values

| Code | Label | Description |
| --- | --- | --- |
| `K009A` | Official (EU) programme | Samples part of a programme designed and coordinated at a European level, e.g. EU MACP as defined in Article 29 of Regulation (EC) No 396/2005 |
| `K005A` | Official (National) programme | Samples part of a programme designed and coordinated at a national level (e.g. Regulation (EU) 2021/1355, 2022/932) |
| `K018A` | Official (National and EU) programme | Samples part of both an EU MACP and national programme. For pesticides, this code should also be used for samples where the analytical scope is wider than the pesticide/crop combination listed in the EU MACP (i.e. more pesticides analysed in an EU MACP commodity). Also used for reporting VMPR results under the national risk-based and randomised surveillance plans for production in the Member States (Plans 1 and 2). For contaminants, this code should also be used when reporting results related to the control plan for food placed on the Union market |
| `K019A` | EU increased control programme on imported food | Samples taken in the context of increased control programmes on imported food, e.g. taken under Regulation (EU) No 2019/1793 |
| `K038A` | Official (National) programme for Third Country Import | Samples taken under the national risk-based control plan for third-country imports for VMPR (Plan 3), but also pesticides if different from K019A. Samples taken under the national risk-based control plan for third-country imports for contaminants according to 2022/932 regulation |
| `K010A` | Occurrence data produced in total diet study (TDS) | Total Diet Study reporting |

(ChemMon 2026 p21)

## Table 2: valid combinations across domains

<!-- Source: ChemMon 2026 pp. 23-26 (Table 2 and descriptions) -->

Table 2 of the source PDF summarises which combinations of `progLegalRef`, `progType`, and `sampStrategy` are valid for each data domain. The constraints are implemented as business rules; all other combinations are rejected. (ChemMon 2026 p22)

### VMPR plan flags

EFSA classifies VMPR samples into four plans based on the combination of `progType` and `sampStrategy`:

- **Plan 1** — National risk-based control plan for production in the Member States. Flagged when `progType ∈ {K005A, K018A}` and `sampStrategy = ST20A` (Selective sampling) and the sample is considered unprocessed. An exception in the processing has been included for insects. (ChemMon 2026 p25)
- **Plan 2** — National risk-based randomised surveillance plan for production in the Member States. Flagged when `progType ∈ {K005A, K018A}` and `sampStrategy = ST10A` (Objective sampling) and the sample is unprocessed. Exception for insects. (ChemMon 2026 p25)
- **Plan 3** — National risk-based control plan for third-country imports. Flagged when `progType = K038A` (Official National programme for Third Country Import), `sampStrategy = ST20A`, and `sampPoint = E010A` (Border Control Posts). (ChemMon 2026 p25)
- **Other** — Any additional sample taken beyond what counts toward the minimum sampling frequencies in Regulation 2022/1646: suspect samples and any other sample taken with `ST90A`. Any sample with a combination not covered by the three plans (including processed products with a combination of Plan 1 or Plan 2) automatically falls into 'Other'. (ChemMon 2026 p25)

### Contaminant control plan flags

- **Control plan for food placed on the Union market**: `progType ∈ {K018A, K005A}` and `sampStrategy = ST20A`. (ChemMon 2026 p25)
- **Third-country imports for contaminants**: `progType = K038A`, `sampStrategy = ST20A`, `sampPoint = E010A` (Border Control Posts). (ChemMon 2026 p25)

### Pesticide control plan flags

- **EU MACP**: `progType ∈ {K009A, K018A}` and `sampStrategy ∈ {ST10A, ST20A}`, and the sample is one of the commodities listed in the EU MACP Regulation (EU) 2024/989 or baby food in Annex II. (ChemMon 2026 p25)
- **MANCP**: `progType = K005A` with `sampStrategy ∈ {ST10A, ST20A, ST30A}`; OR `progType = K018A` with `sampStrategy = ST10A` and sample is NOT one of the 12 commodities in the EU MACP Regulation or `sampStrategy = ST20A`; OR `progType = K038A` with `sampStrategy ∈ {ST10A, ST20A, ST30A}`. (ChemMon 2026 p26)
- **EU increased control programme on imported food**: `progType = K019A`, `sampStrategy = ST30A`, `sampPoint = E010A`, and origin country + `sampMatCode` listed in the revised annexes of Regulation (EU) 2019/1793. (ChemMon 2026 p26)

### Worked examples of valid combinations

| Scenario | Combination |
| --- | --- |
| Randomised control plan result for food placed on the Union market; sample related to EU MACP for PPP | `progLegalRef=N027A`, `progType=K009A`, `sampStrategy=ST10A` |
| Control plan result for food placed on the Union market; sample related to VMPR control Plan 1 | `progLegalRef=N371A`, `progType=K018A`, `sampStrategy=ST20A` |
| Control plan result for food on the Union market regarding Plan 2 of VMPR and MANCP for PPP; a unique sample related to both domains | `progLegalRef=N027A$N371A`, `progType=K018A`, `sampStrategy=ST10A` |
| Control plan result for food on the Union market related to contaminants' control plan | `progLegalRef=N375A`, `progType=K018A`, `sampStrategy=ST20A` |
| Control plan result for food of animal origin entering the Union; sample related to Contaminants' control plan | `progLegalRef=N375A`, `progType=K038A`, `sampStrategy=ST20A`, `sampPoint=E010A` |
| Food of animal origin entering the Union; VMPR control Plan 3 + national plan of pesticides and contaminants' control plan | `progLegalRef=N371A$N027A$N375A`, `progType=K038A`, `sampStrategy=ST20A`, `sampPoint=E010A` |

(ChemMon 2026 pp. 26-27)
