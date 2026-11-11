---
title: "FoodEx2 in ChemMon"
type: "reference"
domain: "all"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
  - "EFSA Journal - 2013 -  - Standard Sample Description ver  2 0 (2).pdf"
source_pages:
  - "ChemMon 2026 pp. 32-33 (Section 2, E.02 sampMatCode)"
  - "ChemMon 2026 pp. 38-39, 42 (FA/FF coding; F33 for acrylamide and FA/FF)"
  - "ChemMon 2026 pp. 43-51 (Table 4)"
  - "ChemMon 2026 pp. 52-55 (sampMatCode examples)"
  - "ChemMon 2026 pp. 115, 141 (Table 10: CHEMON12, CHEMON109)"
  - "SSD2 p. 10 (compound element syntax)"
  - "No-presence p. 9 and use-levels p. 9 (soft-ripened cheese example)"
related:
  - "[[chemmon-overview]]"
  - "[[foodex2-facets]]"
  - "[[foodex2-facets-source-origin]]"
  - "[[foodex2-facets-state-process]]"
  - "[[foodex2-facets-packaging-consumer]]"
  - "[[foodex2-facets-legislative-descriptive]]"
  - "[[vmpr-reporting]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
  - "[[pesticide-reporting]]"
  - "[[baby-food-reporting]]"
  - "[[business-rules]]"
last_updated: "2026-11-11"
---

# FoodEx2 in ChemMon

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p32-33 -->
## How FoodEx2 Is Used

- The mandatory `sampMatCode` element (E.02) in a [[chemmon-overview|ChemMon]] submission uses FoodEx2 to describe the sampled matrix. (ChemMon 2026 p32)
- A **base term** must always be supplied; it is selected from the MTX catalogue reporting hierarchy. **Explicit facets** can be added for detail such as source animal, part/nature or process. (ChemMon 2026 p32-33)

## Code Syntax

FoodEx2 codes follow this pattern:

```
BaseTermCode#FacetHeader.FacetCode$FacetHeader.FacetCode
```

- `#` separates the base term from the first facet.
- `$` separates subsequent facets.
- Each facet is expressed as `FacetHeader.FacetCode`. SSD2 gives the pattern `baseTerm#facet1=value1$...$facetN=valueN` and the example `A01TX#F01.A057E$F02.A069J`. (SSD2 p10)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p33, p42, p52, p115, p141 -->
## Implicit vs Explicit Facets

- Many base terms carry **implicit facets** -- attributes already encoded in the term itself. For example, `A01YM` (pig kidney) implicitly carries F01.A057 (source = pigs) and F02.A069N (part-nature = kidney). (ChemMon 2026 p52)
- If the implicit facets are enough to characterise the matrix, only the base term needs to be reported. Where the base term has implicit facets, explicit facets should only be additional ones not already covered by the implicit facets. (ChemMon 2026 p33)
- The guidance has one validation rule on a duplicated facet: if `sampMatCode` already contains an implicit FA/FF legislative category (F33), the explicit F33 is not needed, and reporting it returns a Warning. See [[business-rules-additives]]. (ChemMon 2026 p141)
- For acrylamide, the explicit facet F33 Legislative classes must be reported; the corresponding rule requires `sampMatCode.legis` to be reported and returns an Error. See [[contaminant-reporting]] and [[business-rules-contaminant]]. (ChemMon 2026 p42, p115)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p43-51 (Table 4), with prose from p33, p38-39 -->
## Mandatory Facets by Domain

The table below restates Table 4 for the facets asked about most often, using the table's own wording for requirement strength. "—" means the Table 4 cell is empty. For the other facets and the full cell text, use the narrow facet references: [[foodex2-facets-source-origin]], [[foodex2-facets-state-process]], [[foodex2-facets-packaging-consumer]], and [[foodex2-facets-legislative-descriptive]].

