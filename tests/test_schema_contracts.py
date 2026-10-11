from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

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


if __name__ == "__main__":
    unittest.main()
