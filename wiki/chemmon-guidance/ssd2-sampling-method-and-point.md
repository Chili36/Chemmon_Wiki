---
title: "SSD2 Sampling: Method, Sampler, and Point"
type: "reference"
domain: "all"
last_updated: "2026-04-23"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 27-28 (Section 2, elements B.05-B.07)"
related:
  - "[[ssd2-elements-sampling]]"
  - "[[ssd2-elements-programme]]"
  - "[[contaminant-reporting]]"
  - "[[vmpr-reporting]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-vmpr]]"
---

# SSD2 Sampling: Method, Sampler, and Point

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 27-28 -->

## Rule Summary (Rule-First)

- `sampMethod` is optional, but some codes carry downstream meaning. In particular, pooled-sample methods (`N002A`, `N031A`) trigger mandatory unit-size reporting on the sampling-unit fields. See [[ssd2-sampling-event-and-unit]]. (`CHEMMON77`)
- `sampler` is mandatory and identifies whether the sample was taken under official control or by a food business operator.
- `sampPoint` is mandatory and locates the sample in the food chain; VMPR reporting also remaps `sampPoint` through a dedicated `vmprClasses` hierarchy.
- For furan and alkylfurans, the guidance points to `sampMethod=N011A` where the dedicated sampling procedure applies. See [[contaminant-reporting]].

## sampMethod — Sampling method

<!-- Source: ChemMon 2026 p27 -->

**Element code:** B.05 · **Name:** `sampMethod` · **Catalogue:** SAMPMD · **Status:** optional

### Purpose

This element provides a reference to the legislation, protocol, or other documentation describing the method of selecting samples from the food chain. If reported, the sampling method codes are selected from the SAMPMD catalogue.

### Catalogue highlights

| Code | Meaning |
| --- | --- |
| `N040A` | Samples taken for the control of dioxins, dioxin-like PCBs and non-dioxin-like PCBs per Commission Regulation (EU) 2017/644 |
| `N009A` | Samples taken per Regulation (EC) No 396/2005 and Directive 2002/63/EC |
| `N042A` | VMPR samples analysed per Regulation (EU) 2022/1644 and 2021/808 |
| `N020A` | No standardised sampling methodology has been defined |
| `N031A` | Mercury samples from fish collected at different places (different batches) and put together before the analysis |
| `N011A` | Furan, 2-methylfuran and 3-methylfuran per part B of the Annex to Commission Regulation (EC) No 333/2007 |
| `N002A` or `N031A` | Analytical results referring to pooled samples, reported either as "pooled/batch" or "pooled" |

### Pooled samples rule

If the analytical result refers to pooled samples, the code `N002A` or `N031A` has to be selected. In these cases, `sampUnitSize` and `sampUnitSizeUnit` become mandatory. See [[ssd2-sampling-event-and-unit]].

## sampler — Sampler

<!-- Source: ChemMon 2026 p28 -->

**Element code:** B.06 · **Name:** `sampler` · **Catalogue:** SAMPLR · **Status:** mandatory

### Purpose

Identifies the person or persons responsible for taking the sample.

| Code | Meaning |
| --- | --- |
| `CX02A` | Samples taken in the context of an official control |
| `CX01A` | Samples taken by food business operators (FBOs) |

## sampPoint — Sampling point

<!-- Source: ChemMon 2026 p28 -->

**Element code:** B.07 · **Name:** `sampPoint` · **Catalogue:** SAMPNT · **Status:** mandatory

### Purpose

Describes the point in the food chain where the sample was taken. The catalogue is based on Eurostat terminology describing activities at different points in the production and consumption chain.

### Main stages

| Stage | Example | XML |
| --- | --- | --- |
| Primary production | Milk samples taken at a farm | `<sampPoint>E100A</sampPoint>` |
| Manufacturing | Milk samples taken at the dairy before the bulk tanker has discharged | `<sampPoint>E301A</sampPoint>` |
| Distribution | Samples taken at wholesale and retail sale | `<sampPoint>E520A</sampPoint>` |
| Packaging | Eggs taken in collection/packing centres | `<sampPoint>E600A</sampPoint>` |
| Border Control Posts | Import samples for VMPR Plan 3 and contaminants monitoring | `<sampPoint>E010A</sampPoint>` |

### VMPR-specific hierarchy

When EFSA generates the VMPR reports, the `SAMPNT.vmprClasses` hierarchy may be applied to classify `sampPoint` codes into `Slaughter`, `Farm`, and `Other`.

### Online sales

In case of foodstuffs purchased directly by consumers via online platforms, the sampling point depends on the origin, e.g. supermarket or farm.
