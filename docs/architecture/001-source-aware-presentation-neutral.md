# Architecture Refinement 001 — Source-Aware + Presentation-Neutral

Date: 2026-10-07
Status: Proposed

## Core idea

Neer-Nilam should not be architected around one hologram technology.

The shared core produces scenes for multiple clients:
- Web GIS
- hologram/optical installation
- projection mapping
- AR/MR
- VR
- museum displays

## Revised flow

External Sources
→ Source Registry + Rights
→ Connectors
→ Raw/Restricted Plane
→ Normalization + QA
→ Canonical Spatiotemporal Core
→ Evidence Engine + Knowledge Graph
→ Scene Composer
→ Presentation Clients

## Temporal model

Distinguish:
- valid time
- observation time
- document/source time
- ingestion time

Do not use one generic historical timestamp for all meanings.

## Missing historical evidence

If a requested date is unsupported, do not silently substitute the nearest state.

Return:
NO_SUPPORTED_STATE

Optionally show nearest documented states as references, clearly labeled.

## Transition semantics

Separate:
1. Evidence transition — a supported historical state/event changes the scene.
2. Presentation transition — cross-fade/dissolve used only for UX.
3. Analytical interpolation — allowed only when a dataset scientifically supports it.

## First software proof

Prefer React + Three.js / React Three Fiber in kiosk mode before introducing a second dedicated renderer.

Unity remains a candidate for a later dedicated installation if hardware/SDK/scene complexity justifies it.

## Scene Composer

The renderer should receive a scene object containing:
- selected time
- temporal semantics
- entities
- layers
- events
- evidence references
- uncertainty
- data gaps
- assets
- attribution

This keeps the display technology replaceable.