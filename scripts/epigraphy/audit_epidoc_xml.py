#!/usr/bin/env python3
"""Create a local, metadata-only audit of EpiDoc XML files.

This tool never downloads source material, edits input files, or extracts
historical claims or inscription text. It records technical metadata and
licence targets declared in the XML so they can be reviewed against the
project's source-level rights hold.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any

TOOL_VERSION = "0.1.0"
XML_NAMESPACE = "{http://www.w3.org/XML/1998/namespace}"
ENTITY_DECLARATION = re.compile(rb"<!\s*ENTITY\b", re.IGNORECASE)
STRUCTURAL_TAGS = (
    "TEI",
    "origDate",
    "date",
    "placeName",
    "persName",
    "orgName",
    "gap",
    "unclear",
    "supplied",
    "choice",
    "lb",
)
CSV_FIELDS = (
    "source_id",
    "relative_path",
    "size_bytes",
    "sha256",
    "parse_status",
    "root_name",
    "root_namespace",
    "xml_lang",
    "xml_id",
    "licence_status",
    "licence_targets_json",
    "licence_elements_without_target",
    "tag_counts_json",
)


def local_name(tag: Any) -> str:
    """Return a namespace-independent XML local name."""
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def namespace_uri(tag: Any) -> str:
    """Return the namespace URI for a namespaced tag, otherwise empty text."""
    if not isinstance(tag, str) or not tag.startswith("{") or "}" not in tag:
        return ""
    return tag[1:].split("}", 1)[0]


def hash_file(path: Path) -> str:
    """Hash a file incrementally, including when it exceeds the parse limit."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def empty_row(source_id: str, path: Path, root: Path) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "relative_path": path.relative_to(root).as_posix(),
        "size_bytes": "",
        "sha256": "",
        "parse_status": "NOT_ASSESSED",
        "root_name": "",
        "root_namespace": "",
        "xml_lang": "",
        "xml_id": "",
        "licence_status": "NOT_ASSESSED",
        "licence_targets_json": "[]",
        "licence_elements_without_target": "",
        "tag_counts_json": "{}",
    }


def scan_file(
    path: Path,
    root: Path,
    source_id: str,
    max_file_bytes: int,
) -> dict[str, Any]:
    """Inspect one XML file; any failure is explicit in the returned row."""
    row = empty_row(source_id, path, root)

    try:
        initial_size = path.stat().st_size
        if initial_size > max_file_bytes:
            row["size_bytes"] = initial_size
            row["sha256"] = hash_file(path)
            row["parse_status"] = "FILE_TOO_LARGE"
            return row

        data = path.read_bytes()
    except OSError:
        row["parse_status"] = "IO_ERROR"
        return row

    row["size_bytes"] = len(data)
    row["sha256"] = hashlib.sha256(data).hexdigest()

    if len(data) > max_file_bytes:
        row["parse_status"] = "FILE_TOO_LARGE"
        return row

    # Reject custom entity declarations before parsing. The standard-library
    # parser does not need remote schemas, and the audit must not expand custom
    # entities from arbitrary source XML.
    if ENTITY_DECLARATION.search(data):
        row["parse_status"] = "UNSAFE_ENTITY_DECLARATION"
        return row

    try:
        document_root = ET.fromstring(data)
    except (ET.ParseError, ValueError):
        row["parse_status"] = "XML_PARSE_ERROR"
        return row

    row["parse_status"] = "PARSED"
    row["root_name"] = local_name(document_root.tag)
    row["root_namespace"] = namespace_uri(document_root.tag)
    row["xml_lang"] = document_root.attrib.get(XML_NAMESPACE + "lang", "")
    row["xml_id"] = document_root.attrib.get(XML_NAMESPACE + "id", "")

    tag_counts: Counter[str] = Counter()
    licence_targets: set[str] = set()
    licence_elements = 0
    licence_elements_without_target = 0

    for element in document_root.iter():
        element_name = local_name(element.tag)
        if element_name in STRUCTURAL_TAGS:
            tag_counts[element_name] += 1
        if element_name == "licence":
            licence_elements += 1
            targets = element.attrib.get("target", "").split()
            if not targets:
                licence_elements_without_target += 1
            licence_targets.update(targets)

    targets_sorted = sorted(licence_targets)
    row["licence_targets_json"] = json.dumps(
        targets_sorted, ensure_ascii=False, separators=(",", ":")
    )
    row["licence_elements_without_target"] = licence_elements_without_target
    row["tag_counts_json"] = json.dumps(
        dict(sorted(tag_counts.items())), ensure_ascii=False, separators=(",", ":")
    )

    if licence_elements == 0:
        row["licence_status"] = "NO_LICENCE_ELEMENT"
    elif targets_sorted and licence_elements_without_target:
        row["licence_status"] = "MIXED_DECLARATIONS"
    elif targets_sorted:
        row["licence_status"] = "DECLARED_TARGET"
    else:
        row["licence_status"] = "DECLARED_WITHOUT_TARGET"

    return row


