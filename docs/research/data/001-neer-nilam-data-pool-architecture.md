# Neer-Nilam Data Pool Architecture 001

Date: 2026-10-08
Status: Proposed canonical data strategy
Scope: Software dataset / evidence pool required to make the first Neer-Nilam demonstration real

## 1. Core principle

The Neer-Nilam data pool is **not a download folder**.

It is a versioned, spatial, temporal, evidence-linked and rights-aware system in which every important claim can answer:

- What is the entity?
- Where is it?
- When was it valid?
- When was it observed?
- What document/source supports it?
- What asset represents it?
- Who reviewed it?
- What rights apply to the source/asset?
- What transformations were performed?
- What uncertainty remains?

## 2. Data planes

Use six logical planes.

### Plane A — Source registry

Stores source identity and legal/provenance metadata.

Required fields:
- source_id
- organization
- title
- URL / locator
- source_type
- publication/update date
- access date
- license
- rights status
- permitted use
- restrictions
- attribution
- version
- checksum where applicable

### Plane B — Raw / restricted evidence

Stores original or restricted material only where access and retention are permitted.

Examples:
- downloaded source files
- source PDFs
- original map files
- manuscript images
- inscription images
- original 3D scans

This plane must not automatically become public application content.

### Plane C — Normalized canonical data

Stores project-controlled representations:
- normalized geometry
- normalized names
- normalized dates
- controlled vocabulary
- entity identities
- relationships
- temporal intervals

### Plane D — Evidence assertions

Stores individual claims and their support.

Example pattern:

Rajaraja I → commissioned/associated-with → Brihadisvara Temple

or:

WaterFeatureX → located-in → Thanjavur landscape

Each assertion must point to one or more sources.

### Plane E — Derived research artifacts

Examples:
- reconstructed historical state
- terrain tiles
- cleaned vector layers
- OCR/HTR output
- aligned inscription transcription
- generated 3D assets
- confidence calculations
- scene-ready datasets

These are derived works and need their own provenance.

### Plane F — Presentation scene packs

A scene pack is the frozen interface contract consumed by the display.

It should contain:
- scene version
- selected temporal state
- entities
- assets
- visible layers
- evidence references
- attribution
- uncertainty
- data gaps
- calibration/installation metadata where required

## 3. Canonical entity model

Every persistent object receives a stable ID.

Minimum conceptual fields:

Entity
- id
- entity_type
- canonical_name
- alternate_names
- geometry
- geometry_type
- spatial_reference
- valid_from
- valid_to
- observation_time
- document_time
- ingestion_time
- source_refs
- evidence_refs
- asset_refs
- rights_status
- confidence
- verification_status
- notes

Entity types should initially include:

- SITE
- MONUMENT
- TEMPLE
- STRUCTURE
- WATER_FEATURE
- RIVER
- CANAL
- TANK
- SETTLEMENT
- ROAD
- ROUTE
- PERSON
- DYNASTY
- RULER
- EVENT
- INSCRIPTION
- MANUSCRIPT
- TEXT
- AGRICULTURAL_FEATURE
- LAND_USE
- ENVIRONMENTAL_OBSERVATION
- 3D_ASSET
- IMAGE_ASSET
- MAP_ASSET

Do not add dozens of types until the vertical slice demonstrates the need.

## 4. Evidence model

Every historically meaningful statement becomes an evidence assertion.

Evidence
- id
- assertion_text
- subject_entity_id
- predicate
- object_entity_id or value
- source_id
- source_locator
- source_date
- valid_from
- valid_to
- confidence
- evidence_class
- verification_status
- reviewer
- verified_at
- notes

Suggested evidence class:

A — directly documented
B — archaeologically supported
C — scholarly interpretation
D — AI-assisted / provisional
E — speculative / uncertain

These labels remain project-level semantics. They must be documented and reviewed by domain experts before public interpretation.

## 5. Source model

Source
- id
- organization
- title
- URL
- source_type
- publication_date
- accessed_at
- license
- rights_status
- permitted_use
- attribution_required
- redistribution_allowed
- derivative_allowed
- commercial_use
- owner
- source_version
- checksum
- notes

Important distinction:

**historical authority != reuse permission**

For example, a government or institutional page can establish a fact while the underlying image/data remains restricted.

## 6. Asset model

