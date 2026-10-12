#!/usr/bin/env python3
"""Fail-closed selector for reviewed Neer-Nilam historical states.

This module makes a selection decision only. It never edits records, creates history,
or relaxes the explicit GAP fallback. v0 uses a conservative rights gate for
commercial-capable presentation: the source registry must be marked REVIEWED (or
RIGHTS_CLEARED), explicitly allow redistribution and commercial use, and the
referenced asset must be hash-identified, VERIFIED, and RIGHTS_CLEARED.
"""
from __future__ import annotations

import copy
import re
from datetime import date
from typing import Any

from scripts.scene_packs.build_scene_pack import GAP_CODE, ScenePackError, _validate_iso_date

SUPPORTED_KINDS = {"DOCUMENTED", "RECONSTRUCTED", "INTERPRETED"}
APPROVED_SOURCE_STATUSES = {"REVIEWED", "RIGHTS_CLEARED"}
APPROVED_YES = {"yes", "true"}
SHA256_PATTERN = re.compile(r"^[a-fA-F0-9]{64}$")


def _covers_interval(
    record_from: str | None,
    record_to: str | None,
    requested_from: str,
    requested_to: str,
    label: str,
) -> bool:
    start = _validate_iso_date(record_from, f"{label}.valid_from")
    end = _validate_iso_date(record_to, f"{label}.valid_to")
    if start is None or end is None:
        return False
    if start > end:
        raise ScenePackError(f"{label}.valid_from must be on or before valid_to")
    return start <= requested_from and end >= requested_to


def _source_is_eligible(
    source: dict[str, Any] | None,
    expected_source_id: str | None = None,
) -> bool:
    if not source:
        return False
    if expected_source_id is not None and str(source.get("source_id", "")).strip() != expected_source_id:
        return False

    status = str(source.get("status", "")).strip().upper()
    if status not in APPROVED_SOURCE_STATUSES:
        return False

    rights_status = str(source.get("rights_status", "")).strip()
    if not rights_status:
        return False
    normalized_rights = re.sub(r"[^a-z0-9]+", " ", rights_status.casefold()).strip()
    rights_tokens = set(normalized_rights.split())
    blocked_rights_tokens = {
        "review", "hold", "discrepancy", "unknown", "unverified",
        "pending", "required", "restricted", "unresolved", "provisional", "nc",
    }
    if rights_tokens & blocked_rights_tokens:
        return False
    if re.search(r"\bnon\s*commercial\b|\ball\s*rights\s*reserved\b|\bno\s*redistribution\b", normalized_rights):
        return False

    if str(source.get("redistribution_allowed", "")).strip().casefold() not in APPROVED_YES:
        return False
    if str(source.get("commercial_use", "")).strip().casefold() not in APPROVED_YES:
        return False
    return True


