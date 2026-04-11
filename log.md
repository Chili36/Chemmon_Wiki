---
title: "Wiki Log"
last_updated: "2026-04-11"
---

# Log

## [2026-04-11] ingest | Section 4 Table 8: contaminant metadata requirements

Patched [[contaminant-reporting]] with durable, reusable Table 8 rules (metadata requirements/recommendations) instead of copying the full table. Added a compact "Relevant Business Rules" anchor list to improve retrieval.

Captured (high-signal) Table 8 guidance for:

- Mycotoxins: matrix-detail note for grains, organic vs conventional facet F21, recovery/uncertainty, moisture, and reconstitution protocol.
- Dioxins/PCBs: congener-level reporting emphasis, fat/dry-basis notes, fish origin, and reconstitution protocol.
- Furan/alkylfurans: as-consumed preparation details (M.20) and the `sampMethod` hook (N011A is already in the sampling element page).
- Arsenic/rice: processed vs unprocessed (F28), dehydrated note, rice/algae ingredient notes.
- Mineral oils: moisture + carbon-number distribution note and the pointer to JRC guidance.
- Metals/nitrates: recovery and expanded uncertainty recommendations, plus the mercury matrix-detail note for fish/seafood.

## [2026-04-11] ingest | Sections 5-11: flags, catalogues, legal limits, reports, validation workflow

Ingested the previously skipped non-element sections of the ChemMon 2026 guidance into small reference pages, and corrected a couple of high-impact FoodEx2/copper/drinking-water details that were either missing or mis-stated.

**Added reference pages (new):**

- `chemmon-matrix-classification-algorithms.md` — where EFSA’s VMPR/pesticide matrix-classification algorithms live and what they do (Section 5).
- `controlled-terminology-catalogues.md` — catalogue/hierarchy overview (LEGREF/PARAM/MTX/etc) and LEGREF specificity guidance (Section 7).
- `legal-limits-database.md` — scope/limitations of EFSA’s Legal Limits Database (Section 8).
- `reporting-flags.md` — domain-flag values (0-3), “in-domain” logic, and examples (Section 9).
- `chemmon-reports.md` — which dashboards/reports exist and which flag values are included (Section 10 / Table 13).
- `data-validation-and-acceptance.md` — ack → BR validation → submit → accept/reject flow and the post-acceptance update constraint (Section 11).

**Patches / refactors:**

- Fixed copper sample-preparation facet guidance (F20/F28) so pesticide vs contaminant coding is no longer inverted, and aligned CHEMMON90_a wording to “F20 (part-consumed-analysed) and/or F28 (process)”. (ChemMon 2026 pp. 40-41; Table 10)
- Added the missing drinking-water recommendation (FoodEx2 `A03DK`) under matrix coding + pesticide/contaminant guidance, and removed the misplaced drinking-water note from additives/flavourings. (ChemMon 2026 p42)
- Moved additives/flavourings-specific F33/F03 guidance out of the global facet reference (`foodex2-facets.md`) into [[food-additives-reporting]] to keep `foodex2-facets.md` closer to a Table 4-derived facet reference.
- Updated `index.md` summaries and curated `related:` links so the selector can find the new pages and graph expansion can pull them in when adjacent pages are selected.

## [2026-04-11] process | Mental-model correction: wiki-as-ontology vs wiki-as-archive

A retrospective on the day's ingest work. The user reviewed my approach and the Codex2 system prompt for the FoodEx2 wiki side by side, and the delta made an error I hadn't spotted visible. All of today's ingest work was done under the wrong mental model.

### The correct framing (Codex2's system prompt, quoted verbatim)

> Your job is not to summarize an entire PDF.
> Your job is to update the wiki with durable, reusable knowledge.

### The wrong framing (what I was actually doing)

My internal workflow was: "take the ChemMon 2026 PDF and turn its sections into wiki pages, prioritizing the sections where the current eval is failing." That is summarizing the PDF, organized by topic and filtered by eval score. It is not what this wiki is for.

### The conceptual difference, named

