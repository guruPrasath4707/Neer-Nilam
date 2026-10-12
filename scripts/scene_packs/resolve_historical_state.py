#!/usr/bin/env python3
"""Resolve a requested historical interval to a fully gated state or the explicit GAP.

This command creates a reviewable resolution report, not a renderer-ready historical
scene. Scene rendering remains GAP-only until the supported-state scene-pack and
client contracts are implemented and validated.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.scene_packs.build_scene_pack import ScenePackError, _load_json, load_evidence_records, load_source_registry
from scripts.scene_packs.state_resolver import resolve_historical_state

DEFAULT_ENTITY = ROOT / "data/entities/NN-SITE-BRIHADISVARA-THANJAVUR.json"
DEFAULT_STATE_DIR = ROOT / "data/historical-states"
DEFAULT_GAP_STATE = ROOT / "data/historical-states/NN-GAP-BRIHADISVARA-001.json"
DEFAULT_EVIDENCE_DIR = ROOT / "data/evidence"
DEFAULT_ASSET_DIR = ROOT / "data/assets"
DEFAULT_SOURCE_REGISTRY = ROOT / "data/manifests/source-registry-v0.csv"


def load_record_directory(directory: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    if not directory.exists():
        return records
    for path in sorted(directory.glob("*.json")):
        record = _load_json(path)
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            raise ScenePackError(f"Record in {path} has no non-empty id")
        if record_id in records:
            raise ScenePackError(f"Duplicate record id {record_id} under {directory}")
        records[record_id] = record
    return records


def _atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(document)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entity", type=Path, default=DEFAULT_ENTITY)
    parser.add_argument("--states-dir", type=Path, default=DEFAULT_STATE_DIR)
    parser.add_argument("--gap-state", type=Path, default=DEFAULT_GAP_STATE)
    parser.add_argument("--evidence-dir", type=Path, default=DEFAULT_EVIDENCE_DIR)
    parser.add_argument("--assets-dir", type=Path, default=DEFAULT_ASSET_DIR)
    parser.add_argument("--source-registry", type=Path, default=DEFAULT_SOURCE_REGISTRY)
    parser.add_argument("--from", dest="requested_from", required=True, help="Requested start date YYYY-MM-DD")
    parser.add_argument("--to", dest="requested_to", required=True, help="Requested end date YYYY-MM-DD")
    parser.add_argument("--output", type=Path, required=True, help="Resolution report JSON (not a scene pack)")
    args = parser.parse_args(argv)

    try:
        entity = _load_json(args.entity)
        gap_state = _load_json(args.gap_state)
        all_states = load_record_directory(args.states_dir)
        evidence = load_evidence_records(args.evidence_dir)
        assets = load_record_directory(args.assets_dir)
        sources = load_source_registry(args.source_registry)
        candidates = [
            state for state in all_states.values()
            if state.get("id") != gap_state.get("id") and state.get("state_kind") != "GAP"
        ]
        resolution = resolve_historical_state(
            args.requested_from,
            args.requested_to,
            entity,
            candidates,
            gap_state,
            evidence,
            sources,
            assets,
        )
        report = {
            "resolver_version": "0.1.0",
            "requested_interval": {"from": args.requested_from, "to": args.requested_to},
            "entity_id": entity.get("id"),
            "resolution_status": resolution["resolution_status"],
            "reason_code": resolution["reason_code"],
            "resolved_state_id": resolution["state"].get("id"),
            "resolved_state_kind": resolution["state"].get("state_kind"),
            "rejected_candidates": resolution.get("rejected_candidates", {}),
            "state": resolution["state"],
            "note": "This is a selection report. It is not a renderer-ready supported scene pack.",
        }
        _atomic_write(args.output, report)
    except (ScenePackError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Resolution: {report['resolution_status']} ({report['reason_code']})")
    print(f"Resolved state: {report['resolved_state_id']} [{report['resolved_state_kind']}]")
    print(f"Wrote resolution report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
