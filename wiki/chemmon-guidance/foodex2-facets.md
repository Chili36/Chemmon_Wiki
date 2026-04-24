---
title: "FoodEx2 Facet Reference (F01-F33)"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 43-51 (Table 4: FoodEx2 main facet descriptions and their relevance for each data domain)"
related:
  - "[[foodex2-in-chemmon]]"
  - "[[foodex2-facets-source-origin]]"
  - "[[foodex2-facets-state-process]]"
  - "[[foodex2-facets-packaging-consumer]]"
  - "[[foodex2-facets-legislative-descriptive]]"
  - "[[ssd2-elements-matrix]]"
  - "[[ssd2-matrix-vmpr-coding]]"
  - "[[vmpr-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
  - "[[business-rules-cross-cutting]]"
---

# FoodEx2 Facet Reference (F01-F33)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 43-51, Table 4 -->

## Overview

FoodEx2 sample matrix codes are built from a **base term** from the MTX catalogue plus optional **facets** that add descriptive attributes. Each facet has a code in the form `F<number>`. Relevance is domain-specific: the same facet may be mandatory, recommended, ignored, or business-rule controlled depending on whether the record is VMPR, pesticide, contaminant, additive, or flavouring.

This page is now a hub for Table 4. Use [[foodex2-in-chemmon]] for code syntax, implicit facets, and worked examples. Use the narrower facet-family pages below for actual domain guidance.

## Fast Routing

- Source, sampled part, ingredient, or source commodity questions: use [[foodex2-facets-source-origin]].
- Physical state, cooking, production method, or process questions: use [[foodex2-facets-state-process]].
- Packaging, target consumer, or part-consumed/analysed questions: use [[foodex2-facets-packaging-consumer]].
- Surrounding medium, fat/alcohol/qualitative descriptors, animal age/gender, or legislative classes: use [[foodex2-facets-legislative-descriptive]].

## Facet Families

| Page | Facets covered | Typical retrieval trigger |
| --- | --- | --- |
| [[foodex2-facets-source-origin]] | `F01`, `F02`, `F04`, `F27` | source animal/species, tissue, ingredient, source commodity, derivative origin |
| [[foodex2-facets-state-process]] | `F03`, `F17`, `F21`, `F28` | physical state, cooking, organic/conventional, wild game, processing |
| [[foodex2-facets-packaging-consumer]] | `F18`, `F19`, `F20`, `F23` | packaging format/material, visible fat/peel, target consumer, feed species |
| [[foodex2-facets-legislative-descriptive]] | `F06`, `F07`, `F10`, `F11`, `F31`, `F32`, `F33` | surrounding medium, fat/alcohol content, qualitative flags, age/gender, legislative class |

## High-Signal Business Rules

- `F33` legislative class is mandatory for acrylamide and FA/FF analytical records in specific ways. See [[foodex2-facets-legislative-descriptive]], [[business-rules-contaminant]], and [[business-rules-additives]].
- `F19` packaging material is mandatory for bisphenol compounds and recommended for PAHs. See [[foodex2-facets-packaging-consumer]] and [[business-rules-contaminant]].
- `F20` and/or `F28` are needed for pesticide copper sample-preparation detail. See [[foodex2-facets-packaging-consumer]], [[foodex2-facets-state-process]], and [[business-rules-pesticide]].
- `F23` is central for VMPR feed/water classification and FA/FF category 13 targeting. See [[foodex2-facets-packaging-consumer]], [[business-rules-vmpr]], and [[business-rules-additives]].
- `F21` organic/conventional and wild-game markers are domain-sensitive. See [[foodex2-facets-state-process]] and [[business-rules-cross-cutting]].

## Relevant Policy

- Keep this hub short. For prompt construction, retrieve this page only when a query asks generally about FoodEx2 facets or needs the routing map.
- For a concrete coding or validation question, prefer one of the narrower facet-family pages plus the relevant domain/business-rule page.
