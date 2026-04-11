---
title: "Data Validation and Acceptance (DCF Workflow)"
type: "reference"
domain: "all"
last_updated: "2026-04-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
source_pages:
  - "pp. 152-153 (Section 11)"
related:
  - "[[business-rules]]"
  - "[[chemmon-reports]]"
  - "[[reporting-flags]]"
  - "[[chemmon-matrix-classification-algorithms]]"
---

# Data Validation and Acceptance (DCF Workflow)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Section 11 -->

## End-to-end flow (as described in the guidance)

<!-- Source: ChemMon 2026 pp. 152-153 -->

1. **Transmit dataset to DCF**: the system sends an automatic acknowledgement ("ack") message.
2. **Receive validation output**: the data provider receives an "ack details" message (downloadable as XML) listing errors found, followed by business-rule validation results.
3. **Fix and re-transmit as needed**: data providers use the troubleshooting suggestions in the GBR and CHEMMON tables (Tables 9 and 10) to resolve errors/warnings, plus network FAQ resources; if needed, contact EFSA via `data.collection@efsa.europa.eu`. (ChemMon 2026 p152)
4. **Submit when valid**: once datasets reach **Valid** or **Valid with Warning** status, the data provider can **Submit** them to the EFSA scientific data warehouse (sDWH) in DCF.
5. **Review in MicroStrategy**: submitted data become visible via validation reports in MicroStrategy for both data providers and validators.
6. **Accept/Reject by validator**: data validators set the final status (**Accepted** or **Rejected**) in MicroStrategy and submit the final status for each dataset ID. (ChemMon 2026 p152)

The guidance points to the DCF user manual for the detailed process steps and UI specifics. (ChemMon 2026 p152)

## Important constraint after acceptance: corrections require the update procedure

<!-- Source: ChemMon 2026 p153 -->

Once data are **Accepted** in the sDWH, the guidance notes they can only be corrected via the record **Update procedure** described in the GDE2 Guidance (Amendment Operations). EFSA therefore encourages thorough validation before acceptance. (ChemMon 2026 p153)

