# Neer-Nilam data/

This directory is the working boundary for project-controlled dataset manifests, schemas and scene-ready data.

## Principles

- Large raw source dumps do not belong in Git by default.
- Every source/asset needs provenance and rights metadata.
- Historical claims require evidence links.
- Spatial data requires CRS/source metadata.
- Temporal data uses valid, observation, document and ingestion time separately.
- Derived data retains lineage to parent sources.

## Proposed layout

data/
  README.md
  manifests/
    source-registry-v0.csv
  schemas/
  entities/
  evidence/
  historical-states/
  assets/
  terrain/
  water/
  maps/
  epigraphy/
  manuscripts/
  scene-packs/
  derived/

## Current state

The repository contains the initial source registry seed only. No bulk source dataset is being copied into the repository yet.

The first target is the Brihadisvara vertical slice described in docs/research/data/002-brihadisvara-vertical-slice-plan.md.
