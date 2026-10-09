# Neer-Nilam — Data-Lake Collection Plan 001

Date: 2026-10-09  
Status: Active — software/data focus  
Scope: Thanjavur–Kumbakonam–Cauvery pilot, beginning with the Brihadisvara vertical slice

## Advisor update

The team has pitched the project and its overall concept to Judy ma'am. The guidance relayed by the team is:

> “She'll find a path for the physical representation. As far as now she said to us that to focus on the software part, that means dataset data lake collection.”

This changes the immediate priority, not the project's evidence or rights standards. The physical representation track remains open and is parked for now while Judy ma'am explores a path. Do not purchase display hardware or describe the physical architecture as selected.

## Collection objective

Create a reproducible local data lake on the external Seagate HDD. Collect small, high-value, source-linked inputs first; document the rest as acquisition tasks; then normalize only the subset needed for the first software slice. Keep raw data out of the public GitHub repository unless there is a specific reason and redistribution rights clearly permit it.

Required flow:

**source registry → lawful acquisition → raw files → checksum and source snapshot → licence inventory → normalized candidate records → evidence assertions → historical states → deterministic scene pack**

## Data domains in the proposal

1. **Heritage authority and archaeology:** monument identity, official descriptions, conservation/restoration records, field/site plans and archaeological publications.
2. **Epigraphy and inscriptions:** structured EpiDoc/XML editions, inscription identifiers, text/translation/edition, rulers/donors/places, stated dates and explicit locators.
3. **Historical geography:** historical maps, place names, settlements, routes, political geography and source-backed event locations. Modern map features must not be treated as historical footprints.
4. **Water systems:** Cauvery and tributaries, tanks, canals, anicuts, temple tanks, command areas, historical water references and current mapped water features.
5. **Terrain and land cover:** elevation model, derived terrain, current land cover and relevant hydrological surfaces. Preserve resolution, CRS, date, processing lineage and licence.
6. **Rainfall, groundwater and agriculture:** bounded, time-aware modern datasets for context. Avoid causal claims unless independently supported.
7. **Manuscripts and Tamil language:** metadata first; images only where item-level rights and permissions allow. Distinguish catalogue date, manuscript date, text date and digitization date.
8. **3D/photogrammetry:** only selected assets with verified site identity, capture metadata, geometry quality and reusable rights.
9. **OCR/AI benchmark data:** domain-fit and licence review before training. Generic isolated character images are not a substitute for damaged stone inscriptions or palm-leaf manuscripts.

## Tier 0 — first local collection run

The checked-in PowerShell collector downloads only these bounded/reviewable inputs:

- DHARMA Tamil Nadu epigraphy repository (shallow clone; repository states edited XML is CC BY 4.0; retain requested attribution).
- DHARMA South Indian Inscriptions repository (shallow clone plus an XML-level licence inventory; record-level declarations can differ).
- HydroRIVERS v1 Asia shapefile archive (about 91 MB compressed according to the source page; preserve archive and licence/citation).
- A bounded modern OpenStreetMap/Overpass extract covering the Thanjavur–Kumbakonam corridor (ODbL; keep query, retrieval date and attribution).

The script is **dry-run by default**. It writes only after the Execute switch, verifies the destination volume, requires a human confirmation, logs each action, preserves original downloads, and generates SHA-256 records. It does not install software packages or download Kaggle data.

## Tier 1 — prepare regional subsets, not global dumps

- **Copernicus DEM:** use a bounded tile/area. Current access guidance says GLO-90 is available to the general public, while GLO-30 access is restricted to defined authorized user categories; check account eligibility rather than bypassing access controls.
- **ESA WorldCover 2021 v200:** CC BY 4.0, 10 m land-cover product. Select only tiles intersecting the pilot. The worldwide product is roughly 117 GB; never sync the whole global map for this pilot. It is a modern snapshot, not historic land cover.
- **JRC Global Surface Water 1984–2024:** select the required layer and regional subset; preserve EC JRC/Google attribution and the required citation. Surface-water observations do not prove an ancient tank existed.
- **CHIRPS v3 rainfall:** public data under CC BY 4.0, with data spanning 1981 to near-present at about 0.05-degree resolution. Choose a period/cadence and clip to the study region before keeping a large time series. Preserve the distinction between final and preliminary products.
- **OpenHistoricalMap:** audit actual corridor feature coverage and item tags before relying on it. Data is CC0 by default unless a feature-level licence override exists.
- **Census of India:** download only relevant Thanjavur catalogue files, record file version and applicable Census/ORGI terms, and cite the exact table/page for extracted facts.

## Tier 2 — permission and item-rights gates

- **TNGIS / Tamil Nadu WRD:** no bulk copy, scraping, redistribution or production use until access/terms and rights are confirmed.
- **NWDP/CWC:** acquire the exact published KML/GeoJSON/SHP resource only after preserving dataset metadata and terms.
- **CICT manuscript library:** discover and record IIIF manifests first. Image rights are per item; a currently visible item shows CC BY-NC 4.0, which may be incompatible with future commercial reuse. No bulk image harvesting.
- **Kriti Sampada/NMM:** metadata assists discovery; it is not a blanket licence for digitized manuscript images.
- **Open Heritage 3D:** each dataset has its own Creative Commons licence and the source reports average download size around 25 GB per site. Select one appropriate dataset and verify its licence/size before requesting it.
- **Kaggle uTHCD/Tamil Handwritten Character Recognition:** listed as about 1.12 GB and subject to competition rules. It contains isolated handwritten characters, not historical inscriptions or palm-leaf folios. Keep as optional baseline research until rules, rights and domain fit are reviewed.
- **TamilOCR/TamilNet GitHub repositories:** code and dataset rights are separate. Do not assume the upstream HP Labs dataset is redistributable simply because model code is public.

## Seagate folder layout

The collector creates this local layout below the chosen target root:

- 00_admin/manifests — acquisition list and run metadata
- 00_admin/licences — licence inventory and source notices
- 00_admin/checksums — SHA-256 manifest
- 01_raw/epigraphy — unchanged public repository snapshots
- 01_raw/hydrology — unchanged HydroRIVERS archive and extraction
- 01_raw/spatial — bounded OSM response and query
- 02_restricted_not_downloaded — only notes/manifests; no restricted source payloads
- 03_normalized — later curated, schema-bound data
- 04_evidence — source-linked assertions and review status
- 05_derived — reproducible derived layers/assets
- 06_logs — JSONL action log
- 07_quarantine — malformed, duplicate, uncertain or rights-unclear files awaiting review

Do not put API keys, passwords or Kaggle tokens in the repository, manifests, logs or filenames. Do not commit raw data or credentials to public GitHub.

## Completion gates for this collection phase

1. Script and acquisition manifest are committed.
2. User runs a dry-run and then an explicit confirmed collection on the external Seagate HDD.
3. Downloaded files have URL, access timestamp, byte size, SHA-256 and source/version recorded.
4. DHARMA XML has a per-file licence inventory.
5. OSM has a retained query, retrieval date, object identifiers, and attribution.
6. Rights-gated sources remain uncollected until permissions/terms are resolved.
7. Next software task: parse selected records into canonical entities/evidence, with no unsupported historical dates or locations promoted to trusted data.

## Research references

The full website/source trail is in docs/sources/WEBSITE_INDEX.md. The actionable dataset rows are in data/manifests/data-lake-acquisition-v1.csv; existing project source IDs remain in data/manifests/source-registry-v0.csv.
