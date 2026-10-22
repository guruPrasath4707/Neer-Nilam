# EpiDoc XML Licence and Structure Audit v0

Date: 2026-10-22  
Status: Implemented as local-only tooling; actual Seagate scan remains pending

## Purpose

The data lake already has two DHARMA epigraphy sources registered:

- SRC-DHARMA-TN — DHARMA Tamil Nadu epigraphy
- SRC-DHARMA-SII — DHARMA South Indian Inscriptions

Their source-registry status remains HOLD_LICENSE_RECONCILIATION. The repository-level licence description and XML-level declarations have differed in the collected inventory. This utility makes that technical discrepancy easier to reproduce without changing the raw corpus or treating a licence URI as permission.

The implementation deliberately stops before historical normalization. It does not extract inscription text, personal/place names, dates, translations, or candidate historical claims. No DHARMA source records, derived reports, or source text are added to public GitHub.

## Inputs and outputs

The script reads regular XML files under one local corpus folder, recursively, in deterministic relative-path order. It calculates SHA-256, records byte size and selected TEI/EpiDoc structural element counts, captures root namespace/language identifiers, and inventories the licence target URIs declared inside each XML file.

It writes two reports outside the scanned input directory:

- CSV, one row per XML file, with relative path, SHA-256, parse status, declared licence targets and selected structural counts.
- JSON summary, with total/parsed/failed files, counts grouped by declared licence target, and limitations.

The report intentionally does not store absolute input paths, inscription text, extracted dates or entity names. It does not follow file symlinks, download remote schemas, contact the network, alter source files, or validate TEI/EpiDoc schema conformance. Custom XML entity declarations are rejected before parsing. Files above the configurable size limit are hashed and flagged without parsing.

## Windows/PowerShell usage

Run from the repository root after confirming the two folders exist on the Seagate data lake. The destination paths below are new report names; the script refuses to overwrite existing reports unless the explicit overwrite flag is added.

    $DataLake = 'F:\Neer-Nilam-DataLake'
    $Auditor = '.\scripts\epigraphy\audit_epidoc_xml.py'
    python $Auditor --root (Join-Path $DataLake '01_raw\epigraphy\DHARMA-TamilNadu') --source-id SRC-DHARMA-TN --csv (Join-Path $DataLake '00_admin\licences\dharma-tamilnadu-xml-audit-v0.csv') --summary-json (Join-Path $DataLake '00_admin\licences\dharma-tamilnadu-xml-audit-v0-summary.json')
    python $Auditor --root (Join-Path $DataLake '01_raw\epigraphy\DHARMA-SII') --source-id SRC-DHARMA-SII --csv (Join-Path $DataLake '00_admin\licences\dharma-sii-xml-audit-v0.csv') --summary-json (Join-Path $DataLake '00_admin\licences\dharma-sii-xml-audit-v0-summary.json')

The program needs Python 3.10 or newer and uses only the Python standard library. If Python is not on PATH, use the same interpreter that was used for the project's existing collection tools.

## Status semantics

- PARSED: well-formed XML was parsed for technical metadata; this is not a legal or historical approval.
- XML_PARSE_ERROR: the file is malformed or not parseable by the standard library.
- UNSAFE_ENTITY_DECLARATION: a custom entity declaration was present and parsing was refused.
- FILE_TOO_LARGE: SHA-256 and size were recorded, but parsing was skipped.
- IO_ERROR: the file could not be read or hashed.
- NO_LICENCE_ELEMENT: the XML parsed but contained no element named licence.
- DECLARED_WITHOUT_TARGET: a licence element existed but did not declare a target URI.
- MIXED_DECLARATIONS: at least one target URI and at least one licence element without a target were found.
- DECLARED_TARGET: one or more target URIs were found.

The process returns exit code 0 when every discovered XML file is technically parseable, 1 if any file needs technical review, and 2 if no XML files were found or command arguments were invalid. A successful exit does not mean the licence or source record is cleared for reuse.

## Rights and evidence gate

The source registry's HOLD_LICENSE_RECONCILIATION decision remains authoritative. The audit reports what the XML declares; it does not decide whether those terms conflict with repository documentation, whether attribution is sufficient, or whether redistribution and derived use are allowed. Do not publish these generated reports in the public repository while the source hold remains active. Keep them with the local data-lake administrative/licence records and append the outcome to the local collection log.

Only after maintainers clarify the licence discrepancy should a separate reviewed task decide whether selected records may move through normalization. Any later evidence assertion still needs an exact source locator, temporal semantics, a verification status, and an independent source review. Modern spatial or hydrological context must not be treated as evidence for an ancient state by itself.

## Validation included with the implementation

The standard-library unittest suite uses synthetic XML written by the tests. It covers hashing, namespace handling, declared licence targets, missing or incomplete licence elements, malformed XML, entity-declaration rejection, size limits, deterministic inventory, output boundaries, refusal to overwrite, exit codes and summary generation. It does not access the user's Seagate drive or assert anything about the current local corpus.
