---
title: "Baby Food Business Rules"
type: "rule-reference"
domain: "baby-food"
last_updated: "2026-11-12"
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

Baby food reporting has two exclusion rules that govern how baby food samples are coded and which legal frameworks apply. CHEMON55 enforces matrix coding consistency for baby food programme references; CHEMON63 disallows N371A when the sampled matrix falls under A03PZ. (ChemMon 2026 p127, p129)

**Source discrepancy:** the Section 3 prose says "A BR prevents that baby foods is reported with progLegalRef (N371A). Please see BR CHEMON55 in Table 9" and describes baby foods as the matrices under A03PV (ChemMon 2026 p85). In Table 10 the N371A rule is CHEMON63 and its condition uses A03PZ (p129); CHEMON55 is the N028A/N318A rule that uses A03PV (p127). Wiki note (not in the guidance): the guidance states no precedence between the prose and Table 10, and does not say whether A03PZ or A03PV is the code the N371A check uses; the wiki reads the rule as written in Table 10 (CHEMON63, A03PZ).

For baby food classification, accepted domains, and worked coding examples, see [[baby-food-reporting]]. For the broader VMPR rules these interact with, see [[business-rules-vmpr]].

## Baby Food & Sample Exclusion Rules

| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMON55 | Error | For N028A/N318A (baby food programme references), `sampMatCode.base` should have as parent term A03PV (Food products for young population). Baby food programme data must reference baby food matrices. See [[baby-food-reporting]]. | All | 127 |
| CHEMON63 | Error | If `sampMatCode` falls under A03PZ (baby food), `progLegalRef` cannot be N371A. The rule gives the reason: these samples are excluded from the VMPR Annual Report as defined in Regulation (EU) 2022/1646 and Regulation (EU) 2022/1644. Its condition names no domain flag. See [[baby-food-reporting]] and [[vmpr-reporting]]. | A03PZ matrix with N371A | 129 |
