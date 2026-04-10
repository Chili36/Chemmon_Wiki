---
title: "SSD2 Elements: Matrix (sampMatCode)"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 32-36 (Section 2, E.02 sampMatCode and related matrix guidance)"
related:
  - "[[ssd2-data-model]]"
  - "[[ssd2-elements-sampling]]"
  - "[[foodex2-in-chemmon]]"
  - "[[vmpr-reporting]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-cross-cutting]]"
---

# SSD2 Elements: Matrix (sampMatCode)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 32-36 -->

## Overview

The matrix group describes the food, feed, or non-food material that was sampled and analysed. The single most important element is `sampMatCode`, which uses FoodEx2 encoding and has extensive domain-specific rules — particularly for VMPR. For general FoodEx2 conventions see [[foodex2-in-chemmon]]; this page focuses on the SSD2 element-level guidance and the domain-specific coding rules that appear in section 2 of the source PDF.

## sampMatCode — Coded description of the matrix of the sample taken

<!-- Source: ChemMon 2026 p32 -->

**Element code:** E.02 · **Name:** `sampMatCode` · **Catalogue:** MTX (FoodEx2) · **Status:** mandatory

### Purpose

Samples in FoodEx2 must be encoded according to the guidance for the harmonised use of the FoodEx2 system and the quality control of the codes (EFSA, 2015). To describe the food or feed product or matrix sampled, the code reflecting the **highest level of detail** is normally used — e.g. select the code for tomatoes instead of the code for Solanaceae. (ChemMon 2026 p32)

### Catalogue and reporting hierarchy

FoodEx2 codes can be selected from the **MTX catalogue** using the **reporting hierarchy**, which includes base terms for food, feed and non-food animal matrices. If the sample is not yet declared/intended for use as either food or feed, the sample must be reported as food. To generate the national/Annual Reports and classify samples according to legal limits or legislative groups, specific analysis hierarchies (Table 11) are defined using the information provided in `sampMatCode` (base terms and facets — both implicit and explicit). (ChemMon 2026 p32)

### Base terms and facets

FoodEx2 requires that a **base term is always supplied**. If the implicit facets are enough to characterise the matrix sampled (see example code), only a base term needs to be reported. Where the base term chosen has implicit facets, reporting of explicit facets should only be additional ones not already covered by the implicit facets. (ChemMon 2026 p33)

<!-- Source: ChemMon 2026 pp. 33-36 (VMPR-specific coding) -->

## VMPR-specific sampMatCode coding

For VMPR monitoring, two facets **must always be present**: the **source (F01) facet** and the **part nature (F02) facet** (except for the special case of feed and water samples coding and processed-composite food as detailed in the paragraphs below). In most cases, these are already pre-assigned in the codes present in the reporting hierarchy as implicit facets when the FoodEx2 browser is used for coding the matrix codes (an exception to this is the case of non-food base terms). (ChemMon 2026 p33)

If reported, the explicit facets supersede the implicit facet pre-assigned in the FoodEx2 selected code when the EFSA categorisation of the matrices according to the VMPR legislation is applied to categorise the matrix in the VMPR national and annual EU reports.

### When F01 must be added explicitly

The F01 source facet code is **not implicitly pre-assigned** in the codes present in the reporting hierarchy referring to raw primary commodities (RPC) derivatives or 'Processed' products; in this case the F01 should be added by the data provider. For example, if the code `A031X` = 'Hen egg mixed whole, dried' or `A02PJ` = 'Milk powder' is selected, then an **explicit F01 code shall be reported** (e.g. `F01.A057Z` = *Gallus* (chicken) (as animal) for the hen dried egg samples or `F01.A057E` = 'Cattle (as animal)' for the dried milk). (ChemMon 2026 p33)

## Wild animal VMPR samples coding

<!-- Source: ChemMon 2026 p33 -->

To encode samples related to wild animals, the code `A07RY` = 'Wild, gathered or hunted' from facet **F21** on the production method list must always be added to the base term by the data provider (explicit facet); this is particularly important to code wild game samples under the VMPR domain.

### Wild game routing

Regulation (EU) 2022/1644 and Regulation (EU) 2022/1646 **no longer consider Wild Game as one of the VMPR Product Category** — except in the case of results of the national risk-based control plan for third countries. The samples will still be classified as Wild Game and will be included in the VMPR National Report. However, **these samples will not be considered for the VMPR EU Annual Report** except for results of the mentioned plan. (ChemMon 2026 p33)

