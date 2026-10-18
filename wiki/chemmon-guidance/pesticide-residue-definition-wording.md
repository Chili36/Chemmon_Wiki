---
title: "Reading Pesticide Residue Definition Wording"
type: "domain-guide"
domain: "pesticide"
last_updated: "2026-10-18"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "datasets/rd-bridge/interpretation_guidance.json"
  - "datasets/rd-bridge/residue_param_map.json"
source_pages:
  - "ChemMon 2026 pp. 59-61 (K.01 paramType, Table 5, examples)"
  - "rd-bridge interpretation_guidance.json @ d399cea, 11 rules"
  - "rd-bridge residue_param_map.json @ d399cea, residue_id 253"
related:
  - "[[ssd2-analysis-parameter-coding]]"
  - "[[pesticide-residue-definition-by-matrix]]"
  - "[[pesticide-residue-definitions-by-food]]"
  - "[[pesticide-reporting]]"
  - "[[legal-limits-database]]"
select_when: "Working out which substances a pesticide residue definition actually requires: what 'expressed as' means, whether the heading substance must be analysed, how sums, salts, esters, conjugates, isomers, common-moiety methods, 'where only' clauses or 'aka' names count, and whether a result is P005A, P004A or P002A."
---

# Reading Pesticide Residue Definition Wording

## Rule Summary (Rule-First)

<!-- Source: datasets/rd-bridge/interpretation_guidance.json @ d399cea, rules EU-TEXT-CONTROLS, OECD-ENFORCEMENT-SCOPE, OECD-EXPRESSION-BASIS, EFSA-WHOLE-VS-PARTS -->

- **The exact EU residue definition for the sampled commodity decides which substances make up the residue.** A pesticide's common name, the heading of the entry, a PARAM catalogue family or a broader risk-assessment definition does not add analytes.
- **"Expressed as X" names the basis for calculating the result**, possibly with a molecular-weight conversion. It does not by itself require X to be measured.
- **"X (Y, expressed as X)" means analyse Y.** X is the heading and the expression basis. **"Sum of X and Y, expressed as X" means analyse both.**
- **The whole-residue code, the active-substance code and the code of a single part are different things.** Report the result for the definition with its whole-residue `paramCode`, and each part with that part's own code (`P002A`). Do not use a whole-residue code for a part just because its label names the same substance.

