from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.scene_packs.state_resolver import resolve_historical_state
from scripts.scene_packs.build_scene_pack import GAP_CODE, ScenePackError

ROOT = Path(__file__).resolve().parents[1]


ENTITY = {
    "id": "NN:site:brihadisvara-thanjavur",
    "verification_status": "VERIFIED",
}
GAP = {
    "id": "NN:state:brihadisvara:gap-001",
    "entity_id": ENTITY["id"],
    "state_kind": "GAP",
    "verification_status": "UNREVIEWED",
    "valid_from": None,
    "valid_to": None,
    "asset_refs": [],
    "evidence_refs": [],
    "uncertainty": {
        "code": GAP_CODE,
        "message": "No reviewed reconstruction is available for the requested interval.",
    },
}
STATE = {
    "id": "NN:state:brihadisvara:documented-001",
    "entity_id": ENTITY["id"],
    "label": "Synthetic resolver test state (not historical project evidence)",
    "state_kind": "DOCUMENTED",
    "verification_status": "VERIFIED",
    "valid_from": "1000-01-01",
    "valid_to": "1100-12-31",
    "asset_refs": ["NN:asset:test-temple"],
    "evidence_refs": ["NN:evidence:test-001"],
}
EVIDENCE = {
    "NN:evidence:test-001": {
        "id": "NN:evidence:test-001",
        "subject_entity_id": ENTITY["id"],
        "source_id": "SRC-TEST",
        "source_locator": "Synthetic test fixture locator only",
        "valid_from": "1000-01-01",
        "valid_to": "1100-12-31",
        "verification_status": "VERIFIED",
        "reviewer": "Test reviewer",
        "verified_at": "2026-10-11",
    }
}
SOURCES = {
    "SRC-TEST": {
        "source_id": "SRC-TEST",
        "status": "RIGHTS_CLEARED",
        "rights_status": "CLEARED",
        "redistribution_allowed": "Yes",
        "commercial_use": "Yes",
        "attribution_required": "Yes",
    }
}
ASSETS = {
    "NN:asset:test-temple": {
        "id": "NN:asset:test-temple",
        "asset_type": "TEST_ONLY",
        "sha256": "a" * 64,
        "source_id": "SRC-TEST",
        "license_id": "TEST_FIXTURE",
        "rights_status": "CLEARED",
        "verification_status": "VERIFIED",
        "verified_by": "Test reviewer",
        "verified_at": "2026-10-11",
        "attribution": "Synthetic test asset; never use as a real model.",
    }
}


def resolve(
    states: list[dict] | None = None,
    entity: dict | None = None,
    evidence: dict | None = None,
    sources: dict | None = None,
    assets: dict | None = None,
    start: str | None = "1020-01-01",
    end: str | None = "1030-12-31",
) -> dict:
    return resolve_historical_state(
        start,
        end,
        entity or copy.deepcopy(ENTITY),
        states if states is not None else [copy.deepcopy(STATE)],
        copy.deepcopy(GAP),
        evidence if evidence is not None else copy.deepcopy(EVIDENCE),
        sources if sources is not None else copy.deepcopy(SOURCES),
        assets if assets is not None else copy.deepcopy(ASSETS),
    )


