---
title: "ChemMon Single SSD2 Collection and Domain Routing"
select_when: "Routing one SSD2 submission across chemical domains using legal reference and parameter; distinguish reporting flags from separate FA/FF data collections."
type: "overview"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 8-9 (single SSD2 data collection, overlap handling, FCM exclusion)"
  - "p. 148 (Section 9, reporting flags)"
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
- When a substance legitimately belongs to multiple domains, business rules of all applicable domains are applied.
- The 2026 ChemMon guidance no longer addresses the specific reporting requirements and analysis hierarchies for Food Contact Materials (FCM) substances.

## Why a Single SSD2 Data Collection

In 2013, EFSA published SSD2 as the data specification for submitting laboratory results in food-chain samples. SSD2 incorporates FoodEx2, a food classification system compatible with EU menu food consumption surveys. (ChemMon 2026 p8)

Data providers are now requested to transmit all chemical monitoring data in SSD2 format. This creates one mechanism for chemical monitoring data, reducing duplicate reporting and conflicting requirements while supporting compliance, exposure assessment, and potential scientific reuse. (ChemMon 2026 p8)

## Resolving Overlapping Domains

The inclusion of veterinary medicinal product residue data under Regulations (EU) 2022/1644 and 2022/1646 exposed a practical problem: the same substance can legitimately fall under more than one domain, creating uncertainty about where to submit the sample and risking duplicate reporting. (ChemMon 2026 p8)

In the single collection, the results for National and Annual Reports are selected using specific analysis hierarchies for each domain, applied to the PARAM and MTX catalogues "plus other catalogues where necessary"; a programme legal reference (`progLegalRef`) is also required to select data for inclusion in the Annual Reports for European monitoring programmes. (ChemMon 2026 pp. 8-9) EFSA also stores five domain flags for each result record, based on `paramCode` and `progLegalRef`, which are used so that specific business rules apply only to the records they are relevant for. (ChemMon 2026 p148) See [[ssd2-programme-legal-reference]] and [[reporting-flags]].

When substances fall into more than one domain, business rules of all applicable domains are applied. A data element defined as optional for ChemMon transmissions in general can still be mandatory for a specific domain or substance, as defined in the specific business rule and detailed in Table 8. See [[business-rules]] and the relevant domain rule slice. (ChemMon 2026 p9)

## Food Contact Materials Exclusion

The 2026 ChemMon guidance no longer addresses the specific reporting requirements and analysis hierarchies for Food Contact Materials (FCM) substances, which belonged to the chemical contaminant domain in ChemMon 2022 and ChemMon 2023. (ChemMon 2026 p9)

## Navigation

- Use [[reporting-flags]] when the question is about domain inclusion or `VMPR` / `PEST` / `OCC` / `ADD` / `FLAV` flags.
- Use [[controlled-terminology-catalogues]] for the catalogue hierarchy and attribute layer that supports routing.
- Use [[chemmon-matrix-classification-algorithms]] when the routing question is specifically about FoodEx2 matrix grouping.
