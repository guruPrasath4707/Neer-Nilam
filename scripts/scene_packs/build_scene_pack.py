#!/usr/bin/env python3
"""Build a deterministic Neer-Nilam scene pack, failing closed on unsupported history.

Python standard library only. Version 0 deliberately supports the explicit GAP state
until reviewed historical-state records and a resolver policy are available.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

SCENE_PACK_VERSION = "0.1.0"
GENERATOR_VERSION = "0.1.0"
DEFAULT_SCENE_ID = "BRH-001-GAP-FIXTURE"
GAP_CODE = "NO_SUPPORTED_RECONSTRUCTION"
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENTITY = ROOT / "data/entities/NN-SITE-BRIHADISVARA-THANJAVUR.json"
DEFAULT_STATE = ROOT / "data/historical-states/NN-GAP-BRIHADISVARA-001.json"


class ScenePackError(ValueError):
    """Raised when source records cannot safely produce a scene pack."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ScenePackError(f"Cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ScenePackError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ScenePackError(f"Expected a JSON object in {path}")
    return value


def _validate_iso_date(value: str | None, name: str) -> str | None:
    if value is None:
        return None
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ScenePackError(f"{name} must be an ISO date (YYYY-MM-DD), got {value!r}") from exc
    if parsed.isoformat() != value:
        raise ScenePackError(f"{name} must use canonical YYYY-MM-DD format, got {value!r}")
    return value


def build_gap_scene_pack(
    entity: dict[str, Any],
    state: dict[str, Any],
    requested_from: str | None = None,
    requested_to: str | None = None,
    scene_id: str = DEFAULT_SCENE_ID,
) -> dict[str, Any]:
    """Return a stable renderer-neutral GAP scene pack for the provided interval.

    This v0 intentionally refuses DOCUMENTED/RECONSTRUCTED/INTERPRETED/PROVISIONAL
    states. A separate reviewed-state selection policy is required before those can
    be resolved. It also refuses assets on a GAP state to prevent visual fallbacks.
    """
    start = _validate_iso_date(requested_from, "requested_from")
    end = _validate_iso_date(requested_to, "requested_to")
    if (start is None) != (end is None):
        raise ScenePackError("Provide both requested_from and requested_to, or neither")
    if start is not None and end is not None and start > end:
        raise ScenePackError("requested_from must be on or before requested_to")
    if not isinstance(scene_id, str) or not scene_id.strip():
        raise ScenePackError("scene_id must be a non-empty string")

    entity_id = entity.get("id")
    if not isinstance(entity_id, str) or not entity_id:
        raise ScenePackError("Entity record must have a non-empty id")
    if state.get("entity_id") != entity_id:
        raise ScenePackError(
            f"State entity_id {state.get('entity_id')!r} does not match entity id {entity_id!r}"
        )
    state_id = state.get("id")
    if not isinstance(state_id, str) or not state_id:
        raise ScenePackError("State record must have a non-empty id")
    if state.get("state_kind") != "GAP":
        raise ScenePackError(
            "Scene-pack v0 only resolves GAP states; reviewed historical-state selection is not implemented"
        )
    if state.get("verification_status") not in {"UNREVIEWED", "REVIEW_REQUIRED", "GAP"}:
        raise ScenePackError("Unexpected verification status on GAP state")

    asset_refs = state.get("asset_refs", [])
    evidence_refs = state.get("evidence_refs", [])
    if not isinstance(asset_refs, list) or not all(isinstance(x, str) for x in asset_refs):
        raise ScenePackError("state.asset_refs must be an array of strings")
    if asset_refs:
        raise ScenePackError("GAP states must not include visual assets or fallback assets")
    if not isinstance(evidence_refs, list) or not all(isinstance(x, str) for x in evidence_refs):
        raise ScenePackError("state.evidence_refs must be an array of strings")

    uncertainty = copy.deepcopy(state.get("uncertainty"))
    if not isinstance(uncertainty, dict):
        uncertainty = {}
    if uncertainty.get("code") != GAP_CODE:
        raise ScenePackError(f"GAP state uncertainty.code must be {GAP_CODE}")
    uncertainty.setdefault(
        "message",
        "No reviewed historical reconstruction is currently available for the requested interval.",
    )

    rights_status = entity.get("rights_status", "REVIEW_REQUIRED")
    rights_notices: list[str] = []
    if rights_status != "CLEARED":
        rights_notices.append(
            f"Entity source/rights status is {rights_status}; this pack embeds no source media or third-party visual assets."
        )

    scene_pack = {
        "scene_pack_version": SCENE_PACK_VERSION,
        "scene_id": scene_id.strip(),
        "requested_interval": {"from": start, "to": end},
        "resolved_state_id": state_id,
        "state_kind": "GAP",
        "entities": [entity_id],
        "layers": [],
        "events": [],
        "evidence_refs": list(evidence_refs),
        "asset_refs": [],
        "uncertainty": uncertainty,
        "attribution": [],
        "rights_notices": rights_notices,
        "data_gaps": [state_id],
        "renderer_hints": {
            "flat": True,
            "peppers_ghost": True,
            "relief_projection": True,
            "historical_geometry": False,
            "asset_fallback_allowed": False,
        },
        # Null, not wall-clock time, keeps identical inputs byte-for-byte reproducible.
        "generated_at": None,
        "generator_version": GENERATOR_VERSION,
    }
    validate_scene_pack(scene_pack)
    return scene_pack


