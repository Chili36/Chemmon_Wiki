---
title: "Wiki Log"
last_updated: "2026-04-07"
---

# Log

## [2026-04-07] setup | Initial ChemMon wiki repo

- Created the ChemMon wiki repo following the LLM wiki pattern.
- Set up empty source and guidance directories.
- Added wiki API with a single Q&A endpoint at /wiki/ask.

## [2026-04-07] ingest | Initial ChemMon guidance compilation

- Created seven topic-oriented markdown pages under `raw/chemmon-guidance/` from the ChemMon 2026 reporting guidance and the SSD2 standard specification.
- Seeded pages for ChemMon overview, SSD2 data model, FoodEx2 in ChemMon, business rules (CHEMMON01-109), VMPR reporting, contaminant reporting, and food additives/flavourings reporting.
- Kept the source PDFs unchanged in `chemmon_docs/`.
- Updated `index.md` with the new page catalog.

## [2026-04-07] maintenance | Writing quality pass

- Fixed incorrect F27 description in foodex2-in-chemmon.md (was "brand or marketing type", should be "source commodity").
- Corrected CHEMMON100 and CHEMMON102 descriptions in vmpr-reporting.md to match the actual business rule definitions.
- Moved copper-specific F20 requirements from contaminant-reporting.md to a new pesticide-reporting.md page, since CHEMMON90_a/b are PPP-domain rules.
- Added pesticide-reporting.md covering legal references, sampling strategies, copper facet codes, and PPP-domain business rules.
- Added page number citations to contaminant-reporting.md source comments.
