---
title: "Baby Food Business Rules"
type: "rule-reference"
domain: "baby-food"
last_updated: "2026-04-10"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Annex B"
related:
  - "[[business-rules]]"
  - "[[baby-food-reporting]]"
  - "[[vmpr-reporting]]"
  - "[[business-rules-vmpr]]"
---

# Baby Food Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Annex B -->

## Overview

Baby food reporting has two exclusion rules that govern how baby food samples are coded and which legal frameworks apply. CHEMMON55 enforces matrix coding consistency for baby food programme references; CHEMMON63 excludes baby food from the VMPR legal framework entirely.

For baby food classification, accepted domains, and worked coding examples, see [[baby-food-reporting]]. For the broader VMPR rules these interact with, see [[business-rules-vmpr]].

## Baby Food & Sample Exclusion Rules

| Rule ID | Severity | Description | Domain |
| --- | --- | --- | --- |
| CHEMMON55 | Error | For N028A/N318A (baby food programme references), `sampMatCode` parent term must be A03PV (Food products for young population). Baby food programme data must reference baby food matrices. See [[baby-food-reporting]]. | All |
| CHEMMON63 | Error | If `sampMatCode` falls under A03PZ (baby food), `progLegalRef` cannot be N371A. Baby food is excluded from the VMPR legal framework. See [[baby-food-reporting]] and [[vmpr-reporting]]. | VMPR |