def validate_scene_pack(pack: dict[str, Any]) -> None:
    """Validate runtime invariants that protect the v0 GAP contract."""
    required = {
        "scene_pack_version", "scene_id", "requested_interval",
        "resolved_state_id", "state_kind", "entities", "layers", "events",
        "evidence_refs", "asset_refs", "uncertainty", "attribution",
        "rights_notices", "data_gaps", "renderer_hints", "generated_at",
        "generator_version",
    }
    missing = required - set(pack)
    extra = set(pack) - required
    if missing or extra:
        raise ScenePackError(f"Scene-pack keys mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
    if pack["state_kind"] == "GAP":
        if not isinstance(pack["uncertainty"], dict) or pack["uncertainty"].get("code") != GAP_CODE:
            raise ScenePackError(f"GAP scene must carry uncertainty code {GAP_CODE}")
        if not pack["resolved_state_id"] or pack["resolved_state_id"] not in pack["data_gaps"]:
            raise ScenePackError("GAP scene must point to its explicit data-gap state")
        if pack["asset_refs"]:
            raise ScenePackError("GAP scene must not reference visual assets")
        if pack["renderer_hints"].get("asset_fallback_allowed") is not False:
            raise ScenePackError("GAP renderer must explicitly disable asset fallbacks")


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entity", type=Path, default=DEFAULT_ENTITY, help="Canonical entity JSON")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE, help="Historical-state JSON (v0: GAP only)")
    parser.add_argument("--from", dest="requested_from", help="Requested start date, YYYY-MM-DD")
    parser.add_argument("--to", dest="requested_to", help="Requested end date, YYYY-MM-DD")
    parser.add_argument("--scene-id", default=DEFAULT_SCENE_ID, help="Stable scene identifier")
    parser.add_argument("--output", type=Path, required=True, help="Output JSON path (explicit to avoid accidental overwrite)")
    args = parser.parse_args(argv)

    try:
        entity = _load_json(args.entity)
        state = _load_json(args.state)
        pack = build_gap_scene_pack(
            entity,
            state,
            requested_from=args.requested_from,
            requested_to=args.requested_to,
            scene_id=args.scene_id,
        )
        _atomic_write_json(args.output, pack)
    except (ScenePackError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote GAP scene pack: {args.output}")
    print(f"State: {pack['resolved_state_id']} ({GAP_CODE}); no historical model/assets substituted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
