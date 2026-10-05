# ChemMon improvement plan

Baseline: 5 October 2026. Compared with the FoodEx2 wiki in `LLM Knowledge Base`.
ChemMon has 70 topic pages, four immutable source PDFs and 38 passing tests.
The existing health check reports the documented CHEMMON03 duplicate.

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

- Create a scoped source-to-wiki review record with source/page evidence,
  findings, resolutions, corpus fingerprints and explicit coverage limitations.
- Audit page families against the full relevant source sections, including
  exceptions, recommendation strength, collection path and applicable year.
- Reconcile overlap with FoodEx2 using verified source/catalogue evidence.
- Establish an independently source-checked rule inventory for CHEMMON, GBR,
  LL, PRE and USE families. Existing wiki IDs alone cannot prove completeness.
- Add stale-audit reporting and a documented maintenance workflow. Structural
  success must never be presented as proof of semantic completeness.

Acceptance: reproducible review scope, actionable open findings, and drift
warnings when reviewed evidence changes. No exhaustive claim for unreviewed text.

## Milestone 3: measured answer quality

- Assemble reviewed selection and answer cases across SSD2, reporting domains,
  and the three additives/flavourings collection paths, including ambiguity
  and insufficient-evidence cases.
- Keep held-out evaluation questions separate from source ingestion.
- Add a dry-run evaluation harness and measure required-page recall, incorrect
  domain selection, answer correctness, citation support, latency and cost.
- Add situation-based `select_when` hints where they improve distinguishability.
- Compare selector and answer models with frozen evidence and recorded settings
  before changing defaults. Existing credentials stay unchanged in milestone 1;
  no live model benchmark is part of its offline verification.

Acceptance: a reproducible baseline with human-reviewed labels and stated limits,
followed by a demonstrated improvement over the same baseline.

## Milestone 4: downstream integration

- Add a bounded `/wiki/context-pack` response with evidence, provenance and a
  compact ChemMon-specific decision policy.
- Add inspectable selection results and per-request model overrides.
- Consider vector retrieval only after an endpoint comparison demonstrates a
  useful quality/latency trade-off. Keep Markdown the authored source of truth.

Acceptance: callers can consume evidence without an intermediate answer, and
integration tests enforce the same evidence budget and provenance contracts.

## Implementation boundaries

Preserve immutable sources and the existing topic structure. Reuse FoodEx2's
tested architectural patterns while keeping ChemMon's domain rules in Markdown.
Do not import FoodEx2-specific coding policies as ChemMon reporting rules.
Record unresolved source conflicts; do not guess catalogue codes. Keep deployment
changes separate from the local implementation and preview.