**Wiki-as-ontology (correct)**. The wiki is a set of small, topic-scoped atoms of durable knowledge about the domain. Sources (PDFs, clarifications, annual updates) are **inputs** that feed into atoms. A new source rarely becomes a new page — it more often patches existing pages, adds a cross-reference, or bumps a `last_updated` field. New pages are created only when a genuinely new concept appears that has no existing home. The wiki's shape is determined by the **domain's concepts**, not by the source's section structure.

**Wiki-as-archive (what I did)**. The wiki is a topic-organized restructuring of the source PDF. Sections of the PDF become pages. New documents become new pages. The wiki's shape mirrors the source's shape. Completeness is measured by "have we written about every section?" rather than "does the wiki cover every durable concept the domain needs?"

The archive mindset explains every weird decision the day produced:

- **Six new element-reference pages** (`ssd2-elements-programme.md`, `-sampling.md`, `-matrix.md`, `-analysis.md`, `-result.md`, `-evaluation.md`) instead of expanding the existing `ssd2-data-model.md`. An archive mindset says "Section 2 of the PDF covers elements, so I'll make an 'elements' family of pages." An ontology mindset says "the existing page covers the SSD2 data model; I should patch it with the missing element definitions, splitting only when the page gets too big."
- **Pages walking the source in document order.** `ssd2-elements-result.md` is structured as M.01 → M.02 → M.03 ..., mirroring the PDF's section numbering. An ontology mindset would have one small page per decision (`resloq-when-required.md`, `exprres-fat-weight-rule.md`, `ccalpha-ccbeta-vmpr-rule.md`) with rules leading and context trailing.
- **Skipping PDF Sections 3-11** because the current eval didn't probe them. An archive mindset says "those sections don't match current failure modes, deprioritize." An ontology mindset says "those sections define workflow, catalogues, legal limits, validation — all durable concepts the wiki must cover, independent of what any single test happens to probe."
- **No structure scan pass.** Linear read, linear write. A principled ingest does three passes: structure scan → rule extraction → gap sweep. I did only the middle one.
- **Document-order narrative preserved.** Sections like "Wild animal VMPR samples coding" from the source PDF became verbatim subsections in `ssd2-elements-matrix.md`, because "it's in the source." An ontology mindset would compress that to a one-line rule (`for wild game in VMPR, F21 must be explicitly set to A07RY`) plus a cross-link to the rule that enforces it.

### Why I defaulted to the archive mindset

Probably three reasons, none of them excuses:

1. **Training bias.** Summarizing a long document is a common task shape and the default answer is "read section by section, write section by section." The archive mindset is the lowest-energy interpretation of an ingest task.
2. **Satisficing.** Archive-style ingest feels productive because progress is measurable — lines written, pages created. The metric rewards quantity over shape. An ontology-style ingest often looks like *fewer* lines and *fewer* new pages, which feels like less work but is actually harder.
3. **Eval anchoring.** Once I had an eval score to move, I anchored on it and framed ingest as "fill the gaps this test has" rather than "complete the knowledge base the domain needs." The eval became a guidance signal when it should have been a measurement signal.

### Concrete corrective action

1. **New file: `INGEST_WORKFLOW.md`** at the repo root. Adapted from Codex2's FoodEx2 system prompt, specialized for this wiki's structure (CHEMMON / GBR / LL business rule tiers, domain slice files, the five page types defined in `SCHEMA.md`, etc.). Contains: the three-pass workflow (A structure scan → B rule extraction → C gap sweep), per-page rules, when-to-patch vs when-to-create guidance, the exact anti-patterns from today's ingest as teaching examples, and explicit "do not" rules (don't read test sets during ingest, don't optimize for a specific test, don't create a new page just because the source has a new section, don't skip Pass A).

2. **This log entry** so the next session starts from a corrected frame rather than the default summarize-the-PDF reflex.

### What this correction does NOT do

It does not retroactively fix the pages that were created under the wrong mental model. `ssd2-elements-programme.md`, `-sampling.md`, `-matrix.md`, `-analysis.md`, `-result.md`, `-evaluation.md`, `foodex2-facets.md`, `chemmon-background.md` all remain as-is. They contain correct content but wrong shape — too big, document-order, created-instead-of-patched. A principled next pass would likely refactor them into smaller rule-first atoms and consolidate back toward the existing `ssd2-data-model.md`. That refactor is a separate piece of work, not part of this correction.

