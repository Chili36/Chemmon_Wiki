---
title: "SSD2 Analysis: Context and Portion Sequence"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 57-58 (Section 2, elements E.06, F.03, H.01)"
related:
  - "[[ssd2-elements-analysis]]"
  - "[[ssd2-elements-matrix]]"
  - "[[contaminant-reporting]]"
  - "[[business-rules-contaminant]]"
---

# SSD2 Analysis: Context and Portion Sequence

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 57-58 -->

## Rule Summary (Rule-First)

- `analysisY` is mandatory for every reported result.
- `origFishAreaCode` is a conditional field for fish, seafood, and marine-origin cases where FAO fishing area matters.
- `anPortSeq` is only for repeated analysis of the same sample with the same method under repeatable conditions; it should not be used as a general way to report multiple analytical runs.

## origFishAreaCode — Area of origin for fisheries or aquaculture

<!-- Source: ChemMon 2026 pp. 57-58 -->

**Element code:** E.06 · **Name:** `origFishAreaCode` · **Catalogue:** `FAREA` · **Status:** optional

### Purpose

For fish, seafood, and other marine products, report the FAO fishing area using the FAREA catalogue. This is mainly relevant where origin-area detail affects interpretation or downstream assessment. (ChemMon 2026 p57)

### Example

| Scenario | XML |
| --- | --- |
| Baltic herring from Skagerrak and Kattegat analysed for BFRs | `<origFishAreaCode>M27IIIa</origFishAreaCode>` |

When relevant, the result may also need the matching expression-basis information such as fat percentage. (ChemMon 2026 p57)

### Related business rule

- `CHEMMON20` — for fish matrices with BFRs, dioxins, or mercury, `origFishAreaCode` should be reported. See [[business-rules-contaminant]].

## analysisY — Year of analysis

<!-- Source: ChemMon 2026 p58 -->

**Element code:** F.03 · **Name:** `analysisY` · **Status:** mandatory

### Purpose

Report the four-digit year in which the analysis was performed. This field is mandatory for all results. (ChemMon 2026 p58)

## anPortSeq — Sample analysed portion sequence

<!-- Source: ChemMon 2026 p58 -->

**Element code:** H.01 · **Name:** `anPortSeq` · **Status:** optional

### Purpose

`anPortSeq` is the sequence number to use when the same laboratory sample is analysed more than once for the same substance under repeatable conditions. (ChemMon 2026 p58)

### When to use it

Use it only for repeated analysis of the same sample with the same method when the legal or technical workflow actually calls for multiple analysed portions, such as aflatoxin workflows in certain dried-fruit contexts. (ChemMon 2026 p58)

### When not to use it

Do not use `anPortSeq` when results are assessed against a legal limit in the ordinary sense. In those cases either:

- report the result from the most accurate/reliable analysis, or
- if equally accurate techniques were used, report the mean value instead

Counter-analyses and confirmation runs should also not be represented through `anPortSeq`; only the result that is actually evaluated should be reported. (ChemMon 2026 p58)
