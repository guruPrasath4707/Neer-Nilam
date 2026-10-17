# Neer-Nilam Platform Technology Roadmap

**Date:** 2026-10-17  
**Status:** Proposed architecture; implementation gates are explicit  
**Repository:** guruPrasath4707/Neer-Nilam  
**Pilot:** Thanjavur–Kumbakonam–Cauvery corridor, beginning with Brihadisvara Temple

## 1. Executive decision

Build Neer-Nilam as a **software-first, evidence-aware digital heritage platform**. Historical truth, source rights, uncertainty, and time semantics belong in the data and domain layers. Maps, 3D viewers, projection mapping, and any holographic installation are replaceable presentation clients; none of them may decide which history is true.

The first software slice is deliberately small: load the repository's existing Brihadisvara scene-pack fixture and clearly show its explicit GAP state. The app must not invent a Chola-era model, silently choose the nearest available period, or treat modern environmental layers as evidence for an ancient state.

## 2. Architecture and direction of data

External or project-created source  
→ source registry and rights review  
→ local raw/restricted data lake  
→ manifest, integrity, licence, and format validation  
→ normalization and quality checks  
→ canonical entities and spatial/temporal records  
→ source-linked evidence assertions  
→ reviewed historical states or explicit GAP records  
→ deterministic renderer-neutral scene pack  
→ accessible web client, 2D GIS client, later 3D / exhibition adapters

Important boundary: a presentation client requests a scene pack. It does not get unrestricted access to the raw data lake and does not infer or promote historical facts.

## 3. Recommended technology stack

| Area | Selected direction | When and why |
|---|---|---|
| Primary application languages | TypeScript and Python | TypeScript for the browser client and explicit contracts; Python for data QA, geospatial processing, reproducible analysis, and a service only when required |
| Browser UI | React 19 + TypeScript strict mode | Component-based accessible evidence and research interfaces |
| Frontend tooling | Vite 8.x; npm initially | Lightweight local development/build and straightforward Windows onboarding; commit the package lockfile before production development continues |
| UI styling | Semantic HTML, CSS variables and CSS modules | Maintain a restrained scientific/editorial UI; avoid making a UI framework or animation the product |
| Shared record contracts | JSON Schema Draft 2020-12 already present in data/schemas | Keep JSON Schema as the source contract for source, entity, evidence, state, and scene-pack records; run contract tests against fixtures |
| Python data QA | Python 3.12+; standard library for the first manifest validator; pytest and Ruff once a Python package is established | Small, deterministic, offline-first validation; add specialist libraries only when a task needs them |
| Vector geospatial processing | GeoPandas, Shapely, pyproj, pyogrio | Inspect, normalize, transform, and validate vector data with CRS and lineage preserved |
| Raster processing | Rasterio, with GDAL/PROJ tooling as required | Work on selected regional rasters with explicit CRS, NoData, resolution, units, extent, and product versions |
| Local analytical files | GeoParquet and Parquet; DuckDB for local analytical queries when useful | Efficient repeatable analysis without forcing a server/database into the first milestone |
| Human GIS inspection | QGIS | Analyst QA and visual inspection, not an application runtime dependency |
| 2D browser GIS | MapLibre GL JS | Add an interactive spatial map after a permitted source/style strategy and a small validated layer exist |
| 3D viewer | Three.js + React Three Fiber 9 + Drei | Later stage, consuming reviewed scene packs and licensed/hash-identified assets; no 3D layer should fabricate missing history |
| API | FastAPI + Pydantic, Python | Only after a defined client or repeatable workflow needs a stable API; validate input/output contracts |
| Persistent spatial database | PostgreSQL + PostGIS | Later gate after entity/evidence schema and query patterns stabilize or multi-user access needs a shared database; not required for the offline pilot |
| Local authoritative storage | Existing external Seagate data lake plus sanitized manifests in Git | Raw payloads remain outside this public repository by default; use versioned manifests, checksums, rights metadata, and derived-data lineage |
| Unit/component tests | pytest for Python; Vitest for TypeScript; React Testing Library for UI components | Validate domain decisions and failure behavior, not only rendered snapshots |
| Browser/end-to-end tests | Playwright | Exercise loading the GAP fixture, evidence/source navigation, map interactions, and accessibility checks as those features arrive |
| Quality gates | TypeScript compiler, Ruff, contract/schema tests, GitHub Actions | Lint/type/test/build on pull requests; do not record PASS unless the job actually ran and passed |
| Dependency/security hygiene | Committed npm lockfile, pinned compatible dependencies, Dependabot, secret scanning, least privilege | Limit supply-chain drift and prevent credentials or restricted data being committed |
| Automation/collection | Keep the existing PowerShell collection scripts | They already serve Windows data-lake workflows. PowerShell remains an appropriate tool, but it should not be the only substantive application code |