Asset
- id
- entity_id
- asset_type
- format
- locator
- source_id
- license
- rights_status
- capture_method
- capture_date
- processing_history
- checksum
- lod
- scale
- coordinate_reference
- review_status

Asset types:
- PHOTO
- MANUSCRIPT_IMAGE
- INSCRIPTION_IMAGE
- RASTER
- VECTOR
- DEM
- ORTHOPHOTO
- POINT_CLOUD
- MESH
- GLB
- TEXTURE
- AUDIO
- MAP
- VIDEO

## 7. Historical state model

Do not put history into a single year column.

HistoricalState
- id
- entity_id
- label
- valid_from
- valid_to
- state_kind
- reconstruction_method
- asset_refs
- evidence_refs
- uncertainty
- reviewer_status
- notes

state_kind examples:
- DOCUMENTED
- RECONSTRUCTED
- INTERPRETED
- PROVISIONAL
- GAP

A state is a defensible set of claims, not a guessed snapshot.

## 8. Temporal dimensions

Keep at least four time dimensions separate:

1. valid time — when the fact/state is asserted to be true
2. observation time — when something was observed/captured
3. document time — when the source/document was produced
4. ingestion time — when Neer-Nilam imported/processed it

These are not interchangeable.

## 9. Spatial model

All spatial entities should have:
- geometry
- CRS/SRID
- provenance
- spatial accuracy where known
- source spatial reference
- transformation history

The system should distinguish:
- authoritative boundary
- surveyed geometry
- remote-sensing-derived geometry
- volunteered/mapped geometry
- project-generated geometry
- historical reconstruction

## 10. First data-source families

### P0 — Heritage authority

Use first:
- UNESCO Great Living Chola Temples
- Archaeological Survey of India
- Tamil Nadu Archaeology
- Tamil Nadu HR&CE

Role:
- authority identity
- significance
- administration
- monument facts
- primary/official references

UNESCO currently identifies Brihadisvara Temple at Thanjavur as part of the Great Living Chola Temples and describes its documented construction/consecration chronology. Treat the UNESCO page as authority/reference, not as a blanket asset-reuse license.

### P0 — Epigraphy

Use:
- Tamil Nadu Archaeology epigraphy resources
- ASI South Indian Inscriptions
- DHARMA epigraphic corpora

DHARMA's Tamil Nadu corpus publishes edited XML under CC BY 4.0 according to its repository README, making it a high-value structured research source subject to its requested attribution.

Do not treat every image in an epigraphic repository as automatically reusable merely because the transcription/XML is reusable.

### P0 — Modern spatial base

Use:
- OpenStreetMap / Overpass
- Survey of India
- Copernicus DEM
- permissioned TNGIS/Bhuvan services

Survey of India states that Indian entities are generally free to collect, generate, process and publish geospatial data subject to the applicable negative-list rules and related guidelines.

Copernicus DEM GLO-30/GLO-90 is available worldwide under its stated open/free licensing conditions with required source notices.

### P0 — Water

Use:
- Tamil Nadu WRD/TNGIS
- NWIC / India-WRIS
- Bhuvan/NRSC water services
- NRSC/ISRO basin atlases
- Tamil Nadu Agriculture reservoir records

The current TN WRD portal reports 14,306 tanks in its technical profile, including system and non-system categories. Use this as a live-source figure only after rechecking at ingestion time.

The National Water Data Portal currently exposes water-resource project datasets including command-area KML, GeoJSON and SHP resources produced by CWC.

### P1 — Historic population / settlement context

Use:
- Census District Census Handbooks
- village/town directories
- primary census abstracts

The 2011 Thanjavur District Census Handbook provides village/town directory information including infrastructure, drinking water, communications, transport and other local facilities.

The 2011 Primary Census Abstract is available down to district/sub-district/village/town/ward levels for Thanjavur.

### P1 — Manuscripts / Tamil texts

Use:
- CICT Digital Library of Tamil Palm-Leaf Manuscripts
- National Mission for Manuscripts / Kriti Sampada
- Roja Muthiah Research Library
- IFP / EAP collections
- Saraswathi Mahal Library / Tamil University as institutional leads

The CICT digital library currently describes 865 manuscript bundles, approximately 100,000 leaves and 41 classical Tamil texts, with IIIF-based access and per-item rights metadata.

NMM's Kriti Sampada is a national manuscript metadata/catalogue system intended to document manuscripts across repositories.

Manuscript ownership and image reuse rights must be handled separately from metadata access.

