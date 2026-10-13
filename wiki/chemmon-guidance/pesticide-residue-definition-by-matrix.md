---
title: "Pesticide Residue Definition and paramCode by Matrix"
type: "domain-guide"
domain: "pesticide"
last_updated: "2026-10-13"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "datasets/rd-bridge/residue_param_map.json"
source_pages:
  - "ChemMon 2026 pp. 59-60 (K.01 paramType), p. 143 (LL_04/LL_04_b), p. 148 (Section 8)"
  - "rd-bridge residue_param_map.json @ 104448e, residue_id 10, 210, 2058"
related:
  - "[[ssd2-analysis-parameter-coding]]"
  - "[[business-rules-legal-limits]]"
  - "[[legal-limits-database]]"
  - "[[pesticide-reporting]]"
  - "[[ssd2-matrix-sampled-matrix]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[pesticide-residue-definitions-by-food]]"
select_when: "Choosing which pesticide paramCode or residue definition to report for a sampled food, or why the PARAM code for the same pesticide differs between foods such as plant products, animal products, milk or honey, including LL_04 errors about the residue definition for the sample analysed."
---

# Pesticide Residue Definition and paramCode by Matrix

## Rule Summary (Rule-First)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, p. 60 and p. 143 -->

- For a pesticide result, report the `paramCode` of the **residue definition that applies to the sampled matrix**. Some pesticides have one EU residue definition for most foods and a different one for specific commodities, so the same pesticide can need a different `paramCode` in different foods.
- MRL compliance requires analysing the **full** residue definition in Regulation (EC) No 396/2005, as reflected in the corresponding `paramCode`. EFSA states that the current valid residue definitions and paramCodes are also available in the EFSA Legal Limits database. (ChemMon 2026 p60)
- EFSA enforces the matrix match with **LL_04/LL_04_b (Error)**: for pesticide records (`is_pest=1`) whose `paramCode` is in the legal limits database, the sampled matrix and `paramCode.base` must be a plausible legal combination (`PlausibleCombinationPPP=1`), **unless the result is reported for a part of a sum**. Error message: "The selected paramCode does not refer to the correct legal Residue Definition for the sample analysed. Please correct the paramCode". (ChemMon 2026 p143)
- `paramType` follows the existing rules in [[ssd2-analysis-parameter-coding]]: the whole residue definition is `P005A` when all parts were analysed (`P004A` when only a subset was), and individual components are `P002A`. LL_04 exempts part-of-sum results, so components reported as `P002A` are not checked against the matrix. (ChemMon 2026 pp. 60, 143)
- The legislation is the official source. EFSA's Legal Limits database is what validation uses; it holds history with dates of applicability ([[legal-limits-database]]). (ChemMon 2026 p148)

## How to choose the paramCode

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, p. 143 -->

1. **Place the sampled food in an Annex I commodity** of Regulation (EC) No 396/2005. Commodity-specific residue definitions are scoped by Annex I codes, often at group level (all products of animal origin, milk), sometimes with excluded sub-groups.
2. **Check whether the pesticide has commodity-specific definitions.** In the EU Pesticides Database these definitions carry an `(R)` marker and a footnote naming the commodity codes. If there is none, one definition and one whole-residue `paramCode` apply in every food.
3. **Pick the scope that contains the commodity.** Use a commodity-specific definition when the commodity falls inside its scope and outside its exclusions; otherwise use the default definition.
4. **Report the whole-residue `paramCode`** of that definition with `P005A`/`P004A`, and any analysed components with `P002A`.
5. **For samples from earlier years**, confirm the definition that applied on the sampling date. Residue definitions change over time; the Legal Limits database keeps limits with dates of applicability, and EFSA applies the limit valid at the sampling date. (ChemMon 2026 p148)

## Examples: one pesticide, different codes by food

<!-- Source: datasets/rd-bridge/residue_param_map.json @ 104448e, residue_id 10, 210, 2058 -->

Snapshot: rd-bridge commit `104448e`, residue map last changed 2026-10-11, derived from the EU Pesticides Database (DG SANTE) and EFSA PARAM 17.6. These are the **latest** EU definitions in that snapshot, not a historical record.