### Version rule

The web shell starts on the React 19.3, Vite 8.3, TypeScript 6 and Node 24 release lines, with compatible package ranges shown in its manifest. Verify package compatibility and commit npm's generated lockfile before treating the shell as reproducible. Add React Three Fiber/Drei and MapLibre only in the phase that implements their real functionality. Do not install the entire future stack now.

## 4. Language and GitHub repository statistics

GitHub uses Linguist to classify committed source files and calculate language percentages. Markdown, CSV, JSON data and other documentation/data files may not count as programming-language bytes, so a repository containing PowerShell collection scripts can show 100% PowerShell even when it has substantial documentation and schemas.

The correct fix is to add genuine maintained application code, not empty files, sample blobs, vendored code, generated code, or a .gitattributes rule that hides the actual collectors. This branch introduces a real TypeScript/React shell which reads existing project records. Once those source files reach the default branch, GitHub should recalculate the language bar in the background; the exact percentages are not under project control.

Target language roles:
- **TypeScript/TSX:** browser UI, scene-pack contract handling, maps, later 3D viewer.
- **Python:** data validation, transformations, analysis, and later service endpoints if needed.
- **PowerShell:** Windows collection, storage verification, and carefully guarded machine-local workflows.
- **SQL:** only when the PostgreSQL/PostGIS phase is approved.
- **JSON, CSV, Markdown:** data contracts, manifests, evidence records, and documentation.

Do not add languages just to make the pie chart look balanced. Language statistics should reflect useful source code.

## 5. Repository layout target

Keep a single project repository, with raw data still external:

- apps/web/ — React + TypeScript application.
- apps/api/ — future FastAPI service, created only when API scope is approved.
- packages/contracts/ — shared TypeScript helpers/types that correspond to data/schemas/; JSON Schema remains authoritative.
- tools/data-quality/ — offline manifest, checksum, provenance, and schema validators.
- data/manifests/ — sanitized acquisition and source manifests.
- data/schemas/ — versioned JSON Schemas.
- data/entities/, data/historical-states/, data/scene-packs/ — small source-controlled project records/fixtures only, each with review status and traceability.
- scripts/collection/ — existing Windows PowerShell acquisition and verification tooling.
- docs/architecture/, docs/research/, docs/project-log/ — decisions, runbooks, and append-only milestone records.
- tests/ — cross-layer fixture and integration coverage where it fits better than colocated tests.

Do not commit the external-drive data lake, raw manuscript images, unlicensed 3D assets, API keys, cookies, tokens, or unreviewed data dumps into the public repository.

## 6. Phased roadmap and completion gates

### Phase 0 — architecture baseline and gap-safe web shell
- Record this roadmap and link it from the repository README.
- Start a minimal TypeScript React app that reads the current Brihadisvara GAP fixture and displays the uncertainty explicitly.
- Add schema/state contract tests and a web CI workflow.
- Generate and commit the npm lockfile during the first local dependency-install session; validate typecheck, tests, and production build before accepting the shell as green.
**Gate:** the app is a real buildable shell, the fixture tests pass, and a missing supported state remains a visible gap rather than an invented model.

### Phase 1 — source, rights, and evidence slice
- Ryan researches and records a focused set of source-backed Brihadisvara claims.
- Update source registry and website index with exact locators and rights status.
- Resolve or keep blocked any source with unclear redistribution terms, including the recorded DHARMA README/XML licence discrepancy.
**Gate:** a reviewer can trace every promoted claim to a specific source passage/record; unsupported claims stay unresolved.

### Phase 2 — repeatable data-quality pipeline
- Vidvat implements offline validation of manifests and checksum metadata, including 120 unique CHIRPS month entries for 2016-01 through 2025-12.
- Record source version, CRS, temporal and spatial coverage, resolution/units, NoData treatment, transformation lineage, attribution, and licence status for each selected layer.
- Build regional subsets and reports only after validating original sources and paths; keep raw files off GitHub.
**Gate:** reproducible tests distinguish valid, missing, mismatched, malformed, unreviewed, and permission-gated inputs without false PASS results.

### Phase 3 — canonical records and scene-pack builder
- Formalize schema versions and IDs for sources, evidence, entities, states, assets, and scene packs.
- Make generation deterministic from versioned metadata and approved assets.
- Add CI checks for schemas, fixture instances, stable output, rights fields, and broken references.
**Gate:** a known, reviewed source set produces the same scene-pack output on repeat runs; an unsupported interval produces an explicit GAP.

