# Neer-Nilam — Project History, Critical Data-Lake Collection and Physical Representation Dossier

**Prepared:** 9 October 2026  
**Status:** first collection and integrity audit verified; critical follow-on session prepared; local execution pending  
**Pilot:** Thanjavur–Kumbakonam–Cauvery corridor, beginning with source-linked Brihadisvara evidence

## 1. Executive summary

Neer-Nilam is a source-aware, spatiotemporal digital heritage intelligence platform. It is not just a hologram or decorative 3D temple. Its core connects historical time, monument, landscape, water systems, settlements, people/events and evidence. A scene composer will produce presentation-neutral scene packs for web GIS, Pepper's Ghost, projection mapping, AR/MR, VR and museum displays.

The team pitched the concept to Judy ma'am. The guidance relayed by the team is that she will explore a path for physical representation and that the immediate focus should be the software part: dataset and data-lake collection. This records the team's report, not an independent statement from the advisor.

## 2. Verified initial collection

The Seagate Expansion Drive was verified as F:, NTFS, USB, online, 931.51 GiB reported capacity and 374 GiB free at the initial inspection.

Initial destination: F:\Neer-Nilam-DataLake  
Run ID: 20261009-111437

| Dataset | Verified result | Important caveat |
|---|---|---|
| DHARMA Tamil Nadu epigraphy | Shallow clone, commit ab94f9e525e2ce21938e63ac93fd80aa78a4e423 | README-vs-XML licence conflict; hold reuse pending clarification |
| DHARMA South Indian Inscriptions | Shallow clone, commit dfa95be6729f162c0e7b70eea15c51da94520ff4 | README-vs-XML licence conflict; hold reuse pending clarification |
| HydroRIVERS Asia | 86.32 MiB ZIP downloaded/extracted; ZIP SHA-256 29780B0A75F90024F22E7E2029E5E3045F7325CDA0528DB65C5CC4C864B98525 | Generalized river network, not a full local tank/canal inventory |
| OpenStreetMap/Overpass | 998 elements saved from bounded corridor query | Modern mapped geography, not historical evidence |

Read-only integrity audit: **581/581 manifest hashes matched**, zero missing files and zero mismatches. The run log had no FAILED, BLOCKED, PARTIAL_RETAINED, REVIEW_REQUIRED or CHECKSUM_FAILED events.

## 3. DHARMA rights discrepancy — open blocker

The inventory contains 553 XML rows:
- 507 files had a matching licence target declaring CC BY-SA 4.0.
- 46 files had no matching licence target detected by the current inventory expression.

The READMEs of both repositories say their edited XML files are CC BY 4.0. Sample files at the collected commits declare CC BY-SA 4.0. “No licence target detected” is the inventory result, not a legal finding that no licence applies.

**Decision:** keep the exact source snapshots and commits for local preservation/technical inspection. Do not redistribute the corpora, publish copied XML, or incorporate inscription text into public reusable derived products until the DHARMA maintainers clarify the governing licence and missing-tag treatment in writing. Preserve the correspondence, date, exact record URI and response in the rights register.

