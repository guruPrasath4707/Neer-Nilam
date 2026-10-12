#!/usr/bin/env python3
"""Render a self-contained accessible HTML evidence view from a GAP scene pack (stdlib only)."""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_DIR = ROOT / "data/evidence"
DEFAULT_SOURCE_REGISTRY = ROOT / "data/manifests/source-registry-v0.csv"


class ViewerRenderError(ValueError):
    """Raised when the scene pack cannot safely be rendered."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ViewerRenderError(f"Cannot load valid JSON from {path}: {exc}") from exc
    if not isinstance(result, dict):
        raise ViewerRenderError(f"Expected a JSON object in {path}")
    return result


def load_evidence_records(directory: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    if not directory.exists():
        return records
    for path in sorted(directory.glob("*.json")):
        record = load_json(path)
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            raise ViewerRenderError(f"Evidence record has no id: {path}")
        if record_id in records:
            raise ViewerRenderError(f"Duplicate evidence id: {record_id}")
        records[record_id] = record
    return records


def load_source_registry(path: Path) -> dict[str, dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "source_id" not in reader.fieldnames:
                raise ViewerRenderError("Source registry must include source_id")
            records: dict[str, dict[str, str]] = {}
            for row in reader:
                source_id = (row.get("source_id") or "").strip()
                if not source_id:
                    continue
                if source_id in records:
                    raise ViewerRenderError(f"Duplicate source id: {source_id}")
                records[source_id] = {k: (v or "").strip() for k, v in row.items() if k}
            return records
    except OSError as exc:
        raise ViewerRenderError(f"Cannot read source registry {path}: {exc}") from exc


def esc(value: Any, fallback: str = "Not recorded") -> str:
    if value is None or value == "":
        value = fallback
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return html.escape(str(value), quote=True)


def safe_url(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip()
    parsed = urlsplit(value)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return None
    return html.escape(value, quote=True)


def render_flat_html(
    scene_pack: dict[str, Any],
    entity: dict[str, Any],
    evidence_records: dict[str, dict[str, Any]],
    sources: dict[str, dict[str, str]],
) -> str:
    """Return deterministic, standalone HTML; all dynamic text is HTML-escaped."""
    scene_id, entity_id = scene_pack.get("scene_id"), entity.get("id")
    if not isinstance(scene_id, str) or not scene_id.strip():
        raise ViewerRenderError("Scene pack must include scene_id")
    if not isinstance(entity_id, str) or entity_id not in scene_pack.get("entities", []):
        raise ViewerRenderError("Entity must be referenced by scene pack")
    if scene_pack.get("state_kind") != "GAP":
        raise ViewerRenderError("Flat viewer v0 only renders GAP scene packs")
    uncertainty = scene_pack.get("uncertainty")
    if not isinstance(uncertainty, dict) or uncertainty.get("code") != "NO_SUPPORTED_RECONSTRUCTION":
        raise ViewerRenderError("GAP scene requires NO_SUPPORTED_RECONSTRUCTION")
    hints = scene_pack.get("renderer_hints") or {}
    if scene_pack.get("asset_refs") or hints.get("historical_geometry") is not False or hints.get("asset_fallback_allowed") is not False:
        raise ViewerRenderError("GAP scenes must not render assets, historical geometry, or fallback visuals")

    interval = scene_pack.get("requested_interval") or {}
    start, end = interval.get("from"), interval.get("to")
    if start is None and end is None:
        interval_text = "No specific historical interval selected"
    elif start is not None and end is not None:
        interval_text = f"{esc(start)} to {esc(end)}"
    else:
        raise ViewerRenderError("Requested interval must be unbounded or contain both endpoints")

    evidence_rows: list[str] = []
    evidence_refs = scene_pack.get("evidence_refs", [])
    if not isinstance(evidence_refs, list) or not all(isinstance(x, str) for x in evidence_refs):
        raise ViewerRenderError("evidence_refs must be an array of strings")
    for evidence_id in evidence_refs:
        evidence = evidence_records.get(evidence_id)
        if evidence is None:
            raise ViewerRenderError(f"Referenced evidence record not found: {evidence_id}")
        source_id = evidence.get("source_id")
        source = sources.get(source_id) if isinstance(source_id, str) else None
        if source is None:
            raise ViewerRenderError(f"Evidence {evidence_id} references unknown source {source_id!r}")
        locator = evidence.get("source_locator")
        if not isinstance(locator, str) or not locator.strip():
            raise ViewerRenderError(f"Evidence {evidence_id} has no source locator")
        source_label = source.get("organization") or source.get("title") or source_id
        href = safe_url(source.get("url"))
        source_label_html = esc(source_label)
        if href:
            source_label_html = f'<a href="{href}" rel="noopener noreferrer">{source_label_html}</a>'
        evidence_rows.append(f'''<article class="evidence">
<h3>{esc(evidence.get("assertion_text") or evidence.get("predicate"), "Source-linked assertion")}</h3>
<dl><dt>Evidence ID</dt><dd><code>{esc(evidence_id)}</code></dd>
<dt>Source</dt><dd>{source_label_html} ({esc(source_id)})</dd>
<dt>Locator</dt><dd>{esc(locator)}</dd>
<dt>Review status</dt><dd><span class="tag">{esc(evidence.get("verification_status"), "UNREVIEWED")}</span></dd>
<dt>Source rights</dt><dd><span class="tag">{esc(source.get("rights_status"), "REVIEW_REQUIRED")}</span></dd></dl>
</article>''')
    if not evidence_rows:
        evidence_rows.append("<p>No linked assertions are recorded.</p>")

    def list_items(key: str) -> str:
        values = scene_pack.get(key, [])
        if not isinstance(values, list):
            raise ViewerRenderError(f"{key} must be an array")
        return "".join(f"<li>{esc(item)}</li>" for item in values) or "<li>None recorded.</li>"

    title = esc(entity.get("canonical_name"), "Neer-Nilam scene")
    gap_message = esc(uncertainty.get("message"), "No reviewed reconstruction is available for this interval.")
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Neer-Nilam evidence view</title>
<style>
:root {{ font-family: system-ui, -apple-system, "Segoe UI", sans-serif; line-height: 1.55; color-scheme: light dark; }}
body {{ max-width: 54rem; margin: 0 auto; padding: clamp(1rem, 4vw, 2.5rem); }}
header, section, footer {{ margin-block: 1.5rem; }} h1 {{ line-height: 1.15; }}
.muted {{ color: GrayText; font-size: .92rem; }}
.notice, .evidence {{ border: 1px solid GrayText; border-radius: .35rem; padding: 1rem; margin-block: 1rem; }}
.notice {{ border-left-width: .35rem; }} .notice h2 {{ margin-top: 0; }}
dl {{ display: grid; grid-template-columns: minmax(8rem, 30%) 1fr; gap: .35rem .8rem; }}
dt {{ font-weight: 650; }} dd {{ margin: 0; min-width: 0; overflow-wrap: anywhere; }}
.tag {{ border: 1px solid GrayText; border-radius: .25rem; padding: .05rem .4rem; }}
code {{ overflow-wrap: anywhere; }} a {{ text-underline-offset: .15em; }}
@media(max-width:34rem) {{ dl {{ grid-template-columns: 1fr; gap: .1rem; }} dd {{ margin-bottom: .6rem; }} }}
@media print {{ body {{ max-width: none; }} }}
</style>
</head>
<body>
<header><p class="muted">NEER-NILAM / FLAT EVIDENCE VIEW</p>
<h1>{title}</h1><p>Scene pack: <code>{esc(scene_id)}</code></p>
<p>Requested interval: <strong>{interval_text}</strong></p></header>
<main>
<section class="notice" role="status" aria-labelledby="gap-title">
<h2 id="gap-title">Historical reconstruction unavailable</h2>
<p>{gap_message}</p><p><strong>Gap code:</strong> <code>NO_SUPPORTED_RECONSTRUCTION</code></p>
<p>This is a gap in the currently resolved project data for this interval, not a claim that no historical evidence exists. No substitute period, temple model, terrain or visual asset has been inserted.</p>
</section>
<section aria-labelledby="evidence-title"><h2 id="evidence-title">Linked evidence and source review</h2>
{''.join(evidence_rows)}</section>
<section aria-labelledby="rights-title"><h2 id="rights-title">Rights and attribution</h2>
<h3>Outstanding rights notices</h3><ul>{list_items("rights_notices")}</ul>
<h3>Attribution</h3><ul>{list_items("attribution")}</ul></section>
<section aria-labelledby="presentation-title"><h2 id="presentation-title">Presentation state</h2>
<p>Flat evidence mode is available. Historical geometry is disabled and renderer asset fallback is prohibited for this GAP state. Other presentation clients must retain this same evidence state.</p></section>
</main><footer><p class="muted">Scene-pack version {esc(scene_pack.get("scene_pack_version"))}; generator {esc(scene_pack.get("generator_version"))}.</p></footer>
</body></html>
'''


def write_atomic(path: Path, document: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
    parser.add_argument("--scene-pack", type=Path, required=True)
    parser.add_argument("--entity", type=Path, default=ROOT / "data/entities/NN-SITE-BRIHADISVARA-THANJAVUR.json")
    parser.add_argument("--evidence-dir", type=Path, default=DEFAULT_EVIDENCE_DIR)
    parser.add_argument("--source-registry", type=Path, default=DEFAULT_SOURCE_REGISTRY)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        pack = load_json(args.scene_pack)
        entity = load_json(args.entity)
        evidence = load_evidence_records(args.evidence_dir)
        sources = load_source_registry(args.source_registry)
        output = render_flat_html(pack, entity, evidence, sources)
        write_atomic(args.output, output)
    except (ViewerRenderError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote standalone flat evidence view: {args.output}")
    print(f"Scene: {pack.get('scene_id')} ({pack.get('state_kind')}); linked evidence: {len(pack.get('evidence_refs', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
