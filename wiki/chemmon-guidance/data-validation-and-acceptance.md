---
title: "Data Validation and Acceptance (DCF Workflow)"
type: "reference"
domain: "all"
last_updated: "2026-11-11"
sources:
  - "EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for  No‐presence  data on food additives and food flavourings.pdf"
  - "EFSA Supporting Publications - 2026 -  - Reporting guidance for use levels on food additives and food flavourings ‐ 2026.pdf"
source_pages:
  - "ChemMon 2026 pp. 152-153 (Section 11)"
  - "No-presence 2026 p. 13 (Section 3), p. 14 (Figure 1), pp. 19-21 (Table 3)"
  - "Use-levels 2026 p. 17 (Section 3), p. 18 (Figure 1), pp. 24-28 (Table 3)"
related:
  - "[[chemmon-data-governance-and-transparency]]"
  - "[[business-rules]]"
  - "[[chemmon-reports]]"
  - "[[reporting-flags]]"
  - "[[chemmon-matrix-classification-algorithms]]"
  - "[[fa-ff-no-presence-data-model]]"
  - "[[fa-ff-use-levels-data-model]]"
---

# Data Validation and Acceptance (DCF Workflow)

<!-- Source: EFSA Supporting Publications - 2026 -  - Chemical monitoring reporting guidance  2026 data collection.pdf, Section 11 -->

## End-to-end flow (as described in the guidance)

<!-- Source: ChemMon 2026 pp. 152-153 -->

1. **Transmit dataset to DCF**: the system sends an automatic acknowledgement ("ack") message.
2. **Receive validation output**: the data provider receives an "ack details" message (downloadable as XML) listing errors found, followed by business-rule validation results.
3. **Fix and re-transmit as needed**: data providers use the troubleshooting suggestions in the GBR and CHEMON tables (Tables 9 and 10) to resolve errors/warnings, plus network FAQ resources; if needed, contact EFSA via `data.collection@efsa.europa.eu`. (ChemMon 2026 p152)
4. **Submit when valid**: once datasets reach **Valid** or **Valid with Warning** status, the data provider can **Submit** them to the EFSA scientific data warehouse (sDWH) in DCF.
5. **Review in MicroStrategy**: submitted data become visible via validation reports in MicroStrategy for both data providers and validators.
6. **Accept/Reject by validator**: data validators set the final status (**Accepted** or **Rejected**) in MicroStrategy and submit the final status for each dataset ID. (ChemMon 2026 p152)

The guidance points to the DCF user manual for the detailed process steps and UI specifics. (ChemMon 2026 p152)

## Important constraint after acceptance: corrections require the update procedure

<!-- Source: ChemMon 2026 p153 -->

Once data are **Accepted** in the sDWH, the guidance notes they can only be corrected via the record **Update procedure** described in the GDE2 Guidance (Amendment Operations). EFSA therefore encourages thorough validation before acceptance. This fits the broader Open Data and transparency rationale in [[chemmon-data-governance-and-transparency]]. (ChemMon 2026 p153)

## FA/FF parallel data collections — same DCF flow, different rule namespaces

<!-- Source: No-presence 2026 p13 (Section 3), p14 (Figure 1); Use-levels 2026 p17 (Section 3), p18 (Figure 1) -->

The two FA/FF parallel data models — [[fa-ff-no-presence-data-model]] and [[fa-ff-use-levels-data-model]] — follow the same overall DCF → sDWH → MicroStrategy flow as above. Section 3 of each guide has the same text and spells the steps out in more detail than ChemMon Section 11 (No-presence 2026 p13; Use-levels 2026 p17):

1. **Roles**: national food authorities, research institutions, academia, food business operators and other interested stakeholders can designate experts as Data Provider (DP) and/or Data Validator (DV). The DP accesses the DCF with EFSA credentials.
2. **Preparation**: each DP "shall compile and report data" with the Excel reporting tool of the data model; the completed file "shall be exported in XML format".
3. **Upload**: the XML file is uploaded in the DCF with the 'Insert New Dataset' button. Once the dataset has a dataset Id and processing is finalised, its status is one of:

| Status | Trigger |
| --- | --- |
| Rejected | "dataset does not comply with the schema or wrong format" |
| Rejected editable | "dataset triggers BRs that are errors (Table 3)" |
| Valid with warnings | "dataset triggers BRs that are warnings (Table 3)" |
| Valid | "no BRs are triggered" |

4. **Read the result**: for 'Rejected', 'Rejected editable' and 'Valid with warnings', the 'Ack view' button gives information on the dataset with a summary of errors/warnings at the end; the 'Ack details' button gives more detail.
5. **Correct**: after the errors have been addressed, the file is uploaded again, replacing the existing dataset, by selecting 'Replace'.
6. **Submit**: "Only datasets in status 'Valid' or 'Valid with warnings' can be submitted" to the sDWH; each DP shall submit them.
7. **Validate**: all submitted data are visible in the MicroStrategy validation dashboards "one day after submitting the dataset in DCF". The DV selects 'Accepted' or 'Rejected' from the 'Confirm-Reject' drop-down in the Confirmation document for each dataset ID, and must submit the final status with the 'Submit' button.

Figure 1 of each guide draws this flow and adds an 'Ack download' option and an 'Update file' step before 'Replace'. (No-presence 2026 p14; Use-levels 2026 p18)

Source discrepancy notes:

- Status spelling: ChemMon p. 152 writes 'Valid with Warning'; the parallel guides write 'Valid with warnings' in the text (No-presence p13; Use-levels p17) and 'Valid with Warnings' in Figure 1 (No-presence p14; Use-levels p18).
- The no-presence Figure 1 labels the preparation step "Reporting tool for use level" (No-presence p14), while its text names the "Excel reporting tool for no-presence data at sample level" (No-presence p13).
- Use-levels p. 17 describes 'Valid with warnings' as triggered by warning rules in Table 3, but every rule in the use-levels Table 3 is an Error (Use-levels pp. 24-28). The no-presence Table 3 has one Warning, `PRE15` (No-presence p21).

What else differs from the SSD2 ChemMon collection:

- **Reporting tool**: each DM has its own Excel reporting tool, cited by DOI. No-presence: `10.5281/zenodo.14893698` (No-presence 2026 p13). Use-levels: `10.5281/zenodo.14893177` (Use-levels 2026 p17).
- **Rule namespace**: validation uses `PRE…` codes for no-presence submissions and `USE…`/`USE_LLDB…` codes for use-levels submissions, instead of the `GBR…`/`CHEMON…`/`LL_…` codes used for SSD2 ChemMon.
- **Catalogues**: both DMs use the `faff` sub-hierarchies of the same EFSA catalogues (`LEGREF.faff`, `PARAM.addAnalysis`/`flavAnalysis`, `CONCLUS.faff`, `ADDFOOD.FARestExc`/`FFRestExc`). See [[controlled-terminology-catalogues]].
