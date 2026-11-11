---
title: "Baby Food Reporting"
select_when: "Infant/baby food scope, matrix classification and exclusions; use with the relevant reporting domain instead of transferring all baby-food rules to VMPR."
type: "domain-guide"
domain: "baby-food"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[vmpr-reporting]]"
  - "[[business-rules]]"
  - "[[foodex2-in-chemmon]]"
  - "[[foodex2-facets-state-process]]"
  - "[[foodex2-facets-packaging-consumer]]"
  - "[[pesticide-reporting]]"
  - "[[contaminant-reporting]]"
source_pages:
  - "p. 19 (progLegalRef examples N028A/N318A)"
  - "pp. 52, 55 (matrix examples)"
  - "p. 70 (dry-matter maximum levels)"
  - "p. 85 (Section 3, baby foods)"
  - "pp. 127, 129 (Table 10: CHEMON55, CHEMON63)"
last_updated: "2026-11-11"
---

# Baby Food Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 52, 55, 85 -->
## FoodEx2 Classification

The baby-food section of the guidance refers to FoodEx2 matrix classifications under the high-level code **`A03PV`** ("Food products for the young population"). (ChemMon 2026 p85) See [[foodex2-in-chemmon]] for general FoodEx2 coding rules in [[chemmon-overview|ChemMon]].

FoodEx2 codes for baby food products used in the guidance examples:

| Code | Description |
| --- | --- |
| `A03QX` | Processed cereal-based foods for infants and young children |
| `A0EQM` | Infant formula |
| `A0EQL` | Follow-on formula |
| `A16GS` | Herbal infusions specific for infants and young children, dry |
| `A03QF` | Infant formula, milk-based, liquid |

(ChemMon 2026 pp. 52, 55)

For records to be included in the **pesticides Annual Report**, the guidance lists these conditions (ChemMon 2026 p85):

- `progLegalRef` must be `N028A`, `N318A` or `N027A` (see Accepted Domains below);
- baby foods are **always** considered to be processed;
- matrix classification code attributes must be **as detailed as possible**, e.g. for infant formula it is important to know whether it was powder or liquid, reconstituted or not.

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 85, 127, 129 -->
## VMPR Exclusion

Baby food samples are **excluded** from the VMPR Annual Report as defined in Regulation (EU) 2022/1646. (ChemMon 2026 p85)

- **CHEMON63** (Error): if `sampMatCode` is under the high-level code `A03PZ` (i.e. the sample is a baby food), `progLegalRef` cannot be `N371A`. (ChemMon 2026 Table 10 p. 129) See [[business-rules-baby-food]].
- **CHEMON55** (Error): if `progLegalRef` is `N028A` or `N318A`, `sampMatCode.base` should have as parent term `A03PV`. (ChemMon 2026 Table 10 p. 127) See [[business-rules-baby-food]].
- Source discrepancy: the p. 85 prose says "A BR prevents that baby foods is reported with progLegalRef (N371A). Please see BR CHEMON55 in Table 9." The rule that does this is CHEMON63, and both rules are in Table 10 (pp. 127, 129). The prose (p. 85) and CHEMON55 name `A03PV`; CHEMON63 names `A03PZ`.

See [[vmpr-reporting]] for full VMPR reporting rules.

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 12, 19, 85 -->
## Accepted Domains

Baby food samples **are** accepted in the ChemMon data collection when they have been analysed for any valid ChemMon parameter, as long as `progLegalRef` is **not** `N371A`. (ChemMon 2026 p85) Each `paramCode` falls under its corresponding domain, e.g. [[pesticide-reporting|pesticides]] or [[contaminant-reporting|contaminants]]. (ChemMon 2026 p19)

For inclusion in the **Pesticides Annual Report**, `progLegalRef` must be one of (ChemMon 2026 p85):

| Code | Legislation |
| --- | --- |
| `N028A` | Directive 2006/125/EC (ChemMon 2026 pp. 19, 85) |
| `N318A` | Commission Delegated Regulation (EU) 2016/127 and Regulation (EU) 2016/128 (ChemMon 2026 Table 12, p. 146); p. 19 and CHEMON55 (p. 127) name only 2016/127 |
| `N027A` | Regulation (EC) No 396/2005 (ChemMon 2026 pp. 12, 19) |

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf pp. 70, 85 -->
## Legal Limits and Analytical Considerations

Baby food legal limits tend to apply to the **ready-to-eat product**, i.e. likely to the reconstituted form, in contrast with other food products where the limits tend to apply to the product as placed on the market. (ChemMon 2026 p85)

For **mycotoxin maximum levels** (Regulation (EU) 2023/915), the levels for the following substances apply to the **dry matter** of the baby food and processed cereal-based foods for infants and young children (ChemMon 2026 p70):
- Aflatoxin B1
- Ochratoxin A
- Deoxynivalenol
- Zearalenone
- Fumonisins

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf p. 55 -->
## Worked Example

### Infant formula based on milk, heated in the microwave inside a plastic feeding bottle
- Code: `A03QF#F28.A07HB$F18.A07NM$F19.A16RX`
- `A03QF` is the base term "Infant formula, milk-based, liquid". F28 `A07HB` is the process (microwave-cooking; see [[foodex2-facets-state-process]]), F18 `A07NM` the packaging format (bottle) and F19 `A16RX` the packaging material (polypropylene, PP) (see [[foodex2-facets-packaging-consumer]]). (ChemMon 2026 p55)