def discover_xml_files(root: Path) -> list[Path]:
    """Return a deterministic list of regular XML files below root."""
    return sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file()
            and not path.is_symlink()
            and path.suffix.lower() == ".xml"
        ),
        key=lambda item: (
            item.relative_to(root).as_posix().casefold(),
            item.relative_to(root).as_posix(),
        ),
    )


def build_summary(source_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    parsed_rows = [row for row in rows if row["parse_status"] == "PARSED"]
    status_counts = Counter(row["parse_status"] for row in rows)
    licence_target_counts: Counter[str] = Counter()

    for row in parsed_rows:
        for target in json.loads(row["licence_targets_json"]):
            licence_target_counts[target] += 1

    return {
        "tool": "neer-nilam-epidoc-xml-audit",
        "tool_version": TOOL_VERSION,
        "source_id": source_id,
        "input_file_count": len(rows),
        "parsed_file_count": len(parsed_rows),
        "non_parsed_file_count": len(rows) - len(parsed_rows),
        "parse_status_counts": dict(sorted(status_counts.items())),
        "files_with_licence_target": sum(
            bool(json.loads(row["licence_targets_json"])) for row in parsed_rows
        ),
        "files_with_licence_element_without_target": sum(
            int(row["licence_elements_without_target"] or 0) > 0
            for row in parsed_rows
        ),
        "files_without_licence_element": sum(
            row["licence_status"] == "NO_LICENCE_ELEMENT" for row in parsed_rows
        ),
        "files_by_licence_target": dict(sorted(licence_target_counts.items())),
        "limitations": [
            "A declared licence URI is recorded as source metadata; it is not a legal determination or rights clearance.",
            "The source registry's DHARMA licence-reconciliation hold remains authoritative until resolved.",
            "The tool does not extract inscription text, names, historical dates, or place claims.",
            "The tool does not download schemas or contact the network, and it does not validate TEI/EpiDoc schema conformance.",
        ],
    }


def is_inside(candidate: Path, directory: Path) -> bool:
    try:
        candidate.relative_to(directory)
        return True
    except ValueError:
        return False


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Audit local EpiDoc XML technical metadata and declared licence targets. "
            "Input XML is read-only; no source text or derived claims are exported."
        )
    )
    parser.add_argument("--root", required=True, type=Path, help="Local corpus directory to scan")
    parser.add_argument("--source-id", required=True, help="Source-registry ID, e.g. SRC-DHARMA-TN")
    parser.add_argument("--csv", required=True, type=Path, help="Output CSV report path")
    parser.add_argument(
        "--summary-json",
        required=True,
        type=Path,
        help="Output aggregate JSON report path",
    )
    parser.add_argument(
        "--max-file-mib",
        type=int,
        default=32,
        help="Maximum XML size to parse (default: 32 MiB); larger files are hashed and flagged",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacement of existing report files (input files are never modified)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)

    try:
        root = args.root.expanduser().resolve(strict=True)
    except (OSError, RuntimeError):
        parser.error("The input root must exist and be accessible.")
    if not root.is_dir():
        parser.error("The input root must be a directory.")
    if not args.source_id.strip():
        parser.error("--source-id cannot be empty.")
    if args.max_file_mib < 1:
        parser.error("--max-file-mib must be at least 1.")

    csv_path = args.csv.expanduser().resolve()
    summary_path = args.summary_json.expanduser().resolve()
    if csv_path == summary_path:
        parser.error("CSV and summary output paths must be different.")
    if is_inside(csv_path, root) or is_inside(summary_path, root):
        parser.error("Report outputs must be outside the scanned corpus directory.")
    if not args.overwrite and (csv_path.exists() or summary_path.exists()):
        parser.error("An output report already exists; choose new paths or pass --overwrite.")

    max_file_bytes = args.max_file_mib * 1024 * 1024
    source_id = args.source_id.strip()
    rows = [
        scan_file(path, root, source_id, max_file_bytes)
        for path in discover_xml_files(root)
    ]
    summary = build_summary(source_id, rows)

    write_csv(csv_path, rows)
    write_summary(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if not rows:
        print("No XML files were found; check the input root.", file=sys.stderr)
        return 2
    if summary["non_parsed_file_count"]:
        print("One or more files need technical review; see the CSV report.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
