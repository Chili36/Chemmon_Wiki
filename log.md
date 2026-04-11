---
title: "Wiki Log"
last_updated: "2026-04-11"
---

# Log

## [2026-04-11] retrieval | Phase timings + OpenAI selector (GPT-5.4-mini)

Infrastructure additions to make the next round of model/architecture experiments measurable, plus a first alternative selector to put the "Sonnet-for-planning, Haiku-for-execution" community pattern under test with a twist: use GPT-5.4-mini as the planner instead.

### Added: `phase_timings_ms` in `trace`

Every `/wiki/ask` response now reports a named breakdown of wall time:

```
phase_timings_ms:
  selector_total:   ms spent in the selector LLM call (+ index read)
  page_read:        ms spent reading selected pages from disk
  graph_expansion:  ms spent building related-neighbor summary blocks
  answerer_total:   ms spent in the answerer LLM call
  overhead:         FastAPI + JSON + network-to-client remainder
```

The numbers approximately sum to `request_wall_time_ms`. First observation on real traces: **~84% of wall time is the answerer call.** Everything else combined is ~16%. Selector tuning and retrieval architecture moves the 16%; the 84% is bounded by Sonnet's per-token generation speed. Useful calibration for what can and cannot be sped up.

### Added: `OpenAIWikiPageSelector` + factory dispatch

New class in `wiki_api/page_selector.py` that mirrors `AnthropicWikiPageSelector` via the OpenAI Responses API. Parses JSON from `response.output_text` rather than implementing OpenAI's tool-call format — simpler, and the existing selector prompt already specifies JSON fallback output. OpenAI SDK added to `requirements.txt` and `OPENAI_API_KEY` expected in `.env`.

`get_selector_runner()` in `app.py` dispatches on the `WIKI_SELECTOR_MODEL` env var: prefix `gpt-` → `OpenAIWikiPageSelector`, everything else → `AnthropicWikiPageSelector` (default). `_MODEL_PRICING_USD_PER_MTOK` gains a `gpt-5.4-mini` entry ($0.75 / $4.50 per M tokens).

### Eval: Haiku vs GPT-5.4-mini as selector (2026-04-11-115246)

Full 50-question eval, selector only changed, everything else held constant (graph expansion on, Sonnet answerer, 60s timeout). **Zero 503 errors this run** — confirmed the timeout fix holds.

| Metric | Haiku selector | **GPT-5.4-mini selector** |
|---|---|---|
| Hit rate | 65.2% (73/112) | **69.6% (78/112)** |
| Δ | — | **+4.4 pp, +5 facts** |
| Improved questions | — | 5 |
| Unchanged | — | 41 |
| Regressed | — | 4 |
| 503 errors | 3 | **0** |
| Avg tokens/query | 11,356 | 11,745 |
| Total cost | $1.57 | $1.70 |
| Avg latency | 8.6s | 8.6s |

### The +4.4 pp headline is mostly 503 recovery

Three questions that 503'd with Haiku completed successfully with GPT-5.4-mini — not because GPT is "better", but because the latency distribution shifted enough to stay under the 60s timeout. Q30 recovered 3/3, Q41 recovered 2/2, Q50 ran to completion but scored 0/5 (genuine content gap).

**Discounting 503 recoveries, the net content move is zero**: 5 improvements and 4 regressions, same total:

- **+** Q5 (documents to consult): 0 → 1/1
- **+** Q7 (why single SSD2): 1 → 2/3
- **+** Q45 (`evalInfo.restrictionException`): 0 → 3/3 — notable recovery, this was a persistent Haiku-side regression that no amount of graph expansion could touch
- **−** Q6 (SSD2/GDE2 precedence): 2 → 1/2 — the question graph expansion specifically fixed, now partially regressed again
- **−** Q17 (VMPR Plan 3): 2 → 1/2
- **−** Q32 (new VMPR categories): 1 → 0/1
- **−** Q47 (VMPR/pesticide classification algorithms): 2 → 0/3