def _candidate_reasons(
    state: dict[str, Any],
    entity: dict[str, Any],
    requested_from: str,
    requested_to: str,
    evidence_records: dict[str, dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    assets: dict[str, dict[str, Any]],
) -> list[str]:
    reasons: list[str] = []
    state_id = state.get("id", "<missing-state-id>")
    if state.get("entity_id") != entity.get("id"):
        reasons.append("ENTITY_MISMATCH")
    if state.get("state_kind") not in SUPPORTED_KINDS:
        reasons.append("STATE_KIND_NOT_RENDERABLE")
    if state.get("verification_status") != "VERIFIED":
        reasons.append("STATE_NOT_VERIFIED")
    try:
        covered = _covers_interval(
            state.get("valid_from"), state.get("valid_to"),
            requested_from, requested_to, f"state[{state_id}]",
        )
    except ScenePackError:
        covered = False
        reasons.append("STATE_INTERVAL_INVALID")
    if not covered:
        reasons.append("STATE_DOES_NOT_COVER_REQUEST")

    evidence_ids = state.get("evidence_refs")
    if not isinstance(evidence_ids, list) or not evidence_ids:
        reasons.append("NO_EVIDENCE_REFERENCES")
        evidence_ids = []
    for evidence_id in evidence_ids:
        record = evidence_records.get(evidence_id) if isinstance(evidence_id, str) else None
        if not record or record.get("id") != evidence_id:
            reasons.append(f"EVIDENCE_MISSING:{evidence_id}")
            continue
        if record.get("subject_entity_id") != entity.get("id"):
            reasons.append(f"EVIDENCE_ENTITY_MISMATCH:{evidence_id}")
        if record.get("verification_status") != "VERIFIED":
            reasons.append(f"EVIDENCE_NOT_VERIFIED:{evidence_id}")
        if not isinstance(record.get("source_locator"), str) or not record["source_locator"].strip():
            reasons.append(f"EVIDENCE_SOURCE_LOCATOR_MISSING:{evidence_id}")
        if not str(record.get("reviewer", "")).strip():
            reasons.append(f"EVIDENCE_REVIEWER_MISSING:{evidence_id}")
        try:
            verified_at = _validate_iso_date(record.get("verified_at"), f"evidence[{evidence_id}].verified_at")
            if verified_at is None:
                reasons.append(f"EVIDENCE_VERIFICATION_DATE_MISSING:{evidence_id}")
        except ScenePackError:
            reasons.append(f"EVIDENCE_VERIFICATION_DATE_INVALID:{evidence_id}")
        try:
            evidence_covers = _covers_interval(
                record.get("valid_from"), record.get("valid_to"),
                requested_from, requested_to, f"evidence[{evidence_id}]",
            )
        except ScenePackError:
            evidence_covers = False
            reasons.append(f"EVIDENCE_INTERVAL_INVALID:{evidence_id}")
        if not evidence_covers:
            reasons.append(f"EVIDENCE_DOES_NOT_COVER_REQUEST:{evidence_id}")
        source_id = record.get("source_id")
        source = sources.get(source_id) if isinstance(source_id, str) else None
        if not _source_is_eligible(source, source_id):
            reasons.append(f"SOURCE_RIGHTS_OR_REVIEW_GATE_FAILED:{source_id}")

    asset_ids = state.get("asset_refs")
    if not isinstance(asset_ids, list) or not asset_ids:
        reasons.append("NO_ASSET_REFERENCES")
        asset_ids = []
    for asset_id in asset_ids:
        asset = assets.get(asset_id) if isinstance(asset_id, str) else None
        if not asset or asset.get("id") != asset_id:
            reasons.append(f"ASSET_MISSING:{asset_id}")
            continue
        if asset.get("verification_status") != "VERIFIED":
            reasons.append(f"ASSET_NOT_VERIFIED:{asset_id}")
        if not str(asset.get("verified_by", "")).strip():
            reasons.append(f"ASSET_REVIEWER_MISSING:{asset_id}")
        try:
            if _validate_iso_date(asset.get("verified_at"), f"asset[{asset_id}].verified_at") is None:
                reasons.append(f"ASSET_VERIFICATION_DATE_MISSING:{asset_id}")
        except ScenePackError:
            reasons.append(f"ASSET_VERIFICATION_DATE_INVALID:{asset_id}")
        if asset.get("rights_status") != "CLEARED":
            reasons.append(f"ASSET_RIGHTS_NOT_CLEARED:{asset_id}")
        if not str(asset.get("license_id", "")).strip():
            reasons.append(f"ASSET_LICENSE_BASIS_MISSING:{asset_id}")
        if not str(asset.get("attribution", "")).strip():
            reasons.append(f"ASSET_ATTRIBUTION_MISSING:{asset_id}")
        if not isinstance(asset.get("sha256"), str) or not SHA256_PATTERN.fullmatch(asset["sha256"]):
            reasons.append(f"ASSET_SHA256_INVALID:{asset_id}")
        source_id = asset.get("source_id")
        source = sources.get(source_id) if isinstance(source_id, str) else None
        if not _source_is_eligible(source, source_id):
            reasons.append(f"ASSET_SOURCE_RIGHTS_OR_REVIEW_GATE_FAILED:{source_id}")

    return list(dict.fromkeys(reasons))


def resolve_historical_state(
    requested_from: str | None,
    requested_to: str | None,
    entity: dict[str, Any],
    candidate_states: list[dict[str, Any]],
    gap_state: dict[str, Any],
    evidence_records: dict[str, dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    assets: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Return a reviewed state only when every gate passes; otherwise return GAP.

    Request interval endpoints are mandatory for historical selection. An exact
    eligible-state tie is treated as ambiguity rather than resolving by list order.
    A GAP response preserves the project's explicit NO_SUPPORTED_RECONSTRUCTION
    state and explains why candidates were not selected.
    """
    start = _validate_iso_date(requested_from, "requested_from")
    end = _validate_iso_date(requested_to, "requested_to")
    if start is None or end is None:
        raise ScenePackError("Historical-state resolution requires both requested_from and requested_to")
    if start > end:
        raise ScenePackError("requested_from must be on or before requested_to")
    if gap_state.get("state_kind") != "GAP":
        raise ScenePackError("gap_state must have state_kind GAP")
    uncertainty = gap_state.get("uncertainty")
    if not isinstance(uncertainty, dict) or uncertainty.get("code") != GAP_CODE:
        raise ScenePackError(f"gap_state must use uncertainty code {GAP_CODE}")

    if entity.get("verification_status") != "VERIFIED":
        return _gap_result(gap_state, "ENTITY_NOT_VERIFIED", [])

    eligible: list[dict[str, Any]] = []
    all_reasons: dict[str, list[str]] = {}
    for state in candidate_states:
        reasons = _candidate_reasons(
            state, entity, start, end, evidence_records, sources, assets
        )
        state_id = str(state.get("id", "<missing-state-id>"))
        if not reasons:
            eligible.append(state)
        else:
            all_reasons[state_id] = reasons

    if len(eligible) == 1:
        return {
            "state": copy.deepcopy(eligible[0]),
            "resolution_status": "SELECTED",
            "reason_code": "VERIFIED_STATE_SELECTED",
            "rejected_candidates": all_reasons,
        }
    if len(eligible) > 1:
        return _gap_result(
            gap_state,
            "AMBIGUOUS_ELIGIBLE_STATES",
            [str(state.get("id", "<missing-state-id>")) for state in eligible],
            all_reasons,
        )
    rejected_ids = sorted(all_reasons)
    return _gap_result(
        gap_state,
        "NO_ELIGIBLE_STATE_COVERS_REQUEST",
        rejected_ids,
        all_reasons,
    )


def _gap_result(
    gap_state: dict[str, Any],
    reason_code: str,
    candidate_ids: list[str],
    rejected: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    state = copy.deepcopy(gap_state)
    uncertainty = copy.deepcopy(state.get("uncertainty") or {})
    uncertainty["code"] = GAP_CODE
    uncertainty["resolution_reason"] = reason_code
    uncertainty["candidate_state_ids"] = list(candidate_ids)
    state["uncertainty"] = uncertainty
    return {
        "state": state,
        "resolution_status": "GAP",
        "reason_code": reason_code,
        "rejected_candidates": rejected or {},
    }
