# Neer-Nilam web shell

This is the initial React + TypeScript application slice for Neer-Nilam. It reads the repository-owned Brihadisvara entity, historical-state, and scene-pack fixture.

The current fixture is an explicit GAP. The application must show the gap rather than substitute a historical model. This shell is not yet the GIS client, API, or 3D viewer.

## Requirements

- Node.js 24 (minimum: 22.12)
- npm

## Run locally

From this directory, run:

    npm install
    npm run dev

The first install generates package-lock.json. Commit that lockfile along with the validated dependency resolution before the shell is treated as reproducible or merged as a foundation for more features.

## Quality checks

    npm run typecheck
    npm test
    npm run build

The GitHub Actions workflow runs these checks for relevant pull requests and updates to main.

## Planned additions, not part of this shell yet

- MapLibre: 2D spatial view after a permitted, validated layer is ready.
- Three.js / React Three Fiber / Drei: reviewed 3D scene rendering after scene-pack contracts, evidence, assets, and rights checks are ready.
- Python validation/normalization tools: assigned workstream is tracked in repository Issue #3.
- FastAPI and PostgreSQL/PostGIS: deferred until API and shared-query requirements are demonstrated.
