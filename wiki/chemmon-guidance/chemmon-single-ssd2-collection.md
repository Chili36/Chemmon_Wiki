---
title: "ChemMon Single SSD2 Collection and Domain Routing"
type: "overview"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 8-9 (single SSD2 data collection, overlap handling, FCM exclusion)"
related:
  - "[[chemmon-background]]"
  - "[[chemmon-overview]]"
  - "[[ssd2-data-model]]"
  - "[[reporting-flags]]"
  - "[[ssd2-programme-legal-reference]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[business-rules]]"
  - "[[contaminant-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[vmpr-reporting]]"
---

# ChemMon Single SSD2 Collection and Domain Routing

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 8-9 -->

## Rule Summary

- ChemMon asks data providers to transmit all chemical monitoring data in SSD2 format.
- The single SSD2 mechanism reduces duplicate reporting and conflicting domain requirements.
- Domain inclusion is controlled mainly by `progLegalRef` and `paramCode`-driven flags.
- When a substance legitimately belongs to multiple domains, business rules from all applicable domains may apply.
- Food Contact Materials are no longer addressed in the 2026 ChemMon guidance.

## Why a Single SSD2 Data Collection

In 2013, EFSA published SSD2 as the data specification for submitting laboratory results in food-chain samples. SSD2 incorporates FoodEx2, a food classification system compatible with EU menu food consumption surveys. (ChemMon 2026 p8)

Data providers are now requested to transmit all chemical monitoring data in SSD2 format. This creates one mechanism for chemical monitoring data, reducing duplicate reporting and conflicting requirements while supporting compliance, exposure assessment, and potential scientific reuse. (ChemMon 2026 p8)

## Resolving Overlapping Domains

The inclusion of veterinary medicinal product residue data under Regulations (EU) 2022/1644 and 2022/1646 exposed a practical problem: the same substance can legitimately fall under more than one domain, creating uncertainty about where to submit the sample and risking duplicate reporting. (ChemMon 2026 p9)

The single collection addresses this with programme legal references and domain flags. `progLegalRef` selects data for inclusion in annual reports for European monitoring programmes, while `paramCode` and legal-reference attributes help determine which business rules and reports apply. See [[ssd2-programme-legal-reference]] and [[reporting-flags]]. (ChemMon 2026 p9)

When substances fall into more than one domain, business rules of all applicable domains are applied. A data element that is optional in general ChemMon transmissions can therefore become mandatory for a specific domain, legal framework, substance, or Table 8 case. See [[business-rules]] and the relevant domain rule slice. (ChemMon 2026 p9)

## Food Contact Materials Exclusion

The 2026 ChemMon guidance no longer addresses Food Contact Materials (FCM). FCM substances were part of the chemical contaminant domain in ChemMon 2022 and ChemMon 2023, but were removed from the 2026 guidance. (ChemMon 2026 p9)

## Navigation

- Use [[reporting-flags]] when the question is about domain inclusion or `VMPR` / `PEST` / `OCC` / `ADD` / `FLAV` flags.
- Use [[controlled-terminology-catalogues]] for the catalogue hierarchy and attribute layer that supports routing.
- Use [[chemmon-matrix-classification-algorithms]] when the routing question is specifically about FoodEx2 matrix grouping.
