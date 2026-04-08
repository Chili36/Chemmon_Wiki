---
title: "FoodEx2 in ChemMon"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[vmpr-reporting]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[baby-food-reporting]]"
  - "[[business-rules]]"
last_updated: "2026-04-07"
---

# FoodEx2 in ChemMon

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p33-40 -->
## How FoodEx2 Is Used

- The `sampMatCode` element in every [[chemmon-overview|ChemMon]] submission uses FoodEx2 to classify the sampled matrix. (ChemMon 2026 p33)
- Each code consists of a **mandatory base term** drawn from the MTX reporting hierarchy, optionally extended with **explicit facets** that add detail about source animal, part/nature, process, etc. (ChemMon 2026 p33-34)

## Code Syntax

FoodEx2 codes follow this pattern:

```
BaseTermCode#FacetHeader.FacetCode$FacetHeader.FacetCode
```

- `#` separates the base term from the first facet.
- `$` separates subsequent facets.
- Each facet is expressed as `FacetHeader.FacetCode` (e.g., `F01.A057` means facet group F01 with code A057). (ChemMon 2026 p34)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p34-37 -->
## Implicit vs Explicit Facets

- Many base terms carry **implicit facets** -- attributes already encoded in the term itself. For example, `A01YM` (pig kidney) implicitly carries F01.A057 (source = pigs) and F02.A069N (part-nature = kidney). (ChemMon 2026 p35)
- **Do not duplicate** an implicit facet as an explicit facet unless a specific business rule requires it. Redundant explicit facets trigger validation warnings. (ChemMon 2026 p35)
- Exception: business rule CHEMMON12 for acrylamide requires certain facets to be stated explicitly even when they are already implicit in the base term. See [[contaminant-reporting]] and [[business-rules]]. (ChemMon 2026 p36)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p36-39 -->
## Mandatory Facets by Domain

The table below summarises which facets are required, recommended, or not applicable for each reporting domain.

| Facet | VMPR | Pesticides | Contaminants | Additives | Flavourings |
| --- | --- | --- | --- | --- | --- |
| F01 Source | Always | Always | Always | Always | Always |
| F02 Part-nature | Always | Always | Always | Recommended | Recommended |
| F03 Physical state | -- | Recommended | Recommended | Recommended | Recommended |
| F21 Production method | Recommended | Required (see [[pesticide-reporting]]) | Required | -- | -- |
| F23 Target consumer | Mandatory for feed | -- | Recommended | Required for infant | Required for infant |
| F28 Process | Required | -- | Required | Required | Required |
| F33 Legislative classes | Required for processed (see [[vmpr-reporting]]) | -- | Required for acrylamide (see [[contaminant-reporting]]) | Mandatory (see [[food-additives-reporting]]) | Mandatory (see [[food-additives-reporting]]) |

(ChemMon 2026 p36-39)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p37-40 -->
## Worked Examples

### Pig kidney
- Code: `A01YM`
- F01.A057 (source = pigs) and F02.A069N (part-nature = kidney) are both **implicit** in the base term -- no explicit facets needed. (ChemMon 2026 p37)

### Sheep blood serum (non-food matrix)
- Code: `A0C60#F01.A0CDE$F02.A0CEY`
- Base term A0C60 is the generic non-food matrix; F01 and F02 are added explicitly to specify sheep and blood serum. (ChemMon 2026 p37)

### Infant formula
- Code: `A03QF#F28.A07HB$F18.A07NM$F19.A16RX`
- Process (F28), packaging type (F18), and packaging material (F19) are stated explicitly. See [[baby-food-reporting]] for baby food classification and domain routing. (ChemMon 2026 p38)

### Pasteurised eggs (organic)
- Code: `A031G#F21.A075E$F28.A07HV`
- F21 specifies organic production; F28 specifies pasteurisation. (ChemMon 2026 p38)

### Potato crisps
- Code: `A011L#F17.A07MY`
- F17 qualifies the cooking method. (ChemMon 2026 p38)

### Hemp seed flour
- Code: `A0F0N#F27.A016B`
- F27 specifies the source commodity (hemp seeds) from which this derivative was obtained. (ChemMon 2026 p39)

### Pizza (takeaway, laminated box)
- Code: `A03ZN#F18.A07NL$F19.A07PN`
- F18 and F19 capture the packaging format and material relevant for contaminant migration. (ChemMon 2026 p39)

### Cheese with legislative class
- Code: `A02RH#F03.A06JA$F33.A0C5F`
- F03 specifies the physical state; F33 captures the legislative classification. (ChemMon 2026 p39)
