# Architecture 002 — Neer-Nilam Data Pool and Scene Contracts

Date: 2026-10-08
Status: Proposed

## 1. System boundary

The physical installation is a presentation client.

The scene producer owns the difficult semantics:

- source lineage
- rights
- entity identity
- time
- evidence
- uncertainty
- derived assets
- data gaps

The presentation client should not decide historical truth.

## 2. Canonical layers

SOURCE
→ RIGHTS
→ RAW/RESTRICTED
→ NORMALIZED
→ ENTITY GRAPH
→ EVIDENCE
→ HISTORICAL STATE
→ SCENE COMPOSER
→ PRESENTATION CLIENT

## 3. Source contract

A source record must answer:

- who published it
- what it is
- where it is
- when it was published/updated
- when Neer-Nilam accessed it
- what license/terms apply
- what uses are permitted
- what attribution is required
- what version/checksum identifies it

## 4. Entity contract

Every entity receives an immutable project ID.

Entity should support:

- name
- alternate names
- type
- geometry
- CRS
- source references
- evidence references
- asset references
- temporal intervals
- confidence
- verification state
- rights references

The same entity must survive renderer changes.

## 5. Evidence contract

Evidence is first-class data.

Minimum fields:

- evidence_id
- subject
- predicate
- object/value
- source_id
- source_locator
- valid interval
- source/document time
- confidence
- evidence class
- verification status
- reviewer
- notes

One source can support multiple assertions.

One assertion can have multiple sources.

Conflicting assertions must coexist rather than being silently merged.

## 6. Historical-state contract

A HistoricalState is a set of evidence-linked assertions and assets that form a defensible representation for a temporal interval.

It is not simply:

year = 1200

It should include:

- state_id
- entity_id
- valid interval
- state kind
- included/excluded entities
- asset references
- evidence references
- uncertainty
- reconstruction method
- review state

## 7. Gap-state contract

An unsupported period is a valid application state.

Required:

- requested interval
- gap code
- explanation
- source search coverage
- nearby documented periods
- no substituted scene

Example:

state_kind = GAP

gap_code = NO_SUPPORTED_RECONSTRUCTION

## 8. Scene-pack contract

A ScenePack should be a deterministic output of the canonical data layer.

Conceptual fields:

- scene_pack_version
- scene_id
- requested_interval
- resolved_state_id
- state_kind
- entities
- layers
- events
- evidence_refs
- asset_refs
- uncertainty
- attribution
- rights notices
- data_gaps
- renderer_hints
- generated_at
- generator_version

Renderer hints may include:
- flat mode
- Pepper's Ghost mode
- relief projection mode
- hybrid mode

The historical meaning must remain identical across modes.

## 9. Presentation neutrality test

The same ScenePack should be able to render:

- normal browser
- Pepper's Ghost prototype
- projection-mapped relief
- future light-field client

A display-specific implementation should not change the underlying evidence.

## 10. Versioning

Track separate versions for:

- source
- normalized data
- evidence graph
- historical state
- asset
- scene pack
- renderer/client
- physical calibration

A new renderer must not silently rewrite historical data.

## 11. Validation pipeline

SOURCE CHECK
→ RIGHTS CHECK
→ STRUCTURE/SCHEMA VALIDATION
→ CRS VALIDATION
→ TEMPORAL VALIDATION
→ ENTITY LINK VALIDATION
→ EVIDENCE LINK VALIDATION
→ ASSET CHECKSUM
→ EXPERT REVIEW
→ SCENE GENERATION

## 12. Reproducibility

Every derived scene should be reproducible from:

- source references
- source versions/checksums
- transformation code version
- configuration
- schema version
- reviewer decisions

## 13. AI boundary

AI services may produce:

- OCR suggestions
- HTR suggestions
- entity candidates
- translation suggestions
- reconstruction hypotheses
- similarity matches

AI cannot directly promote a hypothesis to verified historical state.

Promotion requires the evidence and review workflow.

## 14. API direction

Future service endpoints should conceptually separate:

GET /entities/{id}
GET /evidence/{id}
GET /states/{id}
GET /sources/{id}
GET /scene-packs/{id}

A presentation client asks for a scene, not for unrestricted raw source access.

## 15. First implementation priority

Before building the full backend:

1. define the schemas
2. create fixture records
3. generate one deterministic ScenePack
4. render it in a plain browser
5. render the same pack in the Pepper's Ghost proof
6. render the same pack in a relief/projection proof

This verifies the most important architecture claim early.
