---
title: "Controlled Terminology Catalogues"
type: "reference"
domain: "all"
last_updated: "2026-11-12"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
source_pages:
  - "ChemMon 2026 pp. 144-147 (Section 7; Table 11; Table 12 guidance text p. 147); ChemMon 2026 pp. 78-79 (N.06.4); ChemMon 2026 pp. 80-84 (Table 7); ChemMon 2026 p. 71 (M.16); Use-levels 2026 pp. 11-12, 16 (YESNO fields); No-presence 2026 p. 11 (presenceAdded); No-presence 2026 Table 1 pp. 15-16; No-presence 2026 Table 2 pp. 17-18; No-presence 2026 Table 3 pp. 19-20; Use-levels 2026 pp. 13-14 (presenceAdded, weight); Use-levels 2026 Table 1 pp. 19-21; Use-levels 2026 Table 2 pp. 22-23; Use-levels 2026 Table 3 pp. 24-25"
related:
  - "[[chemmon-data-governance-and-transparency]]"
  - "[[chemmon-change-management]]"
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-programme-legal-reference]]"
  - "[[ssd2-programme-strategy-and-type]]"
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-matrix-sampled-matrix]]"
  - "[[ssd2-analysis-parameter-coding]]"
  - "[[ssd2-evaluation-conclusions]]"
  - "[[reporting-flags]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[fa-ff-no-presence-data-model]]"
  - "[[fa-ff-use-levels-data-model]]"
---

# Controlled Terminology Catalogues

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Section 7 -->

## Overview

ChemMon submissions use EFSA **controlled terminologies** (catalogues): code lists (and their hierarchies) that constrain allowed values for many SSD2 elements (e.g. `progLegalRef`, `paramCode`, `resUnit`). EFSA publishes these catalogues for reference and download via Knowledge Junction / Zenodo. The background rationale for catalogue mapping and machine-readable resources is in [[chemmon-data-governance-and-transparency]]. (ChemMon 2026 p144)

## How catalogues are used in validation

<!-- Source: ChemMon 2026 pp. 144-145 (Table 11 notes) -->

- Every reported code is validated against a **reporting hierarchy** for its catalogue.
- Some catalogues also define one or more **analysis hierarchies** used for legislative/reporting groupings; values in analysis hierarchies are also present in the catalogue’s reporting hierarchy.
- Some “hierarchies” used for reporting are dedicated catalogues derived from MTX (FoodEx2), used for legislative mapping (e.g. VMPR matrix classes and pesticide MATRIX groupings). (ChemMon 2026 pp. 144-145)

## All catalogues and hierarchies (Table 11)

<!-- Source: ChemMon 2026 pp. 144-145 (Table 11); SSD2 elements from Table 7 (docs/ssd2-elements.json) -->

\*, \*\*, \*\*\*: the three validation notes above (reporting hierarchy, analysis hierarchies, MTX-derived catalogues) (ChemMon 2026 pp. 144-145). The SSD2 elements column comes from Table 7 (ChemMon 2026 pp. 80-84).

