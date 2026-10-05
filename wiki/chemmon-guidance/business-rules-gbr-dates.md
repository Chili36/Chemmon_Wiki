---
title: "GBR: Date Validity and Chronological Order"
select_when: "Generic SSD2 date validation: valid calendar dates, no future dates, reporting year, day/month ranges, month required with a day, and production/expiry/sampling/analysis/slaughter ordering. GBR53-100 applicable chemical-data rows; not PRE/USE dates."
type: "rule-reference"
domain: "all"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 106-112 (Table 9)"
related:
  - "[[business-rules-gbr]]"
  - "[[ssd2-sampling-date]]"
  - "[[ssd2-sampling-event-and-unit]]"
  - "[[ssd2-analysis-context]]"
  - "[[ssd2-matrix-sampled-matrix]]"
---

# GBR: Date Validity and Chronological Order

<!-- Source: ChemMon 2026 Table 9, pp. 106-112 -->

These 35 rules are **Active, Error** in the 2026 source table. They describe
SSD2 dates; do not substitute them for PRE sampling-date or USE marketing-date
rules. “Current date” and “current year” are the validation-time concepts in
the source, not fixed values such as 2026. Collection-specific reporting windows
can impose additional constraints; see [[ssd2-sampling-date]].

## Date-field map

Each date comparison below uses the corresponding year, month and day fields.
Field optionality and handling of incomplete dates require the applicable field
specification; a day-range rule alone does not establish that a complete date
is valid or that every component is mandatory.

| Date | Year | Month | Day |
| --- | --- | --- | --- |
| Slaughter | `sampEventInfo.slaughterY` | `sampEventInfo.slaughterM` | `sampEventInfo.slaughterD` |
| Sampling | `sampY` | `sampM` | `sampD` |
| Laboratory arrival | `sampInfo.arrivalY` | `sampInfo.arrivalM` | `sampInfo.arrivalD` |
| Production | `sampMatInfo.prodY` | `sampMatInfo.prodM` | `sampMatInfo.prodD` |
| Expiry | `sampMatInfo.expiryY` | `sampMatInfo.expiryM` | `sampMatInfo.expiryD` |
| Analysis | `analysisY` | `analysisM` | `analysisD` |

## Calendar validity

| Rule ID | Severity | Requirement | Source page |
| --- | --- | --- | --- |
| GBR53 | Error | Slaughter year/month/day must form a valid date. | 106 |
| GBR54 | Error | Sampling year/month/day must form a valid date. | 106 |
| GBR55 | Error | Laboratory-arrival year/month/day must form a valid date. | 106 |
| GBR56 | Error | Production year/month/day must form a valid date. | 106-107 |
| GBR57 | Error | Expiry year/month/day must form a valid date. | 107 |
| GBR58 | Error | Analysis year/month/day must form a valid date. | 107 |

## Reporting year and future dates

| Rule ID | Severity | Requirement | Source page |
| --- | --- | --- | --- |
| GBR61 | Error | `repYear` must be less than or equal to the current year. | 107 |
| GBR62 | Error | Slaughter date must be less than or equal to the current date. | 107 |
| GBR63 | Error | Sampling date must be less than or equal to the current date. | 107 |
| GBR64 | Error | Laboratory-arrival date must be less than or equal to the current date. | 108 |
| GBR65 | Error | Production date must be less than or equal to the current date. | 108 |
| GBR67 | Error | Analysis date must be less than or equal to the current date. | 108 |

There is no corresponding active non-biological expiry-date/future-date rule
in this supplied table. Do not invent a GBR66 or apply the production-date
condition to expiry dates. Expiry still has calendar-validity and chronology
constraints below.

## Day and month ranges

| Rule ID | Severity | Requirement | Source page |
| --- | --- | --- | --- |
| GBR70 | Error | `sampEventInfo.slaughterD` must be between 1 and 31. | 108 |
| GBR71 | Error | `sampD` must be between 1 and 31. | 108 |
| GBR72 | Error | `sampInfo.arrivalD` must be between 1 and 31. | 108 |
| GBR73 | Error | `sampMatInfo.prodD` must be between 1 and 31. | 108 |
| GBR74 | Error | `sampMatInfo.expiryD` must be between 1 and 31. | 109 |
| GBR75 | Error | `analysisD` must be between 1 and 31. | 109 |
| GBR78 | Error | `sampEventInfo.slaughterM` must be between 1 and 12. | 109 |
| GBR79 | Error | `sampM` must be between 1 and 12. | 109 |
| GBR80 | Error | `sampInfo.arrivalM` must be between 1 and 12. | 109 |
| GBR81 | Error | `sampMatInfo.prodM` must be between 1 and 12. | 109 |
| GBR82 | Error | `sampMatInfo.expiryM` must be between 1 and 12. | 109 |
| GBR83 | Error | `analysisM` must be between 1 and 12. | 109 |

For example, 31 satisfies the day range, but 31 February does not satisfy
calendar validity. Both checks matter.

## Reporting a day also requires its month

| Rule ID | Severity | Condition and requirement | Source page |
| --- | --- | --- | --- |
| GBR86 | Error | If `sampEventInfo.slaughterD` is supplied, supply `sampEventInfo.slaughterM`. | 109 |
| GBR87 | Error | If `sampD` is supplied, supply `sampM`. | 110 |
| GBR88 | Error | If `sampInfo.arrivalD` is supplied, supply `sampInfo.arrivalM`. | 110 |
| GBR89 | Error | If `sampMatInfo.prodD` is supplied, supply `sampMatInfo.prodM`. | 110 |
| GBR90 | Error | If `sampMatInfo.expiryD` is supplied, supply `sampMatInfo.expiryM`. | 110 |
| GBR91 | Error | If `analysisD` is supplied, supply `analysisM`. | 110 |
| GBR92 | Error | If analysis-completion day `sampAnInfo.compD` is supplied, supply completion month `sampAnInfo.compM`. | 110 |

GBR92 concerns **completion of analysis**, not `analysisD` / `analysisM`.

## Chronological order between dates

| Rule ID | Severity | Requirement | Source page |
| --- | --- | --- | --- |
| GBR94 | Error | Production date must be less than or equal to expiry date. | 110-111 |
| GBR95 | Error | Production date must be less than or equal to sampling date. | 111 |
| GBR97 | Error | Sampling date must be less than or equal to analysis date. | 111 |
| GBR100 | Error | Slaughter date must be less than or equal to sampling date. | 111-112 |

**Source wording note for GBR100:** the description lists slaughter day/month
but omits the year; the error-message column includes
`sampEventInfo.slaughterY`. The date-field map above retains the full date shown
in that error message. No new ordering between laboratory arrival and sampling
or analysis is inferred from these rows.

## Rules outside chemical-data scope

Table 9 marks isolation-date rules GBR60, GBR69, GBR77, GBR85, GBR93 and GBR99
as applicable to **biological data**. They remain in the source inventory and
are excluded from this ChemMon date reference. The other biological-only GBR,
GBR6, concerns isolate consistency; see the scope notes in [[business-rules-gbr]].
