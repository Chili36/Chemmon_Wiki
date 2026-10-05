# Maintaining the ChemMon wiki

Keep the supplied source PDFs immutable. A new edition belongs in a separate
source file with its collection year recorded. Never overwrite a previous
edition to make a fingerprint check pass.

## Source-led review

1. Run `python tools/source_review.py --prepare /tmp/chemmon-review-new` to
   extract every PDF with physical page boundaries and a corpus snapshot.
   This needs Poppler (`pdftotext`). The output directory must be new.
2. Select a bounded question or page family. Read complete relevant source
   sections, tables, footnotes and exceptions, then compare the wiki. Inspect
   rendered PDF pages when columns, wrapping or figures affect interpretation.
3. Record missing claims, wrong domains, recommendations promoted to requirements,
   obsolete year assumptions and source conflicts. Correct canonical definitions
   and their related summaries together. Preserve exact PDF locators.
4. For rule-ID review, run `python tools/build_rule_inventory.py --output
   /tmp/chemmon-rules-candidate.json`. Its fixed page/column map is for the supplied
   2026 edition. Compare candidate IDs/statuses to the PDF, especially wrapped
   suffixes, combined rows and inactive rules. Check the edition before adopting
   a candidate. Never generate expected IDs from wiki text.
5. Update `docs/source-review.json` only after reviewing the changed material.
   Record reviewer, date, scope, limitations and evidence for each finding;
   resolved findings need a resolution. Set `snapshot` to the reviewed result
   of `wiki_api.source_review.corpus_snapshot(root)`. A fresh hash is not a review.
6. Run `python tools/source_review.py`, `python tools/health_check.py --json`,
   and `pytest -q`. Inspect warnings; ordinary health success allows documented
   coverage gaps. CI also rejects stale/invalid/missing review records.
7. Add a dated entry to `log.md`. Keep deployment separate from content review.

## Reading the results

The review status is `current`, `stale`, `invalid` or `missing`. Current means
files match a scoped review; it does not mean all facts have been verified.
Open findings and missing active IDs are actionable backlog. Structural health
checks cannot infer whether regulatory prose is complete or correct.

The rule checker distinguishes missing active definitions, unexpected wiki IDs,
inactive definitions and duplicates. CHEMON (source) maps to CHEMMON (wiki).
The old duplicate CHEMMON03 was a wiki error, not an exception to uniqueness.

Keep evaluation labels and answer grading separate from ingestion. See
[[EVALUATION]]. Never update a gold label solely because a model disagreed with it.
