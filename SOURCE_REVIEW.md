# Source review — 5 October 2026

This is a scoped, assistant-conducted review of the supplied PDFs. Independent human
review is unavailable and deferred at the user’s request. This source comparison
does not certify the whole wiki or establish model-answer quality.

## Findings and corrections

- **GBR result rules corrected:** GBR27 requires units for results other than
  BIN; GBR28 requires `resQualValue` for BIN; GBR29 covers all listed numeric
  result, limit and uncertainty fields. The previous wiki reversed GBR27 and
  misattributed GBR28. Source: ChemMon Table 9, pp. 102–103.
- **GBR101 corrected:** the uniqueness key includes `paramCode.base`, `sampId`,
  `sampAnId` and `anPortSeq`, with an exception for RF-XXXX-XXX-XXX. Source p. 112.
  GBR2 now preserves the `progId` / `progLegalRef` exclusion (p. 98).
- **GBR coverage completed:** reviewed the complete Table 9 rows, pp. 98–112,
  and added all 67 omitted active, non-biological definitions. The 83 applicable
  rules are now covered once across the core, consistency, numeric-result and
  date references. GBR22/42 retain Warning severity; two inactive and seven
  biological-only IDs are documented separately. GBR3/4 now retain the related
  event/sample identifiers as well as the descriptor fields. This is an
  assistant source comparison, not an independently certified validator.
- **CHEMON attribution corrected:** Table 10 has one CHEMON03, for the analytical
  method. The alleged source duplicate was a wiki error. Unsupported CHEMMON01,
  CHEMMON02 and the country-consistency CHEMMON03 entries were removed. The
  source uses CHEMON; this wiki retains CHEMMON as an explicit spelling alias.
  Merged CHEMON39/79 IDs and the missing CHEMON64 definition were corrected.
- **Recommendation strength corrected:** CHEMON37 is a Warning for action-taken
  reporting in contaminants/additives/flavourings (p. 121), not an Error.
- **Legal-limit scope restored:** the LL rules now preserve numeric-result,
  unprocessed-sample, limit-type and part-of-sum conditions (pp. 141–143).
  Page 68 contradicts itself about processed samples; the result page now
  identifies that conflict and follows the complete rule-table conditions.
- **VMPR/FoodEx2 overlap checked:** F01/F02 exceptions (p. 33) and the sheep/goat
  F23 example (p. 36) were reconciled. A read-only query of the local FoodEx2
  catalogue confirms A18ET/A18EV/A18EX/A18EY under A07VF. The query, result and
  database fingerprint are saved in `reports/source-review/2026-10-05-catalogue-check.json`.
  This confirms a local snapshot, not the latest online catalogue.
- **Three FA/FF paths checked for facet strength:** ChemMon pp. 38–39 and
  CHEMON109 p. 141; no-presence §2.7 pp. 7–8 and PRE15 p. 21; use-levels §2.7
  pp. 7–8 and USE23 p. 27. Explicit duplication of implicit F33 warns in the
  first two paths, and is an Error for use levels. The field names and F03
  recommendation/requirement distinctions remain separate.
- **Cheese example qualified by catalogue version:** ChemMon p. 39 prints an
  explicit F33 for A02RH; both parallel guides p. 9 treat it as implicit. Local
  MTX 17.2 (valid from 14 July 2026) confirms implicit F33.A0C5F. The wiki now
  gives a version-qualified example, adds the sliced-state facet only when
  known, and preserves the source discrepancy and different rule severities.
  Query, attributes and database hash are saved in
  `reports/source-review/2026-10-05-cheese-catalogue-check.json`. The historical
  catalogue release intended by ChemMon p. 39 is still unknown; this check
  does not establish that the source example was correct in an earlier release.
- **Related summary defects corrected:** removed a leftover unsupported
  CHEMMON01 cross-reference, restored VMPR F01/F02 exceptions in the FoodEx2
  overview (p. 33), and corrected the omelette's explicit-F33 label and the
  syrup-type code A1B1Y in the additive worked examples (p. 40).

## Broader comparison completed

The full ChemMon Table 10 (pp. 113–143) has now been compared, including
continuations, error-message columns, comments, inactive rows and named
DOMAIN/FOODEX2 rules. All **100 active CHEMON definitions** now show scope,
severity and source page. The four inactive CHEMON IDs remain documented.
The source totals are 51 active Errors and 49 active Warnings.

