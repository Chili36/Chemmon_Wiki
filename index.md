---
title: "Wiki Index"
last_updated: "2026-04-07"
---

# Index

This is the content-oriented catalog for the ChemMon reporting guidance wiki layer.

## Orientation

- [README.md](README.md): Repo overview, current status, directory layout, and working conventions.
- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md): What this wiki is for, why it exists, and the LLM-wiki operating model behind it.
- [log.md](log.md): Chronological record of ingests and maintenance work.

## Guiding Principles

- Chemical monitoring reporting follows EFSA's annual call for data and the associated guidance documents. Code and report samples according to the current year's guidance, not prior years.
- When the guidance is ambiguous, prefer the interpretation that maintains data quality and regulatory compliance over the one that is easier to implement.
- Business rules (CHEMMON01-CHEMMON109+) are the authoritative validation layer. If a business rule and a prose section of the guidance conflict, the business rule takes precedence.
- Reporting domains (chemical DCF, biological/zoonoses DCF) have specific routing rules. Not all parameters belong in the same domain.

## ChemMon Guidance

- [chemmon-overview.md](raw/chemmon-guidance/chemmon-overview.md): High-level explanation of ChemMon purpose, reporting domains, data submission cycle, and the role of business rules.
- [ssd2-data-model.md](raw/chemmon-guidance/ssd2-data-model.md): SSD2 logical model overview including main entities, element types, mandatory fields, and validation levels.
- [foodex2-in-chemmon.md](raw/chemmon-guidance/foodex2-in-chemmon.md): How FoodEx2 is used for matrix classification in ChemMon, mandatory facets by domain, and worked coding examples.
- [business-rules.md](raw/chemmon-guidance/business-rules.md): Comprehensive reference of GBR, CHEMMON01-CHEMMON109, and legal limit business rules with severities, domain applicability, and 2026 changes.
- [vmpr-reporting.md](raw/chemmon-guidance/vmpr-reporting.md): VMPR domain-specific rules including control plans, sampling strategies, FoodEx2 coding, result types, feed/water coding, processed products, wild game, and insects.
- [pesticide-reporting.md](raw/chemmon-guidance/pesticide-reporting.md): Pesticide residues domain rules including legal references, sampling strategies, and copper-specific F20 facet requirements.
- [contaminant-reporting.md](raw/chemmon-guidance/contaminant-reporting.md): Contaminant reporting rules covering acrylamide, dioxins/PCBs, BFRs, arsenic, chlorates, bisphenol, PAHs, 3-MCPDs, mineral oils, mycotoxins, and nitrates.
- [food-additives-reporting.md](raw/chemmon-guidance/food-additives-reporting.md): Food additives and flavourings reporting rules including mandatory F33, expression types, result reporting, restrictions/exceptions, conclusion reporting, and 2026 legal limit rules.
- [baby-food-reporting.md](raw/chemmon-guidance/baby-food-reporting.md): Baby food classification, VMPR exclusion rules (CHEMMON55/63), accepted domains, legal limits, and coding examples.

## Source Layer

- [chemmon_docs](chemmon_docs): Immutable EFSA PDF source collection used to build and verify the wiki.
