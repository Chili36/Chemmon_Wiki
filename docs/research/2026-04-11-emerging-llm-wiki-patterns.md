---
title: "Emerging LLM Wiki Patterns — State of Community Practice"
date: "2026-04-11"
type: "research-note"
context: "Web research one week after Andrej Karpathy's initial LLM wiki gist (2026-04-04). Captured to ground future design decisions in what the broader community has published, rather than iterating in isolation."
---

# Emerging LLM Wiki Patterns — State of Community Practice

## Why this note exists

Andrej Karpathy published his "LLM wiki" gist on 2026-04-04. Over the following week, a substantial volume of writeups, implementations, and open-source projects appeared. This note captures the subset directly relevant to the ChemMon_Wiki project's design, so we don't have to re-research the same ground in a later session. It is a snapshot of community practice as of 2026-04-11 — **patterns have not yet crystallized into consensus** and are likely to evolve.

This is a research note, not a spec. It documents what others are doing and where we compare. It does not prescribe what to build — that decision lives in project planning.

## Key findings

### 1. Selector/planner model convention: Sonnet, not Haiku

The consistent community pattern for multi-step retrieval flows is:

> *"Sonnet 4.5 for complex planning, multiple Haiku 4.5s for execution."*

Applied to a wiki selector → answerer pipeline, this means:

- **Selector** (reads the catalog, decides which pages to load) = Sonnet — this is the planning step and benefits from the bigger model
- **Answerer** (reads the selected pages, writes the grounded answer) = Haiku or Sonnet depending on answer complexity

**Our current ChemMon_Wiki configuration is inverted**: Haiku selector, Sonnet answerer. Flipping the selector to Sonnet is the single cheapest architectural change that aligns us with community convention. If selector quality degrades as the catalog grows (the "regression on expanded index" pattern), this is where it originates.

### 2. Graph expansion at retrieval time

Two independent writeups describe the same retrieval technique, stated differently:

> *"At query time, a retrieval hit is expanded through the graph: neighboring blocks, direct links, backlinks, and page summaries are pulled in before the model answers."*

> *"The backlinks panel shows everything that references any given concept. The model doesn't forget to add backlinks."*

**The pattern:** when the selector returns N pages, automatically include pages linked FROM those N pages (forward links) and pages linking TO them (backlinks), up to a depth and size budget. The answerer then sees not just the selected pages but their linked neighborhood.

**Why it matters for our selector regressions**: when page-selection drift causes the selector to pick an adjacent page instead of the exact-match page, graph expansion still pulls in the exact-match page through the `[[wiki-link]]` reference. Graph expansion makes retrieval more robust to selector noise without making the selector smarter.

**Implementation sketch**: in `wiki_api/app.py`, after the selector returns `pages_used`, parse each page's body for `[[wiki-link]]` references, resolve them, and append to the page set (subject to a total-token budget). Requires a link-resolution helper that can handle the `[[page-name]]` → actual file path mapping. Our existing `tools/health_check.py` already has a wiki-link regex that could be factored out for reuse.

### 3. LLM-based lint is the next step beyond rule-based health checks

Our current `tools/health_check.py` validates frontmatter, wiki-link resolution, rule-ID coverage, and stale path references. All rule-based. The community pattern is an **LLM-driven** lint pass that additionally checks for:

