# Project Log 007 — Local Collector Launch Blocker and Recovery

Date: 2026-10-09
Status: Collector verified on GitHub; local execution not started

## What happened

The first attempt to update and launch the collector was run from PowerShell's current directory `C:\Windows\System32`. Therefore:

- `git pull origin main` failed because this directory is not a Git working tree.
- The relative path `./scripts/collection/Collect-NeerNilamData.ps1` could not resolve because it is relative to the current directory, not to the Neer-Nilam repository.
- These errors occurred before the collector started. No data-lake collection was performed by these commands.

## Repository verification

The public repository `guruPrasath4707/Neer-Nilam` is reachable, its default branch is `main`, and the collector is present at:

`scripts/collection/Collect-NeerNilamData.ps1`

The README confirms that the collector is dry-run by default. Its initial intended set is DHARMA Tamil Nadu epigraphy, DHARMA SII epigraphy with an XML-level licence inventory, HydroRIVERS Asia, and a bounded current OpenStreetMap/Overpass cutout. It does not bulk-download Kaggle datasets, permission-sensitive manuscript images, or restricted government GIS.

## Recovery sequence

1. Locate the existing local clone using known project locations. If no clone is found, create a separate fresh clone in a clearly named user source folder without overwriting an existing directory.
2. Inspect `git status`. Do not pull over uncommitted or untracked local work; review it first.
3. Update a clean clone using `git pull --ff-only origin main`.
4. Confirm the collector file exists and run it without `-Execute`. This is the dry-run check.
5. Before collection, verify the actual physical disk model, volume label, drive letter and available space. Only then run with `-Execute` and follow the collector's explicit confirmation prompts.
6. Review run logs, checksums, failed items and per-record licence inventory before treating any collected data as usable.

## Status and guardrails

- Repository collector: verified remotely; no claim that it has run locally.
- Seagate data downloads: **not yet completed**.
- No destructive Git action or forced reset is part of this recovery.
- Keep raw datasets on the external data drive; keep manifests, source records, code and project logs in GitHub.
- The active project direction remains software-first data-lake collection following the guidance relayed after the pitch to Judy ma'am; physical representation remains open while she explores a path.
