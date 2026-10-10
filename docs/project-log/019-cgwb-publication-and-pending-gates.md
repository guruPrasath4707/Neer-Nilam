# Project Log 019 — CGWB Listing Confirmed; Acquisition and Local Finalization Still Open

**Date:** 2026-10-10  
**Status:** Official catalogue listing confirmed; PDF payload not yet validated; local DOCX placement not yet confirmed.

## 1. CGWB yearbook listing

The official Central Ground Water Board (CGWB) publications catalogue currently lists **“Groundwater Year Book, Tamilnadu UT of Puducherry (2024 - 2025)”** under publication-detail record 2023. The catalogue identifies CGWB as author and gives year of issue 2026. This confirms that the target publication is listed; it does not prove that the download endpoint currently returns a valid PDF.

Source record and recovery steps: [CGWB yearbook 2024–2025 access review](../sources/CGWB-yearbook-2024-2025-access-review.md).

Earlier local collector attempts against the public download/media endpoints failed PDF validation. The returned files were quarantined and must remain quarantined. No valid 2024–2025 yearbook is recorded as acquired at this point. Do not infer success from the catalogue entry, filename, HTTP status or download counter.

**Acquisition gate:** retrieve via the official catalogue's Download action; parse the resulting document; verify title/reporting year/coverage/page numbering; compute SHA-256; record size, final URL, acquisition time and a new manifest row; review report-specific reuse terms. Do not publish the full PDF to public GitHub.

## 2. Public-log privacy correction

The archived local log at `docs/project-log/archive/Neer-Nilam_Log_2026-10-09_131205.txt` was updated in commit 67fadb5 to replace one literal Windows profile path with `[LOCAL_WINDOWS_PROFILE]`. The original source-log SHA-256 recorded by the publishing session remains a provenance value for the unredacted local source; it is not a checksum of the now-redacted public archive.

The storage audit CSV remains the historical 2026-10-10 09:51:10 snapshot and has not been edited to change its findings.

## 3. Two untracked CHIRPS metadata candidates in the local clone

A later local PowerShell attempt stopped safely when it found these pre-existing untracked files under `%USERPROFILE%\source\Neer-Nilam`:

- `docs/collection-runs/CHIRPS-monthly-2016-2025-20261010-012138-checksums.csv`
- `docs/collection-runs/CHIRPS-monthly-2016-2025-20261010-012138-manifest.csv`

They were not staged, deleted or included in the publication commit. A separately published metadata set for run `20261010-093810` already exists under `docs/collection-runs/`. The two `012138` candidates should be compared locally against that published run (row counts, filename/path keys, sizes, SHA-256 values, statuses and timestamps) before deciding whether they are a distinct useful run, stale duplicates or inconsistent metadata. Do not use `git clean`, `git add -A`, or overwrite the published metadata during this comparison.

## 4. Word dossier remains a local task

The earlier storage audit marked the expected Seagate dossier path as REVIEW. The user subsequently located two 10 October DOCX candidates in `%USERPROFILE%\Desktop\Neer Nilan` (timestamps 09:53 and 10:12); their contents still need comparison before choosing the authoritative copy. No claim is made here that a DOCX has since been copied to `F:\Neer-Nilam-DataLake\06_PROJECT_DOCUMENTS`.

## 5. Rights gate remains open

DHARMA repository README declarations still conflict with licence statements detected in a subset of XML files, and 46 collected XML records lack a detected licence target. Preserve provenance and hold redistribution or reusable derived outputs until the maintainers clarify the applicable terms in writing. No legal conclusion is inferred for records without a detected licence target.

## Current next actions

1. Retrieve and validate the listed CGWB 2024–2025 PDF.
2. Compare the two local DOCX candidates and copy the chosen file to the Seagate only after explicit local verification; then update the local log and run a focused re-audit.
3. Compare the two local `012138` CHIRPS manifests with the published `093810` run and decide their disposition explicitly.
4. Request written DHARMA licence clarification and retain the response in the source/rights evidence trail.
