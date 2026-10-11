# Neer-Nilam data/

This directory is the working boundary for project-controlled dataset manifests, schemas and scene-ready data.

## Principles

- Large raw source dumps do not belong in Git by default.
- Every source/asset needs provenance and rights metadata.
- Historical claims require evidence links.
- Spatial data requires CRS/source metadata.
- Temporal data uses valid, observation, document and ingestion time separately.
- Derived data retains lineage to parent sources.
- A historical data gap is a valid result; do not substitute an unreviewed scene.

## Layout

```text
data/
  manifests/       source and acquisition registries
  schemas/         entity, evidence, historical-state, and scene-pack contracts
  entities/        canonical entity records
  evidence/        source-linked assertions
  historical-states/ reviewed states and explicit GAP records
  assets/          asset metadata and rights manifests
  terrain/ water/ maps/ epigraphy/ manuscripts/ derived/
  scene-packs/     deterministic renderer-neutral outputs
```

## Current executable slice

The Brihadisvara identity record now links one official-source identity assertion marked `SOURCE_LOCATED_REVIEW_PENDING`. That assertion is not a historical reconstruction claim. An explicit `NO_SUPPORTED_RECONSTRUCTION` state remains the only selectable state in v0.

The Python standard-library builder at `scripts/scene_packs/build_scene_pack.py` emits deterministic GAP scene-pack JSON, includes resolvable entity/state evidence references, and carries source attribution and outstanding rights notices. It refuses missing evidence/source records, mismatched entities, and fallback visual assets.

Run from the repository root:

```powershell
python -m unittest discover -s tests -v
python scripts/scene_packs/build_scene_pack.py --from 1000-01-01 --to 1010-12-31 --output data/scene-packs/BRH-001-GAP-FIXTURE.json
```

No bulk source dataset is copied into this repository. Large/raw source files remain on the external data lake; only appropriate schemas, metadata, small fixtures, audit artifacts, and reproducible code belong here.