## Feed and water VMPR samples coding

<!-- Source: ChemMon 2026 pp. 33-35 -->

Samples of feed and water given to animals should be coded as described in this section. When a feed sample is analysed, the `sampMatCode` must be selected from the **feed section of the reporting hierarchy of the MTX catalogue**. The textual description of each base term under the feed section contains the wording '(feed)' (e.g. for the code `A05CR` = 'Barley grain (feed)').

### F23 target-consumer facet — the key rule

To report feed samples, the `sampMatCode` must always contain an implicit or explicit **F23 target-consumer facet** code to characterise the species for which the feed was intended. (ChemMon 2026 p33)

- If the specific explicit facet F23 is **not reported** and the implicit facet F23 is the generic 'Animal feed' (`A07TV`), the sample will be classified in the VMPR Product Category **'Other'**.
- If an **explicit facet F23 specific to an animal species is reported**, then the sample will be classified in a specific VMPR Product Category other than the Category 'Other'. (ChemMon 2026 p33)

### Conflicting F23 facets

If more facet F23 codes are explicitly reported and refer to different animal species (i.e. they are in conflict) in the final `sampMatCode` for the very same sample, then the analytical result reported for this sample will **not be included in the VMPR reports** created by EFSA because the sample will be classified in the VMPR Product Category 'Other'. (ChemMon 2026 p34)

### Worked coding examples for feed

| `sampMatCode` reported | Implicit and explicit facets | Note |
| --- | --- | --- |
| `A0BBB#F23.A07VC` (Barley roasted (feed)) | Implicit F02 = 'Feed-related (as part nature)'; Implicit F23 = 'Animal feed'; Explicit F23 = 'Pig feed' | **Correct coding** — with the explicit F23 code added to the base term ABBB, this sample will be classified in the VMPR Product Category 'Pigs' |
| `A0BBB#F23.A07VC$F23.A18EH` (Barley roasted (feed)) | Implicit F02 = 'Feed-related'; Implicit F23 = 'Animal feed'; Explicit F23 = {'Pig feed', 'Chicken feed'} | Refers to a feed fed to two different species (pigs AND chickens); sample will be classified in the VMPR Product Category 'Other' |
| `A0BTL#F23.A07VC` (Turkeys/Complete feed (feed)) | Implicit F02 = 'Feed-related'; Implicit F23 = 'Turkey feed'; Explicit F23 = 'Pig feed' | **Incorrect coding** — the F23 codes are contradictory. Sample will be classified as 'Other', not 'Poultry' or 'Pigs' |
| `A0BBB` (Barley roasted (feed)) | Implicit F02 = 'Feed-related'; Implicit F23 = 'Animal feed'; no explicit F23 | Acceptable coding; classified as 'Other' because the only F23 is the generic implicit `A07TV` |

(ChemMon 2026 p34)

### Feed category organisation

The codes under the feed section are **grouped into 14 categories** (e.g. 'Cereal grains and products derived thereof (feed)'). If a feed base term is selected from one of the first 13 categories — which implicitly contain the facet target consumer code `A07TV` = 'Animal feed' which does not refer specifically to the target consumer species — then an **explicit facet code for F23 target consumer must be selected** by the data provider. The facet code to be selected must be one of the codes listed under the facet target consumer code `A07TX` = 'Feed for animals' (e.g. code `A07VE` = 'Rabbit feed'). (ChemMon 2026 p35)

The implicit and/or explicit facet F23 target consumer will be used by EFSA to classify the sample results in one of the VMPR legislative matrix categories used in the VMPR reports (bovines, pigs, sheep & goats, horses, poultry, rabbit, farmed game, wild game, aquaculture, milk, eggs and honey). (ChemMon 2026 p35)

### Special case: Complementary feed

If the **last category** of feed codes in the reporting hierarchy is selected (i.e. 'Compound feed (feed)' = `A0BT0`), then the code already implicitly contains a facet F23 designating the target-consumer species and the data provider doesn't need to report an explicit F23 target consumer as the analytical result will be automatically be included in the VMPR Annual Report in the appropriate VMPR legislative matrix category. In some cases (e.g. `A0BV0` = 'Unspecified Complete Feed'), it is not possible to specify a species in the implicit facets so an explicit facet F23 describing the target-consumer is needed if the record is intended for inclusion in an Annual Report (e.g. VMPR). (ChemMon 2026 p35)

