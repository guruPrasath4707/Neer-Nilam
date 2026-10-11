# Architecture 003 — Deterministic Scene-Pack Builder v0

**Status:** Initial executable slice; GAP-only by design  
**Purpose:** Turn the Brihadisvara site entity, source-linked identity evidence and explicit historical GAP fixture into a reproducible, renderer-neutral scene-pack JSON document.

## Why GAP-only first

The repository does not yet contain three source-reviewed historical state records, a reviewed visual asset, or a supported-state selection policy. The builder therefore emits only `state_kind=GAP` with `NO_SUPPORTED_RECONSTRUCTION`. This means **the current project data does not support rendering a reviewed historical reconstruction for the requested interval**; it is not a claim that historical evidence does not exist.

A minimal identity assertion is recorded from the UNESCO World Heritage Centre page: Brihadisvara Temple at Thanjavur is a component of the Great Living Chola Temples property. The assertion is `SOURCE_LOCATED_REVIEW_PENDING`; the source record remains flagged for rights/terms review. It supplies context for an evidence panel only, not grounds for reconstructing architecture, terrain, water, or a particular historical period.

The builder must never substitute the nearest known date, use an unreviewed 3D model, or produce a visually persuasive scene when the temporal resolver returns a gap.

## Run

From the repository root with Python 3.10+ (standard library only):

```powershell
python -m unittest discover -s tests -v
python scripts/scene_packs/build_scene_pack.py --from 1000-01-01 --to 1010-12-31 --output data/scene-packs/BRH-001-GAP-FIXTURE.json
```

To generate an unbounded “no interval selected” gap fixture, omit both `--from` and `--to`. The `--output` argument is required to prevent accidental overwrites.

## Contract enforced by v0

- Entity and state IDs must agree.
- A complete requested interval uses canonical `YYYY-MM-DD` dates with start on or before end; both ends are required together.
- Only an explicit GAP state is currently accepted.
- GAP state must use `NO_SUPPORTED_RECONSTRUCTION` and cannot reference visual assets.
- Evidence references on the entity or state must resolve to evidence records, point to the scene entity, and reference a registered source with a locator.
- Sources that require attribution are represented in the scene pack; unresolved source rights remain visible as rights notices.
- Render hints disable asset fallback and historical geometry for a GAP.
- `generated_at` is null rather than wall-clock time. The same inputs yield the same serialized scene pack.
- No third-party imagery, meshes, raw data, or long source text is embedded.

## Deliberate limitations

- No React/Three.js renderer yet.
- No date-to-supported-state resolver yet.
- No EpiDoc normalization or claim-evidence import yet.
- No geometry, terrain, or water layers yet.
- Runtime invariants are checked with the Python standard library; a dedicated JSON Schema validation dependency/CI gate remains a follow-up.

## Next gate

Add additional source-linked assertions only after source and use-rights review; implement reviewed-state selection that refuses ambiguity and still falls back to GAP when no eligible, reviewed state covers the requested interval. Do not enable historical rendering until review state, temporal interval, assets, sources, and rights gates all pass.


## Flat-browser presentation client

The companion `scripts/scene_packs/render_flat_viewer.py` generates a standalone, accessible HTML evidence view from the scene pack, entity, evidence JSON and source registry. It renders a prominent GAP notice, the evidence locator and review state, and attribution/rights notices. All dynamic text is HTML escaped; source links accept only HTTP(S) URLs; output is atomically written and deterministic. There is no JavaScript bundle or external asset dependency.

Generate the view with:

```powershell
python scripts/scene_packs/build_scene_pack.py --output data/scene-packs/BRH-001-GAP-FIXTURE.json
python scripts/scene_packs/render_flat_viewer.py --scene-pack data/scene-packs/BRH-001-GAP-FIXTURE.json --output prototypes/flat-viewer/BRH-001-GAP-FIXTURE.html
```

The viewer is a flat fallback/provenance inspection proof, not the final interactive GIS/3D application. It fails closed if the scene is not GAP-only, a referenced evidence/source record is missing, or fallback/historical geometry is enabled.
