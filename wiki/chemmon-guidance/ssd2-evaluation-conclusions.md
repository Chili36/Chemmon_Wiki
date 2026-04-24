---
title: "SSD2 Evaluation: Conclusions and Comments"
type: "reference"
domain: "all"
last_updated: "2026-04-24"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "p. 76 (Section 2, element N.06)"
related:
  - "[[ssd2-elements-evaluation]]"
  - "[[controlled-terminology-catalogues]]"
  - "[[food-additives-reporting]]"
  - "[[business-rules-cross-cutting]]"
  - "[[business-rules-additives]]"
---

# SSD2 Evaluation: Conclusions and Comments

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p76 -->

## Rule Summary (Rule-First)

- `evalInfo.conclusion` classifies the reason or interpretation behind an outcome.
- `evalInfo.com` is the free-text explanation field.
- Use these fields when an apparently above-limit result is still considered compliant for a documented reason, when follow-up investigations need explanation, or when additives/flavourings require label/natural-occurrence interpretation.
- For additives/flavourings, `evalInfo.conclusion` uses the same `CONCLUS.faff` code family that also appears as `presenceAdded` in the parallel DMs.

## evalInfo.conclusion / evalInfo.com — Conclusion and comment

<!-- Source: ChemMon 2026 p76 -->

**Element codes:** N.06.1, N.06.2 · **Names:** `evalInfo.conclusion`, `evalInfo.com` · **Catalogue:** `CONCLUS`

### Purpose

`evalInfo.conclusion` classifies the findings of follow-up investigations or explains why the final assessment differs from a simple above/below-limit reading. `evalInfo.com` carries the human-readable explanation. (ChemMon 2026 p76)

### Typical uses

- explain compliant outcomes despite elevated results, such as natural occurrence or environmental contamination
- flag long shelf-life products where the applicable MRL at time of marketing differed from the current one
- record additive/flavouring label-presence and natural-occurrence interpretations

(ChemMon 2026 p76)

### Additives and flavourings

For additives and flavourings, `evalInfo.conclusion` is strongly recommended to indicate whether the substance was present on the label, added, or naturally occurring. The relevant codes come from the `CONCLUS.faff` hierarchy:

| Code | Meaning |
| --- | --- |
| `C19A` | Yes, present on label / added |
| `C20A` | No, not present on label / not added |
| `C05A` | Natural occurrence |

Combinations such as `C20A$C05A` are valid when the substance is not declared/added but occurs naturally. (ChemMon 2026 p76)

## Related business rules

- `CHEMMON26` — follow-up investigation should be accompanied by `evalInfo.conclusion`. See [[business-rules-cross-cutting]].
- `CHEMMON66_a` / `CHEMMON66_b` — conclusion should explain compliant/non-compliant assessments that do not line up with the simple above/detected pattern. See [[business-rules-cross-cutting]].
- `CHEMMON87` — `evalInfo.conclusion` is highly recommended for additives/flavourings. See [[business-rules-additives]].
- `CHEMMON88` — `evalInfo.restrictionException` is highly recommended for additives/flavourings. See [[business-rules-additives]].
