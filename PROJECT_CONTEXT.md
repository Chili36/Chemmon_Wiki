---
title: "Project Context"
last_updated: "2026-04-07"
source_inspiration:
  - "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
---

# What We Are Building

A persistent markdown knowledge base for EFSA Chemical Monitoring reporting guidance so an LLM can support ChemMon reporting questions from a maintained body of structured knowledge instead of re-reading raw guidance PDFs from scratch each time.

In this workspace, that means:

- `chemmon_docs/` holds the immutable source PDFs.
- `raw/chemmon-guidance/` holds the LLM-maintained markdown pages extracted, organized, cross-linked, and kept concise for both human reading and machine use.
- The knowledge base is topic-oriented rather than document-oriented, so rules about reporting domains, mandatory facets, business rules, and submission procedures live in dedicated pages instead of a single large dump.

# Why We Are Building It

The goal is not simple document retrieval. The goal is to compile knowledge once, preserve the synthesis, and keep improving it over time.

Why this matters for ChemMon:

- ChemMon reporting guidance is updated annually and contains domain-specific rules that interact with each other.
- Many reporting questions require combining rules from multiple sections of the guidance, plus EFSA clarifications that live only in Teams channels.
- A maintained wiki reduces repeated interpretation work, surfaces contradictions or edge cases earlier, and makes downstream reporting more consistent.
- Structured markdown pages are easier for an LLM to search, update, cite, and cross-reference than raw PDFs or one-off chat history.

# Operating Model

- New source documents are added to the raw source layer first.
- The LLM reads them, extracts the durable rules, and updates the markdown knowledge base.
- The markdown layer becomes the default working context for answering questions, while the raw PDFs remain the source of truth for verification.
- EFSA official clarifications from the reporting Teams channel are ingested as they arrive.

# Design Principle

This project follows the general pattern described in Andrej Karpathy's `llm-wiki` gist published on April 4, 2026: raw sources stay immutable, while the LLM incrementally builds and maintains a persistent interlinked wiki that compounds in value over time.
