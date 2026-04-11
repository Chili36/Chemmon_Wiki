---
title: "Wiki Index"
last_updated: "2026-04-11"
---

# Index

This is the content-oriented catalog for the ChemMon reporting guidance wiki layer.

## Orientation

- [README.md](README.md): Repo overview, current status, directory layout, and working conventions.
- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md): What this wiki is for, why it exists, and the LLM-wiki operating model behind it.
- [SCHEMA.md](SCHEMA.md): Page types, frontmatter fields, wiki-link convention, and source-comment convention. Required reading before editing any wiki page.
- [log.md](log.md): Chronological record of ingests and maintenance work.

## Guiding Principles

- Chemical monitoring reporting follows EFSA's annual call for data and the associated guidance documents. Code and report samples according to the current year's guidance, not prior years.
- When the guidance is ambiguous, prefer the interpretation that maintains data quality and regulatory compliance over the one that is easier to implement.
- Business rules (CHEMMON01-CHEMMON109+) are the authoritative validation layer. If a business rule and a prose section of the guidance conflict, the business rule takes precedence.
- Reporting domains (chemical DCF, biological/zoonoses DCF) have specific routing rules. Not all parameters belong in the same domain.

## ChemMon Guidance

### Overview & References

- [chemmon-overview.md](wiki/chemmon-guidance/chemmon-overview.md): High-level explanation of ChemMon purpose, reporting domains, data submission cycle, and the role of business rules.
- [chemmon-background.md](wiki/chemmon-guidance/chemmon-background.md): Background and rationale — why the single SSD2 data collection, resolving overlapping domains, FCM exclusion, compound element flexibility, Open Data and free-text reduction, revision cadence, meaning of 'residue'.
- [ssd2-data-model.md](wiki/chemmon-guidance/ssd2-data-model.md): SSD2 logical model overview including main entities, element types, mandatory fields, and validation levels.
- [foodex2-in-chemmon.md](wiki/chemmon-guidance/foodex2-in-chemmon.md): How FoodEx2 is used for matrix classification in ChemMon, mandatory facets by domain, and worked coding examples.
- [foodex2-facets.md](wiki/chemmon-guidance/foodex2-facets.md): Full F01-F33 facet reference — per-domain descriptions of each FoodEx2 facet drawn from Table 4 of the source guidance.
- [controlled-terminology-catalogues.md](wiki/chemmon-guidance/controlled-terminology-catalogues.md): Which EFSA catalogues/hierarchies ChemMon uses (LEGREF, PARAM, MTX, UNIT, etc.) and how they drive validation and domain routing.
- [reporting-flags.md](wiki/chemmon-guidance/reporting-flags.md): How EFSA sets the five domain flags (0-3 values) from `progLegalRef` and `paramCode`, and how flags drive business-rule applicability and reports.
- [legal-limits-database.md](wiki/chemmon-guidance/legal-limits-database.md): EFSA Legal Limits Database for MRL evaluation: what it covers, sampling-date applicability, and relationship to legal-limit rules.
- [chemmon-matrix-classification-algorithms.md](wiki/chemmon-guidance/chemmon-matrix-classification-algorithms.md): Where EFSA’s VMPR/pesticide matrix-classification algorithms live and how FoodEx2 `sampMatCode` is grouped for reporting.
- [chemmon-reports.md](wiki/chemmon-guidance/chemmon-reports.md): Which validation dashboards, national reports, EU annual reports, and AROC extracts are produced, and which domain flags are included.
- [data-validation-and-acceptance.md](wiki/chemmon-guidance/data-validation-and-acceptance.md): DCF lifecycle: ack/ack-details, business-rule validation statuses, submit/accept/reject, and post-acceptance update procedure.

### SSD2 Element Reference

Per-element reference pages covering the ~88 SSD2 elements required for ChemMon submissions. Start at the element group that matches your question; the pages cross-link to the relevant business rules.

- [ssd2-elements-programme.md](wiki/chemmon-guidance/ssd2-elements-programme.md): Programme group — `progId`, `progLegalRef`, `sampStrategy`, `progType` plus Table 2 valid combinations across all domains.
- [ssd2-elements-sampling.md](wiki/chemmon-guidance/ssd2-elements-sampling.md): Sampling group — `sampMethod`, `sampler`, `sampPoint`, `sampEventId`, `sampUnitType`, `sampUnitSize`, `sampId`, `sampCountry`, sampling date, `origSampId`.
- [ssd2-elements-matrix.md](wiki/chemmon-guidance/ssd2-elements-matrix.md): Matrix group — `sampMatCode` (with VMPR/feed/non-food/insects coding), `sampMatText`, `origCountry`, `sampAnId`, `anMatCode`, `anMatText`.
- [ssd2-elements-analysis.md](wiki/chemmon-guidance/ssd2-elements-analysis.md): Analysis / laboratory / parameter / method — `origFishAreaCode`, `analysisY`, `anPortSeq`, `labId`, `labAccred`, `labCountry`, `paramType`, `paramCode`, `paramText`, `anMethRefId`, `anMethType`, `anMethCode`.
- [ssd2-elements-result.md](wiki/chemmon-guidance/ssd2-elements-result.md): Result group — `resId`, `accredProc`, `resUnit`, `resLOD`, `resLOQ`, `CCalpha`, `CCbeta`, `resVal`, recovery, expression of results, `resQualValue`, `resType`, `resValUncert`, `resInfo.notSummed`.
- [ssd2-elements-evaluation.md](wiki/chemmon-guidance/ssd2-elements-evaluation.md): Evaluation group — `evalLowLimit`, `evalLimitType`, `evalCode`, `actTakenCode`, `evalInfo.conclusion`, `evalInfo.com`.

