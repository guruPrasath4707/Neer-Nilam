from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.scene_packs.build_scene_pack import (
    DEFAULT_SCENE_ID,
    GAP_CODE,
    ROOT,
    ScenePackError,
    build_gap_scene_pack,
)


ENTITY = {
    "id": "NN:site:brihadisvara-thanjavur",
    "canonical_name": "Brihadisvara Temple, Thanjavur",
    "rights_status": "REVIEW_REQUIRED",
}
STATE = {
    "id": "NN:state:brihadisvara:gap-001",
    "entity_id": ENTITY["id"],
    "state_kind": "GAP",
    "verification_status": "UNREVIEWED",
    "asset_refs": [],
    "evidence_refs": [],
    "uncertainty": {
        "code": GAP_CODE,
        "message": "No reviewed historical reconstruction is currently available for the requested interval in the current project dataset.",
    },
}


class ScenePackBuilderTests(unittest.TestCase):
    def test_default_pack_is_explicit_gap_without_fallback(self) -> None:
        pack = build_gap_scene_pack(ENTITY, STATE)
        self.assertEqual(pack["scene_id"], DEFAULT_SCENE_ID)
        self.assertEqual(pack["state_kind"], "GAP")
        self.assertEqual(pack["uncertainty"]["code"], GAP_CODE)
        self.assertEqual(pack["data_gaps"], [STATE["id"]])
        self.assertEqual(pack["asset_refs"], [])
        self.assertFalse(pack["renderer_hints"]["asset_fallback_allowed"])
        self.assertFalse(pack["renderer_hints"]["historical_geometry"])
        self.assertIsNone(pack["generated_at"])

    def test_requested_interval_is_preserved(self) -> None:
        pack = build_gap_scene_pack(ENTITY, STATE, "1000-01-01", "1010-12-31")
        self.assertEqual(pack["requested_interval"], {"from": "1000-01-01", "to": "1010-12-31"})
        self.assertEqual(pack["state_kind"], "GAP")

    def test_requires_both_interval_bounds(self) -> None:
        with self.assertRaisesRegex(ScenePackError, "both requested_from"):
            build_gap_scene_pack(ENTITY, STATE, "1000-01-01", None)

    def test_rejects_invalid_date(self) -> None:
        with self.assertRaisesRegex(ScenePackError, "ISO date"):
            build_gap_scene_pack(ENTITY, STATE, "1000-13-01", "1010-12-31")

    def test_rejects_reversed_interval(self) -> None:
        with self.assertRaisesRegex(ScenePackError, "on or before"):
            build_gap_scene_pack(ENTITY, STATE, "1010-01-01", "1000-01-01")

    def test_rejects_entity_mismatch(self) -> None:
        state = dict(STATE, entity_id="NN:site:other")
        with self.assertRaisesRegex(ScenePackError, "does not match"):
            build_gap_scene_pack(ENTITY, state)

    def test_fails_closed_for_non_gap_state(self) -> None:
        state = dict(STATE, state_kind="RECONSTRUCTED")
        with self.assertRaisesRegex(ScenePackError, "only resolves GAP"):
            build_gap_scene_pack(ENTITY, state)

    def test_rejects_assets_on_gap_state(self) -> None:
        state = dict(STATE, asset_refs=["NN:asset:unreviewed-temple-model"])
        with self.assertRaisesRegex(ScenePackError, "must not include visual assets"):
            build_gap_scene_pack(ENTITY, state)

    def test_requires_gap_code(self) -> None:
        state = dict(STATE, uncertainty={"code": "SOME_OTHER_CODE"})
        with self.assertRaisesRegex(ScenePackError, GAP_CODE):
            build_gap_scene_pack(ENTITY, state)

    def test_same_inputs_produce_identical_objects_and_bytes(self) -> None:
        first = build_gap_scene_pack(ENTITY, STATE, "1000-01-01", "1010-12-31")
        second = build_gap_scene_pack(ENTITY, STATE, "1000-01-01", "1010-12-31")
        first_bytes = json.dumps(first, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        second_bytes = json.dumps(second, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        self.assertEqual(first, second)
        self.assertEqual(first_bytes, second_bytes)

    def test_cli_writes_scene_pack_from_repository_fixtures(self) -> None:
        script = ROOT / "scripts/scene_packs/build_scene_pack.py"
        entity_path = ROOT / "data/entities/NN-SITE-BRIHADISVARA-THANJAVUR.json"
        state_path = ROOT / "data/historical-states/NN-GAP-BRIHADISVARA-001.json"
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "scene.json"
            result = subprocess.run(
                [sys.executable, str(script), "--entity", str(entity_path), "--state", str(state_path), "--output", str(output_path)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["state_kind"], "GAP")
            self.assertEqual(payload["uncertainty"]["code"], GAP_CODE)
            self.assertIn("asset_fallback_allowed", payload["renderer_hints"])


if __name__ == "__main__":
    unittest.main()
