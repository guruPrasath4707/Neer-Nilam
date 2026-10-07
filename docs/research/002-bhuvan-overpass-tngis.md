# Research Log 002 — Bhuvan + Overpass + TNGIS

Date: 2026-10-07
Status: Completed research pass

## Finding

The three websites show that Neer-Nilam needs a Source Registry and Data Rights layer in addition to the time engine, knowledge graph and holographic renderer.

## Bhuvan

Bhuvan's live catalog exposes water, soil, vegetation, land/environment and other geospatial products, including water-body and soil-moisture resources.

Use for Neer-Nilam:
- modern environmental context
- land/water visualization
- possible service/partnership integration

Constraint:
Bhuvan terms are permission-sensitive. Do not assume bulk ingestion or redistribution is allowed.

## Overpass / OSM

Overpass Turbo provides query-driven access to OpenStreetMap features and export/query tooling.

Potential pilot context:
- roads
- rivers
- canals
- waterways
- water bodies
- buildings
- places
- mapped heritage/tourism features

Constraint:
Track OSM attribution, element IDs, query/source timestamp and transformations.

## TNGIS

TNGIS provides a broad state GIS application ecosystem. The inspected map editor exposes administrative boundaries, transport, tourism, drainage, tanks, reservoirs, rivers and land-use layers, plus GIS operations and WMS/WFS/shapefile/Excel/KML inputs.

Constraint:
TNGIS terms require appropriate approval for public/commercial reuse; data ownership belongs to respective departments.

## Architectural consequence

Create:

External Sources
→ Source Registry / Rights
→ Connectors
→ Restricted Raw Plane
→ Normalize + QA
→ Canonical Neer-Nilam Core
→ Evidence / Knowledge Graph
→ Scene Composer
→ Web / Hologram / XR

## New principle

Evidence does not equal ownership.

A source may support a historical or geographic claim without giving Neer-Nilam permission to redistribute the underlying source asset.

## Hologram consequence

The physical display should not scrape/query external sources frame-by-frame.

It should receive a presentation-ready, source-aware scene produced by the Neer-Nilam core.

See website IDs W001–W006 in the website index.