| Pesticide | Scope (Annex I) | Residue definition | Whole-residue `paramCode` |
|---|---|---|---|
| Acetamiprid | Default (no exception applies) | Acetamiprid | `RF-0014-001-PPP` |
| Acetamiprid | `1000000` animal products, except `1040000` honey | Sum of acetamiprid and N-desmethyl-acetamiprid (IM-2-1), expressed as acetamiprid | `RF-00003326-PAR` |
| 2-phenylphenol | Default (no exception applies) | Sum of 2-phenylphenol and its conjugates, expressed as 2-phenylphenol | `RF-00007633-PAR` |
| 2-phenylphenol | `1000000` animal products, except `1040000` honey | 2-phenylphenol (parent only) | `RF-0823-001-PPP` |
| Thiabendazole | Default (no exception applies) | Thiabendazole | `RF-0416-001-PPP` |
| Thiabendazole | `1000000` animal products, except `1020000` milk and `1040000` honey | Sum of thiabendazole and 5-hydroxythiabendazole, expressed as thiabendazole | `RF-00007629-PAR` |
| Thiabendazole | `1020000` milk | Sum of thiabendazole, 5-hydroxythiabendazole and its sulfate conjugate, expressed as thiabendazole | `RF-00007630-PAR` |

Annex I names: `1000000` products of animal origin (terrestrial animals), `1020000` milk, `1040000` honey and other apiculture products.

What the examples teach:

- **Direction varies.** Acetamiprid and thiabendazole add metabolites for animal products; 2-phenylphenol goes the other way, from a sum with conjugates in plant products to the parent compound only in animal products.
- **Exclusions matter.** Honey (`1040000`) sits inside the animal-products group but is excluded from all three exceptions, so honey takes the default definition. Thiabendazole in cow milk uses the milk-specific code `RF-00007630-PAR`, not the general animal-product code.
- **Components keep their own codes.** In bovine meat, acetamiprid's whole residue is `RF-00003326-PAR` (`P005A`); its parts, acetamiprid `RF-0014-001-PPP` and IM-2-1 `RF-00002836-PAR`, can be reported as `P002A`.
- **Source wording can need interpretation.** For 2-phenylphenol and thiabendazole the EU footnote reads "code 100000"; rd-bridge reads it as `1000000` because the excluded codes nest inside that group. Treat such rows as interpreted, not verbatim.

## Finding the definition for other pesticides

- [[pesticide-residue-definitions-by-food]] lists every pesticide whose definition differs by commodity in the pinned snapshot, with scopes and whole-residue codes. A pesticide not on that list has one definition for all foods.
- The EU Pesticides Database and EFSA's Legal Limits database are the reference sources for residue definitions and validated matrix/`paramCode` combinations.
- [rd-bridge](https://github.com/Chili36/rd-bridge) is a derived, **non-official** bridge from EU residue definitions and their commodity scopes to EFSA PARAM codes, maintained with evidence and flags for uncertain links. Its `resolve` command takes a FoodEx2 code and a pesticide and returns the applicable definition and code, or the candidate definitions when the food cannot be placed in one Annex I commodity. Use it as a lookup aid; LL_04 validation against the Legal Limits database decides.
- Processed and composite foods may not map cleanly to one Annex I commodity. Do not guess the scope; check the candidates.

## Scope limits

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, pp. 143, 148 -->

- This page covers **pesticide** residue definitions under Regulation (EC) No 396/2005. Substances that are also veterinary medicines have separate VMPR marker residues; see [[vmpr-reporting]].
- It covers definitions and codes only, not MRL values or compliance evaluation; see [[ssd2-evaluation-limits]] and [[business-rules-legal-limits]].

## Relevant Business Rules

| Rule | How it constrains this topic |
|---|---|
| `LL_04` / `LL_04_b` (Error) | Sampled matrix and whole-residue `paramCode.base` must be a plausible legal combination in the Legal Limits database; part-of-sum results are exempt. |
| `LL_03` (Error) | `paramType` must be reported for multicomponent/sum parameters. |
| `LL_03_b` (Warning) | `paramType` should equal EFSA's pre-assigned value. |

## Relevant Policy

- The legislation decides; the Legal Limits database is EFSA's validation reference; rd-bridge is a derived helper. When they disagree, follow the legislation and report the discrepancy.
- A definition valid today may not be the one that applied to an older sample. Use the sampling date.