- Contradictions between pages
- Stale claims (where source PDF has been updated but the wiki page wasn't)
- **Orphan pages with no inbound links**
- Important concepts mentioned in prose but lacking their own dedicated page
- Missing cross-references where two pages discuss the same concept without linking

> *"periodically, ask the LLM to health-check the wiki for contradictions between pages, stale claims, orphan pages with no inbound links, important concepts mentioned but lacking their own page, and missing cross-references."*

**Expected cost**: expensive in tokens (the LLM needs to read every page at least once), cheap in frequency (run weekly or on-demand, not per-request). This is a maintenance-loop tool, not a hot-path tool.

### 4. Wiki scale limit is 50-100k tokens — we are well under it

One writeup puts a specific number on when the pure wiki pattern stops working:

> *"The 50,000-100,000 token threshold is where the wiki approach stops working reliably: beyond that, the index cannot fit in context, and LLM context window limitations force a retrieval layer regardless of the storage format."*

**Our state**: `index.md` is ~6 KB / ~1500 tokens. The entire wiki body is ~100 KB / ~25k tokens. We are comfortably under the failure threshold (25-50% of it depending on where exactly the limit falls for a given model).

**Implication**: selector quality issues we observe (noisier retrieval on expanded catalogs) are NOT scale-related. We are not hitting a context-window ceiling. The issue lives in the selector's reasoning at moderate catalog sizes, which is addressable by (a) better selector model, (b) graph expansion, or (c) more discriminating catalog entries.

### 5. Source document treatment varies by type

> *"A 50-page research white paper requires extraction on a section-by-section basis while a tweet or social media thread only requires a primary insight and corresponding context."*

We are already doing this implicitly — the ChemMon 2026 PDF is a 156-page technical document ingested section-by-section. This is standard practice, not a new insight for our situation.

### 6. Karpathy's gist itself is not evolving

The gist was last touched 2026-04-04. The 30+ comment thread contains implementations and extensions but no revised thinking from Karpathy himself. The canonical statement of the pattern is stable. Further community evolution is happening in blog posts and open-source implementations, not in the gist.

## Alignment check: what we already do right

The ChemMon_Wiki project (as of 2026-04-11) already matches these community patterns:

| Pattern | Our implementation |
|---|---|
| Raw/wiki separation | `chemmon_docs/` (immutable source PDFs) vs `wiki/chemmon-guidance/` (compiled markdown) |
| Index file fits in single context | `index.md` at ~1500 tokens |
| Topic-oriented pages, not document dumps | 18 pages across overview, domain guides, rule slices, element references |
| Consistent frontmatter schema | `SCHEMA.md` defines 5 page types + 7 domain values |
| Wiki-style backlinks | `[[page-name]]` syntax throughout |
| Source attribution per claim | `<!-- Source: <pdf>, <page range> -->` HTML comments + inline `(ChemMon 2026 p<n>)` markers |
| Rule-based health check | `tools/health_check.py` validates frontmatter, cross-links, rule-ID coverage |
| Incremental ingestion with logged passes | `log.md` tracks ingest passes chronologically |

## Gaps vs community pattern

| Gap | Impact | Complexity to close |
|---|---|---|
| Selector uses Haiku (community pattern is Sonnet for planning) | Likely source of some selector regressions on expanded catalog | Low — one-line `.env` change, restart server |
| No graph expansion at retrieval time | Retrieval is brittle to selector drift; answerer only sees exact pages selected | Medium — new logic in `wiki_api/app.py` to parse wiki-links from selected pages and append linked pages to the injection set, with a total-token budget |
| Health check is rule-based only | Contradictions, orphans, missing cross-references go undetected until a query surfaces them | Medium-high — new `tools/lint_wiki.py` that runs an LLM over the whole wiki with a structured prompt; expensive per run, cheap in frequency |

## Open-source implementations worth examining

Three Karpathy-pattern implementations published in the first week. Listed by relevance to our situation:

1. **[ussumant/llm-wiki-compiler](https://github.com/ussumant/llm-wiki-compiler)** — Claude Code plugin that compiles markdown knowledge files into a topic-based wiki. Directly implements Karpathy's LLM Knowledge Base pattern. Closest in design to what we built; worth reading for their ingestion flow.
2. **claude-obsidian** (358 stars on GitHub, referenced in Karpathy gist comments) — Full Claude Code plugin with hot cache, **contradiction flagging**, and an **8-category lint system**. The lint system is the most directly applicable piece for our "LLM-based lint" gap. Worth reading their category taxonomy and prompt structure before building our own.
3. **[nvk/llm-wiki](https://github.com/nvk/llm-wiki)** — LLM-compiled knowledge bases with parallel multi-agent research, thesis-driven investigation, source ingestion, wiki compilation, querying, and artifact generation. Larger-scale implementation; relevant if we grow to multi-domain (e.g., add a FoodEx2 wiki alongside ChemMon).

Other implementations seen in passing (not prioritised):

- **[hellohejinyu/llm-wiki](https://github.com/hellohejinyu/llm-wiki)** — LLM-powered personal wiki CLI. Smaller scope.
- **ask-shorty** (from Karpathy gist comments) — Uses a dense compression technique ("Shorty") claimed to give ~95% token reduction with knowledge graphs and multi-layer retrieval fusion. Interesting but speculative; compression as a first-class retrieval step.

## Non-goals / things we are not copying

A few patterns that appear in community writeups but are not appropriate for the ChemMon_Wiki specifically:

- **Obsidian-style personal vaults** — the Karpathy pattern originates in personal-notes land. Our wiki is a domain-reference wiki for a specific reporting standard, not a personal knowledge base. Organisational patterns optimised for sprawling personal notes (daily notes, inbox, meetings folders) don't apply.
- **Multi-agent parallel research (nvk/llm-wiki)** — useful at large scale or with multiple source types. We have one primary source PDF and one secondary (SSD2 2013 spec). Serial ingestion is simpler and sufficient.
- **Ed25519-signed consensus knowledge bases (from a gist comment)** — solves cryptographic trust across multiple models in open networks. Not our problem.

## Sources

Community writeups and docs consulted on 2026-04-11:

- [Karpathy `llm-wiki` gist (original pattern statement)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 2026-04-04, no subsequent updates from author
- [MindStudio: LLM Wiki vs RAG — when to use markdown knowledge bases](https://www.mindstudio.ai/blog/llm-wiki-vs-rag-markdown-knowledge-base-comparison)
- [MindStudio: What Is Andrej Karpathy's LLM Wiki? How to Build a Personal Knowledge Base With Claude Code](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code)
- [Antigravity: Karpathy's LLM Knowledge Bases — the post-code AI workflow](https://antigravity.codes/blog/karpathy-llm-knowledge-bases)
- [Antigravity: Karpathy's LLM Wiki — the complete guide to his idea file](https://antigravity.codes/blog/karpathy-llm-wiki-idea-file)
- [VentureBeat: Karpathy shares LLM Knowledge Base architecture that bypasses RAG](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an)
- [Analytics Vidhya: LLM Wiki Revolution — how Karpathy's idea is changing AI](https://www.analyticsvidhya.com/blog/2026/04/llm-wiki-by-andrej-karpathy/)
- [Atlan: LLM Wiki vs RAG Knowledge Base — Karpathy approach explained](https://atlan.com/know/llm-wiki-vs-rag-knowledge-base/)
- [DAIR.AI Academy: LLM Knowledge Bases (Karpathy pattern overview)](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy)
- [Louis Wang: Building a self-improving personal knowledge base powered by LLM](https://louiswang524.github.io/blog/llm-knowledge-base/)
- [Techbuddies: Inside Karpathy's LLM Knowledge Base — a markdown-first alternative to RAG](https://www.techbuddies.io/2026/04/04/inside-karpathys-llm-knowledge-base-a-markdown-first-alternative-to-rag-for-autonomous-archives/)
- [Artificial Analysis: Claude Sonnet 4.6 vs Haiku 4.5 model comparison](https://artificialanalysis.ai/models/comparisons/claude-sonnet-4-6-vs-claude-4-5-haiku)

Open-source implementations referenced:

- [ussumant/llm-wiki-compiler](https://github.com/ussumant/llm-wiki-compiler)
- [nvk/llm-wiki](https://github.com/nvk/llm-wiki)
- [hellohejinyu/llm-wiki](https://github.com/hellohejinyu/llm-wiki)

## Next research passes

Things worth re-searching in 1-2 weeks as the community pattern continues to evolve:

- **Graph expansion algorithms** — specifically, how to budget token injection when expanding through linked pages. Is depth=1 enough? How do people cap the expanded neighborhood size?
- **Lint prompt taxonomies** — claude-obsidian has 8 categories. What are they? Is there a common taxonomy emerging?
- **Selector-vs-answerer model cost curves** — as Haiku and Sonnet pricing evolves, where does the crossover for retrieval flows land?
- **Eval methodologies** — synthesis-question test sets vs lookup-question test sets. Is anyone publishing standard benchmarks?
- **Cross-document synthesis** (for when we move beyond one source PDF) — how do multi-source wikis handle conflicting claims across inputs?