| Catalogue | Reporting hierarchy\* | Analysis hierarchies\*\* | SSD2 elements (Table 7) | Notes |
| --- | --- | --- | --- | --- |
| `ACTION` | Master hierarchy | Not applicable | `actTakenCode` |  |
| `ADDFOOD` | Master hierarchy | `FARestExc` and `FFRestExc` | `evalInfo.restrictionException` | ChemMon: the element is optional and codes are selected from ADDFOOD; `ADD00881A` is the example for "No restrictions/exceptions to be reported" (ChemMon 2026 pp. 78-79). FA/FF parallel DMs: `FARestExc` must be used with `progLegalRef=N112A` and `FFRestExc` with `progLegalRef=N113A`, and `ADD00881A` must be selected when nothing applies (No-presence 2026 p19, PRE03/PRE04; Use-levels 2026 p24, USE04/USE05). |
| `ANLYMD` | Master hierarchy | Not applicable | `anMethCode` |  |
| `ANLYREFMD` | Master hierarchy | Not applicable | `anMethRefCode` |  |
| `ANLYTYP` | Master hierarchy | Not applicable | `anMethType` |  |
| `CONCLUS` | Master hierarchy | `faff` (food additives and food flavourings) | `evalInfo.conclusion` | Codes and FA/FF usage: see the FA/FF table below and [[ssd2-evaluation-conclusions]]. |
| `COUNTRY` | Master hierarchy | Master hierarchy | `localOrgCountry`, `repCountry`, `sampCountry`, `origCountry`, `procCountry`, `labCountry` |  |
| `EXPRRES` | Master hierarchy | Not applicable | `exprResType` |  |
| `FAREA` | Master hierarchy | Not applicable | `origFishAreaCode` |  |
| `LABACC` | Master hierarchy | Not applicable | `labAccred` |  |
| `LEGREF` | `ChemMonLegref` (printed so; p. 147 and p. 149 write `ChemMonLegRef`) | See Table 12 on [[ssd2-programme-legal-reference]] for domain applicability | `progLegalRef` | Domain attributes `VMPR`, `PEST`, `OCC`, `ADD`, `FLAV` drive the domain flags. The FA/FF parallel DMs use the sub-hierarchy **`faff`** directly (only `N112A` and `N113A` allowed). See [[reporting-flags]]. |
| `LMTTYP` | Master hierarchy | Not applicable | `evalLimitType` |  |
| `MDACC` | Master hierarchy | Not applicable | `accredProc` |  |
| `MTX` | Reporting hierarchy; use food, feed or non-food matrices as applicable | `MTXCLS` – `vmprCls` (VMPR)\*\*\*; `MATRIX` (pesticide residues)\*\*\* | `sampMatCode`, `anMatCode` | Also `matCode` in the use-levels DM. Legislative mappings derived from MTX: [[chemmon-matrix-classification-algorithms]]; SSD2 matrix behaviour: [[ssd2-matrix-sampled-matrix]]. |
| `NUTS` | `NUTS2024` | Not applicable | `sampArea`, `origArea`, `procArea` |  |
| `PARAM` | `ChemMonRep` | `addAnalysis`, `flavAnalysis`, `chemAnalysis`, `pestParam`, `vmprParam` | `isolParamCode`, `paramCode` | `addAnalysis` = FA, `flavAnalysis` = FF. See [[ssd2-analysis-parameter-coding]] and [[reporting-flags]]. |
| `PARAMTYP` | Master hierarchy | Master hierarchy | `paramType` |  |
| `POSNEG` | Master hierarchy | Not applicable | `resQualValue` |  |
| `PRGTYP` | Master hierarchy | Not applicable | `progType` |  |
| `REFTM` | Master hierarchy | Not applicable | `sampAnRefTime` |  |
| `RESEVAL` | Master hierarchy | Not applicable | `evalCode`, `evalInfo.resAsses` |  |
| `SAMPLR` | Master hierarchy | Not applicable | `sampler` |  |
| `SAMPMD` | Master hierarchy | Not applicable | `sampMethod` |  |
| `SAMPNT` | Master hierarchy | `vmprClasses` (VMPR) | `sampPoint` |  |
| `SAMPSTR` | `chemSampStr` | Not applicable | `sampStrategy` | See [[ssd2-programme-strategy-and-type]]. |
| `SAMPUNTYP` | Master hierarchy | Not applicable | `sampUnitType` |  |
| `UNIT` | `chemUnit` | Not applicable | `sampUnitSizeUnit`, `sampSizeUnit`, `anPortSizeUnit`, `resUnit` | Also `unit` in the use-levels DM. |
| `VALTYP` | `chemValTyp` | Not applicable | `resType` | "The resType indicates the type of analytical result obtained for a substance in a product", e.g. `VAL` (M.16, ChemMon 2026 p71). |
| `YESNO` | Master hierarchy | Not applicable | `resValRecCorr` |  |

## Catalogue usages surfaced by the FA/FF parallel data models