The PRE and USE comparison covers their complete field sections, examples and
Tables 1–3: **18 PRE fields / 17 rules** and **31 USE fields / 29 rules**. PRE
has 16 Errors and one Warning; all USE rules are Errors. Field optionality,
repeatability, catalogue restrictions, identifiers, dates and numeric conventions
were checked alongside the rule tables, rather than inferred from rule IDs.

Significant corrections include:

- CHEMON92 validates the sampled/analysed **matrix** base terms in VetDrugRes,
  not the parameter code. CHEMON100 includes all six VMPR evaluation codes,
  including J041A. Related matrix, analysis and annual-change summaries agree.
- CHEMON26 is Warning; CHEMON33 is Error despite “should” in its description.
  CHEMON43_b accepts sampling year **≤** submission year minus one in 2026.
- CHEMON31 preserves the P002A exception; CHEMON45 preserves unvalidated-method
  and not-summed exceptions. CHEMON46 includes both J003A and J031A.
- CHEMON54 maps N317A to increased import controls, and CHEMON36/54/83/105 are
  no longer confined to an unsupported single domain. CHEMON83 tests the
  presence of facet F10.A18PX, not equality to a matrix base code.
- Result-assessment fields use the source spelling `evalInfo.resAsses`.
  The evaluation reference now explains its relationship with `evalCode` and
  the pesticide annual-report exception to assessment-based counting.
- CHEMON106 is a potassium-sorbate recommendation. CHEMON107 names six
  parameters and requires the BIN-and-NEG trigger. Broader LOD recommendations
  in field prose remain distinguished from that narrower validation row.
- USE maximum-permitted-level guidance now distinguishes a numeric MPL from
  Quantum satis and applies the limit to combined added/naturally occurring
  amounts. Optional `minLevel`, exact-level conventions, preparation factors
  and the mandatory full marketing date remain explicit. PRE `resId` and USE
  `recId` are kept separate. Source shorthand does not create new schema fields.

`reports/source-review/2026-10-05-broader-review.json` records each reviewed
rule, independently extracted source severity, page, canonical reference and
all 49 field names/requirements. Rendered spot checks covered ChemMon pp. 120,
129, 133, 136; PRE pp. 15, 16, 21; USE pp. 21, 26, 27. Regression checks compare
canonical rule coverage, severity and page locators with the independent source
record; they do not claim to test every sentence's meaning.

## What remains open

1. **Boolean grouping in CHEMON66_a/85/93 (SRC-012).** The PDFs mix “and” and
   “or” without parentheses. The wiki gives the contextual reading and retains
   every condition, but exact boundary behaviour needs the collection's
   executable rule definition. No invented predicate is certified here.
2. **USE19 zero-level condition (SRC-013).** The description says “typical or
   maximum”; the error message differs and mistypes C19A as C10A. Both levels
   zero fail the added-substance condition. Whether each must independently
   be positive cannot be settled from this PDF wording alone.
3. **CONCLUS hierarchy spelling (SRC-014).** ChemMon p. 76 says `fa_ff`;
   the parallel guides say `faff`. C19A/C20A/C05A agree. No live catalogue alias
   equivalence has been established; use the target collection's configuration.

These are source uncertainties, not uncompleted table review or requests for
human sign-off. The 2013 SSD2 foundation and remaining ChemMon prose are not
exhaustively reviewed. Current legal changes and later catalogues are outside
this fixed-edition comparison. The previously documented cheese example's
historical catalogue edition is still unknown.

## Reproducibility

`docs/source-review.json` records scope, findings, resolutions and hashes for all
supplied PDFs, topic pages and the index. A changed, added or removed file makes
the audit stale. Open findings remain visible after drift, but need rechecking.
`docs/rule-inventory.json` is independently derived from the PDF table columns:
92 GBR, 104 CHEMON, 11 LL, 17 PRE and 29 USE IDs. Inactive rows are retained;
explicitly biological-only GBRs are excluded from missing-active warnings.
Counts are inventory coverage, not a semantic accuracy score.

See [[MAINTENANCE_WORKFLOW]] for commands and [[EVALUATION]] for the separate
question-and-answer review process.
