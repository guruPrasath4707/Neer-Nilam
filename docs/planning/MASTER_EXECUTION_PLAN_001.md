# Neer-Nilam — Master Execution Plan 001

Date: 2026-10-09  
Status: Active  
Current phase: **Software-first data-lake collection**

## Advisor direction

The team has pitched the overall concept to Judy ma'am. Guidance as relayed by the team: “She'll find a path for the physical representation. As far as now she said to us that to focus on the software part, that means dataset data lake collection.”

Immediate priority therefore moves to source acquisition, data rights, local data lake structure, provenance/checksums and normalization. Physical-display work is parked as an immediate task while Judy ma'am explores options. It remains undecided, not cancelled.

## Current objective

Build a reproducible, source-linked Brihadisvara vertical slice from a carefully collected subset of data, then grow the Thanjavur–Kumbakonam–Cauvery corpus. No statewide mass dump.

Target flow:

**source registry → rights → raw collection → checksums/licence inventory → normalized record → evidence assertion → supported temporal state or explicit GAP → scene pack → replaceable presentation client**

## Workstreams

### W1 — Data lake and source rights (active)

- Use data/manifests/data-lake-acquisition-v1.csv as the actionable acquisition queue.
- Run scripts/collection/Collect-NeerNilamData.ps1 locally against the Seagate drive.
- Initial collection: DHARMA Tamil Nadu, DHARMA SII, HydroRIVERS Asia, bounded OSM extract.
- Generate checksum manifest and XML-level licence inventory.
- Stage CHIRPS v3 rainfall, ESA WorldCover, JRC Global Surface Water, and Copernicus DEM only after selecting a regional/time subset.
- Keep TNGIS/WRD, NWDP/CWC, CICT manuscript images, Kaggle, and Open Heritage 3D behind their rights / terms / item / size gates.

### W2 — Normalize and validate software data (next)

- Parse DHARMA EpiDoc/XML without flattening original text, editorial markup, uncertainty tags or bibliography.
- Discover records relevant to Brihadisvara and the corridor; do not assume every inscription has an exact location.
- Preserve original source IDs, commit SHA, file path, declared license URI, retrieval date and SHA-256.
- Create canonical entities only from stable identifiers and supported metadata.
- Convert claims into evidence assertions with source locators, temporal semantics, confidence and verification status.
- Treat records without enough information as candidate/reference-only, not trusted historical facts.

### W3 — Historical state and scene-pack software

- Select three defensible Brihadisvara states only after source review and, where possible, expert input.
- Preserve explicit NO_SUPPORTED_RECONSTRUCTION GAP behavior.
- Build deterministic scene-pack generation and a local React + Three.js/R3F renderer.
- Include object selection, evidence panel, water/context layer, flat fallback and explicit uncertainty.
- No continuous historical morphing unless a source-supported transformation model exists.

### W4 — Water, land and environmental context

- Separate modern water/land-cover observations from historical water features and claims.
- Select and document exact spatial resolution, CRS, vintage, time cadence and licence for every raster/vector layer.
- Do not infer that a present-day mapped channel existed in an ancient period without independent historical evidence.
- Do not assert causal connections between ancient irrigation and modern groundwater/rainfall without a validated analysis design.

### W5 — Physical presentation (paused as immediate build; undecided)

- Judy ma'am is exploring a path for the physical representation.
- Preserve the existing comparison of Pepper's Ghost, projection-mapped physical relief and hybrid options.
- Do not buy expensive hardware now.
- If resumed, use the same evidence-linked scene across candidate renderers and choose only after measured comparison.

## Gate order

1. Gate A — data acquisition and audit: local collection run, permissions, checksums, licence inventory and source snapshots.
2. Gate B — normalization: EpiDoc parser and source-linked canonical candidate records.
3. Gate C — historical evidence: reviewed claims, date intervals and spatial relationships; explicit data gaps.
4. Gate D — software scene: reproducible scene pack plus browser/flat renderer.
5. Gate E — physical proof: restart after advisor direction and once a stable software scene exists.
6. Gate F — presentation selection: only after measured evidence; no hardware commitment beforehand.

## Definition of done for the first data-lake/software vertical slice

- Acquisition manifest and full website trail updated.
- Local raw collection on Seagate with action log, source/version metadata and SHA-256.
- XML-level licensing inventory for collected epigraphy repositories.
- OSM query/response retained with retrieval timestamp and ODbL notes.
- Normalized candidate records link to exact source file and locator.
- At least 9 source-linked evidence assertions, each explicitly marked reviewed/unreviewed.
- Three supported historical states are source-defensible, or the unsupported state remains explicit until such support exists.
- One rights-cleared temple asset and one terrain/water context layer.
- One deterministic scene pack with a flat renderer and explicit data gap.

## Stop rules

Do not mass-download statewide/global data; do not access restricted sources without authorization; do not treat public GitHub as proof of dataset rights; do not treat generic handwritten-character datasets as validated historical epigraphy data; do not commit raw third-party or permission-sensitive data into this public repository; do not promote AI output or unsourced dates to trusted history.

## Immediate queue

1. Run the collector dry run on the Windows machine.
2. Confirm the mounted external Seagate volume and sufficient free space.
3. Run the confirmed Tier-0 collection.
4. Review log, per-file XML licences and checksums.
5. Build the EpiDoc parsing/triage script and identify corpus records related to the pilot.
6. Stage bounded rainfall, water, land cover, and DEM subsets.
7. Build canonical entities/evidence assertions and the deterministic scene pack.
8. Resume physical proof work only when the software scene and Judy ma'am's direction make it useful.