### Domain Guides

- [vmpr-reporting.md](wiki/chemmon-guidance/vmpr-reporting.md): VMPR domain-specific rules including control plans, sampling strategies, FoodEx2 coding, result types, feed/water coding, processed products, wild game, and insects.
- [pesticide-reporting.md](wiki/chemmon-guidance/pesticide-reporting.md): Pesticide residues domain rules including legal references, sampling strategies, and copper-specific F20 facet requirements.
- [contaminant-reporting.md](wiki/chemmon-guidance/contaminant-reporting.md): Contaminant reporting rules covering acrylamide, dioxins/PCBs, BFRs, arsenic, chlorates, bisphenol, PAHs, 3-MCPDs, mineral oils, mycotoxins, and nitrates.
- [food-additives-reporting.md](wiki/chemmon-guidance/food-additives-reporting.md): Food additives and flavourings reporting rules including mandatory F33, expression types, result reporting, restrictions/exceptions, conclusion reporting, and 2026 legal limit rules.
- [baby-food-reporting.md](wiki/chemmon-guidance/baby-food-reporting.md): Baby food classification, VMPR exclusion rules (CHEMMON55/63), accepted domains, legal limits, and coding examples.

### Business Rules

The full 131-rule catalog is sliced into nine files by applicability. Start at the hub if you're unsure which slice to open; otherwise jump directly to the relevant domain or tier.

- [business-rules.md](wiki/chemmon-guidance/business-rules.md): **Hub** — explains the three groups of business rules (GBR/CHEMMON/subset-specific) and links to the nine slice files by domain/tier.
- [business-rules-gbr.md](wiki/chemmon-guidance/business-rules-gbr.md): General Business Rules (16 rules) applying across all EFSA SSD2 data collections — sampling event consistency, geographic validation, result value/unit rules.
- [business-rules-cross-cutting.md](wiki/chemmon-guidance/business-rules-cross-cutting.md): CHEMMON rules (46 rules) marked "All" or applying to multiple domains — analytical method, result value & type, sampling & programme, cross-domain matrix, evaluation & action, FoodEx2 validation.
- [business-rules-vmpr.md](wiki/chemmon-guidance/business-rules-vmpr.md): VMPR-specific rules (11 CHEMMON rules) — accreditation, species/breed consistency, VMPR evaluation codes, 2026 geographic consistency.
- [business-rules-pesticide.md](wiki/chemmon-guidance/business-rules-pesticide.md): Pesticide-specific rules (14 CHEMMON rules) — country of sampling, expression of results, copper facets, non-compliant origin, 2026 N422A exclusivity.
- [business-rules-contaminant.md](wiki/chemmon-guidance/business-rules-contaminant.md): Contaminant-specific rules (19 CHEMMON rules) — dioxin/PCB congeners, matrix facets (acrylamide, bisphenol, PAHs, arsenic, BFRs, mycotoxins), feed expression.
- [business-rules-additives.md](wiki/chemmon-guidance/business-rules-additives.md): Food additives & flavourings rules (12 CHEMMON rules) — F33 legislative classes, expression type, physical state, 2026 substance-specific requirements.
- [business-rules-baby-food.md](wiki/chemmon-guidance/business-rules-baby-food.md): Baby food exclusion rules (CHEMMON55, CHEMMON63) — matrix coding consistency for baby food programmes and VMPR legal framework exclusion.
- [business-rules-legal-limits.md](wiki/chemmon-guidance/business-rules-legal-limits.md): Legal Limit rules (11 rules) comparing reported values to MRLs/MLs/MPLs across VMPR, pesticide, and food additive domains.
- [business-rules-2026-changes.md](wiki/chemmon-guidance/business-rules-2026-changes.md): Reference log of amended, merged, new, and deactivated rules for the 2026 data collection.

## Source Layer

- [chemmon_docs](chemmon_docs): Immutable EFSA PDF source collection used to build and verify the wiki.