### Phase 4 — spatial client and data API
- Start with validated layers in MapLibre and clearly labeled date/source metadata.
- Add the FastAPI/Pydantic service only when the app needs multiple stable query endpoints or shared workflows.
- Add PostgreSQL/PostGIS only when the reviewed data model or spatial queries need persistent shared storage; document migrations, backup, and access controls.
**Gate:** source/rights and entity/evidence semantics are enforced at ingestion and service boundaries.

### Phase 5 — reviewed 3D heritage viewer
- Use React Three Fiber/Three.js with reviewed, attribution-complete and hash-identified assets.
- Keep site geometry, water/terrain, inscriptions, and historical states separated by what the evidence actually supports.
- A scene pack with GAP must render a gap explanation and references; no nearest-state substitution and no fake continuous historical morphing.
- Measure load time, asset size, memory use, keyboard accessibility, reduced-motion behavior, and low-end hardware performance.
**Gate:** scientific/domain review and rights review pass; performance is measured on target devices rather than assumed.

### Phase 6 — physical / immersive presentation proof
- Keep Pepper's Ghost, projection-mapped relief, AR/MR, VR, and any hybrid as alternative adapters to the same scene contract.
- Perform low-cost, measurable A/B prototypes with the same supported scene; document viewing angle, contrast, calibration, environmental constraints, user comprehension, and cost.
- Do not buy expensive hardware or claim a display architecture is chosen until evidence from trials and the advisor's path supports it.
**Gate:** the chosen presentation improves understanding and can preserve provenance, uncertainty, and gap states.

### Phase 7 — optional AI research tools
- Consider OCR/HTR, translation suggestions, entity matching, and reconstruction hypotheses only for a named dataset/problem with verified rights and a test benchmark.
- Treat outputs as proposals with model/version, input lineage, confidence basis, and human review.
- AI cannot independently promote a claim, historical state, or asset to verified.
**Gate:** baseline metrics, error analysis, bias/coverage limits, and human review flow are documented.

## 7. Non-goals for the initial milestone

- No statewide bulk data dump.
- No unapproved paid APIs/cloud subscriptions.
- No managed/cloud database before the local prototype justifies it.
- No full vector-tile infrastructure or custom map server before a validated layer and licensing strategy exist.
- No AI reconstruction presented as fact.
- No expensive holographic display purchase or physical architecture lock-in.
- No language-statistic manipulation.

## 8. Team responsibility boundaries

- **Project lead:** architecture/contract approval, integration, scope control, review and merge decisions, and physical display coordination.
- **Ryan Feodor (RyanFeodor):** historical source research, specific claim/evidence records, source index, uncertainty, attribution, and rights notes.
- **Vidvat (vidvatg):** offline data/manifest quality checks, checksum reconciliation, GIS normalization specifications, readiness report, tests, and reproducibility notes.
- Both contributors use separate branches and pull requests, report blockers in their GitHub issue, and do not alter/move the external data lake without approval.

## 9. Decision rules

1. Evidence and source rights precede rendering.
2. JSON Schema, fixture records, and data provenance remain versioned and testable.
3. Time fields have distinct meanings: historical validity, observation, source/document time, and ingestion time.
4. Modern geography and environmental observations are context, not direct proof of a historical state.
5. Gaps and conflicts are retained explicitly, never silently merged away.
6. Every asset requires source, hash, attribution, permission/rights, and review state before production use.
7. A new renderer must not change the meaning of a scene pack.
8. Dependency versions are compatibility-tested and lockfiles are committed.
9. Raw data remains external unless an item-specific redistribution decision permits repository inclusion.

## 10. Official technical references

- React + TypeScript: https://react.dev/learn/typescript
- Vite guide and supported versions: https://vite.dev/guide/ and https://vite.dev/releases
- React Three Fiber install/React compatibility: https://r3f.docs.pmnd.rs/getting-started/installation
- Three.js WebGL renderer: https://threejs.org/docs/pages/WebGLRenderer
- MapLibre GL JS: https://maplibre.org/maplibre-gl-js/docs/
- FastAPI: https://fastapi.tiangolo.com/
- GeoPandas: https://geopandas.org/en/latest/docs.html
- DuckDB spatial: https://duckdb.org/docs/current/core_extensions/spatial/overview
- PostGIS: https://postgis.net/docs/en/postgis_introduction.html
- Vitest: https://vitest.dev/guide/
- GitHub repository language detection: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-repository-languages
- GitHub Linguist behavior and overrides: https://github.com/github-linguist/linguist/blob/main/docs/how-linguist-works.md and https://github.com/github-linguist/linguist/blob/main/docs/overrides.md
