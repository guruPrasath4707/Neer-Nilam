from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.scene_packs.state_resolver import resolve_historical_state

from scripts.scene_packs.build_scene_pack import (
    DEFAULT_SCENE_ID,
    build_gap_scene_pack,
    load_evidence_records,
    load_source_registry,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "data/schemas"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_valid_schema(test: unittest.TestCase, instance: dict, schema_name: str) -> None:
    schema = read_json(SCHEMAS / schema_name)
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda error: list(map(str, error.absolute_path)),
    )
    test.assertEqual(
        errors,
        [],
        "\n".join(
            f"{schema_name} at {list(error.absolute_path)}: {error.message}"
            for error in errors
        ),
    )


class SchemaContractTests(unittest.TestCase):
    def test_canonical_entity_conforms_to_schema(self) -> None:
        entity = read_json(ROOT / "data/entities/NN-SITE-BRIHADISVARA-THANJAVUR.json")
        assert_valid_schema(self, entity, "entity-v0.schema.json")

    def test_source_linked_evidence_conforms_to_schema(self) -> None:
        evidence = read_json(ROOT / "data/evidence/NN-EVID-BRH-COMPONENT-001.json")
        assert_valid_schema(self, evidence, "evidence-v0.schema.json")

    def test_gap_state_conforms_to_schema(self) -> None:
        state = read_json(ROOT / "data/historical-states/NN-GAP-BRIHADISVARA-001.json")
        assert_valid_schema(self, state, "historical-state-v0.schema.json")

    def test_committed_gap_scene_fixture_conforms_to_schema(self) -> None:
        pack = read_json(ROOT / "data/scene-packs/BRH-001-GAP-FIXTURE.json")
        assert_valid_schema(self, pack, "scene-pack-v0.schema.json")

    def test_asset_schema_accepts_explicitly_cleared_hash_identified_asset(self) -> None:
        asset = {
            "id": "NN:asset:test-cleared",
            "asset_type": "TEST_ONLY",
            "sha256": "a" * 64,
            "source_id": "SRC-TEST",
            "source_locator": "Synthetic schema test only",
            "license_id": "TEST_FIXTURE",
            "rights_status": "CLEARED",
            "verification_status": "VERIFIED",
            "verified_by": "Schema test reviewer",
            "verified_at": "2026-10-11",
            "attribution": "Synthetic test asset; not for production use.",
            "file_path": None,
            "mime_type": None,
            "transformations": [],
            "notes": "Fixture for schema validation only.",
        }
        assert_valid_schema(self, asset, "asset-v0.schema.json")

    def test_asset_schema_rejects_malformed_sha256(self) -> None:
        asset = {
            "id": "NN:asset:test-cleared",
            "asset_type": "TEST_ONLY",
            "sha256": "not-a-hash",
            "source_id": "SRC-TEST",
            "license_id": "TEST_FIXTURE",
            "rights_status": "CLEARED",
            "verification_status": "VERIFIED",
            "verified_by": "Schema test reviewer",
            "verified_at": "2026-10-11",
            "attribution": "Synthetic test asset; not for production use.",
        }
        schema = read_json(SCHEMAS / "asset-v0.schema.json")
        errors = list(Draft202012Validator(schema).iter_errors(asset))
        self.assertTrue(any(list(error.absolute_path) == ["sha256"] for error in errors))

    def test_generated_pack_conforms_to_schema_and_keeps_evidence_trace(self) -> None:
        entity = read_json(ROOT / "data/entities/NN-SITE-BRIHADISVARA-THANJAVUR.json")
        state = read_json(ROOT / "data/historical-states/NN-GAP-BRIHADISVARA-001.json")
        evidence = load_evidence_records(ROOT / "data/evidence")
        sources = load_source_registry(ROOT / "data/manifests/source-registry-v0.csv")
        pack = build_gap_scene_pack(
            entity,
            state,
            scene_id=DEFAULT_SCENE_ID,
            evidence_records=evidence,
            sources=sources,
        )
        assert_valid_schema(self, pack, "scene-pack-v0.schema.json")
        self.assertIn("NN:evidence:brh:component-001", pack["evidence_refs"])
        self.assertTrue(pack["attribution"])
        self.assertTrue(pack["rights_notices"])
        self.assertFalse(pack["renderer_hints"]["asset_fallback_allowed"])


    def test_current_project_resolution_stays_gap_until_real_review_gates_pass(self) -> None:
        entity = read_json(ROOT / "data/entities/NN-SITE-BRIHADISVARA-THANJAVUR.json")
        gap = read_json(ROOT / "data/historical-states/NN-GAP-BRIHADISVARA-001.json")
        state_dir = ROOT / "data/historical-states"
        candidates = [
            read_json(path) for path in sorted(state_dir.glob("*.json"))
            if path.name != "NN-GAP-BRIHADISVARA-001.json"
        ]
        evidence = load_evidence_records(ROOT / "data/evidence")
        sources = load_source_registry(ROOT / "data/manifests/source-registry-v0.csv")
        assets_dir = ROOT / "data/assets"
        assets = {}
        for path in sorted(assets_dir.glob("*.json")) if assets_dir.exists() else []:
            asset = read_json(path)
            assets[asset["id"]] = asset

        result = resolve_historical_state(
            "1000-01-01",
            "1010-12-31",
            entity,
            candidates,
            gap,
            evidence,
            sources,
            assets,
        )
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertEqual(result["reason_code"], "ENTITY_NOT_VERIFIED")
        self.assertEqual(result["state"]["state_kind"], "GAP")
        self.assertEqual(result["state"]["uncertainty"]["code"], "NO_SUPPORTED_RECONSTRUCTION")



if __name__ == "__main__":
    unittest.main()