**Selector choice changes which questions get right, not how many.** Haiku and GPT-5.4-mini have different blind spots. Some blind spots are addressable by graph expansion; others (like Q45) only clear with a selector model change. Suggests ensemble / A/B routing would beat either alone.

### Cost did not drop

Predicted GPT-5.4-mini would be cheaper based on per-token pricing ($0.75 input vs $1.00 for Haiku). Eval shows otherwise: **$1.70 total vs $1.57, +8%**. Two reasons:

1. The selector is ~2k tokens of ~11k total per query. Per-token price difference is rounding error.
2. GPT picked slightly larger page sets on a few queries, pushing the answerer input up.

**The biggest cost lever is the answerer model**, not the selector model. Swapping selectors moves pennies. If cost is the target, the interesting experiment is cheaper answerer, not cheaper selector.

### What phase timings revealed

Per-query wall time is bounded by `answerer_total`, which in turn is bounded by Sonnet's generation speed at ~50-80 tokens/second for ~500-token outputs. Typical breakdown:

```
selector_total:  ~2s    (17%)
page_read:       ~0ms   (0%)
graph_expansion: ~7ms   (0%)
answerer_total:  ~10s   (84%)
overhead:        ~2ms   (0%)
```

The only levers that materially move wall time:

1. **Streaming API** — doesn't reduce total, improves perceived TTFT from 10s to ~1s
2. **Swap Sonnet answerer to Haiku** — ~2-3× speedup on generation, some accuracy cost
3. **Smaller answerer input** — marginal; Sonnet throughput is output-bound, not input-bound

Selector tuning, retrieval architecture, graph expansion — all move the other 16%. Worth remembering when deciding where to spend effort next.

### Open items

