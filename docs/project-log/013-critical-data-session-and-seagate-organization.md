# Project Log 013 — Critical Data Acquisition and Seagate Organization

Date: 2026-10-09
Status: Planning and script committed; Windows execution pending

The user requested the critical download pass, canonical categorization on Seagate, an append-only root Log.txt and a Word document with project history and physical-representation research. The priority relayed after the Judy ma'am pitch remains software and dataset/data-lake collection. Judy ma'am is exploring physical representation; no display purchase or final selection is approved.

## Script

scripts/collection/Prepare-NeerNilamCriticalData.ps1, version 1.1.0. Dry-run by default, checks target drive and free space, requires exact confirmation, creates canonical folders, moves initial sources while keeping old paths as junctions, appends Log.txt, copies the Word dossier and manifest, downloads selected open sources with signature validation, logs source failures and gated rights/access, and writes session log, manifest and checksums. Optional metadata publishing separately requires PUBLISH-METADATA and does not stage raw datasets.

## Priority 0

- Reorganize the already-collected DHARMA, HydroRIVERS and OSM sources.
- Request monthly CHIRPS v3 from 2016-2025 as a bounded temporal baseline; later clip to the local corridor.
- Download and validate the Tamil Nadu Season and Crop Report 2024-2025 and Statistical Handbook climate/rainfall, agriculture and irrigation PDFs.
- Discover and validate the official CGWB Tamil Nadu/Puducherry yearbook PDF; mark manual if a direct PDF cannot be validated.
- Attempt one ESA WorldCover tile candidate only with strict TIFF validation; failed candidate stays logged as failure.

## Priority 1 gates

JRC Global Surface Water tile/version; Copernicus DEM GLO-90 and access; Census files/terms; National Archives/Abhilekh Patal/David Rumsey map and archive records; CICT/Kriti Sampada manuscript items; Kaggle uTHCD rules; TamilOCR/TamilNet upstream rights; TNGIS/WRD permission/API; Open Heritage 3D item rights.

## Folder taxonomy and Word dossier

Canonical folders: 00_ADMIN, 01_RAW_DATA, 02_WORKING_DERIVED, 03_EVIDENCE_MODEL, 04_SCENE_PACKS, 05_PHYSICAL_REPRESENTATION, 06_PROJECT_DOCUMENTS, 07_LOGS, 08_REPORTS and 09_QUARANTINE. The dossier captures logs 001-012, verified first collection, checksums, DHARMA discrepancy, prioritized source plan, evidence architecture and the Pepper's Ghost versus relief projection versus hybrid comparison.

## Physical representation

Pepper's Ghost is a low-cost focal floating-image proof. Projection-mapped physical relief represents terrain, water, settlement and routes more directly. Hybrid relief + projection + optional focal optical layer remains the best current exhibition hypothesis only after independent low-cost tests with the same source-backed scene. Keep source/evidence/uncertainty on a separate accessible interface. Judy ma'am is exploring the physical path; implementation remains undecided.

## Critical limitation

The follow-on downloads have NOT happened in this tool session. The local script has to run on Windows with the actual HDD connected. A plan is not proof of a download: trust the local session manifest, source logs, file signatures and SHA-256 values. DHARMA raw XML and public reusable derivatives remain on hold until written licence clarification resolves README-vs-file declarations.
