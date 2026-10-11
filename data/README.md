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

The Brihadisvara identity record links one official-source identity assertion marked `SOURCE_LOCATED_REVIEW_PENDING`. This is an identity/context claim, not historical reconstruction evidence. The current scene state remains the explicit `NO_SUPPORTED_RECONSTRUCTION` GAP.

Build the scene pack, then render it as a standalone flat evidence view (Python 3.10+, standard library only):

```powershell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/scene_packs/build_scene_pack.py --output data/scene-packs/BRH-001-GAP-FIXTURE.json
python scripts/scene_packs/render_flat_viewer.py --scene-pack data/scene-packs/BRH-001-GAP-FIXTURE.json --output prototypes/flat-viewer/BRH-001-GAP-FIXTURE.html
```

The flat viewer shows the resolved state, requested time interval, linked source locator, review status, attribution and outstanding rights notice. Test suite includes automated Draft 2020-12 JSON Schema checks for the core fixtures and generated pack. It has no external JavaScript dependency, embeds no source media, escapes dynamic HTML text, and refuses non-GAP states or fallback visuals.

No bulk source dataset is copied into this repository. Large/raw files remain on the external data lake; only appropriate schemas, metadata, small fixtures, audit artifacts, and reproducible code belong here.