<!-- Source: No-presence 2026 p11, Table 1 pp. 15-16, Table 2 pp. 17-18; Use-levels 2026 pp. 13-14, Table 1 pp. 19-21, Table 2 pp. 22-23; ChemMon 2026 pp. 76, 144 -->

The [[fa-ff-no-presence-data-model]] and [[fa-ff-use-levels-data-model]] make some catalogue usages more explicit than the ordinary SSD2 analytical path. Some are shared with SSD2 analytical reporting, while others are specific to the parallel FA/FF data models:

| Catalogue | Where it shows up | Hierarchy / usage |
| --- | --- | --- |
| `CONCLUS` | `presenceAdded` (both FA/FF DMs); `evalInfo.conclusion` on SSD2 analytical submissions | Source discrepancy (hierarchy spelling): both parallel guides print **`faff`** (No-presence p11; Use-levels p13, Table 1 p20) and so does ChemMon Table 11 (p. 144); only ChemMon p. 76 prints **`fa_ff`**. The matching codes/labels establish the same concept family; this is a documentation naming discrepancy, not proof that software accepts both hierarchy identifiers. Codes: `C19A` (Yes, present on label/added), `C20A` (No, not present on label/not added), `C05A` (Natural occurrence). No-presence DM accepts `C20A` only; use-levels DM accepts all three plus combinations like `C19A$C05A`; SSD2 analytical additives/flavourings use the same named conclusion codes in `evalInfo.conclusion`. See [[ssd2-evaluation-conclusions]]. |
| `FUNC` | `functionOf` (both FA/FF DMs) | Functional class of the food additive. Table 2 of each guide lists 33 classes: 27 with a description (1 sweeteners, 2 colours, 3 preservatives, 4 antioxidants, 5 carriers, 6 acids, … 27 contrast enhancers), 28 "nutrient" (no description), and five "Annex III" classes (29-33). (No-presence 2026 pp. 17-18; Use-levels 2026 pp. 22-23) `functionOf` must be reported when `progLegalRef=N112A` in the parallel DMs (No-presence 2026 p20, PRE07; Use-levels 2026 p25, USE10). |
| `EXPRRES` | `weight` (use-levels DM only) | Hierarchy: **`WDFat`** — whole weight / dry matter / fat weight. Drives whether `fatPerc` or `moistPerc` must also be reported. (Use-levels 2026 pp. 14-15, 20) |
| `YESNO` | `foodIndustry`, `widelyConsumed`, `maxPermittedLevelDefined` (use-levels DM) | Codes `Y` / `N`. For `maxPermittedLevelDefined`, "The only codes that can be used are ‘Y’ or ‘N’" (Use-levels 2026 p16; USE14, p25). `widelyConsumed`: `Y` for widely consumed products, `N` otherwise (Use-levels 2026 p12). `foodIndustry`: Yes = food industry, No = food additive/flavouring producer (Use-levels 2026 p11). The guidance does not list the catalogue's full content. |

The FA/FF parallel DMs have their own field types, catalogue restrictions and `PRE…` / `USE…` / `USE_LLDB…` rules. Some field constraints have no separate rule ID; the rule-ID list does not replace Table 1 or the field sections. See the DM pages for the rule tables.

## Choosing `progLegalRef` (LEGREF) for correct reuse

<!-- Source: ChemMon 2026 p. 147; Table 12 itself is on [[ssd2-programme-legal-reference]] -->

- Use the **most specific** LEGREF term available, to ensure correct inclusion in the intended reports and downstream reuse.
- Reporting the generic term `N129A` (Regulation (EC) No 178/2002) will still flag records for occurrence-style reuse (see [[reporting-flags]]), but may not align with inclusion criteria for the statutory EU Annual Reports. (ChemMon 2026 p147)
- If a needed piece of legislation is missing from `LEGREF` / `ChemMonLegRef`, data providers should contact EFSA with a suggested new term "during the major release consultation period in October–November each year or, if there is an urgent unpredicted need, at any other time". (ChemMon 2026 p147)