It also does not retroactively ingest PDF Sections 3-11. Those are still missing from the wiki. The concept eval showed them as ~13 facts of missing coverage (catalogues, Legal Limits database, reporting flags, validation workflow).

### What a correct ingest pass would look like

For reference, so the next session knows what to build toward:

1. **Pass A (structure scan)**: walk all 156 pages of the ChemMon 2026 PDF. Build a map of every section, classify each as rule-bearing / narrative / procedural / historical. Identify which existing wiki pages each rule-bearing section patches. Expect ~2-3 new pages at most for a pass of this size, not 6-8.
2. **Pass B (rule extraction)**: for each rule-bearing section, extract definitions / rules / tie-breaks / exceptions into target pages in rule-first order. Sections 3-11 get covered because they contain durable domain concepts, not because they match a failure mode. Each page stays narrow — one concept, one decision.
3. **Pass C (gap sweep)**: check orphans, missing cross-links, stale frontmatter, index updates, contradictions.
4. **Final state**: a wiki where every durable ChemMon concept has a small, retrieval-optimized page, the eval measures coverage rather than drives it, and the answerer sees high-signal-density context per selected page.

### Open items after the correction

- The wrongly-shaped pages from today are still in the wiki. Refactor-vs-leave-alone is a future decision.
- Sections 3-11 of the ChemMon 2026 PDF are still not covered. A pass done under the new `INGEST_WORKFLOW.md` guidance would address this.
- Infrastructure work from today (graph expansion, phase timings, GPT-5.4-mini selector, token cost attribution) is unaffected — those are retrieval-layer changes, architecturally separate from the ingest question.
- The 4 retrieval misses on content that *does* exist in the wiki (Q7, Q14, Q15, Q46 from the concept eval) suggest that even with the wrong-shape pages, some of the failure is in the selector / answerer, not the content.

## [2026-04-11] eval | General-concepts test set: RAG 92.4% vs Wiki 78.5%

First run of a new 50-question test set designed to probe conceptual / definitional knowledge ("what is X", "what does X describe", "why X") rather than narrow lookup. The intent was to measure whether the wiki's curated structure helps on the kind of question wikis are theoretically supposed to be good at.

Test set: `chemmon_testset_50_general_concepts.json` (cold — deliberately not read before running, to avoid contaminating the ingest direction).
Eval run: `guidance_with_claude/tests/manual/chemmon_eval_runs/2026-04-11-133157`
Configuration: Sonnet 4.6 answerer, GPT-5.4-mini selector, graph expansion on, 60s timeout.

### Headline result

| Mode | Facts hit | Facts total | Hit rate | Cost | Avg latency |
|---|---|---|---|---|---|
| rag | 133 | 144 | **92.4%** | $2.63 | 8.77s |
| wiki | 113 | 144 | **78.5%** | $1.57 | 8.81s |

**Gap: 13.9 percentage points, RAG winning.** Both systems scored higher on this test than on the original lookup test (RAG 84.8%→92.4%, Wiki 69.6%→78.5%), suggesting the concept test is easier overall — possibly because "what is X" questions are more forgiving than the exact-fact lookup questions in the original set.

### The shape of the gap is telling

| Bucket | Count | Note |
|---|---|---|
| Both perfect (tied at 100%) | 29 | 58% of the test |
| Wiki > RAG | 6 | e.g. Q31 origCountry, Q37 anMethType, Q41 resLOQ, Q44 evalCode |
| Partial tie (same hit count) | 1 | |
| RAG > Wiki by 1 fact | 7 | minor gaps, mostly recoverable via selector tuning |
| RAG > Wiki by 2+ facts | 7 | **the entire headline gap lives here** |

**35 of 50 questions (70%) are ties or wiki wins.** On the content we've ingested, the wiki performs at parity with or better than RAG. The 13.9-point gap is concentrated in seven "catastrophic miss" questions, not spread across the test set.

### Where the catastrophic misses live

Seven questions where wiki scored 0-1 while RAG scored 2-4:

