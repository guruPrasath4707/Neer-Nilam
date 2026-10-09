# Neer-Nilam

**A Spatiotemporal Digital Heritage Intelligence Platform for Tamil Nadu**

Neer-Nilam explores how Tamil Nadu's historical landscape can be represented as a time-aware, spatially connected digital system linking heritage sites, people, events, inscriptions, manuscripts, settlements, water systems, agriculture, and modern environmental context.

## Current priority

**Software foundations and dataset/data-lake collection**, following the guidance relayed after pitching the project to Judy ma'am. Judy ma'am is exploring a path for the physical representation. The physical display choice remains open and is not the current implementation gate.

The pilot remains focused on the **Thanjavur–Kumbakonam–Cauvery corridor**, beginning with a source-linked Brihadisvara vertical slice, not a statewide data dump.

## Core principles

- Evidence and provenance come before visual spectacle.
- AI-assisted reconstruction is provisional until expert verification.
- Historical states are represented from evidence rather than invented continuous morphing.
- Modern geography is not silently substituted for historical geography.
- Source rights, attribution, uncertainty and transformations are recorded.
- Raw datasets should be stored on the user's external data drive, not committed to this public repository unless redistribution rights are explicitly cleared.
- The presentation layer remains replaceable; no final physical display technology has been selected.

## Data collection

The curated acquisition queue is data/manifests/data-lake-acquisition-v1.csv. The master website/source trail is docs/sources/WEBSITE_INDEX.md.

The first-stage Windows collector is scripts/collection/Collect-NeerNilamData.ps1. The critical follow-on session is scripts/collection/Prepare-NeerNilamCriticalData.ps1; it organizes the existing Seagate data lake, appends Log.txt, copies the Word dossier, attempts selected monthly CHIRPS v3 and official statistical report downloads with file-signature validation, and records access/rights-gated resources. It is dry-run by default and requires explicit execution and confirmation. Run locally in PowerShell 7. Public GitHub does not receive raw datasets.

Dry run:
    pwsh -ExecutionPolicy Bypass -File .\scripts\collection\Collect-NeerNilamData.ps1 -DestinationRoot 'F:\Neer-Nilam-DataLake'

Confirmed collection, only after verifying that the destination is the actual Seagate volume:
    pwsh -ExecutionPolicy Bypass -File .\scripts\collection\Collect-NeerNilamData.ps1 -DestinationRoot 'F:\Neer-Nilam-DataLake' -Execute

It downloads only the initial public/reviewable set: DHARMA Tamil Nadu epigraphy, DHARMA SII with per-file XML licence inventory, HydroRIVERS Asia, and a bounded current OSM corridor extract. It does not automatically download Kaggle data, manuscript images, restricted government GIS, whole-world raster collections, or large 3D datasets.

Read docs/research/data/003-data-lake-collection-plan-001.md and docs/research/data/004-critical-collection-session-runbook-001.md before acquisition. The follow-on source queue is data/manifests/critical-data-acquisition-session-v1.csv. The Word project-history and physical-representation dossier is stored at docs/project-dossier/Neer-Nilam_Project_History_and_Collection_Dossier_2026-10-09.docx. A public webpage is not blanket permission to republish its data or images.

## Project log

Major ideas, prompts, research results, decisions, assumptions, rejected approaches, collection milestones, permissions and current status are recorded in docs/project-log/. Routine commands are not individually logged.

## Repository status

**Visibility:** Public  
**Phase:** software-first data-lake collection  
**Pilot start:** Brihadisvara Temple, Thanjavur  
**Physical representation:** undecided; guidance path is being explored by Judy ma'am  
**Application implementation:** not yet started
