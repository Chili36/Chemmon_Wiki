---
title: "SSD2 Evaluation: Conclusions and Comments"
type: "reference"
domain: "all"
last_updated: "2026-11-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 75-78 (Section 2, elements N.05, N.06.1, N.06.2; N.06.3 example)"
related:
  - "[[ssd2-elements-evaluation]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[food-additives-reporting]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-additives]]"
---

# SSD2 Evaluation: Conclusions and Comments

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 75-78 -->

## Rule Summary (Rule-First)

- `evalInfo.conclusion` classifies the reason or interpretation behind an outcome.
- `evalInfo.com` is the free-text explanation field.
- Use these fields when an apparently above-limit result is still considered compliant for a documented reason, when follow-up investigations need explanation, or when additives/flavourings require label/natural-occurrence interpretation.
- For additives/flavourings, `evalInfo.conclusion` uses the FA/FF CONCLUS codes that also appear as `presenceAdded` in the parallel DMs; the PDFs differ in hierarchy spelling, as noted below.

## evalInfo.conclusion / evalInfo.com — Conclusion and comment

<!-- Source: ChemMon 2026 p76 -->

**Element codes:** N.06.1, N.06.2 · **Names:** `evalInfo.conclusion`, `evalInfo.com` · **Catalogue:** `CONCLUS`

### Purpose

`evalInfo.conclusion` classifies the findings of follow-up investigations or explains why the final assessment differs from a simple above/below-limit reading. `evalInfo.com` carries the human-readable explanation. (ChemMon 2026 p76)

### Typical uses

- explain compliant outcomes despite elevated results, such as natural occurrence or environmental contamination
- report a long shelf-life product with `C08A` ("Long shelf-life product", `CONCLUS` catalogue) when the MRL in place at the time of placing it on the market differed from the MRL applicable in the current data collection for that pesticide/crop combination; "The BRs checking against the MRLs will not be applicable"
- record additive/flavouring label-presence and natural-occurrence interpretations

(ChemMon 2026 p76)

### Additives and flavourings

For additives and flavourings, `evalInfo.conclusion` is highly recommended to indicate whether the substance was present on the label, added, or naturally occurring. ChemMon p. 76 names the hierarchy `CONCLUS.fa_ff`; the parallel PRE/USE guides write `CONCLUS.faff`. The identical codes, labels and examples establish the same FA/FF concept family. Treat the underscore difference as a documentation naming discrepancy, not a different meaning for the submitted codes. Preserve each source’s spelling when discussing its hierarchy; a software catalogue lookup must use the configured identifier:

| Code | Meaning |
| --- | --- |
| `C19A` | Yes, present on label / added |
| `C20A` | No, not present on label / not added |
| `C05A` | Natural occurrence |

Combinations such as `C20A$C05A` are valid when the substance is not declared/added but occurs naturally. (ChemMon 2026 p76)

Additive/flavouring examples (ChemMon 2026 p76):

| Case | `evalInfo.conclusion` | `evalInfo.com` |
| --- | --- | --- |
| Ascorbic acid added as FA and naturally occurring | `C19A$C05A` | |
| Ascorbic acid added as ingredient and naturally occurring | `C19A$C05A` | "Ascorbic acid added as ingredient" |
| Substance added as carry-over, and not as FA | `C19A` | "Carry-over" |
| Caffeine added as flavouring and declared on the label | `C19A` | |
| "Flavourings" declared on the label, without specifying "ethyl vanillate" | `C20A` | |

### Worked examples: action, conclusion, comment

| Case | Coding |
| --- | --- |
| Follow-up investigation indicates illegal treatment and additional sampling is planned | `actTakenCode` = `I`; `evalInfo.conclusion` = `C04A`; `evalInfo.com` = "increased testing for this product in aquaculture is planned" |
| Non-compliant result with a rapid alert notification in RASFF | `evalCode` = `J003A`; `actTakenCode` = `R`; `evalInfo.com` = "Reference number 2018.1567" |
| Result considered compliant because investigations indicate the exceedance may be due to natural occurrence | `evalCode` = `J002A`; `actTakenCode` = `I`; `evalInfo.conclusion` = `C05A`; `evalInfo.com` gives the reason |
| Compliant, food additive present on the label and naturally occurring in the food | `evalCode` = `J002A`; `evalInfo.conclusion` = `C19A$C05A` |
| Non-compliant, food additive not present on the label while found in the food | `evalCode` = `J003A`; `evalInfo.conclusion` = `C20A` |

(ChemMon 2026 p77)

The guidance shows two equivalent syntaxes: one compound element, e.g. `<evalInfo>conclusion=C04A$com=increased testing for this product in aquaculture is planned</evalInfo>`, or separate elements `<evalInfo.conclusion>C04A</evalInfo.conclusion>` and `<evalInfo.com>…</evalInfo.com>`. (ChemMon 2026 p77)

With `evalInfo.resAsses`: `<evalInfo>resAsses=J037A$conclusion=C05A$com=Result is within a physiological range for this sample to be a naturally occurring hormone</evalInfo>`. Where `evalInfo.resAsses` is reported and differs from `evalCode`, the reason must be reported in `evalInfo.conclusion`. (ChemMon 2026 p78)

## Related business rules

- `CHEMON26` — follow-up investigation should be accompanied by `evalInfo.conclusion`. See [[business-rules-cross-cutting]].
- `CHEMON66_a` / `CHEMON66_b` — Warning conditions for assessment/evaluation differences: retain the Presence limit condition in 66_a and all three negative conditions in 66_b. The warning text and assessment guidance establish the grouping; consult the full rows and contextual reading. See [[business-rules-cross-cutting]].
- `CHEMON87` — `evalInfo.conclusion` is highly recommended for additives/flavourings. See [[business-rules-additives]].
- `CHEMON88` — `evalInfo.restrictionException` is highly recommended for additives/flavourings. See [[business-rules-additives]].
