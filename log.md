---
title: "Wiki Log"
last_updated: "2026-04-11"
---

# Log

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
