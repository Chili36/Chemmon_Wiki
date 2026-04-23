---
title: "SSD2 Sampling: Event and Unit"
type: "reference"
domain: "all"
last_updated: "2026-04-23"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 29-30 (Section 2, elements C.01-C.04)"
related:
  - "[[ssd2-elements-sampling]]"
  - "[[ssd2-elements-programme]]"
  - "[[ssd2-sample-identifiers]]"
  - "[[business-rules-gbr]]"
  - "[[business-rules-vmpr]]"
  - "[[business-rules-cross-cutting]]"
---

# SSD2 Sampling: Event and Unit

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 29-30 -->

## Rule Summary (Rule-First)

- `sampEventId` represents the sampling unit at a point in time. Multiple samples taken from the same unit should share it.
- If `sampEventId` is omitted, EFSA substitutes `sampId`.
- `sampUnitType` describes what that sampling unit is (batch, individual sample, tanker, etc.).
- `sampUnitSize` and `sampUnitSizeUnit` are normally optional, but become mandatory for pooled samples. In pooled cases, `sampUnitSizeUnit` must be `G005A` and `sampUnitSize` must be the number of pooled single samples. (`CHEMMON77`)

## sampEventId — Sampling event identification code

<!-- Source: ChemMon 2026 p29 -->

**Element code:** C.01 · **Name:** `sampEventId` · **Status:** optional

### Purpose

`sampEventId` is the unique identifier representing the sampling unit extracted at a certain time from the sampled population. It can be reported when multiple samples are taken from a single sampling unit at one timepoint. The sampling unit could be a batch, animal, flock, herd, or holding.

### Default behaviour

If no value is reported in `sampEventId`, EFSA automatically substitutes `sampId` during data submission.

### Domain-specific behaviour

- **Pesticide residues**: this element is not used when counting the number of samples for report creation and can be left empty.
- **VMPR**: if two samples are taken from a single pig at slaughter (for example kidney and muscle), the two samples should share the same `sampEventId` and count as one pig in the VMPR national sampling plan.

### Consistency check

A business rule checks whether samples with different `sampId` values but the same `sampEventId` refer to the same animal species. See [[business-rules-vmpr]] for `CHEMMON76`.

## sampUnitType — Sampling unit type

<!-- Source: ChemMon 2026 pp. 29-30 -->

**Element code:** C.02 · **Name:** `sampUnitType` · **Catalogue:** SAMPUNTYP · **Status:** optional

### Purpose

Describes the sampling unit defined in the sampling method and can be used to indicate whether the sample contains material from multiple individuals or lots.

### Examples

| Description | XML |
| --- | --- |
| Milk samples taken before the dairy bulk tanker has discharged | `<sampUnitType>G202A</sampUnitType>` |
| Single samples such as one animal or one fruit | `<sampUnitType>G203A</sampUnitType>` |

## sampUnitSize and sampUnitSizeUnit — Sampling unit size

<!-- Source: ChemMon 2026 p30 -->

**Element codes:** C.03 and C.04 · **Names:** `sampUnitSize`, `sampUnitSizeUnit` · **Status:** optional

### Purpose

These elements report the size of the sampling unit and its unit of measurement, i.e. how a sample is created before analysis.

### Example (standard individual sample)

| Description | XML |
| --- | --- |
| An individual rice sample made up of 300 grams collected and analysed for mycotoxins | `<sampUnitSizeUnit>G148A</sampUnitSizeUnit><sampUnitSize>300</sampUnitSize>` |

### Pooled samples rule

In the specific case of pooled samples, `sampUnitSizeUnit` must be reported with code `G005A` (`Unit`) and `sampUnitSize` must report the number of single samples pooled. The system returns an error if this is not followed.

| Description | XML |
| --- | --- |
| A pooled sample made up of five units of fish collected at different points and combined before mercury analysis | `<sampUnitSizeUnit>G005A</sampUnitSizeUnit><sampUnitSize>5</sampUnitSize>` |
