from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

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
        Draft202012Validator(
            schema,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        ).iter_errors(instance),
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
        errors = list(Draft202012Validator(
            schema,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        ).iter_errors(asset))
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



    def test_entity_schema_rejects_impossible_validity_date(self) -> None:
        entity = read_json(ROOT / "data/entities/NN-SITE-BRIHADISVARA-THANJAVUR.json")
        entity["valid_from"] = "2026-02-30"
        schema = read_json(SCHEMAS / "entity-v0.schema.json")
        errors = list(Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        ).iter_errors(entity))
        self.assertTrue(any(list(error.absolute_path) == ["valid_from"] for error in errors))

    def test_evidence_schema_rejects_impossible_calendar_date(self) -> None:
        evidence = read_json(ROOT / "data/evidence/NN-EVID-BRH-COMPONENT-001.json")
        evidence["valid_from"] = "2026-02-30"
        schema = read_json(SCHEMAS / "evidence-v0.schema.json")
        errors = list(Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        ).iter_errors(evidence))
        self.assertTrue(any(list(error.absolute_path) == ["valid_from"] for error in errors))

    def test_verified_evidence_requires_review_and_full_date_coverage(self) -> None:
        evidence = read_json(ROOT / "data/evidence/NN-EVID-BRH-COMPONENT-001.json")
        evidence["verification_status"] = "VERIFIED"
        schema = read_json(SCHEMAS / "evidence-v0.schema.json")
        errors = list(Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        ).iter_errors(evidence))
        paths = {tuple(error.absolute_path) for error in errors}
        self.assertIn(("reviewer",), paths)
        self.assertIn(("verified_at",), paths)
        self.assertIn(("valid_from",), paths)
        self.assertIn(("valid_to",), paths)

    def test_historical_state_schema_rejects_impossible_validity_date(self) -> None:
        state = read_json(ROOT / "data/historical-states/NN-GAP-BRIHADISVARA-001.json")
        state["valid_from"] = "2026-02-30"
        schema = read_json(SCHEMAS / "historical-state-v0.schema.json")
        errors = list(Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        ).iter_errors(state))
        self.assertTrue(any(list(error.absolute_path) == ["valid_from"] for error in errors))


    def test_verified_evidence_requires_nonempty_claim_payload(self) -> None:
        evidence = read_json(ROOT / "data/evidence/NN-EVID-BRH-COMPONENT-001.json")
        evidence["verification_status"] = "VERIFIED"
        evidence["reviewer"] = "Schema test reviewer"
        evidence["verified_at"] = "2026-10-12"
        evidence["valid_from"] = "1000-01-01"
        evidence["valid_to"] = "1100-12-31"
        evidence["assertion_text"] = ""
        evidence["object_entity_id"] = None
        evidence["value"] = None
        schema = read_json(SCHEMAS / "evidence-v0.schema.json")
        errors = list(Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        ).iter_errors(evidence))
        self.assertTrue(any(error.validator == "anyOf" for error in errors))

    def test_verified_renderable_state_requires_evidence_assets_and_bounded_dates(self) -> None:
        state = read_json(ROOT / "data/historical-states/NN-GAP-BRIHADISVARA-001.json")
        state["state_kind"] = "DOCUMENTED"
        state["verification_status"] = "VERIFIED"
        state["valid_from"] = "1000-01-01"
        state["valid_to"] = "1010-12-31"
        schema = read_json(SCHEMAS / "historical-state-v0.schema.json")
        errors = list(Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        ).iter_errors(state))
        paths = {tuple(error.absolute_path) for error in errors}
        self.assertIn(("evidence_refs",), paths)
        self.assertIn(("asset_refs",), paths)

    def test_scene_pack_interval_requires_both_bounds_or_neither(self) -> None:
        pack = read_json(ROOT / "data/scene-packs/BRH-001-GAP-FIXTURE.json")
        pack["requested_interval"]["from"] = "1000-01-01"
        schema = read_json(SCHEMAS / "scene-pack-v0.schema.json")
        errors = list(Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        ).iter_errors(pack))
        self.assertTrue(any(list(error.absolute_path) == ["requested_interval"] for error in errors))

    def test_asset_schema_rejects_impossible_verification_date(self) -> None:
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
            "verified_at": "2026-02-30",
            "attribution": "Synthetic test asset; not for production use."
        }
        schema = read_json(SCHEMAS / "asset-v0.schema.json")
        errors = list(Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        ).iter_errors(asset))
        self.assertTrue(any(list(error.absolute_path) == ["verified_at"] for error in errors))


    def test_repository_records_have_valid_schemas_and_resolvable_references(self) -> None:
        source_path = ROOT / "data/manifests/source-registry-v0.csv"
        required_source_fields = {
            "source_id", "organization", "title", "url", "rights_status",
            "redistribution_allowed", "commercial_use", "status",
        }
        with source_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or [])
            self.assertTrue(required_source_fields.issubset(headers))
            source_rows = list(reader)

        sources = load_source_registry(source_path)
        self.assertEqual(len(source_rows), len(sources))
        for row in source_rows:
            for field in required_source_fields:
                self.assertTrue((row.get(field) or "").strip(), f"Blank source field {field}: {row.get('source_id')}")
            parsed_url = urlparse(row["url"].strip())
            self.assertIn(parsed_url.scheme.casefold(), {"http", "https"})
            self.assertTrue(parsed_url.netloc, f"Source URL has no host: {row['source_id']}")

        entities = {}
        for path in sorted((ROOT / "data/entities").glob("*.json")):
            record = read_json(path)
            self.assertTrue(record.get("id"), f"Missing entity ID: {path}")
            self.assertNotIn(record["id"], entities, f"Duplicate entity ID: {record['id']}")
            assert_valid_schema(self, record, "entity-v0.schema.json")
            entities[record["id"]] = record

        evidence = load_evidence_records(ROOT / "data/evidence")
        for record_id, record in evidence.items():
            assert_valid_schema(self, record, "evidence-v0.schema.json")
            self.assertIn(record.get("subject_entity_id"), entities, f"Unknown subject for {record_id}")
            self.assertIn(record.get("source_id"), sources, f"Unknown source for {record_id}")
            object_id = record.get("object_entity_id")
            if isinstance(object_id, str) and object_id.strip():
                self.assertIn(object_id, entities, f"Unknown object entity for {record_id}")

        states = {}
        for path in sorted((ROOT / "data/historical-states").glob("*.json")):
            record = read_json(path)
            self.assertTrue(record.get("id"), f"Missing state ID: {path}")
            self.assertNotIn(record["id"], states, f"Duplicate state ID: {record['id']}")
            assert_valid_schema(self, record, "historical-state-v0.schema.json")
            states[record["id"]] = record

        assets = {}
        assets_dir = ROOT / "data/assets"
        for path in sorted(assets_dir.glob("*.json")) if assets_dir.exists() else []:
            record = read_json(path)
            self.assertTrue(record.get("id"), f"Missing asset ID: {path}")
            self.assertNotIn(record["id"], assets, f"Duplicate asset ID: {record['id']}")
            assert_valid_schema(self, record, "asset-v0.schema.json")
            self.assertIn(record.get("source_id"), sources, f"Unknown source for asset {record['id']}")
            assets[record["id"]] = record

        for entity_id, entity in entities.items():
            for source_id in entity.get("source_refs", []):
                self.assertIn(source_id, sources, f"Unknown source {source_id} on {entity_id}")
            for evidence_id in entity.get("evidence_refs", []):
                self.assertIn(evidence_id, evidence, f"Unknown evidence {evidence_id} on {entity_id}")
            for asset_id in entity.get("asset_refs", []):
                self.assertIn(asset_id, assets, f"Unknown asset {asset_id} on {entity_id}")

        for state_id, state in states.items():
            self.assertIn(state.get("entity_id"), entities, f"Unknown entity on state {state_id}")
            for evidence_id in state.get("evidence_refs", []):
                self.assertIn(evidence_id, evidence, f"Unknown evidence {evidence_id} on state {state_id}")
            for asset_id in state.get("asset_refs", []):
                self.assertIn(asset_id, assets, f"Unknown asset {asset_id} on state {state_id}")

        for path in sorted((ROOT / "data/scene-packs").glob("*.json")):
            pack = read_json(path)
            assert_valid_schema(self, pack, "scene-pack-v0.schema.json")
            for entity_id in pack.get("entities", []):
                self.assertIn(entity_id, entities, f"Unknown entity in {path.name}: {entity_id}")
            for evidence_id in pack.get("evidence_refs", []):
                self.assertIn(evidence_id, evidence, f"Unknown evidence in {path.name}: {evidence_id}")
            for asset_id in pack.get("asset_refs", []):
                self.assertIn(asset_id, assets, f"Unknown asset in {path.name}: {asset_id}")
            state_id = pack.get("resolved_state_id")
            if state_id:
                self.assertIn(state_id, states, f"Unknown resolved state in {path.name}: {state_id}")
            for gap_id in pack.get("data_gaps", []):
                self.assertIn(gap_id, states, f"Unknown data-gap state in {path.name}: {gap_id}")

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




    def test_real_unreviewed_site_evidence_and_source_block_synthetic_candidate(self) -> None:
        # Negative integration test only: the candidate below is synthetic and must
        # never be registered as a real historical state or asset.
        entity = read_json(ROOT / "data/entities/NN-SITE-BRIHADISVARA-THANJAVUR.json")
        entity["verification_status"] = "VERIFIED"
        gap = read_json(ROOT / "data/historical-states/NN-GAP-BRIHADISVARA-001.json")
        evidence = load_evidence_records(ROOT / "data/evidence")
        sources = load_source_registry(ROOT / "data/manifests/source-registry-v0.csv")

        synthetic_state_id = "NN:state:synthetic-negative-test-only"
        synthetic_asset_id = "NN:asset:synthetic-negative-test-only"
        candidate = {
            "id": synthetic_state_id,
            "entity_id": entity["id"],
            "label": "SYNTHETIC NEGATIVE TEST ONLY — not historical evidence",
            "state_kind": "DOCUMENTED",
            "verification_status": "VERIFIED",
            "valid_from": "1000-01-01",
            "valid_to": "1010-12-31",
            "evidence_refs": ["NN:evidence:brh:component-001"],
            "asset_refs": [synthetic_asset_id],
        }
        assets = {
            synthetic_asset_id: {
                "id": synthetic_asset_id,
                "asset_type": "TEST_ONLY",
                "sha256": "a" * 64,
                "source_id": "SRC-UNESCO-TNT",
                "license_id": "TEST_FIXTURE_ONLY",
                "rights_status": "CLEARED",
                "verification_status": "VERIFIED",
                "verified_by": "Automated test",
                "verified_at": "2026-10-12",
                "attribution": "Synthetic test only; not a real asset.",
            }
        }

        result = resolve_historical_state(
            "1000-01-01",
            "1010-12-31",
            entity,
            [candidate],
            gap,
            evidence,
            sources,
            assets,
        )
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertEqual(result["state"]["state_kind"], "GAP")
        reasons = result["rejected_candidates"][synthetic_state_id]
        self.assertIn("EVIDENCE_NOT_VERIFIED:NN:evidence:brh:component-001", reasons)
        self.assertIn("EVIDENCE_VERIFICATION_DATE_MISSING:NN:evidence:brh:component-001", reasons)
        self.assertIn("EVIDENCE_DOES_NOT_COVER_REQUEST:NN:evidence:brh:component-001", reasons)
        self.assertIn("SOURCE_RIGHTS_OR_REVIEW_GATE_FAILED:SRC-UNESCO-TNT", reasons)
        self.assertIn("ASSET_SOURCE_RIGHTS_OR_REVIEW_GATE_FAILED:SRC-UNESCO-TNT", reasons)

if __name__ == "__main__":
    unittest.main()
