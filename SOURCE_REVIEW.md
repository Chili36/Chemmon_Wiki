# Source review — 5 October 2026

This is a scoped, assistant-conducted review of the supplied PDFs. It has not
received independent human sign-off and does not certify the whole wiki.

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

## What remains open

1. **CHEMON semantic review is incomplete.** Correct ID coverage does not prove
   that conditions, domains, severity, catalogue labels or exceptions match.
   Review the remaining Table 10 definitions against their full rows before
   describing the wiki as submission-ready guidance.
2. **PRE/USE field semantics need further review.** The ID inventory and scoped
   facet checks do not establish that every field, condition and exception has
   been compared with the complete source sections and rules.
3. **The 2013 SSD2 foundation and the rest of the 2026 prose are not exhaustively
   reviewed.** Nor are PRE/USE field descriptions fully certified by the rule-ID
   inventory. Worked examples outside the scoped checks, current legal changes
   and later catalogues require fresh verification.

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