| Q | Wiki / RAG | Question | Root cause |
|---|---|---|---|
| Q7 | 0/3 vs 2/3 | What problem are harmonised ChemMon business rules trying to solve? | **Retrieval miss** — content exists in `chemmon-background.md` and `business-rules.md` but the selector doesn't pull them in the right combination |
| Q14 | 0/3 vs 3/3 | Why use the most specific LEGREF code? | **Retrieval miss** — content exists in `ssd2-elements-programme.md` |
| Q15 | 0/2 vs 2/2 | What does sampStrategy describe? | **Retrieval miss** — we have a full `sampStrategy` section in `ssd2-elements-programme.md` |
| Q46 | 0/3 vs 3/3 | Three groups of business rules in ChemMon? | **Retrieval miss** — `business-rules.md` literally opens with "organised into three tiers: GBR, CHEMMON, Legal Limit" |
| Q47 | 0/3 vs 3/3 | Controlled terminology catalogues? | **Content gap** — Section 7 of PDF, never ingested |
| Q49 | 0/3 vs 3/3 | Reporting flags in the EFSA sDWH? | **Content gap** — Section 9 of PDF, never ingested |
| Q50 | 0/4 vs 4/4 | Data validation and acceptance workflow? | **Content gap** — Section 10-11 of PDF, never ingested |

**Four of seven are real content gaps in PDF sections that were unilaterally skipped during the second ingest pass.** Those cost about 13 facts. The other three are retrieval failures on content that exists in the wiki but the selector isn't finding in the right combination — particularly painful because Q46 asks about "three groups of business rules" and `business-rules.md` answers that exactly in its first three bullets.

### Projected ceiling after closing the content gaps

If Sections 7-11 of the PDF are ingested (catalogues, Legal Limits, reporting flags, validation workflow), the three 0/N content-gap questions (~13 facts) should largely recover. The four retrieval misses (Q7, Q14, Q15, Q46) are harder — they need selector tuning or different graph expansion, not more content.

Rough projection: 113 + ~13 content-gap recoveries + 2-4 retrieval fixes = **128-132 / 144 ≈ 89-92%**. That lands at or within a couple of points of RAG's 92.4%, on this test set.

### What this does and doesn't prove

**Proven**:
- On content the wiki has ingested, it matches or beats RAG on conceptual definitions (35/50 questions)
- The remaining gap is ~80% content-coverage and ~20% retrieval-quality, NOT a wiki-approach failure
- The wiki can realistically reach RAG parity on this test set with ~1-2 hours of targeted ingest

**NOT proven**:
- Whether wiki beats RAG on **true cross-cutting synthesis** (rule interactions, multi-domain trade-offs, conflict resolution). This test set is definitional, not relational. Those questions still haven't been written or run.
- Whether wiki holds its accuracy as the wiki grows to cover the full PDF (scaling behavior untested)

### Process finding

The second ingest pass (earlier today, commit `f3e0570`) explicitly skipped PDF Sections 3-11, covering only Sections 1-2 (background + SSD2 element reference). The decision was framed in the commit as "the biggest failure modes are covered, running the eval is the highest-value next step" — i.e. optimizing for specific failure modes in the first eval rather than completing the wiki. This concept test surfaces exactly which facts that skipping decision cost. See the conversation log for the conversation where the user called this out as a process issue: optimizing for eval score instead of wiki completeness is not what the wiki is *for*.

### Open items

- **Ingest pass 3**: Sections 3-11 of the PDF (baby food specifics, contaminant specifics, classification algorithm, business rules narrative, catalogues, Legal Limits, reporting flags, validation workflow). ~1-2 hours of focused work. Should close most of the content gaps surfaced by this test.
- **Q46 retrieval failure**: diagnose why the selector doesn't pick `business-rules.md` for a "three groups of business rules" question — the hub page's opening exactly answers it. Might be a selector-prompt or frontmatter-summary issue, not a content issue.
- **True synthesis test set**: distinct from this concept test, which is still definitional. Would need questions of the form "given condition X, how do rules A and B interact" or "if a sample falls in domains P and V, which progLegalRef combination applies and why". Open question whether this is worth commissioning.
- **Cost comparison on concept test**: RAG $2.63 vs wiki $1.57. Wiki is ~40% cheaper here too, consistent with the lookup test.

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