| Facet | VMPR | Pesticides | Contaminants | Additives | Flavourings |
| --- | --- | --- | --- | --- | --- |
| F01 Source | Indicates the animal species sampled; important to select species level or lower | — | Origin of the raw commodity; usually already an implicit facet | Source of the raw agricultural commodity; species must be specified for fish/seafood and for algae-based products | Same as additives |
| F02 Part-nature | Must be reported (the MRL depends on the target tissue) | Part sampled, e.g. fat samples from animals | Part sampled | Part sampled | Part sampled |
| F03 Physical state | — | — | For reporting the physical state | For reporting the physical state | For reporting the physical state |
| F21 Production method | `A07RY` should be used to identify wild game | Required for the organic vs conventional analysis | Recommended; required for the mycotoxin organic vs non-organic analysis | — | — |
| F23 Target consumer | Must be used for feed samples if not already implicit | Must be used for feed samples if not already implicit | Must be used for feed samples if not already implicit; can also indicate the age of the human consumer | Same as contaminants | Same as contaminants |
| F28 Process | Required to distinguish processed food samples | Required to distinguish processed food samples | Required to distinguish processed food samples | Required to distinguish processed food samples | Required to distinguish processed food samples |
| F33 Legislative classes | Required for processed products (see [[vmpr-reporting]]) | — | Required for samples analysed for acrylamide (see [[contaminant-reporting]]) | Required (see [[food-additives-reporting]]) | "Recommended" in Table 4, but mandatory in the prose and in validation; see the Source discrepancy note in [[foodex2-facets-legislative-descriptive]] |

(ChemMon 2026 pp. 43-51)

Requirements stated in the prose rather than in Table 4:

- VMPR: F01 and F02 must always be present, except for the special feed, water and processed-composite cases; an implicit facet satisfies this without being repeated explicitly. Use [[ssd2-matrix-vmpr-coding]] and [[vmpr-reporting]]. (ChemMon 2026 p33)
- VMPR wild animals: `A07RY` from F21 must always be added to the base term as an explicit facet. (ChemMon 2026 p33)
- Additives and flavourings: F33 must always be present; if it is not implicitly assigned it must be added explicitly. (ChemMon 2026 p38)
- Additives and flavourings: F03 should be considered for the legislative categories listed on p. 38 and, if not implicitly assigned, is highly recommended to be added. If the sample is formulated for infants (<12 months), F23 should be added if it is not implicitly assigned. (ChemMon 2026 p38-39)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p52-55 -->
## Worked Examples

### Pig kidney
- Code: `A01YM`
- F01.A057 (source = pigs) and F02.A069N (part-nature = kidney) are both **implicit** in the base term -- no explicit facets needed. (ChemMon 2026 p52)

### Sheep blood serum (non-food matrix)
- Code: `A0C60#F01.A0CDE$F02.A0CEY`
- Base term A0C60 is the generic non-food animal-related matrix; F01 (sheep for meat production) and F02 (blood serum) are added explicitly. (ChemMon 2026 p52)

### Infant formula
- Code: `A03QF#F28.A07HB$F18.A07NM$F19.A16RX`
- Infant formula based on milk, heated in the microwave inside a plastic feeding bottle: process (F28 = microwave-cooking), packaging format (F18 = bottle) and packaging material (F19 = polypropylene) are stated explicitly. See [[baby-food-reporting]] for baby food classification and domain routing. (ChemMon 2026 p55)

### Pasteurised eggs (organic)
- Code: `A031G#F21.A07SE$F28.A07HV`
- F21.A07SE specifies organic production; F28.A07HV specifies pasteurisation. (ChemMon 2026 p52)

### Potato crisps
- Code: `A011L#F17.A07MY`
- Acrylamide category 2: indicate whether batch fried or continuously fried. F17.A07MY = outside light brown. (ChemMon 2026 p52-53)

### Hemp seed flour
- Code: `A0F0N#F27.A016B`
- Base term A0F0N (dried nuts/seeds and related flours and powders) with F27 naming the source commodity, hemp seeds. (ChemMon 2026 p55)

### Pizza (takeaway, laminated box)
- Code: `A03ZN#F18.A07NL$F19.A07PN`
- F18 = box, F19 = laminated paper-plastic foil. The takeaway itself is reported in `sampPoint`. (ChemMon 2026 p54)
- If the pizza is not packed: `A03ZN#F10.A18PX` (qualitative-info = not packed). (ChemMon 2026 p54)

### Other examples in the guidance

