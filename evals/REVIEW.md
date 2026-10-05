# Evaluation case review queue

All cases below are **draft**. A human reviewer should verify the source, accepted page alternatives, forbidden selections and answer rubric before setting `human-reviewed` and recording their name in `evals/cases.json`. No model output constitutes that approval.

## units-bin (development)

In SSD2, does GBR27 require resUnit when resType is BIN? What does GBR28 require?

Source: ChemMon 2026 Table 9 pp. 102–103

Expected page alternatives: [["business-rules-gbr.md", "ssd2-result-units-and-limits.md"]]

- State that GBR27 applies when resType differs from BIN.
- GBR28 requires resQualValue for BIN.
- Mention GBR29 if numeric limits are present; do not say BIN never needs units.

## vmpr-exception (development)

For VMPR reporting, do F01 and F02 always have to be supplied, including feed, water and processed food?

Source: ChemMon 2026 pp. 33–38

Expected page alternatives: [["ssd2-matrix-vmpr-coding.md", "vmpr-reporting.md"]]

- Do not make F01/F02 universal. Preserve feed/water and processed/composite exceptions.
- Do not confuse F01/F02 exceptions with absence of all matrix requirements.

## three-paths (development)

I have additive information from labels, laboratory results and manufacturers. Can I submit all three with the same data model?

Source: ChemMon 2026 and parallel guidance introductions; draft route classification needs human review

Expected page alternatives: [["food-additives-reporting.md"]]

- Distinguish SSD2 analytical results, no-presence collection and use-levels collection.
- Ask which type of record is being submitted if necessary; do not apply USE rules universally.

## pre-implicit (development)

For 2026 no-presence data, an implicit F33 is already present. Is another explicit F33 an Error?

Source: No-presence 2026 §2.7 pp. 7–8, Table 3 p. 21

Expected page alternatives: [["fa-ff-no-presence-data-model.md"]]

- Identify PRE15 as Warning; explicit F33 is not needed if implicit.
- Do not call it USE23 or a submission-blocking Error.

## use-implicit (development)

For 2026 use-level data, may I add an explicit F33 that is already implicit in matCode?

Source: Use-levels 2026 §2.7 pp. 7–8, Table 3 p. 27

Expected page alternatives: [["fa-ff-use-levels-data-model.md"]]

- USE23 prohibits the duplicate and is an Error.
- Keep matCode and use-level data distinct from sampMatCode/PRE15.

## ssd2-additive-implicit (development)

For 2026 analytical SSD2 food-additive results, what happens if I repeat the implicit F33?

Source: ChemMon 2026 Table 10 p. 141

Expected page alternatives: [["business-rules-additives.md", "food-additives-reporting.md"]]

- CHEMON109 (wiki CHEMMON109) is a Warning in 2026.
- Do not turn a possible 2027 change into the 2026 rule.

## pesticide-ll (development)

For a processed pesticide sample, do LL_01_PPP and LL_02_PPP apply in the same way as for an unprocessed sample?

Source: ChemMon 2026 Table 10 pp. 141–142

Expected page alternatives: [["business-rules-legal-limits.md"]]

- State that these rule definitions require an unprocessed sample.
- Preserve VAL and W002A-or-empty conditions; do not claim processing makes every legal obligation disappear.

## contaminant-action (development)

For a contaminant result with evalCode J003A in 2026, is omission of actTakenCode an Error under CHEMON37?

Source: ChemMon 2026 Table 10 p. 121

Expected page alternatives: [["business-rules-cross-cutting.md", "ssd2-evaluation-actions.md"]]

- CHEMON37 is a Warning, and actTakenCode should be reported.
- Do not transfer CHEMON85 VMPR/pesticide requirements to contaminants.

## ambiguous-facet (development)

Is F03 mandatory for my additive data?

Source: ChemMon 2026 pp. 38–39; No-presence/Use-levels §2.7 pp. 7–8

Expected page alternatives: [["food-additives-reporting.md"]]

- Request reporting path, category and whether F03 is implicit before a categorical answer.
- Distinguish SSD2 recommendations from PRE/USE conditional requirements.

## no-evidence (development)

What is the weather in Stockholm tomorrow?

Source: Out of scope of all four supplied source documents

Expected page alternatives: []

- Say the supplied evidence cannot answer; do not invent a weather forecast or cite a reporting page.

## uniqueness-key (held-out)

Does GBR101 reject any repeated paramCode and sampAnId, or can portions and Not in list change the outcome?

Source: ChemMon 2026 Table 9 p. 112

Expected page alternatives: [["business-rules-gbr.md"]]

- Include paramCode.base, sampId, sampAnId and anPortSeq in the uniqueness key.
- Preserve exception RF-XXXX-XXX-XXX.

## vmpr-feed-group (held-out)

Which F23 target-consumer code does the 2026 VMPR guidance use for sheep/goat feed?

Source: ChemMon 2026 p. 36; local catalogue query in reports/source-review

Expected page alternatives: [["ssd2-matrix-vmpr-coding.md"]]

- Report grouped code A07VF.
- If listing children, use A18ET, A18EV, A18EX and A18EY; do not repeat the PDF typo.
- Distinguish catalogue correction from original PDF wording.

## baby-vmpr (held-out)

Can a sample coded under baby-food A03PZ be reported with VMPR progLegalRef N371A?

Source: ChemMon 2026 Table 10 p. 129

Expected page alternatives: [["business-rules-baby-food.md", "baby-food-reporting.md"]]

- CHEMON63 excludes N371A for samples under A03PZ.
- Do not infer that all other collections exclude baby food.

## pre-report-year (held-out)

In the 2026 no-presence collection, what repYear and sampY should I report, and is repYear mandatory?

Source: No-presence 2026 §§2.5–2.6 p. 7, PRE01/16

Expected page alternatives: [["fa-ff-no-presence-data-model.md"]]

- repYear optional; if present 2026.
- sampY is mandatory and expected 2025 for this collection.
- Do not substitute USE marketing-year rules.

## use-date (held-out)

Why do use-level data need marketYear, marketMonth and marketDay rather than just a reporting year?

Source: Use-levels 2026 §§2.5–2.6 p. 7

Expected page alternatives: [["fa-ff-use-levels-data-model.md"]]

- All three marketing-date fields are mandatory.
- Explain legal-limit checks use the marketing date; repYear is the collection year.

## future-edition (held-out)

What changed in EFSA chemical-monitoring reporting for the 2028 collection?

Source: Corpus edition boundary; no 2028 source

Expected page alternatives: []

- State that the supplied 2026 sources do not establish 2028 rules.
- Do not present anticipated future transitions as verified 2028 guidance.
