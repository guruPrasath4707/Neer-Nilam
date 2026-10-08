# Project Log 004 — Physical Representation + Data Pool Architecture

Date: 2026-10-08
Status: Active workstream

## Repository review

The private Neer-Nilam repository was reviewed through its complete current Git tree.

Current repository role:
**planning, research, architecture and data-contract documentation; no application source yet.**

## Physical representation work

Deep research moved the project beyond a single-display mindset.

Current leading physical architecture hypothesis:

**physical relief + dynamic projection + optional Pepper's Ghost focal layer + separate evidence UI**

Pepper's Ghost and projection-mapped relief are now deliberately treated as comparable proof tracks.

The project will not purchase expensive display hardware before measured prototype gates pass.

## Data-pool work

The project now has:

- data workspace
- source registry v0
- Brihadisvara acquisition manifest v0
- entity schema v0
- evidence schema v0
- historical-state schema v0
- scene-pack schema v0
- Brihadisvara vertical-slice plan
- data-pool/evidence architecture contract
- seed Brihadisvara identity fixture
- explicit historical GAP-state fixture
- explicit scene-pack GAP fixture

## Current data strategy

The first useful dataset is a small, audited Brihadisvara evidence graph.

It is not a statewide download operation.

Priority is:

authority → epigraphy → spatial base → water → historical maps/settlement → manuscripts → 3D → derived scene pack.

## Important research sources added

The deeper research added government, academic, heritage, water, manuscript, DEM and structured epigraphy sources to the master website index.

The current index continues through W187.

## Immediate next build gate

The first actual software implementation should create a deterministic local scene-pack renderer that can consume:

- one canonical entity
- one GAP state
- placeholder supported states
- evidence references
- local assets
- renderer hints for flat/Pepper's Ghost/relief projection

Only after that should bulk source acquisition begin.