- **Q6 regression under GPT selector**: we fixed this via graph expansion for Haiku; GPT picks differently and partially re-introduces it. Worth understanding why — the GPT selector's page pick for Q6 doesn't include `chemmon-overview.md` and expansion from its chosen pages doesn't surface the precedence content.
- **Ensemble or A/B routing**: given the overlap is only ~80% between Haiku and GPT selector choices, a simple ensemble (run both, merge page sets) might beat either alone. Speculative.
- **Sonnet selector** (the community pattern we haven't tried): the research note flagged this as the "correct" community convention. Still untested. Maybe the next thing to run.
- **Answerer model experiments**: the real cost and latency live in the answerer. Haiku answerer on a subset of questions could halve both latency and cost, at unknown accuracy cost.

## [2026-04-11] retrieval | Graph expansion (Option C) + fixed wiki cost tracking

Two architectural changes in the same session, driven by the reality-check conversation and a follow-up web-research pass showing that graph expansion at retrieval time is an emerging community pattern for Karpathy-style wikis. Both land together so the eval comparison sees the full picture.

### Fix 1: total_cost_usd in the wiki ask trace

Earlier eval runs reported `cost=0.0` for every wiki-mode query because the chemmon-wiki service never emitted a cost field, and `document-chat` hardcoded zero when routing wiki responses back to callers. Every wiki-vs-RAG cost comparison to date was asymmetric — RAG was measured, wiki was blind.

**Changes:**
- `wiki_api/app.py`: added a per-model pricing table covering Haiku 4.5, Sonnet 4.6, Opus 4.6, and the 3.7 Sonnet fallback. New `_compute_call_cost()` helper reads the per-call token summaries (input/output split) and returns USD. Aggregated selector + answerer cost is written to `trace.total.total_cost_usd`. Unknown models contribute zero rather than crash.
- Paired fix in `guidance_with_claude/apps/document-chat/backend/app.py`: the chemmon-wiki handler now reads `trace.total.total_tracked_tokens` and `trace.total.total_cost_usd` from the wiki response and passes them into the ChatResponse. The previous code read `trace.token_summary.total_tracked_tokens`, which never existed in the wiki's trace structure.

**Verified via live query**: 11,226 total tokens, $0.031648 cost for a single "What is progId used for?" question. Haiku selector $0.0035, Sonnet answerer $0.0286.

### Fix 2: Graph expansion — Option C (summary-only related-neighbor injection)

**Problem**: The 2026-04-11-010813 eval showed 5 regressions from the first ingest pass (Q2, Q5, Q6, Q18, Q45). Manual inspection of Q6 revealed the selector had picked a page *adjacent* to the one containing the precedence-rule answer — not the page itself. Yesterday's answer came from `chemmon-overview.md`; today's selector picked `ssd2-data-model.md` instead. Same wiki content, different selection.

**Decision**: use curated `related:` frontmatter edges (depth 1, no transitive expansion) and inject SHORT SUMMARIES of each neighbor, not full page content. Summaries come from the `index.md` one-line descriptions already parsed into `WikiPage.summary`. This is Option C from the graph-expansion discussion — documented in `docs/research/2026-04-11-emerging-llm-wiki-patterns.md`.

**Rationale for summary-only over full-page**:
- Full-page expansion would push per-query tokens from ~8k to ~20k — blowing past RAG's typical ~8-10k injection budget on this workload
- Summaries are ~50-150 tokens each; 8 of them adds ~400-600 tokens total
- The answerer gets "neighbor exists, here's what it's about" — enough context to surface the adjacent fact when the summary contains it, without full content bloat

**Changes in `wiki_api/app.py`**:
- New `_expand_related_summaries()` helper: walks each selected page's `related:` frontmatter list, deduplicates against the selected set, reads each neighbor's title + summary, builds short context blocks prefixed with `[RELATED CONTEXT — brief summary only...]`. Hard caps: max 8 neighbors, ~2000 expansion tokens.
- `AskRequest` gains `use_graph_expansion: bool = True` for A/B testing.
- `ask_question()` appends expansion blocks to the answerer's pages input when enabled.
- Trace emits `graph_expansion.enabled`, `graph_expansion.neighbors_count`, and `graph_expansion.neighbors_added` so every eval run records what was pulled in.

### Eval run 2026-04-11-094003

Rerun the 50-question ChemMon test set with both fixes live (Haiku selector, Sonnet answerer, graph expansion on, cost tracking fixed).

**Headline**: 65.2% (73/112) — **identical** to the previous run.

**But the headline is a lie**, because the 503 distribution changed:
- Previous run (2026-04-11-010813): 503s on Q5 and Q13 (3 facts lost)
- This run (2026-04-11-094003): 503s on **Q30, Q41, Q50** (10 facts lost)

Q30 scored 3/3 in the previous run and 0/3 this run because document-chat returned a 503, not because graph expansion regressed. Q41 same pattern (2/2 → 0/2). Both have `answer_tokens: 0` confirming they never got an answer generated.

**Fair comparison — questions that completed successfully in both runs**:

| Metric | Previous | With expansion | Delta |
|---|---|---|---|
| Facts hit (on 99 common facts) | 68 | **73** | **+5** |
| Hit rate (on 45 common questions) | 68.7% | **73.7%** | **+5.0 pp** |

Graph expansion produced a genuine **+5 percentage point gain** on the questions where both runs completed. The flat headline masked the improvement because the 503 noise cut the other way.

**Questions that graph expansion fixed**:
- **Q6** (SSD2/GDE2 precedence): 0/2 → 2/2 — the specific regression that motivated this work; fixed cleanly.
- **Q2** (reporting domains covered): 1/3 → 3/3 — selector picked a different page; summary of `chemmon-overview.md` surfaced the domain list.
- **Q32** (new VMPR categories insects/reptiles/casings): 0/1 → 1/1 — selector picked an adjacent page; matrix-page summary carried the fact.

**Zero real regressions** from graph expansion. The two apparent regressions (Q30, Q41) are both 503 infrastructure failures, not content or retrieval misses.

### Token and cost reality — honest numbers for the first time

With the cost tracking fixed, we finally have apples-to-apples wiki-vs-RAG numbers:

| Metric | Wiki (expansion on) | RAG baseline | Ratio |
|---|---|---|---|
| Avg tokens / query | ~12,100 | ~8,400 | 1.44× |
| Avg cost / query | **$0.031** | $0.068 | **0.46×** |
| Hit rate | 65.2% | 84.8% | 0.77× |
| Cost per accuracy point | **$0.00048** | $0.00080 | **0.60×** |

**Wiki is ~55% cheaper per query than RAG** and **~40% more cost-efficient per accuracy point**, despite using 44% more tokens on the input side. The cost gap comes from the Haiku+Sonnet mixed tier (Haiku selector at $1/M input) vs RAG's all-Sonnet path.

The initial worry — "we're using 20k tokens for what RAG handles in a fraction" — turned out to be wrong. With honest measurement, wiki is in the same order of magnitude as RAG on tokens and materially cheaper on dollars. The gap is accuracy, not efficiency.

### Still-zero questions — content gaps that graph expansion cannot fix

Questions that remained 0/N after this run (excluding the 503s):

- Q4 transmission timing — partial content exists in `chemmon-background.md` but not matching the specific facts the test wants
- Q18, Q19 pesticide EU MACP / MANCP plan flagging — multi-criteria Table 2 logic, content exists in `ssd2-elements-programme.md` but the selector/answerer combo isn't extracting it cleanly
- Q28 VMPR F01/F02 always-present rule — content exists in `ssd2-elements-matrix.md`
- **Q36 drinking water data reporting** — genuine content gap, PDF p42 never ingested
- Q45 `evalInfo.restrictionException` — mentioned in cross-references but not given its own definition
- **Q48 business rules grouping** — wants meta-structure summary; needs an explicit "how the rules are organized" page
- Q49 domain flag values 0/1/2/3 — may not exist in the PDF prose at all
- **Q50 end-to-end DCF validation workflow** — genuine gap, section 10 not ingested

Three of these (Q36, Q48, Q50) are real content gaps that a targeted ingest pass could close. The rest are retrieval-side issues that graph expansion didn't touch.

### Open investigation: the 503 storm

Three questions failed with document-chat returning 503 Service Unavailable in this run, on a different set of questions than the previous run. Same server, same code, flaky behavior. Q30 and Q50 are both large multi-fact questions; Q41 is medium complexity. Possible causes to investigate:
- Chemmon-wiki answerer timeout on long questions (graph expansion increases context size which might push response time past a threshold)
- Document-chat client timeout
- Rate limiting somewhere upstream

Worth diagnosing before any further eval runs, because 503 variance is drowning real accuracy signal across runs.

### What this session established

- **Graph expansion works.** Option C (summary-only, curated edges) produces measurable accuracy gains on exactly the questions where selector drift caused regressions, without blowing the token budget.
- **Wiki is cheaper than RAG.** With honest cost accounting, wiki costs roughly half what RAG costs per query and is more efficient per accuracy point. The earlier worry about token efficiency was based on a measurement bug.
- **The accuracy ceiling is still 65-75%.** Closing the remaining 10-15 percentage points to RAG requires targeted content ingest (Q36, Q50) and content restructuring for the meta-questions (Q48, Q49), not more retrieval architecture work.
- **The 503 storm needs to be fixed before further eval runs.** Otherwise every comparison is contaminated by which questions happened to 503 that day.

## [2026-04-11] ingest | Section 1 Background + Section 2 SSD2 element reference

Second ingest pass driven by the diagnosis from the 2026-04-10 eval run where the wiki scored 36.6% (41/112 facts) vs RAG's 84.8% (95/112 facts). The failure modes were:

1. **Missing per-element definitions** — the existing `ssd2-data-model.md` enumerated the logical structure but named only ~8 of the ~88 SSD2 elements; questions about specific fields like `progId`, `progLegalRef`, `CCalpha`, `paramType` got "the wiki doesn't mention this" answers.
2. **Missing background/rationale** — questions about **why** the single SSD2 collection exists, **why** free-text was reduced, and similar historical "why" questions had no target content in the wiki.
3. **Definitions alongside rules** — for fields that had business rules captured (e.g. `progLegalRef` in CHEMMON68), the rules were in the wiki but the field's own purpose statement was not.

**Ingested directly from the source PDF** (ChemMon 2026, pp. 5-76), **not from the test set** — to keep the eval honest. Six new pages (2094 lines total):

- `chemmon-background.md` — rationale for single SSD2 consolidation, FCM exclusion, compound element flexibility, catalogue browser, Open Data / Transparency / free-text reduction, revision cadence, meaning of "residue". (Source: pp. 5-10)
- `foodex2-facets.md` — complete F01-F33 per-domain facet reference. (Source: Table 4, pp. 43-51)
- `ssd2-elements-programme.md` — progId, progLegalRef, sampStrategy, progType + Table 2 valid combinations. (pp. 17-26)
- `ssd2-elements-sampling.md` — sampMethod, sampler, sampPoint, sampEventId, sampUnitType, sampUnitSize, sampId, sampCountry, date elements, origSampId. (pp. 27-32)
- `ssd2-elements-matrix.md` (expanded) — sampMatCode VMPR/feed/non-food/insect coding plus sampMatText, origCountry, sampAnId, anMatCode, anMatText. (pp. 32-36, 56)
- `ssd2-elements-analysis.md` — analysisY, anPortSeq, labId, labAccred, labCountry, paramType, paramCode, paramText, anMethRefId, anMethType, anMethCode. (pp. 57-64)
- `ssd2-elements-result.md` — resId, accredProc, resUnit, resLOD, resLOQ, CCalpha, CCbeta, resVal, resValRec/Corr, exprResPerc/Type, resQualValue, resType (including AWR), resValUncert, resInfo.notSummed. (pp. 64-73)
- `ssd2-elements-evaluation.md` — evalLowLimit, evalLimitType, evalCode, actTakenCode, evalInfo.conclusion/com. (pp. 73-76)

**Eval result (guidance_with_claude/tests/manual/chemmon_eval_runs/2026-04-11-010813):**

- **Wiki hit rate: 36.6% → 65.2%** (+28.6 pp, +32 facts)
- **25 of 50 questions improved**; 20 unchanged; 5 regressed
- **RAG baseline** (from 2026-04-10 run): 84.8% — wiki still ~19.6 pp behind
- **2 infrastructure failures** (Q5, Q13 hit transient 503s from document-chat, unrelated to wiki content)

**Notable wins** — all of these went from 0 hits to full hits after the ingest:

- Q8 (Why free-text reduced) — 0/3 → 3/3
- Q9 (What is progId for?) — 0/2 → 2/2
- Q10 (progId in annual reports) — 0/3 → 3/3
- Q11 (What is progLegalRef for?) — 0/2 → 2/2
- Q25 (Why is sampling date mandatory?) — 0/2 → 2/2
- Q27 (How detailed should sampMatCode be?) — 0/2 → 2/2
- Q37 (What do paramType P002A/P004A/P005A mean?) — 0/3 → 3/3
- Q41 (What do CCalpha and CCbeta mean?) — 0/2 → 2/2

**Notable regressions** — adding content changed which pages the selector picks, and 5 questions got worse:

- Q2 (Which reporting domains) — 3/3 → 1/3
- Q6 (Precedence when SSD2/GDE2 conflict) — 2/2 → 0/2 *(the fact we ingested on 2026-04-10 for test #5)*
- Q18 (How pesticides EU MACP flagged) — 1/3 → 0/3
- Q45 (evalInfo.restrictionException) — 3/3 → 0/3

These regressions happened with the same wiki content as yesterday. The LLM selector is making different choices now that `index.md` has grown from ~30 to ~45 catalog entries — a classic scaling issue where more candidates can mean noisier selection. The wiki content is still correct; the selector just isn't pulling it in for these specific questions.

**Remaining content gaps** (questions that still scored 0 after the ingest):

- Q4 (transmission timing) — partially in background but not matching
- Q13 (503 transient) and Q5 (503 transient) — not content issues
- Q18, Q19 (Plan flagging logic) — covered in programme page Table 2 but selector miss
- Q28 (F01/F02 always present for VMPR) — covered in matrix page
- Q32 (new VMPR categories: insects/reptiles/casings) — covered in matrix page
- Q36 (drinking water data) — **real gap**, section on p42 not ingested
- Q48 (how business rules grouped) — wants a meta-structure summary
- Q49 (domain flag values 0,1,2,3) — may not exist in PDF prose
- Q50 (end-to-end DCF validation workflow) — **real gap**, section 10 not ingested

**What this ingest did and did not demonstrate:**

- **Did** — the diagnosis from the first eval was correct. The wiki was missing specific content; adding it from the source PDF directly recovered exactly the facts the test asked about.
- **Did** — the PDF-driven (not test-driven) ingest approach works. The content was extracted by systematically reading sections 1 and 2 of the source, not by cherry-picking for the test.
- **Did not** — close the gap to RAG. The wiki is still ~20 points behind; several remaining gaps are real content not yet captured, and the 5 regressions indicate the LLM selector has a scaling ceiling that more content alone cannot fix.
- **Did not** — prove wiki is the right tool for this workload. The 50-question test set is heavy on lookup questions where RAG's whole-PDF recall wins structurally.

Next step is a reality check on whether to continue closing content gaps, work on the selector regressions, or accept the 65% result and stop.

## [2026-04-10] refactor | Patterns refactor (closes #1)

Aligned the repo with community best practices that have crystallized around Karpathy-style LLM wikis: compiled layer, short opinionated files, selective injection via the LLM selector, schema + frontmatter, compiler-analogy layer naming.

**Structural changes:**

- **Split `business-rules.md`** (27 KB / 299 lines / 100+ rules) into **nine slice files** under `wiki/chemmon-guidance/business-rules-*.md`: gbr, cross-cutting, vmpr, pesticide, contaminant, additives, baby-food, legal-limits, 2026-changes. Rule text preserved verbatim 1:1 — IDs, severities, source comments, and citations unchanged. Only the hosting file changed.
- **Added a ninth slice (`business-rules-contaminant.md`)** beyond the original 8-file plan: 19 CONT-only CHEMMON rules had no clean home otherwise. Contaminant is a first-class domain in the wiki alongside VMPR, pesticide, additives, and baby-food.
- **`business-rules.md` rewritten as a short hub page** (~40 lines) linking to the 9 slices. Preserves `[[business-rules]]` as a valid backlink target for generic queries.
- **Renamed `raw/chemmon-guidance/` → `wiki/chemmon-guidance/`** to match the pattern-language tier naming. `chemmon_docs/` remains the raw PDF source layer.
- **Sliced files ARE the distilled layer** for rule-lookup-shaped flows. No separate `distilled/` tier added — that's only worth building if a task-shaped flow (e.g. "FoodEx2 code this roasted coffee") becomes painful.

**Schema and frontmatter:**

- **Added `SCHEMA.md`** defining five page types (overview, reference, domain-guide, rule-reference, hub), seven domain values, required frontmatter fields, wiki-link convention, source-comment convention, and rule ID conventions.
- **Enriched frontmatter on all 18 wiki pages** with `type` and `domain` fields per schema.

**Page selection:**

- **Kept the LLM selector as the only selection path.** An earlier iteration of this branch added a deterministic keyword/rule-ID fast-path in `wiki_api/app.py` to short-circuit the selector call. It was removed before merge because it pushed routing intelligence out of the wiki layer and into code — the fast-path's slice mapping could silently drift from the actual files, keyword patterns weren't derivable from frontmatter, and adding a new routing rule meant editing `app.py` instead of the wiki. Premature optimization for a problem the LLM selector doesn't actually have at this scale.
- The slice split still helps the LLM selector significantly: questions about baby food or acrylamide now get a ~30-line or ~50-line file as context instead of the 27 KB business-rules dump.

**Health check:**

- **Added `tools/health_check.py`** validating frontmatter schema compliance, resolving every `[[wiki-link]]`, checking CHEMMON rule-ID coverage across slice files, and detecting stale `raw/chemmon-guidance/` prose references. Runnable standalone or via `tests/test_health.py` in CI.
- **Known source bug surfaced as a warning**: the EFSA guidance defines `CHEMMON03` twice with different text (once as an analytical method rule, once as a PPP country consistency rule). Both entries preserved verbatim in the slice files; the health check flags it as a warning (not error) for human review.

**Tests:**

- Updated `tests/test_wiki_store.py` and `tests/test_app.py` to check broader membership assertions (16+ pages) instead of hardcoded `"business-rules.md"` lookup.
- Added `tests/test_health.py` wrapping the health check for CI.
- Full suite: **19 tests passing, 0 failing, 1 warning** (the expected CHEMMON03 duplicate).

**Explicitly out of scope for this pass:**

- No deterministic fast-path for page selection — see note above.
- No second distilled tier (task-oriented decision files).
- No idea file capturing the pattern itself — this is a domain repo.
- No `WikiStore` subdirectory support (flat filenames sidestep the work).
- No static viewer changes.
- No rename of `chemmon_docs/` → `raw/`.
- No rule rewording, renumbering, or severity changes.

## [2026-04-07] setup | Initial ChemMon wiki repo

- Created the ChemMon wiki repo following the LLM wiki pattern.
- Set up empty source and guidance directories.
- Added wiki API with a single Q&A endpoint at /wiki/ask.

## [2026-04-07] ingest | Initial ChemMon guidance compilation

- Created seven topic-oriented markdown pages under `wiki/chemmon-guidance/` from the ChemMon 2026 reporting guidance and the SSD2 standard specification.
- Seeded pages for ChemMon overview, SSD2 data model, FoodEx2 in ChemMon, business rules (CHEMMON01-109), VMPR reporting, contaminant reporting, and food additives/flavourings reporting.
- Kept the source PDFs unchanged in `chemmon_docs/`.
- Updated `index.md` with the new page catalog.

## [2026-04-07] maintenance | Writing quality pass

- Fixed incorrect F27 description in foodex2-in-chemmon.md (was "brand or marketing type", should be "source commodity").
- Corrected CHEMMON100 and CHEMMON102 descriptions in vmpr-reporting.md to match the actual business rule definitions.
- Moved copper-specific F20 requirements from contaminant-reporting.md to a new pesticide-reporting.md page, since CHEMMON90_a/b are PPP-domain rules.
- Added pesticide-reporting.md covering legal references, sampling strategies, copper facet codes, and PPP-domain business rules.
- Added page number citations to contaminant-reporting.md source comments.

## [2026-04-08] ingest | Full-document second pass (pages 21-156)

- Expanded business-rules.md from 30 rules to 100+ rules across GBR, CHEMMON, and legal limit categories, organized into 9 subcategories.
- Added baby-food-reporting.md covering VMPR exclusion (CHEMMON55/63), accepted domains, classification codes, and legal limit basis.
- Expanded vmpr-reporting.md with feed/water coding, processed products with F33, wild game exclusions, insects as novel food, and baby food exclusion cross-reference.
- Expanded contaminant-reporting.md with 9 new substance sections: dioxins/PCBs, BFRs, arsenic, chlorates, bisphenol, PAHs, 3-MCPDs, mineral oils, and nitrates.
- Expanded food-additives-reporting.md with result reporting rules, 4 new worked examples, restriction/exception coding, and conclusion reporting.
- Updated index.md with revised page descriptions and the new baby food page.
