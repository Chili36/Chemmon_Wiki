---
title: "ChemMon Scope and Legal Basis"
type: "overview"
domain: "all"
last_updated: "2026-11-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 5-8 (Section 1.1 Background: purpose, audience, legal framework, border control posts); p. 11 (Table 1, N422A); p. 146 (Table 12, N422A)"
related:
  - "[[chemmon-background]]"
  - "[[chemmon-overview]]"
  - "[[ssd2-programme-legal-reference]]"
  - "[[reporting-flags]]"
  - "[[pesticide-reporting]]"
  - "[[vmpr-reporting]]"
  - "[[contaminant-reporting]]"
  - "[[food-additives-reporting]]"
  - "[[chemmon-reports]]"
---

# ChemMon Scope and Legal Basis

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 5-8, 11, 146 -->

## Rule Summary

- ChemMon guidance is for data providers reporting SSD2 files to EFSA for chemical parameters in food and feed.
- The covered reporting domains are contaminants, food additives, food flavourings, pesticide residues, and veterinary medicinal product residues.
- Pesticides and VMPR are statutory annual-report domains with calendar-year inclusion windows; other chemical monitoring data can be transmitted when ready.
- `progLegalRef` is the practical field that connects a submitted dataset to the legal framework and reporting domain.

## Purpose and Audience

This guidance is intended for data providers reporting datasets to EFSA in SSD2 format that contain results for chemical parameters related to:

- occurrence of contaminants in food and feed
- food additives
- food flavourings
- monitoring of pesticide residues
- veterinary medicinal product residue levels in food and feed

(ChemMon 2026 p5)

Except for the statutory EU Annual Report domains (pesticide residues and VMPR), samples taken in any year can be transmitted to the EFSA Scientific Data Warehouse when the data provider has the data ready. Only samples taken in the specific calendar year are included in each year's national and Annual Report. (ChemMon 2026 p5)

## Main Legal Framework

EFSA receives the results of testing for substances in food and feed under:

- Regulation (EC) No 396/2005: maximum residue levels of pesticides in or on food and feed of plant and animal origin; Regulation (EU) 2021/1355: multiannual national control programmes for pesticide residues; Regulation (EU) 2024/989: the coordinated multiannual control programme of the Union for pesticide residues (2025, 2026 and 2027).
- Regulation (EC) No 178/2002 (as amended): general food law.
- Regulation (EU) 2017/625: official controls and associated delegated acts.
- Regulation (EU) 2023/915: maximum levels for certain contaminants in food (it repealed Regulation (EC) No 1881/2006).
- Regulation (EC) No 1333/2008: food additives.
- Regulation (EC) No 1334/2008: food flavourings.
- Regulation (EU) 2022/1644 and Regulation (EU) 2022/1646: official controls of VMPR in live animals and animal products.
- Directive 2002/32/EC: undesirable substances in animal feed.
- Regulation (EU) 2016/127, Regulation (EU) 2016/128 and Directive 2006/125/EC: baby food.
- Regulation (EU) 2019/1793: official controls of certain goods from third countries.
- Regulation (EU) 2019/1873: intensified official controls on products of animal origin, added in the 2026 guidance as `progLegalRef` N422A.
- Regulation (EU) 2022/931 and Regulation (EU) 2022/932: official controls on the presence of contaminants in food.

(ChemMon 2026 pp. 5-6, 11)

Source discrepancy: Table 1 says N422A "has been flagged for contaminants, pesticides, VMPR, food additives and food flavourings" (ChemMon 2026 p11), while Table 12 gives N422A the domain attributes OCC, PEST, VMPR only (ChemMon 2026 p146). The guidance does not resolve this; see [[ssd2-programme-legal-reference]] for Table 12.

For newly adopted and amended regulations not applicable to data collected by EFSA in the reference year, the provisions of the older regulations remain in force. (ChemMon 2026 p8)

Results on chemicals in food not covered by the listed legislation can also be reported to EFSA. (ChemMon 2026 p6)

## Border Control Post Results

Results from Border Control Posts (BCPs) are to be reported to TRACES (Article 133 of Regulation (EU) 2017/625). Member States are also required to report these border control analyses to EFSA in SSD2 format, because the level of detail differs from TRACES, for:

- VMPR (Article 9 of Regulation (EU) 2022/1646)
- contaminants (Article 8 of Regulation (EU) 2022/932)
- pesticides (Article 31 of Regulation (EC) No 396/2005 and the SCoPAFF Pesticide Residue meeting)

A future assessment of SSD2 and TRACES compatibility is planned to help Member States avoid double reporting. (ChemMon 2026 pp. 7-8)

## Navigation

- Use [[ssd2-programme-legal-reference]] for the element-level `progLegalRef` rules and canonical `LEGREF` values.
- Use [[reporting-flags]] for how legal references and parameters set domain flags.
- Use [[chemmon-reports]] for how records flow into annual and national reports.
