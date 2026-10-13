---
title: "Baby Food Business Rules"
type: "rule-reference"
domain: "baby-food"
last_updated: "2026-10-05"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "Table 10, pp. 113-143"
related:
  - "[[business-rules]]"
  - "[[baby-food-reporting]]"
  - "[[vmpr-reporting]]"
  - "[[business-rules-vmpr]]"
---

# Baby Food Business Rules

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Table 10, pp. 113-143 -->

## Overview

Baby food reporting has two exclusion rules that govern how baby food samples are coded and which legal frameworks apply. CHEMMON55 enforces matrix coding consistency for baby food programme references; CHEMMON63 disallows N371A when the sampled matrix falls under A03PZ.

For baby food classification, accepted domains, and worked coding examples, see [[baby-food-reporting]]. For the broader VMPR rules these interact with, see [[business-rules-vmpr]].

## Baby Food & Sample Exclusion Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMMON55 | Error | For N028A/N318A (baby food programme references), `sampMatCode` parent term must be A03PV (Food products for young population). Baby food programme data must reference baby food matrices. See [[baby-food-reporting]]. | All | 127 |
| CHEMMON63 | Error | If `sampMatCode` falls under A03PZ (baby food), `progLegalRef` cannot be N371A. The restriction here is the named A03PZ/N371A combination. See [[baby-food-reporting]] and [[vmpr-reporting]]. | VMPR | 129 |
