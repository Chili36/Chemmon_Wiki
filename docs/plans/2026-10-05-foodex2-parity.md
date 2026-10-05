# ChemMon improvement plan

Baseline: 5 October 2026. Compared with the FoodEx2 wiki in `LLM Knowledge Base`.
ChemMon has 70 topic pages, four immutable source PDFs and 38 passing tests.
The initial health check reported a CHEMMON03 duplicate, then attributed to the source. Milestone 2 source review later established that it was a wiki error.

## Milestone 1: reliable evidence and usable navigation

Completed locally on 5 October 2026:

- [x] Make `max_pages` a strict final evidence budget. Remove the index from
  answer evidence and keep per-request limits out of shared mutable state.
- [x] Make related-summary expansion opt-in and identify summaries explicitly;
  only full pages can support citations. Preserve source locators in evidence.
- [x] Give the selector an explicit JSON contract and a concise topic catalogue;
  reject malformed selections instead of silently answering from the index.
- [x] Serve orientation documents, derive navigation from page metadata, and
  add search, domain filtering, working wiki links and backlinks.
- [x] Correct the source-confirmed VMPR exception and remove the incomplete
  duplicated sheep/goat code list in favour of the canonical matrix page.
- [x] Extend local health checks for index/service consistency, source files,
  frontmatter relations and dates; configure CI to run these and the tests.
- [x] Update usage documentation, record semantic changes, and verify the
  viewer in a local preview without replacing the running deployment.

Acceptance: a one-page request can return one substantive page; no response
exceeds its requested limit; summaries/index cannot be cited as rule evidence;
all listed navigation pages open; search and internal links work; tests and
health checks pass with the known source-duplicate warning documented.

Verification: 69 tests passed; health check passed with zero errors and the
known CHEMMON03 warning. All 77 catalogue/navigation entries returned readable
content from the local preview. Browser checks covered orientation navigation,
full-text search, domain filtering, rendered wiki links and backlinks. No live
model evaluation or deployment update was performed; CI is configured and will
run when these changes reach GitHub.

## Milestone 2: source coverage and maintenance

Implemented on `codex/chemmon-foodex2-parity`:

- [x] Scoped review with source locators, findings/resolutions, corpus hashes and
  explicit limits in `docs/source-review.json` and `SOURCE_REVIEW.md`.
- [x] Reviewed complete selected rule rows and relevant VMPR/FA/FF sections for
  exceptions, severity and collection-path differences. Corrected confirmed
  GBR, CHEMON attribution, action-reporting and LL defects in related pages.
- [x] Reconciled sheep/goat F23 with a read-only local FoodEx2 catalogue query;
  saved the database hash, query and result.
- [x] Independently extracted rule inventory from PDF columns: 92 GBR,
  104 CHEMON, 11 LL, 17 PRE and 29 USE IDs, including inactive entries.
- [x] Added stale/invalid/missing audit reporting, preparation and inventory
  tools, JSON health output, maintenance instructions and CI freshness checks.

- [x] Completed the full Table 9 comparison and added all 67 omitted applicable
  active GBR definitions in three focused references. The source-derived check
  now confirms exactly one definition for each of the 83 applicable GBR IDs.
- [x] Qualified the conflicting A02RH cheese examples using a recorded local
  MTX 17.2 query; retained the historical catalogue-version limitation and
  Warning/Error distinctions. Corrected related example and rule-reference defects.

Acceptance met for a scoped, reproducible review. Two open findings remain:
remaining CHEMON semantic review and unreviewed PRE/USE field semantics.
The 2013 foundation and the rest of the 2026 prose are not exhaustively reviewed.

## Milestone 3: measured answer quality

Implementation ready; quality acceptance remains open:

- [x] Created 16 source-informed draft cases: 10 development and 6 reserved
  held-out cases, including ambiguity and insufficient evidence. Review queue:
  `evals/REVIEW.md`. They were authored after the source-led content changes.
- [x] Implemented offline validation and explicit live comparison modes for
  selection and frozen-evidence answers. Record corpus/catalogue/prompt hashes,
  model settings, recall, wrong-domain/path selections, tokens, latency, failures
  and optional cost estimates. Unknown pricing is null.
- [x] Added fingerprint-bound human answer grading for correctness and citation
  support, distinct from mechanical citation membership.
- [x] Added 20 situation-based selection hints and a summary/hints comparison
  switch. No model defaults changed.
- [x] Saved dry-run reports for both configured model names. No API calls made.
- [ ] Human review of labels and live baseline/model comparisons.
- [ ] Demonstrate improvement against that same reviewed baseline before
  accepting model/default changes. Dry runs do not meet this criterion.

## Milestone 4: downstream integration

Implemented and tested:

- [x] `/wiki/context-pack` returns full evidence, source locators, page hashes,
  review status and a compact ChemMon decision policy, without an answer call.
- [x] Policy occupies one page slot. Page and character budgets are enforced;
  oversized pages are omitted whole with reasons. Only full evidence is citable.
- [x] `/wiki/select` exposes selection metadata/trace; `/wiki/review-status`
  exposes audit and inventory results. Selection metadata is not citable.
- [x] Per-request selector/answerer overrides leave shared defaults unchanged.
- [x] Retained Markdown retrieval. Vector retrieval is deferred until a measured
  endpoint comparison justifies its cost and complexity.

Acceptance met by integration tests for budgets, provenance, model isolation and
zero answer calls for context export. No deployment or live-provider verification
is included in this branch's offline checks.

## Branch verification

114 tests pass. Health reports zero errors and two documented semantic-review
warnings. Source and inventory fingerprints are current, with no missing,
duplicate, unexpected or inactive canonical rule IDs. All 84 listed navigation
pages return readable content from the local preview on port 8006; browser
review confirms the new GBR navigation and rendered date-rule tables.

The two saved evaluation dry runs describe the earlier corpus snapshot, made
zero model calls and have unmeasured quality/cost scores. They are historical
workflow checks, not a quality baseline for the expanded corpus. Human review
and live evaluation remain pending; no model defaults have changed.

## Implementation boundaries

Preserve immutable sources and the existing topic structure. Reuse FoodEx2's
tested architectural patterns while keeping ChemMon's domain rules in Markdown.
Do not import FoodEx2-specific coding policies as ChemMon reporting rules.
Record unresolved source conflicts; do not guess catalogue codes. Keep deployment
changes separate from the local implementation and preview.
