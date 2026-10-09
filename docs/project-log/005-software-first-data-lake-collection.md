# Project Log 005 — Software-First Data-Lake Collection

Date: 2026-10-09  
Status: Active — collection workflow committed; local run pending

## Advisor checkpoint and immediate priority

The team has pitched the overall Neer-Nilam concept to Judy ma'am. The guidance relayed by the team is:

> “She'll find a path for the physical representation. As far as now she said to us that to focus on the software part, that means dataset data lake collection.”

Accordingly, the active focus is now **software foundations and dataset/data-lake collection**. Judy ma'am is exploring a path for physical representation. That physical track is paused as an immediate implementation priority, not cancelled; there is no final display selection and no hardware purchase.

## Collection work committed

- Added a data-lake acquisition manifest that distinguishes auto-downloadable candidates from rights, login, licence, size and relevance gates.
- Added a Windows PowerShell collector that targets a local Seagate data-lake root, defaults to dry-run, requires the Execute switch plus confirmation, and records action logs and checksums.
- First collection candidates: DHARMA Tamil Nadu epigraphy, DHARMA SII epigraphy with a per-file XML licence scan, HydroRIVERS Asia, and a bounded OpenStreetMap/Overpass corridor extract.
- Added contemporary land cover, surface water, rainfall, terrain, Census, historical map and OCR discovery sources to the acquisition queue.
- Updated the master website index with research pages inspected in this pass (W188 onward), including useful, rights-gated and reference-only sources.
- Extended the source registry with licence and usage notes for new source families.

## Important findings and guardrails

1. DHARMA Tamil Nadu repository describes its edited XML as CC BY 4.0 and asks for attribution to the project, funder and editors.
2. SII XML examples include CC BY-SA 4.0 declarations. Do not apply one repository-level licence to every record; the collector generates an XML-level licence inventory.
3. HydroRIVERS Asia shapefile is a useful regional network layer, but it generalizes river reaches and is not a complete inventory of small channels, tanks or historical irrigation structures.
4. OpenStreetMap is ODbL. The bounded cutout is current mapped geography, not a historical map.
5. ESA WorldCover is a contemporary 10 m product; only area-specific tiles are appropriate. Its global archive is too large for blind bulk download.
6. JRC Global Surface Water has a current 1984–2024 product and requires acknowledgement/citation; detected water is not proof of historic infrastructure.
7. CHIRPS v3 offers a public-domain/CC BY 4.0 rainfall series since 1981, but regional/time-window clipping should precede sustained collection.
8. Copernicus DEM GLO-30 access is subject to authorized-user categories; current guidance says general users can access GLO-90. The collector does not attempt to bypass access controls.
9. CICT images, TNGIS/WRD, NWDP/CWC, Kaggle competition data, and Open Heritage 3D assets remain gated by item/terms/permission/size review.
10. Kaggle's uTHCD set is isolated Tamil handwritten characters, not an epigraphy or palm-leaf corpus. It is optional benchmark material, not evidence that an OCR model can read damaged inscriptions.

## Storage and privacy decision

Raw research data should live on the user's external drive, not in this public GitHub repository, unless each artefact's redistribution rights are explicitly cleared. GitHub holds source records, manifests, schemas, scripts, checksums, attribution, transforms and project logs. Restricted images/data are not copied to the lake until permissions are confirmed.

## Current status

- Documentation and collection script: committed to repository.
- Data downloaded to the user's Seagate HDD by this chat: **not yet done**. The collection must be run on the Windows computer where the external drive is connected.
- Physical display architecture: undecided; Judy ma'am is exploring options.
- Next: run the script in dry-run mode, verify the target is the Seagate volume, then run the confirmed collection; review logs/checksums and begin normalization of the relevant inscription and spatial records.
