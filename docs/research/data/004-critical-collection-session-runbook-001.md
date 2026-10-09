# Neer-Nilam Critical Acquisition and Seagate Organization Runbook

Date: 2026-10-09
Repository: https://github.com/guruPrasath4707/Neer-Nilam
Local clone: C:\Users\gurun\source\Neer-Nilam
Seagate data lake: F:\Neer-Nilam-DataLake

## Status distinction

The initial four source tasks are already collected and the first 581-file hash audit passed. The follow-on download session is NOT completed until the local run manifest confirms which files passed validation.

## What the critical script does

1. Verifies the target volume and free space; requires an explicit confirmation.
2. Creates canonical folders for raw datasets, derived assets, evidence, scene packs, physical-display research, documents, logs, reports and quarantine.
3. Moves existing DHARMA, HydroRIVERS and OSM roots to canonical folders while retaining their old paths with NTFS junctions. Aborts rather than merges if both old and new paths already exist.
4. Creates or appends the root Log.txt without replacing an existing file.
5. Copies the Word dossier and acquisition manifest from GitHub to the HDD.
6. Attempts selected 2016-2025 monthly CHIRPS v3 files; the TN Season and Crop Report 2024-2025; Statistical Handbook climate/rainfall, agriculture and irrigation PDFs; dynamic CGWB yearbook link discovery; and one ESA WorldCover tile candidate.
7. Validates PDF/TIFF signatures and minimum sizes, retries downloads, quarantines invalid payloads, and creates run manifests and checksums.
8. Records gated JRC surface water, Copernicus DEM, Census, historical maps, manuscripts, Kaggle, TNGIS and heritage 3D instead of scraping or presuming rights.
9. Writes a per-run JSONL log, CSV acquisition manifest, SHA-256 inventory, source note and sanitized summary. Optional metadata publishing stages generated metadata only, never raw datasets.

## Step 1 — synchronize the clone

    git -C 'C:\Users\gurun\source\Neer-Nilam' status --short
    git -C 'C:\Users\gurun\source\Neer-Nilam' pull --ff-only origin main

If status shows local changes, inspect them before pulling.

## Step 2 — safe dry run

    pwsh -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\gurun\source\Neer-Nilam\scripts\collection\Prepare-NeerNilamCriticalData.ps1' -DestinationRoot 'F:\Neer-Nilam-DataLake'

Dry run creates no files and performs no downloads.

## Step 3 — execute the collection

    pwsh -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\gurun\source\Neer-Nilam\scripts\collection\Prepare-NeerNilamCriticalData.ps1' -DestinationRoot 'F:\Neer-Nilam-DataLake' -Execute

Confirm the displayed drive model/label is the intended Seagate, then type COLLECT-NEERNILAM-P0. Keep the HDD connected until completion.

The default rainfall period is January 2016 through December 2025: at most 120 selected monthly global TIFFs, expected around 2.5-3 GiB. This is not a mirror of the complete CHIRPS 1981-present archive. Clip valid files to the pilot corridor before analysis.

## Step 4 — optional GitHub metadata publish

After inspecting local run outcomes, use the Execute command with PublishMetadata:

    pwsh -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\gurun\source\Neer-Nilam\scripts\collection\Prepare-NeerNilamCriticalData.ps1' -DestinationRoot 'F:\Neer-Nilam-DataLake' -Execute -PublishMetadata

The script requires a separate exact PUBLISH-METADATA confirmation. Only the generated summary, manifest, checksum CSV and Log snapshot are staged.

## Folder taxonomy

00_ADMIN: manifests, source notes, licences, checksums and provenance
01_RAW_DATA: epigraphy, hydrology, geospatial, climate, groundwater, agriculture, land cover, surface water, terrain, Census, historical maps, manuscripts, OCR and heritage 3D
02_WORKING_DERIVED: derived rasters, vectors and tables
03_EVIDENCE_MODEL: sources, claims, entities and historical states
04_SCENE_PACKS: renderer-neutral Brihadisvara scene packs
05_PHYSICAL_REPRESENTATION: research and prototypes
06_PROJECT_DOCUMENTS: Word dossier
07_LOGS: per-run JSONL logs
08_REPORTS: audits
09_QUARANTINE: invalid or partial downloads

Old raw source paths are kept as compatibility junctions where reorganization succeeds.

## Manual and rights-gated sources

JRC Global Surface Water requires tile/layer/version selection. Copernicus DEM uses official GLO-90 access and current terms; do not bypass GLO-30 eligibility restrictions. Census requires exact file and terms review. NAI, Abhilekh Patal and David Rumsey items require catalogue and reproduction checks. CICT/Kriti Sampada images need item-level rights. Kaggle uTHCD requires authenticated access and rule review; isolated handwriting is not an inscription corpus. TNGIS/WRD requires permitted API/data access. Open Heritage 3D requires item-specific site, size, metadata and licence review.

DHARMA README-versus-XML licence conflicts remain unresolved. Keep the corpus on hold for redistribution and public reusable derivatives until written clarification. Recent rainfall, groundwater, crop data, land cover, OSM and HydroRIVERS are modern context, not proof of ancient states.
