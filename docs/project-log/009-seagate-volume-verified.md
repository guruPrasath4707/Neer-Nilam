# Project Log 009 — Seagate Destination Verified

Date: 2026-10-09
Status: Physical target verified; first collection run not yet executed

## Verified from the user's PowerShell output

The target drive inspection returned:

- Drive letter: `F:`
- Volume label: `Seagate Expansion Drive`
- File system: NTFS
- Physical disk number: 1
- Physical model: Seagate Expansion
- Bus type: USB
- Capacity reported by Windows: 931.51 GiB
- Free space reported by Windows: 374 GiB
- Disk operational status: Online

This matches the intended Seagate external HDD and exceeds the collector's 3 GiB minimum free-space check.

## Current collection status

- Repository: cloned locally at `C:\Users\gurun\source\Neer-Nilam`.
- Git update: `git pull --ff-only origin main` reported `Already up to date.`
- Collector dry run: successful; no data downloaded or lake directories created by dry-run mode.
- Physical destination check: successful according to the user's volume and disk output.
- Actual collection: **pending** until the user runs the collector with `-Execute` and types the exact confirmation `COLLECT`.

## Next action

Run:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\gurun\source\Neer-Nilam\scripts\collection\Collect-NeerNilamData.ps1' -DestinationRoot 'F:\Neer-Nilam-DataLake' -Execute
```

The collector will re-check the target, available space and confirmations, then attempt the two DHARMA Git snapshots, HydroRIVERS Asia archive and bounded current OSM extract. Review actual per-source outcomes, action logs, SHA-256 checksums and XML licence inventory after completion. A failed or partial download must not be treated as valid data.

## Scientific and rights guardrails

This is a starter collection, not a complete data lake. Current OSM features and generalized modern river data provide spatial context, not proof of historical waterways or structures. Review per-record epigraphy licence declarations and HydroSHEDS terms before redistribution. Kaggle datasets, manuscripts, restricted government data, and global raster collections remain separate, gated acquisition tasks.

Project priority remains software-first data-lake collection following the guidance relayed after pitching to Judy ma'am. Physical representation remains undecided while Judy ma'am explores a path.
