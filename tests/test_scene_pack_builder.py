from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.scene_packs.render_flat_viewer import ViewerRenderError, render_flat_html

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
EVIDENCE_ID = "NN:evidence:brh:component-001"
EVIDENCE = {
    "id": EVIDENCE_ID,
    "subject_entity_id": ENTITY["id"],
    "predicate": "is-component-of",
    "source_id": "SRC-UNESCO-TNT",
    "source_locator": "UNESCO World Heritage Centre, Great Living Chola Temples, Outstanding Universal Value / Brief synthesis.",
    "verification_status": "SOURCE_LOCATED_REVIEW_PENDING",
}
SOURCE = {
    "SRC-UNESCO-TNT": {
        "source_id": "SRC-UNESCO-TNT",
        "organization": "UNESCO World Heritage Centre",
        "title": "Great Living Chola Temples",
        "url": "https://whc.unesco.org/en/list/250",
        "rights_status": "REVIEW_REQUIRED",
        "attribution_required": "Yes",
    }
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

    def test_entity_evidence_is_included_and_attributed_but_not_auto_approved(self) -> None:
        entity = dict(ENTITY, evidence_refs=[EVIDENCE_ID])
        pack = build_gap_scene_pack(entity, STATE, evidence_records={EVIDENCE_ID: EVIDENCE}, sources=SOURCE)
        self.assertEqual(pack["evidence_refs"], [EVIDENCE_ID])
        self.assertTrue(any("UNESCO World Heritage Centre" in item for item in pack["attribution"]))
        self.assertTrue(any("rights status is REVIEW_REQUIRED" in item for item in pack["rights_notices"]))
        self.assertFalse(pack["renderer_hints"]["historical_geometry"])

    def test_rejects_missing_referenced_evidence(self) -> None:
        entity = dict(ENTITY, evidence_refs=[EVIDENCE_ID])
        with self.assertRaisesRegex(ScenePackError, "Referenced evidence record not found"):
            build_gap_scene_pack(entity, STATE)

    def test_rejects_unknown_evidence_source(self) -> None:
        entity = dict(ENTITY, evidence_refs=[EVIDENCE_ID])
        evidence = dict(EVIDENCE, source_id="SRC-NOT-REGISTERED")
        with self.assertRaisesRegex(ScenePackError, "unknown source"):
            build_gap_scene_pack(entity, STATE, evidence_records={EVIDENCE_ID: evidence}, sources=SOURCE)

    def test_rejects_evidence_about_another_entity(self) -> None:
        entity = dict(ENTITY, evidence_refs=[EVIDENCE_ID])
        evidence = dict(EVIDENCE, subject_entity_id="NN:site:other")
        with self.assertRaisesRegex(ScenePackError, "not about scene entity"):
            build_gap_scene_pack(entity, STATE, evidence_records={EVIDENCE_ID: evidence}, sources=SOURCE)

    def test_same_inputs_produce_identical_objects_and_bytes(self) -> None:
        entity = dict(ENTITY, evidence_refs=[EVIDENCE_ID])
        first = build_gap_scene_pack(entity, STATE, "1000-01-01", "1010-12-31", evidence_records={EVIDENCE_ID: EVIDENCE}, sources=SOURCE)
        second = build_gap_scene_pack(entity, STATE, "1000-01-01", "1010-12-31", evidence_records={EVIDENCE_ID: EVIDENCE}, sources=SOURCE)
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
            self.assertEqual(payload["evidence_refs"], [EVIDENCE_ID])
            self.assertTrue(any("UNESCO World Heritage Centre" in item for item in payload["attribution"]))
            self.assertIn("asset_fallback_allowed", payload["renderer_hints"])


    def test_flat_viewer_renders_gap_and_source_review_notice(self) -> None:
        entity = dict(ENTITY, evidence_refs=[EVIDENCE_ID])
        pack = build_gap_scene_pack(entity, STATE, evidence_records={EVIDENCE_ID: EVIDENCE}, sources=SOURCE)
        document = render_flat_html(pack, entity, {EVIDENCE_ID: EVIDENCE}, SOURCE)
        self.assertIn('role="status"', document)
        self.assertIn("Historical reconstruction unavailable", document)
        self.assertIn("NO_SUPPORTED_RECONSTRUCTION", document)
        self.assertIn("SOURCE_LOCATED_REVIEW_PENDING", document)
        self.assertIn("UNESCO World Heritage Centre", document)
        self.assertIn("REVIEW_REQUIRED", document)
        self.assertIn("asset fallback is prohibited", document)
        self.assertNotIn("<script", document.lower())

    def test_flat_viewer_escapes_dynamic_markup(self) -> None:
        entity = dict(ENTITY, canonical_name='<img src=x onerror="alert(1)">')
        pack = build_gap_scene_pack(entity, STATE)
        document = render_flat_html(pack, entity, {}, SOURCE)
        self.assertIn("&lt;img src=x onerror=&quot;alert(1)&quot;&gt;", document)
        self.assertNotIn("<img src=x", document)

    def test_flat_viewer_rejects_unknown_evidence(self) -> None:
        pack = build_gap_scene_pack(ENTITY, STATE)
        pack["evidence_refs"] = ["NN:evidence:missing"]
        with self.assertRaisesRegex(ViewerRenderError, "Referenced evidence record not found"):
            render_flat_html(pack, ENTITY, {}, SOURCE)

    def test_flat_viewer_rejects_unsupported_scene_state(self) -> None:
        pack = build_gap_scene_pack(ENTITY, STATE)
        pack["state_kind"] = "RECONSTRUCTED"
        with self.assertRaisesRegex(ViewerRenderError, "only renders GAP"):
            render_flat_html(pack, ENTITY, {}, SOURCE)

    def test_flat_viewer_output_is_deterministic(self) -> None:
        entity = dict(ENTITY, evidence_refs=[EVIDENCE_ID])
        pack = build_gap_scene_pack(entity, STATE, evidence_records={EVIDENCE_ID: EVIDENCE}, sources=SOURCE)
        first = render_flat_html(pack, entity, {EVIDENCE_ID: EVIDENCE}, SOURCE)
        second = render_flat_html(pack, entity, {EVIDENCE_ID: EVIDENCE}, SOURCE)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