### P1 — Historic maps

Use:
- British Library / India Office Records
- Survey/archive maps
- historical cadastral/settlement sources where rights permit

Historic maps are evidence sources for historical landscape reconstruction, not automatically modern GIS base layers.

### P1 — 3D and imagery

Preferred order:
1. project-owned capture
2. explicitly commissioned/permissioned model
3. open-license 3D with verified terms
4. reference-only imagery for modeling guidance

Open Heritage 3D provides downloadable heritage datasets with dataset-specific Creative Commons licensing; the project FAQ says license type is supplied by the content owner. Average downloads can be very large, so storage/processing must be planned.

## 11. First Brihadisvara data pack

The first vertical slice does **not** require all Tamil Nadu.

Minimum target:

### A. Authority
- site identity
- monument identity
- coordinates/geometry
- official significance references
- management references

### B. Historical state evidence
Three supported historical states are required eventually, but their dates must be selected from research rather than copied from an AI recommendation.

For each state:
- state label
- valid interval
- evidence assertions
- sources
- confidence
- review status
- 3D/2D representation
- known gaps

### C. Unsupported state
One intentionally unsupported period record.

It must contain:
- requested period
- reason for insufficiency
- nearby documented references
- no substituted geometry

### D. Water context
At minimum:
- Cauvery relationship/context
- one or more relevant water entities
- modern water-reference geometry
- historical water evidence where actually documented

### E. Landscape
At minimum:
- terrain
- temple/site footprint
- selected roads/paths
- settlement footprint
- water features

### F. Evidence
At least three evidence records per supported state for the prototype.

### G. 3D
At minimum:
- one reviewed temple model
- one terrain/relief representation
- one fallback flat renderer

## 12. Rights classes for the data pool

Use:

R0 — project-owned
- project-created geometry
- project-created metadata
- project-created derived scene descriptions

R1 — reusable with explicit open license
- e.g. verified CC BY / compatible terms

R2 — permissioned
- usable under written permission/MoU/vendor agreement

R3 — reference only
- can inform research but should not be redistributed

R4 — restricted / prohibited
- do not ingest into production without explicit authorization

The source registry must preserve the original rights state even after deriving a transformed artifact.

## 13. Data-quality rules

No production record should be accepted without:
- stable source reference
- provenance
- spatial provenance where applicable
- temporal semantics
- rights status
- confidence
- verification state

Reject:
- uncited historical claims
- copied AI summaries presented as facts
- guessed dates
- unknown-license 3D assets
- duplicate entities without merge provenance
- geometry with unknown CRS
- silent nearest-state substitution

## 14. Derived-data pipeline

SOURCE → CAPTURE/REFERENCE → RIGHTS CHECK → RAW/RESTRICTED → NORMALIZE → QA → ENTITY/EVIDENCE LINK → EXPERT REVIEW → DERIVED ASSET → SCENE PACK

AI can assist inside the pipeline.

AI must not silently bypass:
- source provenance
- evidence linkage
- human verification
- rights classification

## 15. First software directory proposal

data/
  sources/
  raw/
  restricted/
  normalized/
  entities/
  evidence/
  historical-states/
  assets/
  terrain/
  water/
  maps/
  manuscripts/
  epigraphy/
  scene-packs/
  derived/
  manifests/

Every major directory gets a README explaining:
- allowed contents
- provenance requirements
- rights policy
- naming convention
- checksum expectations

Do not put large original source dumps into the Git repository by default. Use external object storage/artifact storage with manifests and hashes.

## 16. First engineering artifacts

Create before bulk collection:

- Source Registry v0
- Entity dictionary v0
- Evidence schema v0
- Historical State schema v0
- Asset manifest v0
- Scene Pack schema v0
- Brihadisvara vertical-slice dataset plan
- rights matrix
- provenance/transform log

## 17. Current data decision

The first useful "dataset" is a **small, high-quality Brihadisvara evidence graph**, not a giant statewide dump.

The first target is roughly:

1 site → 10–30 entities → 3 supported states + 1 gap → 9+ evidence assertions → 1 terrain model → 1 temple model → 1 water context → 1 scene pack

This is deliberately small enough to audit manually.

## 18. Next data gate

Do not start mass downloading.

First build the Brihadisvara source registry and source-to-claim matrix.

Then collect only the minimum data required to turn one claim into one verified scene element.