References:
- [Tamil Nadu corpus README at collected commit](https://github.com/erc-dharma/tfa-tamilnadu-epigraphy/blob/ab94f9e525e2ce21938e63ac93fd80aa78a4e423/README.md)
- [SII corpus README at collected commit](https://github.com/erc-dharma/tfa-sii-epigraphy/blob/dfa95be6729f162c0e7b70eea15c51da94520ff4/README.md)
- [Tamil Nadu XML sample with CC BY-SA declaration](https://github.com/erc-dharma/tfa-tamilnadu-epigraphy/blob/ab94f9e525e2ce21938e63ac93fd80aa78a4e423/DHARMA_INSTamilNadu00031.xml)
- [SII XML sample with CC BY-SA declaration](https://github.com/erc-dharma/tfa-sii-epigraphy/blob/dfa95be6729f162c0e7b70eea15c51da94520ff4/DHARMA_INStfaSIIv05p1i0228.xml)

## 4. Chronological project history: Logs 001–013

| Log | Date | Milestone |
|---|---|---|
| 001 | 7 Oct 2026 | Immersive heritage concept: time → monument → landscape → water → people/events → evidence. Early DeepSeek directions were hypotheses. |
| 002 | 7 Oct 2026 | Source research and display options: Pepper's Ghost, transparent displays, projection mapping, light-field, volumetric and AR/MR. No expensive hardware before a measured proof. |
| 003 | 7 Oct 2026 | Stage-1 physical-presentation report archived as input to validation. D018 blocks expensive display purchases before proof gates. |
| 004 | 8 Oct 2026 | Physical relief + dynamic projection + optional optical overlay + separate evidence UI became leading exhibition hypothesis; data and evidence schemas documented. |
| 005 | 9 Oct 2026 | Software-first data-lake collection prioritized after the advisor checkpoint. |
| 006 | 9 Oct 2026 | Groundwater, agriculture, historical map and archive catalogue sources added. |
| 007 | 9 Oct 2026 | Local run attempt failed from C:\Windows\System32; no collection occurred in that attempt. |
| 008 | 9 Oct 2026 | Fresh clone at C:\Users\gurun\source\Neer-Nilam; Git pull up to date and dry-run returned no writes/downloads. |
| 009 | 9 Oct 2026 | Seagate F: verified as USB/NTFS, online, 931.51 GiB capacity and 374 GiB free at initial inspection. |
| 010 | 9 Oct 2026 | First data collection completed: DHARMA Tamil Nadu and SII, HydroRIVERS Asia, OSM, licence inventory and SHA-256 manifest. |
| 011 | 9 Oct 2026 | Integrity audit: 581 hashes matched, zero missing, zero mismatches. |
| 012 | 9 Oct 2026 | DHARMA README-vs-XML licence discrepancy confirmed and marked HOLD_LICENSE_RECONCILIATION. |
| 013 | 9 Oct 2026 | Critical session queue, organizer, root Log.txt, runbook and Word dossier prepared; local execution remains pending. |

Full chronological entries are maintained in [docs/project-log/](../project-log/). Master timeline: [Log.txt](../project-log/Log.txt).

## 5. Critical acquisition priorities

### Priority 0: local session candidates

1. Reorganize the already-collected DHARMA, HydroRIVERS and OSM assets into canonical folders, keeping compatibility junctions so previous manifest paths can still resolve.
2. Request CHIRPS v3 monthly global rainfall files for January 2016–December 2025 (up to 120 files, expected around 2.5–3 GiB), then clip valid rasters to the pilot corridor. This is not a mirror of the complete 1981–present archive.
3. Download and validate the official Tamil Nadu Season and Crop Report 2024–2025.
4. Download and validate selected Tamil Nadu Statistical Handbook 2023–24 sections for climate/rainfall, agriculture and irrigation.
5. Discover the official CGWB Groundwater Year Book Tamil Nadu/Puducherry 2024–2025 PDF. If the current portal uses a dynamic link that cannot be verified, mark it manual rather than claiming success.
6. Attempt one candidate ESA WorldCover 2021 v200 3×3-degree tile. A failed URL or invalid response is a logged failure, never an accepted raster.

### Priority 1: manual, regional and/or rights-gated

- JRC Global Surface Water 1984–2024: select layer/version and appropriate tile.
- Copernicus DEM GLO-90: use the official access path and selected regional tile; do not bypass GLO-30 eligibility limits.
- Census of India: select exact Thanjavur files and terms.
- National Archives of India, Abhilekh Patal and David Rumsey: catalogue discovery, exact local-scale map/record selection and item-level access/reproduction review.
- CICT/Kriti Sampada: identify relevant manuscript items first; manuscript image rights differ from catalogue access.
- Kaggle uTHCD: requires authenticated account and current competition-rules review; isolated handwritten characters are not a substitute for inscription/palm-leaf images.
- TamilOCR/TamilNet: review code/model licence and upstream dataset terms separately.
- TNGIS/Tamil Nadu WRD: no bulk scrape until official API/terms/permission are confirmed.
- Open Heritage 3D: verify exact site coverage, file size, capture metadata and explicit dataset licence.

The active queue is [critical-data-acquisition-session-v1.csv](../../data/manifests/critical-data-acquisition-session-v1.csv). The script writes a local per-run manifest, JSONL log, checksums and a sanitized optional GitHub summary. A plan or script is not proof of download: only the local validated manifest confirms a result.

## 6. Seagate folder taxonomy

- 00_ADMIN: manifests, source notes, licences, checksums and provenance.
- 01_RAW_DATA: epigraphy, hydrology, geospatial, climate, groundwater, agriculture, land cover, surface water, terrain, Census, historical maps, manuscripts, OCR and heritage 3D.
- 02_WORKING_DERIVED: derived rasters, vectors and tables, separate from raw inputs.
- 03_EVIDENCE_MODEL: source records, claims, entities and historical states.
- 04_SCENE_PACKS: renderer-neutral Brihadisvara scene packs.
- 05_PHYSICAL_REPRESENTATION: display research and experiments.
- 06_PROJECT_DOCUMENTS: project dossier and important handoffs.
- 07_LOGS: per-session JSONL logs.
- 08_REPORTS: audit reports.
- 09_QUARANTINE: invalid/partial downloads.

Root Log.txt is append-only and summarizes project milestones and session events. Existing raw source roots are moved only when the target does not exist; NTFS junctions remain at legacy paths. The script refuses a conflicting old/new path pair rather than merging or overwriting it.

## 7. Evidence and software architecture

Canonical flow:

**Source → Evidence → Entity → Historical State → Scene Pack → Presentation Client**

Record source identity, URL/version/commit, retrieval time, checksum, author/editor, publication context, historical/valid time, claim text, evidence class, support locators, contradictions, confidence basis, human review, licence/attribution, transformations and downstream scene packs.

Distinguish documented claims, archaeological observations, scholarly interpretation, AI-assisted proposals and unresolved/speculative claims. When evidence is missing, expose a GAP/NO_SUPPORTED_RECONSTRUCTION; do not silently substitute the nearest state or invent continuous history. Separate historical state changes from presentation fades and from scientifically supported analytical interpolation.

Modern OSM, HydroRIVERS, rainfall, groundwater, crop reports and land cover provide modern context, not direct proof of Chola-era geography or conditions.

## 8. Physical representation research and recommendation

The physical layer is a presentation client, not the core value of Neer-Nilam.

### Pepper's Ghost
A low-cost floating-image illusion using a concealed display and inclined reflector. Good for a focal temple/narrative highlight. Limitations include restricted viewing geometry, ambient-light and black-level sensitivity, alignment/ghosting, and no true volumetric image or physical landscape depth.

### Projection-mapped physical relief
A fabricated physical terrain/landscape model with calibrated projection layers. Strong semantic fit for elevation, river/water context, settlements, routes and spatial relations. Risks include projector calibration, shadows/occlusion, room light, fabrication and maintenance. Projection changes surface appearance but does not physically rebuild demolished/expanded geometry.

### Hybrid relief + projection + optional Pepper's Ghost
The strongest current exhibition hypothesis: relief as stable spatial substrate, projection for temporal/contextual layers, optional optical focal overlay for the monument, separate evidence interface and deterministic physical controls. It has added complexity and should proceed only if it demonstrates measurable benefit after simpler proofs.

### Decision gate
Judy ma'am is exploring the physical path. No final display decision or expensive hardware purchase is approved. Build a software scene and test low-cost Pepper's Ghost and relief-projection prototypes separately using the same source-backed scene. Test the hybrid only if those experiments support it. Measure illumination, useful viewing arc, ghosting, projection alignment, calibration time, readability, state-change comprehension and whether visitors understand uncertainty. Require reproducible setup, safety, offline operation and an accessible web/2D mirror.

## 9. Current run instructions

Repository and current script:
- [Prepare-NeerNilamCriticalData.ps1](../../scripts/collection/Prepare-NeerNilamCriticalData.ps1)
- [Critical collection runbook](../research/data/004-critical-collection-session-runbook-001.md)

Update the clone without overwriting unreviewed changes (PowerShell):
    git -C 'C:\Users\gurun\source\Neer-Nilam' status --short
    git -C 'C:\Users\gurun\source\Neer-Nilam' pull --ff-only origin main

Save the separately supplied Word dossier as Neer-Nilam_Project_History_and_Collection_Dossier_2026-10-09.docx in your Windows Downloads folder before running the organizer.

Dry run:
    pwsh -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\gurun\source\Neer-Nilam\scripts\collection\Prepare-NeerNilamCriticalData.ps1' -DestinationRoot 'F:\Neer-Nilam-DataLake'

Execute:
    pwsh -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\gurun\source\Neer-Nilam\scripts\collection\Prepare-NeerNilamCriticalData.ps1' -DestinationRoot 'F:\Neer-Nilam-DataLake' -Execute

Verify the displayed disk/volume/free space and type COLLECT-NEERNILAM-P0 only if it is the intended Seagate drive. Keep the drive connected until completion.

After auditing the local manifest, logs, hashes, source sidecars and quarantine, optional metadata publication:
    pwsh -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\gurun\source\Neer-Nilam\scripts\collection\Prepare-NeerNilamCriticalData.ps1' -DestinationRoot 'F:\Neer-Nilam-DataLake' -Execute -PublishMetadata

The script separately asks for PUBLISH-METADATA; only the sanitized summary, manifest, checksum file and Log snapshot are staged. Raw third-party datasets are not staged.

## 10. Next gates

1. Run the critical organizer/download session locally on the verified external drive.
2. Review each source's true outcome and hashes; do not treat a planned item as downloaded.
3. Obtain written DHARMA rights clarification before distribution or public reusable derivatives.
4. Record a human-reviewed disposition for the 46 no-tag records.
5. Select and normalize only relevant corridor records after rights and metadata review.
6. Build a small audited Brihadisvara evidence graph and deterministic renderer-neutral scene pack.
7. Use the same scene in low-cost Pepper's Ghost and relief-projection proofs. Decide any hybrid only from measured results.

## Non-negotiable guardrails

- Evidence/provenance over visual spectacle.
- Historical states are supported by evidence, not fabricated continuous morphing.
- Modern geography is not silently substituted for historical geography.
- AI-assisted reconstruction remains provisional until expert verification.
- Rights, attribution and uncertainty remain visible in metadata and the experience.
- Keep raw data on the external HDD; public GitHub carries code, manifests, documentation and sanitized reports only.