class HistoricalStateResolverTests(unittest.TestCase):
    def test_selects_a_single_fully_eligible_reviewed_state(self) -> None:
        result = resolve()
        self.assertEqual(result["resolution_status"], "SELECTED")
        self.assertEqual(result["reason_code"], "VERIFIED_STATE_SELECTED")
        self.assertEqual(result["state"]["id"], STATE["id"])
        self.assertFalse(result["state"]["state_kind"] == "GAP")

    def test_no_candidates_falls_back_to_gap(self) -> None:
        result = resolve(states=[])
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertEqual(result["reason_code"], "NO_ELIGIBLE_STATE_COVERS_REQUEST")
        self.assertEqual(result["state"]["state_kind"], "GAP")
        self.assertEqual(result["state"]["uncertainty"]["code"], GAP_CODE)

    def test_unreviewed_state_falls_back_to_gap(self) -> None:
        candidate = copy.deepcopy(STATE)
        candidate["verification_status"] = "UNREVIEWED"
        result = resolve(states=[candidate])
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("STATE_NOT_VERIFIED", result["rejected_candidates"][STATE["id"]])

    def test_state_that_does_not_cover_full_interval_is_rejected(self) -> None:
        result = resolve(start="0999-01-01", end="1030-12-31")
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("STATE_DOES_NOT_COVER_REQUEST", result["rejected_candidates"][STATE["id"]])

    def test_unreviewed_evidence_blocks_selection(self) -> None:
        evidence = copy.deepcopy(EVIDENCE)
        evidence["NN:evidence:test-001"]["verification_status"] = "SOURCE_LOCATED_REVIEW_PENDING"
        result = resolve(evidence=evidence)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("EVIDENCE_NOT_VERIFIED:NN:evidence:test-001", result["rejected_candidates"][STATE["id"]])

    def test_source_without_explicit_commercial_clearance_blocks_selection(self) -> None:
        sources = copy.deepcopy(SOURCES)
        sources["SRC-TEST"]["commercial_use"] = "Review"
        result = resolve(sources=sources)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("SOURCE_RIGHTS_OR_REVIEW_GATE_FAILED:SRC-TEST", result["rejected_candidates"][STATE["id"]])

    def test_asset_rights_not_cleared_blocks_selection(self) -> None:
        assets = copy.deepcopy(ASSETS)
        assets["NN:asset:test-temple"]["rights_status"] = "REVIEW_REQUIRED"
        result = resolve(assets=assets)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("ASSET_RIGHTS_NOT_CLEARED:NN:asset:test-temple", result["rejected_candidates"][STATE["id"]])

    def test_missing_asset_checksum_blocks_selection(self) -> None:
        assets = copy.deepcopy(ASSETS)
        assets["NN:asset:test-temple"]["sha256"] = "not-a-hash"
        result = resolve(assets=assets)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("ASSET_SHA256_INVALID:NN:asset:test-temple", result["rejected_candidates"][STATE["id"]])

    def test_multiple_eligible_states_are_ambiguous(self) -> None:
        second = copy.deepcopy(STATE)
        second["id"] = "NN:state:brihadisvara:documented-002"
        result = resolve(states=[copy.deepcopy(STATE), second])
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertEqual(result["reason_code"], "AMBIGUOUS_ELIGIBLE_STATES")
        self.assertEqual(result["state"]["state_kind"], "GAP")

    def test_unverified_entity_blocks_resolution(self) -> None:
        entity = copy.deepcopy(ENTITY)
        entity["verification_status"] = "UNREVIEWED"
        result = resolve(entity=entity)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertEqual(result["reason_code"], "ENTITY_NOT_VERIFIED")

    def test_requires_both_interval_dates(self) -> None:
        with self.assertRaisesRegex(ScenePackError, "requires both"):
            resolve(start="1020-01-01", end=None)

    def test_rejects_reversed_interval(self) -> None:
        with self.assertRaisesRegex(ScenePackError, "on or before"):
            resolve(start="1030-01-01", end="1020-01-01")

    def test_does_not_mutate_gap_fixture(self) -> None:
        original = copy.deepcopy(GAP)
        resolve(states=[])
        self.assertEqual(GAP, original)


    def test_evidence_without_locator_blocks_selection(self) -> None:
        evidence = copy.deepcopy(EVIDENCE)
        evidence["NN:evidence:test-001"]["source_locator"] = ""
        result = resolve(evidence=evidence)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("EVIDENCE_SOURCE_LOCATOR_MISSING:NN:evidence:test-001", result["rejected_candidates"][STATE["id"]])


    def test_source_not_reviewed_blocks_selection_even_when_permissions_are_yes(self) -> None:
        sources = copy.deepcopy(SOURCES)
        sources["SRC-TEST"]["status"] = "READY_TO_REVIEW"
        result = resolve(sources=sources)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("SOURCE_RIGHTS_OR_REVIEW_GATE_FAILED:SRC-TEST", result["rejected_candidates"][STATE["id"]])

    def test_unresolved_rights_label_blocks_despite_cleared_status(self) -> None:
        sources = copy.deepcopy(SOURCES)
        sources["SRC-TEST"]["status"] = "RIGHTS_CLEARED"
        sources["SRC-TEST"]["rights_status"] = "LICENSE_DISCREPANCY_REVIEW"
        result = resolve(sources=sources)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("SOURCE_RIGHTS_OR_REVIEW_GATE_FAILED:SRC-TEST", result["rejected_candidates"][STATE["id"]])

    def test_source_registry_key_and_record_id_must_match(self) -> None:
        sources = copy.deepcopy(SOURCES)
        sources["SRC-TEST"]["source_id"] = "SRC-OTHER"
        result = resolve(sources=sources)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("SOURCE_RIGHTS_OR_REVIEW_GATE_FAILED:SRC-TEST", result["rejected_candidates"][STATE["id"]])

    def test_evidence_that_only_overlaps_request_is_rejected(self) -> None:
        evidence = copy.deepcopy(EVIDENCE)
        evidence["NN:evidence:test-001"]["valid_from"] = "1025-01-01"
        evidence["NN:evidence:test-001"]["valid_to"] = "1100-12-31"
        result = resolve(evidence=evidence, start="1020-01-01", end="1030-12-31")
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("EVIDENCE_DOES_NOT_COVER_REQUEST:NN:evidence:test-001", result["rejected_candidates"][STATE["id"]])

    def test_adjacent_historical_era_is_not_substituted(self) -> None:
        nearby = copy.deepcopy(STATE)
        nearby["valid_from"] = "0900-01-01"
        nearby["valid_to"] = "1019-12-31"
        result = resolve(states=[nearby], start="1020-01-01", end="1030-12-31")
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertEqual(result["reason_code"], "NO_ELIGIBLE_STATE_COVERS_REQUEST")
        self.assertEqual(result["state"]["state_kind"], "GAP")
        self.assertIn("STATE_DOES_NOT_COVER_REQUEST", result["rejected_candidates"][nearby["id"]])

    def test_malformed_evidence_interval_fails_closed(self) -> None:
        evidence = copy.deepcopy(EVIDENCE)
        evidence["NN:evidence:test-001"]["valid_from"] = "circa-1000"
        result = resolve(evidence=evidence)
        self.assertEqual(result["resolution_status"], "GAP")
        reasons = result["rejected_candidates"][STATE["id"]]
        self.assertIn("EVIDENCE_INTERVAL_INVALID:NN:evidence:test-001", reasons)
        self.assertIn("EVIDENCE_DOES_NOT_COVER_REQUEST:NN:evidence:test-001", reasons)

    def test_invalid_evidence_verification_date_fails_closed(self) -> None:
        evidence = copy.deepcopy(EVIDENCE)
        evidence["NN:evidence:test-001"]["verified_at"] = "2026-02-30"
        result = resolve(evidence=evidence)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("EVIDENCE_VERIFICATION_DATE_INVALID:NN:evidence:test-001", result["rejected_candidates"][STATE["id"]])

    def test_reversed_candidate_state_interval_fails_closed(self) -> None:
        candidate = copy.deepcopy(STATE)
        candidate["valid_from"] = "1030-01-01"
        candidate["valid_to"] = "1020-12-31"
        result = resolve(states=[candidate])
        self.assertEqual(result["resolution_status"], "GAP")
        reasons = result["rejected_candidates"][candidate["id"]]
        self.assertIn("STATE_INTERVAL_INVALID", reasons)
        self.assertIn("STATE_DOES_NOT_COVER_REQUEST", reasons)

    def test_asset_without_named_clearance_basis_blocks_selection(self) -> None:
        assets = copy.deepcopy(ASSETS)
        assets["NN:asset:test-temple"]["license_id"] = ""
        result = resolve(assets=assets)
        self.assertEqual(result["resolution_status"], "GAP")
        self.assertIn("ASSET_LICENSE_BASIS_MISSING:NN:asset:test-temple", result["rejected_candidates"][STATE["id"]])

    def test_cli_returns_gap_report_for_current_unreviewed_entity(self) -> None:
        script = ROOT / "scripts/scene_packs/resolve_historical_state.py"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "resolution.json"
            completed = subprocess.run(
                [
                    sys.executable, str(script),
                    "--from", "1000-01-01",
                    "--to", "1010-12-31",
                    "--output", str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["resolution_status"], "GAP")
            self.assertEqual(report["reason_code"], "ENTITY_NOT_VERIFIED")
            self.assertEqual(report["resolved_state_kind"], "GAP")
            self.assertEqual(report["state"]["uncertainty"]["code"], GAP_CODE)
            self.assertIn("not a renderer-ready", report["note"])


if __name__ == "__main__":
    unittest.main()
