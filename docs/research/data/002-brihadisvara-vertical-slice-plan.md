# Brihadisvara Vertical Slice 001 — Dataset Acquisition Plan

Date: 2026-10-08
Status: Proposed
Purpose: Define the smallest trustworthy data package that can drive both the flat-screen software proof and the future physical installation.

## 1. The vertical slice

The first Neer-Nilam dataset should represent one place deeply:

**Brihadisvara Temple, Thanjavur**

Do not begin with a statewide warehouse.

The vertical slice must be sufficient to demonstrate:

**time → scene → object → evidence → source → uncertainty**

## 2. Four scene states

The software proof needs four selectable states:

### State S1
A historically supported period/state selected after source review.

### State S2
A second historically supported period/state selected after source review.

### State S3
A third historically supported period/state selected after source review.

### State SGAP
An intentionally unsupported requested period.

SGAP must return:

NO_SUPPORTED_RECONSTRUCTION

It must not silently substitute S1/S2/S3.

The exact three historical dates are not yet approved. The dates suggested in prior AI research are hypotheses only.

## 3. Minimum entity set

Start with approximately 20 entities.

### Site
- Brihadisvara Temple site

### Monument/architecture
- main temple/sanctum
- vimana
- prakara/enclosure
- principal entrance/gopura
- selected mandapa
- selected shrine

### People/history
- Rajaraja I
- selected dynasty/entity representing the relevant political context
- one or two documented events

### Water/landscape
- Cauvery
- one relevant canal/water feature if evidence supports it
- one or more relevant tank entities only when source-supported
- temple-site landscape polygon
- Thanjavur settlement reference

### Spatial/context
- selected roads/paths
- modern administrative context
- terrain/DEM-derived surface

### Documents
- at least three inscription/text entities
- at least one manuscript/text entity only if it genuinely informs the chosen narrative

The list is intentionally provisional. Entity inclusion must follow evidence, not a desire to make the graph look large.

## 4. Evidence target

For each supported historical state:

Minimum:
- 3 evidence assertions
- at least 2 independent source families where practical
- explicit confidence
- explicit evidence class
- reviewer state

Total initial target:

**9+ evidence assertions**

The unsupported state should also have an evidence-gap record explaining why reconstruction is not currently supported.

## 5. Source acquisition order

### 1. Authority

Register:
- UNESCO Great Living Chola Temples
- ASI
- Tamil Nadu Archaeology
- Tamil Nadu HR&CE

### 2. Epigraphy

Register:
- ASI South Indian Inscriptions references
- Tamil Nadu Archaeology epigraphy records
- DHARMA Tamil Nadu corpus
- DHARMA South Indian Inscriptions corpus

### 3. Modern spatial

Register:
- Survey of India
- OpenStreetMap/Overpass
- Copernicus DEM
- TNGIS/Bhuvan with rights classification

### 4. Water

Register:
- TN WRD/TNGIS
- NWIC / India-WRIS
- NRSC/ISRO water resources products
- other state water records after rights verification

### 5. Historic settlement context

Register:
- Census District Census Handbook
- Primary Census Abstract
- historic map sources

### 6. 3D / imagery

Prefer:
1. project-owned capture
2. written permission / commissioned model
3. explicitly compatible open-license model
4. reference-only imagery

## 6. Source-to-claim workflow

For every important statement:

SOURCE
→ SOURCE LOCATOR
→ CLAIM / ASSERTION
→ ENTITY
→ VALID TIME
→ CONFIDENCE
→ REVIEW STATE

A web page alone should not become a production claim without recording the exact locator or document reference.

## 7. Asset workflow

For each reusable asset:

asset acquisition
→ rights check
→ checksum
→ metadata
→ entity mapping
→ processing record
→ derived version
→ scene usage

Every derived asset must retain parent-source references.

## 8. 3D minimum

The software proof does not require a perfect photogrammetric temple.

It requires:

- one reviewed temple mesh
- one terrain/relief representation
- one efficient scene-ready GLB
- one flat-screen fallback

The historical authenticity of the mesh must be documented separately from the visual polish of the model.

## 9. Water minimum

The first water representation should not attempt to simulate the entire Cauvery basin.

It should contain:

- a spatial representation of the Cauvery relationship/context
- one or more verified water features relevant to the chosen narrative
- provenance for each feature
- modern/historical distinction
- time semantics
- confidence

Hydrological modeling is a later research track unless a defensible model is needed for the initial story.

## 10. Manuscript and epigraphy minimum

The first physical demo does not require a full AI manuscript system.

The vertical slice needs only enough textual evidence to demonstrate the architecture:

- source document
- inscription/text record
- transcription or structured excerpt where rights permit
- source locator
- language/script metadata
- entity links
- temporal semantics
- confidence/review

AI-generated reconstruction should remain clearly marked provisional.

## 11. Rights-first rule

Before downloading a large dataset ask:

1. Do we need the original asset?
2. Is a reference link enough?
3. Can we derive the required geometry or metadata ourselves?
4. Is the license compatible with the intended use?
5. Does the source permit redistribution?
6. Is the source only a factual authority but not an asset source?
7. Can a permission/MoU resolve the restriction?

The smallest legal dataset is preferable to the largest dataset.

## 12. Initial storage strategy

Git repository:
- schemas
- manifests
- metadata
- small text fixtures
- reproducible processing scripts
- checksums
- scene-pack definitions

External storage:
- large PDFs
- original 3D meshes
- point clouds
- orthophotos
- large raster/imagery
- manuscript image collections
- full video

The repository should contain enough metadata to reconstruct provenance without storing every original byte.

## 13. First dataset folders

data/
  sources/
  normalized/
  entities/
  evidence/
  historical-states/
  assets/
  water/
  terrain/
  maps/
  epigraphy/
  manuscripts/
  scene-packs/
  manifests/

Use a separate restricted storage location for content that cannot be redistributed.

## 14. Acquisition exit criteria

The vertical slice is ready for software integration only when:

- all four scene states are represented
- supported states have source-linked evidence
- the gap state has an explicit reason
- all production assets have rights status
- all spatial data has CRS/source metadata
- temporal fields are populated
- confidence/review fields are populated
- scene pack can be generated deterministically
- no AI-only claim is presented as verified history

## 15. What we should NOT collect yet

Do not mass download:

- statewide historical maps
- all Tamil Nadu tanks
- all manuscript scans
- all epigraphic images
- all Open Heritage 3D datasets
- statewide high-resolution satellite imagery
- all census tables
- every possible 3D temple model

These can wait until the schema and first scene are proven.

## 16. Next concrete data task

Create:

1. Source Registry v0
2. Brihadisvara entity register v0
3. Claim/evidence matrix v0
4. Historical-state register v0
5. Asset manifest v0
6. Scene-pack v0

Then populate only the smallest set of records needed for S1/S2/S3/SGAP.