These are readings of the legal wording, not extra rules. Where a reading and the legal text disagree, the legal text wins; see [Status of these readings](#status-of-these-readings).

## How to read common wording

<!-- Source: datasets/rd-bridge/interpretation_guidance.json @ d399cea, rules OECD-SUMMED-COMPONENTS, OECD-CONVERSION, OECD-FREE-CONJUGATED, OECD-ISOMER-COVERAGE, OECD-COMMODITY-VARIANTS, EU-CONDITIONAL-CLAUSE, EU-ALIASES-NOT-EXTRA -->

| Wording | Reading | Not |
|---|---|---|
| "sum of A, B and C", "including", "mixture of" | Each named constituent is a part of the residue. A group counts as one part only when the text names a class without listing its members. | The heading counted again as an extra part when it only labels the sum. |
| "determined as", "hydrolysable to", "common moiety", "calculated in total as" | One measurement converts several forms to a common product. Keep apart the substance finally determined, the precursor forms it covers and the substance used to express the result. | The conversion product or expression basis treated as a separately required parent analyte. |
| "its salts", "its esters", "its conjugates", "free and conjugated" | Usually widens what counts as the named residue, for example by requiring hydrolysis. | A separate analyte for every unnamed salt, ester or conjugate. Named, analytically distinct forms still count separately. |
| "sum of isomers" (unnamed) | The total for the named compound. | Specific stereoisomers invented. When E/Z, cis/trans or R/S forms are named and have their own terms, keep them distinct. |
| A commodity-specific (R) definition, e.g. for animal products | Read it independently of the default. Plant and animal definitions can use different marker substances. | Components copied from the default definition into the exception. The product scope is not an analyte. |
| "Where only Y is detected …, the residue definition of Y applies" | An alternative rule that depends on which substances are found. | Both branches treated as one sum that must be measured together. |
| "aka", "also called", "formerly" | An alternative or former name of the same substance. | A second component. Separately listed strains or isomers stay separate. |

<!-- Source: datasets/rd-bridge/residue_param_map.json @ d399cea, residue_id 7, 3050, 284 -->

Examples from the EU wording: 2,4-D is the "sum of 2,4-D, its salts, its esters and its conjugates, expressed as 2,4-D". Cycloxydim includes products "which can be determined as" two glutaric acid derivatives, "calculated in total as cycloxydim". Dinocap's definition switches to meptyldinocap's "where only meptyldinocap or its corresponding phenol are detected". The legal text for each pesticide is in the EU Pesticides Database.

## Worked example: chloridazon

<!-- Source: datasets/rd-bridge/residue_param_map.json @ d399cea, residue_id 253 -->

Commission Regulation (EU) 2023/710 gives chloridazon two definitions. In rd-bridge this is the one case so far where the reading has been checked against the legal act.

| Scope (Annex I) | Residue definition | Whole-residue `paramCode` |
|---|---|---|
| Default | Chloridazon (sum of chloridazon and chloridazon-desphenyl, expressed as chloridazon) | `RF-00005729-PAR` |
| `1000000` products of animal origin; except `1040000` honey | Chloridazon (chloridazon-desphenyl, expressed as chloridazon) | `RF-00005712-PAR` |

- **Default:** two parts, chloridazon `RF-0080-001-PPP` and chloridazon-desphenyl `RF-00006186-PAR`. Analysing only one of them is a subset.
- **Animal products:** one part, chloridazon-desphenyl `RF-00006186-PAR`. Chloridazon is only the expression basis. Analysing chloridazon-desphenyl covers the definition, but analysing the parent chloridazon alone does not.

## From the reading to paramType

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, pp. 59-61 -->

Once the parts are known, apply Table 5 of the ChemMon guidance ([[ssd2-analysis-parameter-coding]]):

- **`P005A`**: every part named in the definition was analysed and included in the result for the whole-residue `paramCode`.
- **`P004A`**: one or more parts were not analysed, so the result is a sum of a subset.
- **`P002A`**: the result for a single part of the sum, reported with that part's own code.

A **simple** definition is analysed with one calibration substance, which can be a mix of isomers. A **multicomponent** definition needs several, such as a parent and its metabolites. Only multicomponent definitions summed from separate measurements need a reported `paramType`; elsewhere EFSA pre-assigns it. For MRL compliance the full definition in Regulation (EC) No 396/2005 must be analysed, and EFSA strongly recommends also reporting the parts as `P002A`. (ChemMon 2026 pp. 59-60)

ChemMon's own example: "aldicarb (sum of aldicarb, its sulfoxide and its sulfone, expressed as aldicarb)" in plant commodities, with all three analysed. Report `RF-0020-001-PPP` as `P005A`, plus aldicarb `RF-0020-002-PPP`, aldicarb sulfoxide `RF-0020-003-PPP` and aldicarb sulfone `RF-0020-004-PPP` as `P002A`. Here "expressed as aldicarb" sits inside an explicit sum, so aldicarb is both a part and the expression basis. (ChemMon 2026 p61)

## Status of these readings

<!-- Source: datasets/rd-bridge/interpretation_guidance.json @ d399cea, rules EU-TEXT-CONTROLS, OECD-ENFORCEMENT-SCOPE, OECD-EXPRESSION-BASIS, OECD-SUMMED-COMPONENTS, OECD-CONVERSION, OECD-FREE-CONJUGATED, OECD-ISOMER-COVERAGE, OECD-COMMODITY-VARIANTS, EU-CONDITIONAL-CLAUSE, EU-ALIASES-NOT-EXTRA, EFSA-WHOLE-VS-PARTS -->

- **Order of authority:** the residue definition in Regulation (EC) No 396/2005 and its amendments decides; EFSA validates against its Legal Limits database ([[legal-limits-database]]); the readings above help interpret the wording.
- **Where the readings come from:** the wording rules paraphrase the OECD *Guidance Document on the Definition of Residue* (revised 2009, ENV/JM/MONO(2009)30). It explains how enforcement residues are chosen and expressed, but it is **not EU law**. The rules about EU wording (conditional clauses, alternative names) are rd-bridge's readings of the legal text. They are taken from rd-bridge's curated guidance index, which records a source and locator for each rule. They are not verbatim quotes and the wiki has not checked them against the OECD text.
- **One definition at a time:** a reading that fits one definition does not settle another with similar wording. Check the legal text for each case.
- **Model output is not evidence:** rd-bridge uses these rules to prompt a model when it splits definitions into parts. Those model readings are not authoritative, and the wiki does not cite them.

## Relevant Business Rules

| Rule | How it constrains this topic |
|---|---|
| `LL_03` (Error) | `paramType` must be reported for multicomponent/sum parameters. |
| `LL_03_b` (Warning) | `paramType` should equal EFSA's pre-assigned value. |
| `LL_04` / `LL_04_b` (Error) | The whole-residue `paramCode` must be a plausible legal combination with the sampled matrix; results for a part of a sum are exempt. See [[pesticide-residue-definition-by-matrix]]. |

## Relevant Policy

- The legal wording wins over any reading on this page, and over rd-bridge.
- A result is `P005A` only when every part the definition names was analysed. The expression basis counts as a part only when the definition lists it in the sum.
