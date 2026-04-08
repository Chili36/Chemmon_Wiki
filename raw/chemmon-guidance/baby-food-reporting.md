---
title: "Baby Food Reporting"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
related:
  - "[[chemmon-overview]]"
  - "[[vmpr-reporting]]"
  - "[[business-rules]]"
  - "[[foodex2-in-chemmon]]"
  - "[[pesticide-reporting]]"
  - "[[contaminant-reporting]]"
last_updated: "2026-04-07"
---

# Baby Food Reporting

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## FoodEx2 Classification

Baby food is classified under FoodEx2 high-level code **A03PV** ("Food products for the young population").

Key FoodEx2 base terms for baby food products:

| Code | Description |
| --- | --- |
| A03QX | Processed cereal-based foods for infants and young children |
| A0EQM | Infant formula |
| A0EQL | Follow-on formula |
| A1RGS | Herbal infusions for infants (dry) |
| A03QF | Infant formula milk-based (liquid) |

Matrix classification must be **as detailed as possible**. For infant formula, distinguish between:
- Powder vs liquid form
- Reconstituted vs not reconstituted

Baby foods are **always** considered processed products.

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## VMPR Exclusion

Baby food samples are **excluded** from the VMPR Annual Report per Regulation (EU) 2022/1646.

- **CHEMMON55** prevents baby foods being reported with `progLegalRef` N371A.
- **CHEMMON63**: If `sampMatCode` is under A03PZ, `progLegalRef` cannot be N371A.

See [[vmpr-reporting]] for full VMPR reporting rules.

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Accepted Domains

Baby food samples **are** accepted in ChemMon data collection under other domains ([[pesticide-reporting|pesticides]], [[contaminant-reporting|contaminants]]) as long as `progLegalRef` is **not** N371A.

For inclusion in the **Pesticides Annual Report**, `progLegalRef` must be one of:

| Code | Legislation |
| --- | --- |
| N028A | Directive 2006/125/EC |
| N318A | Regulation (EU) 2016/127 |
| N027A | General food law reference |

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Legal Limits and Analytical Considerations

Baby food legal limits tend to apply to the **ready-to-eat product** (likely the reconstituted form).

For **mycotoxin maximum levels** (Regulation 2023/915), the following substances have levels that apply to **dry matter**:
- Aflatoxin B1
- Ochratoxin A
- Deoxynivalenol
- Zearalenone
- Fumonisins

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf -->
## Worked Example

### Infant formula milk-based with packaging
- Code: `A03QF#F28.A07HB$F18.A07NM$F19.A16RX`
- A03QF is the base term for infant formula milk-based (liquid). F28 specifies the physical state, F18 describes the packaging type, and F19 provides additional packaging detail.
