---
title: "SSD2 Analysis: Context and Portion Sequence"
type: "reference"
domain: "all"
last_updated: "2026-11-11"
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
- `origFishAreaCode` is optional; for fish, seafood and other marine products the FAO fishing area should be reported.
- `anPortSeq` should only be used for repeated analysis of the same sample with the same method under repeatable conditions, and only when legally required.

## origFishAreaCode — Area of origin for fisheries or aquaculture

<!-- Source: ChemMon 2026 pp. 57-58 -->

**Element code:** E.06 · **Name:** `origFishAreaCode` · **Catalogue:** `FAREA` · **Status:** optional

### Purpose

For fish, seafood and other marine products the Food and Agriculture Organization (FAO) fishing area should be reported. Codes can be selected from the FAREA catalogue. (ChemMon 2026 p57)

### When the fishing area is unknown

For fish analysed for brominated flame retardants, dioxins and PCBs, or mercury, Table 8 recommends specifying the area of origin. When the specific area is not available, report `origFishAreaCode` = `M99` (Unknown) and, as a minimum, give the fish's original environment (`from freshwater` or `from saltwater`) in `origFishAreaText` (E.07). See [[contaminant-reporting]]. (ChemMon 2026 Table 8 pp. 86, 95)

### Example

| Scenario | XML |
| --- | --- |
| Baltic herring caught in Skagerrak and Kattegat tested for brominated flame retardants | `<origFishAreaCode>M27IIIa</origFishAreaCode>` `<exprResPerc>fatPerc=45</exprResPerc>` `<exprResType>B003A</exprResType>` |

In this case the percentage fat should always be reported, and results are reported for each congener. (ChemMon 2026 p58)

### Related business rule

- `CHEMON20` — for fish matrices with BFRs, dioxins, or mercury, `origFishAreaCode` should be reported. See [[business-rules-contaminant]].

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

`anPortSeq` should only be used for repeated analysis of the same sample with the same method (i.e. under repeatable conditions) and only when legally required, e.g. aflatoxins in dried fruits, where three laboratory samples belonging to the same original sample must be analysed according to Regulation (EU) 2023/2782. Example: `<anPortSeq>1</anPortSeq>` for each portion into which the laboratory sample is divided and analysed for aflatoxins. (ChemMon 2026 p58)

### When not to use it

If different methods are used for the same sample and parameter, only the most accurate and reliable result should be reported (irrespective of the existence of a legal limit). (ChemMon 2026 p58)

When reporting results which are subject to assessment against a legal limit, `anPortSeq` must not be used. Either:

- the result derived with the most accurate or reliable analysis must be reported, or
- when samples were analysed with equally accurate techniques, the mean value should be reported; in that case the date of the last component result and the most applicable analytical method should be reported. (ChemMon 2026 p58)

**Source discrepancy:** p. 58 says `anPortSeq` must not be used for results subject to assessment against a legal limit, yet the same section gives aflatoxins in dried fruits under Regulation (EU) 2023/2782 as the case where it is legally required. The guidance does not reconcile the two statements.

Where the sample taken is analysed more than once for the same parameter as a counter-analysis or to confirm a positive sample, the only result to be reported is the one for which the evaluation is performed, and the sample analysed portion should not be used. (ChemMon 2026 p58)
