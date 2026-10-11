# Architecture 003 — Deterministic Scene-Pack Builder v0

**Status:** Initial executable slice; GAP-only by design  
**Purpose:** Turn the existing Brihadisvara entity and explicit historical GAP fixture into a reproducible, renderer-neutral scene-pack JSON document.

## Why GAP-only first

The repository does not yet contain three source-reviewed historical state records, a reviewed asset manifest, or a supported-state selection policy. The builder therefore emits only \`state_kind=GAP\` with \`NO_SUPPORTED_RECONSTRUCTION\`. This means **the current project data does not support rendering a reviewed historical reconstruction for the requested interval**; it is not a claim that historical evidence does not exist.

It must never substitute the nearest known date, use an unreviewed 3D model, or produce a visually persuasive scene when the evidence layer resolved to a gap.

## Run

From the repository root with Python 3.10+ (standard library only):

\`\`\`powershell
python -m unittest discover -s tests -v
python scripts/scene_packs/build_scene_pack.py --from 1000-01-01 --to 1010-12-31 --output data/scene-packs/BRH-001-GAP-FIXTURE.json
\`\`\`

To generate an unbounded “no interval selected” gap fixture, omit both \`--from\` and \`--to\`. The \`--output\` argument is required to prevent accidental overwrites.

## Contract enforced by v0

- Entity and state IDs must agree.
- A complete requested interval uses canonical \`YYYY-MM-DD\` dates with start on or before end; both ends are required together.
- Only an explicit GAP state is currently accepted.
- GAP state must use \`NO_SUPPORTED_RECONSTRUCTION\`.
- GAP state cannot reference scene assets, and render hints disable asset fallback and historical geometry.
- The output carries the entity ID, resolved gap-state ID, uncertainty message, and data-gap reference.
- \`generated_at\` is null rather than wall-clock time. The same inputs yield the same serialized scene pack.
- No third-party imagery, meshes, raw data, or new historical assertions are embedded.

## Deliberate limitations

- No React/Three.js renderer yet.
- No date-to-supported-state resolver yet.
- No EpiDoc normalization or claim-evidence import yet.
- No geometry, terrain, or water layers yet.
- Runtime invariants are checked with the Python standard library; a dedicated JSON Schema validation dependency/CI gate remains a follow-up.

## Next gate

Build and validate source-linked evidence assertions using only rights-eligible records; then implement reviewed-state selection that refuses ambiguity and still falls back to GAP when no eligible, reviewed state covers the requested interval. Do not enable historical rendering until review state, time interval, assets, sources, and rights gates all pass.