| Category in feed hierarchy | Feed example | Implicit facets | XML |
| --- | --- | --- | --- |
| #1 | 'Barley, roasted (feed)' used for breeding pigs | F02 = 'Feed-related'; F23 = 'Animal feed' | `<sampMatCode>A0BBB#F23.A07VC</sampMatCode>` — F23.A07VC is needed to allocate the record to species 'pigs' |
| #14 | 'Complementary feed (incomplete diet) (feed)' used for breeding pigs | F02 = 'Feed-related'; F23 = 'Animal feed' and 'Pig feed' | `<sampMatCode>A0BV8</sampMatCode>` — explicit F23 facet term is not needed |

(ChemMon 2026 p35)

### Goat and sheep feed special case

For the very particular cases where the feed base term implicitly contains an F23 facet 'Sheep and goat feed' (`A07VF`), it is always necessary to add one of the four codes grouped under the `A07VF` code. In particular, for goat feed samples, either 'Kids reared for reproduction or meat production feed' (code `A18EX`) or 'Dairy/reproductive goat feed' (code `A18EY`) should be specified; for sheep feed samples, either 'Lambs reared for reproduction or meat production feed' (code `A18ET`) or 'Dairy/reproductive sheep feed' (code `A18EV`) should be specified. (ChemMon 2026 p36)

### Water samples

When samples of water given to farmed animals are to be coded, select from the list of terms in 'Non-food purposes' from the reporting hierarchy one of the codes in the 'Environment' group. Since these terms do not contain an implicit facet for the target consumer species, a code for the F23 facet must be added. (ChemMon 2026 p36)

| Water example | XML |
| --- | --- |
| Water from a 'Watering place for animals' for cattle | `<sampMatCode>A0F7N#F23.A07TY</sampMatCode>` |

## Non-food matrices VMPR samples coding

<!-- Source: ChemMon 2026 p36 -->

When non-food matrices have been analysed (e.g. urine, retina, or hair samples from pig), the default base term `A0C60` = 'Non-food animal-related matrices' should be used. In such cases, it is important to include an **explicit F01 'Source' facet code** to characterise the source animal species as well as an **F02 'Part nature'** to characterise the sample. (ChemMon 2026 p36)

| Example | MTX (FoodEx2) code |
| --- | --- |
| Cow hair sample | `<sampMatCode>A0C60#F02.A0ESP$F01.A057E</sampMatCode>` — Base: Non-food animal-related matrices (A0C60); F02 Part-nature: Hair (A0ESP); F01 Source: Cattle (A057E) |
| Cow retina sample | `<sampMatCode>A0C60#F02.A0ESJ$F01.A057E</sampMatCode>` — F02 Part-nature: Retina (A0ESJ); F01 Source: Cattle (A057E) |

## New VMPR product categories: insects, reptiles, edible casings

<!-- Source: ChemMon 2026 p36 -->

Regulation (EU) 2022/1646 introduces **three new VMPR product categories**: **insects, reptiles, and edible casings**.

### Authorised insects as novel food

The only **four insects authorised as novel food** in the EU for food production are:

- *Tenebrio molitor*
- *Locusta migratoria*
- *Acheta domesticus*
- *Alphitobius diaperinus*

Therefore, only those insects can be sampled and reported to EFSA. The aforementioned insects can be sampled and reported to EFSA as **frozen/whole animal, dried and/or powdered**. (ChemMon 2026 p36)

### Edible casings

For edible casings, the base term to be used is `A0F1J`. When including the source, the source commodity (**F27 facet**) must be manually inserted. (ChemMon 2026 p36)

### Related business rules

- **CHEMMON76** — For VMPR with the same `sampEventId`, the F01 (species/breed) facet must be identical across all samples in the event.
- **CHEMMON91** — For VMPR, only one F33 (legislative class) facet under VR classes should be reported per sample.
- **CHEMMON92** — For VMPR, the base term of `paramCode` must belong to the vetDrugRes hierarchy.
- **FOODEX2_SAMMAT** — `sampMatCode` must follow FoodEx2 coding rules.

See [[business-rules-vmpr]] and [[business-rules-cross-cutting]]. For the complete per-domain facet reference (F01-F33), see [[foodex2-facets]].

