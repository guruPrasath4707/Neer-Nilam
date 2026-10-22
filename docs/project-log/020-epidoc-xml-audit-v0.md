# Project Log 020 — Local EpiDoc XML Audit Utility

Date: 2026-10-22  
Status: Code and synthetic tests committed on a feature branch; local corpus scan pending

## Why this work

The next software gate is normalization of a small, source-linked epigraphy subset. Before selected records can be considered, the known DHARMA licence discrepancy needs a reproducible per-file technical inventory. The source registry continues to hold both DHARMA sources under HOLD_LICENSE_RECONCILIATION.

## Implemented

- Added a standard-library Python utility to inventory local EpiDoc XML structure, SHA-256, file size, parse status and declared licence target URIs.
- Added a compact aggregate report and explicit non-success status for malformed, oversized, unreadable or unsafe-to-parse XML.
- Kept the output metadata-only: no inscription text, extracted place/person names, historical dates, raw corpus files or generated audit reports are committed.
- Added synthetic unit tests and a GitHub Actions workflow.
- Documented the local Windows invocation and interpretation limits in the EpiDoc audit runbook.

## Boundaries

This is a local technical audit, not a rights clearance, EpiDoc schema-validation result, evidence assertion or historical reconstruction. The script does not access the Seagate drive automatically, download anything, modify raw files, or resolve rights. Public GitHub remains code/documentation only until each source's rights permit any additional material.

## Next gate

Run the audit locally against the existing DHARMA-TamilNadu and DHARMA-SII folders on the confirmed data lake. Review every licence-target group and non-parsed row, keep the generated reports local, and only then plan a separately reviewed normalization task if the licence hold is resolved.