| Sample | `sampMatCode` | Note from the guidance | Page |
| --- | --- | --- | --- |
| Urine sample from a dairy cow | `A0C60#F01.A0C9L$F02.A0CET$F31.A0C8V` | F01 = dairy cow, F02 = urine, F31 = young non-adult mammal (above 1 year). Source discrepancy: the split elements printed beside this code show `A057F`, `A0F0Y` and `A0F0Y`, which do not match the facet codes in the full code. | p52 |
| Royal jelly | `A0CVG` | | p52 |
| Processed cereal-based foods for infants and young children | `A03QX` | | p52 |
| Infant formula | `A0EQM` | | p52 |
| Follow-on formula | `A0EQL` | | p52 |
| Herbal infusions specific for infants and young children, dry | `A16GS` | | p52 |
| Crispbread (acrylamide category 6) | `A0CHT#F28.A07GX` | Indicate whether the product is baked; F28.A07GX = baking | p53 |
| Roasted coffee (acrylamide category 7) | `A03GL#F17.A07MY`, `A03GL#F17.A07MZ` or `A03GL#F17.A07NA` | Extent of cooking: outside light brown, outside brown, outside dark brown/slightly burned | p53 |
| Chewing gum | `A035M` | | p53 |
| Dry peas | `A0DCD` | Drying of peas is not considered processed if the moisture content is between 16 and 19% | p53 |
| Green peas | `A012J` | Fresh peas without pods are considered unprocessed | p53 |
| Dry camomile flowers | `A0D9D#F28.A07KG` | Herbal infusion, dried product considered unprocessed | p53 |
| Bovine meat (muscle), excluding the visible fat | `A01QX#F20.A0F4V` | Food tested and reported in line with the sample description to which the pesticide and VMPR MRLs apply | p53 |
| Deer fresh meat (muscle) from hunted, not farmed, animals | `A01SA#F21.A07RY` | F21.A07RY must be selected for a wild animal; it should not be reported if the animal was farmed or raised | p53-54 |
| Feed sample of maize grains for chicken/poultry | `A07XG#F23.A18EH` | F23 = `A07VD` (poultry feed) or one of its sub-codes, e.g. `A18EH` (chicken feed) | p54 |
| Water given to farmed rabbit | `A0F7L#F23.A07VE` | Freshwater for animal farming and rabbit feed | p54 |
| Bread made with hemp seed flour | `A0BY0#F04.A016B$F04.A0F0M` | `A0BY0` = leavened bread and similar; F04 ingredients = hemp seeds and nut/seeds paste/emulsion | p55 |

(ChemMon 2026 p52-55)

### Soft-ripened cheese: source discrepancy and catalogue version

The supplied PDFs disagree: ChemMon 2026 p. 39 shows
`A02RH#F03.A06JA$F33.A0C5F`, with F33 explicit; no-presence p. 9 and use-levels
p. 9 show `A02RH`, with F33 already implicit. Do not treat the first example as
a version-independent instruction to add F33.

A read-only check on 5 October 2026 of the **local MTX catalogue 17.2**
(valid from 14 July 2026) confirms:

- `A02RH` is Soft-ripened cheese and carries implicit `F33.A0C5F`
  (FA-01.7.2 Ripened cheese).
- Use `A02RH#F03.A06JA` **when the actual product is sliced**: A06JA means
  Slices, steaks or other flat cuts. Do not infer a physical state from the
  fact that a product is cheese.
- In that snapshot, omit an explicit F33.A0C5F because it duplicates the
  implicit class. CHEMON109 and PRE15 assign Warning severity to duplicate
  F33; USE23 assigns Error severity. The collection-specific conditions remain
  in [[food-additives-reporting]].

The query, returned term attributes, catalogue metadata and database hash are
recorded in `reports/source-review/2026-10-05-cheese-catalogue-check.json`;
see [[SOURCE_REVIEW]]. This is a checked local snapshot, not a latest-catalogue
claim. Its date is later than the PDFs, so it does not establish which historical
catalogue release the ChemMon example intended. It checked term labels, implicit
facets and reportability, not every validation condition for a complete record.
Check the catalogue used by the
receiving collection before reusing an example from another edition.