## sampMatText — Text description of the matrix of the sample taken

<!-- Source: ChemMon 2026 p56 -->

**Element code:** E.03 · **Name:** `sampMatText` · **Status:** optional

### Purpose

After describing the matrix with the most detailed level of information available using FoodEx2 in the `sampMatCode` field, this free text data element can be completed to report **a full textual description of the product sampled and to provide additional relevant information**. This will provide a possibility of crosschecking for the codes reported and could highlight any data quality problem at the data analysis level. (ChemMon 2026 p56)

### When FoodEx2 codes are insufficient

In cases in which suitable codes to describe the item sampled cannot be found, **it is recommended to ask EFSA for support or the addition of codes**. (ChemMon 2026 p56)

### What NOT to include

The description of the product sampled should **not include the brand name** which can be reported in the element E.10 (`sampMatInfo`). (ChemMon 2026 p56)

## origCountry — Country of origin on the sample taken

<!-- Source: ChemMon 2026 p56 -->

**Element code:** E.04 · **Name:** `origCountry` · **Catalogue:** COUNTRY · **Status:** mandatory

### Purpose

The country of origin must be completed for all samples in **ISO 3166-1-alpha-2 format**. Reporting countries are encouraged to identify the origin of the product, particularly for unprocessed (raw) food products and for cases where a non-compliant sample has been found. (ChemMon 2026 p56)

### Rule for products with multiple countries in the supply chain

Goods whose production involved more than one country will be deemed to originate in the country where they underwent their last, substantial, economically justified processing. (ChemMon 2026 p56)

### Unspecific country codes

The unspecific country codes `AA`, `XC`, `XD`, `XE`, `XX` may be used when the true origin is not known — see the [[ssd2-elements-sampling#sampcountry-country-of-sampling]] page for the Table 3 mapping. Note that for **non-compliant results**, these codes cannot be used.

### Related business rules

- **CHEMMON95** — For PPP with `evalCode` = J003A (non-compliant), `origCountry` must not be XX, AA, EU, XC, XD, or XE.
- **CHEMMON99** — For import programmes (K038A/K019A/E010A), `origCountry` cannot equal `sampCountry`.
- **GBR13** — `origArea` must be geographically within `origCountry`.

See [[business-rules-pesticide]], [[business-rules-cross-cutting]], and [[business-rules-gbr]].

## sampAnId / anMatCode / anMatText — Sample analysed identification

<!-- Source: ChemMon 2026 p56 -->

**Element codes:** F.01 (`sampAnId`), G.01 (`anMatCode`), G.02 (`anMatText`) · **Status:** default inheritance from sample

### Purpose

These three elements describe the sample as it was actually analysed, which **may differ from the sample as it was taken** — for example, if only a sub-portion was analysed or if the sample was homogenised before analysis.

### Default behaviour (inheritance)

When left empty, the three elements `sampAnId`, `anMatCode` and `anMatText` will be assumed to have respectively the same value as:

- `sampAnId` ← `sampId` (element D.01)
- `anMatCode` ← `sampMatCode` (element E.02)
- `anMatText` ← `sampMatText` (element E.03)

Therefore, **there is no need to provide these data elements unless the nature of the sample analysed differs from the sample taken**. (ChemMon 2026 p56)

### sampAnId specifics

Each sample analysed must be identified by a unique sample identification reference (`sampAnId`) **no longer than 100 characters**. When the analytical results corresponding to different parameters are reported for the same sample analysed, the unique sample (analysed) identification number (`sampAnId`) must be maintained for that sample analysed in all transmissions. (ChemMon 2026 p56)

### anMatCode / anMatText distinction

- `anMatCode` — reports the matrix sample analysed characteristics encoded using FoodEx2 catalogue codes.
- `anMatText` — describes the sample analysed as **free text** and could be reported on a voluntary basis if the sample analysed description (`anMatCode`) through the FoodEx2 codes are not sufficiently detailed. (ChemMon 2026 p56)

### Related business rules

- **CHEMMON27** — For VMPR/pesticides, `sampMatCode` should equal `anMatCode` (the sampled and analysed matrices are usually the same). See [[business-rules-cross-cutting]].
- **FOODEX2_ANMAT** — `anMatCode` must follow FoodEx2 coding rules.
- **GBR4** — Sample analysed / matrix analysed consistency. See [[business-rules-gbr]].
