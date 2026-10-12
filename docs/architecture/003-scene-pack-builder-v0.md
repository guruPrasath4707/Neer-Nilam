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

## Schema contract validation

The existing Draft 2020-12 schemas are checked by automated tests in `tests/test_schema_contracts.py`. Install `requirements-dev.txt` before running the full suite; GitHub Actions uses the same dependency file and runs the same tests. Coverage includes the canonical site entity, source-linked evidence record, GAP state, committed fixture pack, and a freshly generated pack. This is separate from the runtime invariants in the builder and protects against silently drifting fixture shapes.

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


## Historical-state resolution gate

`scripts/scene_packs/state_resolver.py` and its report CLI `scripts/scene_packs/resolve_historical_state.py` implement a conservative first resolver. The CLI requires both requested interval endpoints and writes a decision report, not a supported renderer pack.

A state is eligible only when all of these checks pass:
- the canonical entity is marked `VERIFIED`;
- the candidate is `DOCUMENTED`, `RECONSTRUCTED`, or `INTERPRETED`, with `verification_status=VERIFIED`;
- its bounded valid interval fully covers the requested interval;
- it links evidence records for the same entity, each marked `VERIFIED`, with a reviewer, verification date, source locator, and an interval covering the request;
- each evidence source is `REVIEWED` or `RIGHTS_CLEARED`, and explicitly permits redistribution and commercial use;
- at least one referenced scene asset exists, has a valid SHA-256, reviewer/date, a named licence basis, attribution, `verification_status=VERIFIED`, `rights_status=CLEARED`, and an eligible source record.

No eligible state returns the explicit GAP with a reason code; multiple eligible states return GAP with `AMBIGUOUS_ELIGIBLE_STATES`. Candidate order is never used to choose between competing states. `PROVISIONAL` is not render-eligible. This is deliberately conservative and the rights flags must only be set after item-specific review; it is not a legal conclusion.

The asset metadata contract is `data/schemas/asset-v0.schema.json`; registration and clearance expectations are documented in `data/assets/README.md`. The current repository has no production asset registered and the canonical entity is still unreviewed, so the CLI should report GAP. Synthetic test records exercise positive selection without being added as project evidence or production assets.

The selector currently produces a resolution report only. The existing scene-pack builder and flat viewer remain GAP-only; connecting a selected supported state to a renderable scene pack is a separate gate and is not implied by a `SELECTED` report.


## Source-rights and temporal contract hardening — 2026-10-12

The resolver treats the source registry identity and rights label as separate gates: the dictionary key must match the source record's own `source_id`, the source must be `REVIEWED` or `RIGHTS_CLEARED`, redistribution and commercial use must both be explicitly affirmative, and `rights_status` must be populated without review/hold/discrepancy/unknown/pending/restricted or non-commercial markers. A self-contradictory row such as `status=RIGHTS_CLEARED` with `rights_status=LICENSE_DISCREPANCY_REVIEW` remains ineligible. This is a conservative interpretation of recorded fields, not an external legal determination.

Regression tests cover sources still in review despite optimistic permission flags, contradictory rights labels, source-ID mismatch, evidence that overlaps but does not span the full requested interval, malformed evidence dates, a reversed state interval, and an adjacent historical era that must remain GAP. Synthetic fixtures remain test-only.
