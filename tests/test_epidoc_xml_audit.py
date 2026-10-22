from __future__ import annotations

import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "scripts" / "epigraphy"),
)

from audit_epidoc_xml import build_summary, discover_xml_files, main, scan_file


TEI_FIXTURE = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"
     xml:lang="eng" xml:id="synthetic-fixture">
  <teiHeader>
    <fileDesc>
      <publicationStmt>
        <availability>
          <licence target="https://creativecommons.org/licenses/by-sa/4.0/">Synthetic fixture</licence>
        </availability>
      </publicationStmt>
    </fileDesc>
  </teiHeader>
  <text><body>
    <p><placeName>Invented Place</placeName><persName>Invented Person</persName></p>
    <origDate when="1900"/><gap/><unclear/><supplied/><choice/><lb/>
  </body></text>
</TEI>
"""


class EpidocXmlAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.base = Path(self.tempdir.name)
        self.root = self.base / "corpus"
        self.root.mkdir()

    def write(self, relative: str, content: bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_records_hash_namespace_and_structure_without_text(self) -> None:
        path = self.write("nested/sample.XML", TEI_FIXTURE)
        row = scan_file(path, self.root, "SRC-TEST", 1024 * 1024)

        self.assertEqual(row["parse_status"], "PARSED")
        self.assertEqual(row["source_id"], "SRC-TEST")
        self.assertEqual(row["relative_path"], "nested/sample.XML")
        self.assertEqual(row["sha256"], hashlib.sha256(TEI_FIXTURE).hexdigest())
        self.assertEqual(row["root_name"], "TEI")
        self.assertEqual(row["root_namespace"], "http://www.tei-c.org/ns/1.0")
        self.assertEqual(row["xml_lang"], "eng")
        self.assertEqual(row["xml_id"], "synthetic-fixture")
        self.assertEqual(
            json.loads(row["licence_targets_json"]),
            ["https://creativecommons.org/licenses/by-sa/4.0/"],
        )
        counts = json.loads(row["tag_counts_json"])
        self.assertEqual(counts["placeName"], 1)
        self.assertEqual(counts["persName"], 1)
        self.assertEqual(counts["origDate"], 1)
        self.assertEqual(counts["TEI"], 1)
        self.assertNotIn("Invented Place", json.dumps(row))

    def test_records_multiple_distinct_licence_targets(self) -> None:
        xml = TEI_FIXTURE.replace(
            b"</availability>",
            b'<licence target="https://creativecommons.org/licenses/by/4.0/">Other fixture</licence></availability>',
        )
        path = self.write("multi.xml", xml)
        row = scan_file(path, self.root, "SRC-TEST", 1024 * 1024)
        targets = json.loads(row["licence_targets_json"])

        self.assertEqual(len(targets), 2)
        self.assertEqual(targets, sorted(targets))
        self.assertEqual(row["licence_status"], "DECLARED_TARGET")

    def test_flags_licence_element_without_target(self) -> None:
        xml = TEI_FIXTURE.replace(
            b'<licence target="https://creativecommons.org/licenses/by-sa/4.0/">Synthetic fixture</licence>',
            b"<licence>Unlinked declaration</licence>",
        )
        path = self.write("no-target.xml", xml)
        row = scan_file(path, self.root, "SRC-TEST", 1024 * 1024)

        self.assertEqual(row["parse_status"], "PARSED")
        self.assertEqual(row["licence_status"], "DECLARED_WITHOUT_TARGET")
        self.assertEqual(row["licence_elements_without_target"], 1)

    def test_flags_document_without_licence_element(self) -> None:
        xml = TEI_FIXTURE.replace(
            b'<availability>\n          <licence target="https://creativecommons.org/licenses/by-sa/4.0/">Synthetic fixture</licence>\n        </availability>',
            b"<availability />",
        )
        path = self.write("no-licence.xml", xml)
        row = scan_file(path, self.root, "SRC-TEST", 1024 * 1024)

        self.assertEqual(row["parse_status"], "PARSED")
        self.assertEqual(row["licence_status"], "NO_LICENCE_ELEMENT")

    def test_malformed_xml_is_reported_not_silently_skipped(self) -> None:
        path = self.write("broken.xml", b"<TEI><text></TEI>")
        row = scan_file(path, self.root, "SRC-TEST", 1024 * 1024)

        self.assertEqual(row["parse_status"], "XML_PARSE_ERROR")
        self.assertNotEqual(row["sha256"], "")

    def test_custom_entity_declaration_is_rejected_before_parse(self) -> None:
        xml = b'<!DOCTYPE TEI [<!ENTITY x "expanded">]><TEI>&x;</TEI>'
        path = self.write("entity.xml", xml)
        row = scan_file(path, self.root, "SRC-TEST", 1024 * 1024)

        self.assertEqual(row["parse_status"], "UNSAFE_ENTITY_DECLARATION")
        self.assertEqual(row["licence_status"], "NOT_ASSESSED")

    def test_oversized_file_is_hashed_and_flagged(self) -> None:
        content = b"<TEI>synthetic large fixture</TEI>"
        path = self.write("large.xml", content)
        row = scan_file(path, self.root, "SRC-TEST", 10)

        self.assertEqual(row["parse_status"], "FILE_TOO_LARGE")
        self.assertEqual(row["sha256"], hashlib.sha256(content).hexdigest())

    def test_summary_counts_each_file_per_declared_target(self) -> None:
        first = scan_file(self.write("a.xml", TEI_FIXTURE), self.root, "SRC-TEST", 1024 * 1024)
        changed_fixture = TEI_FIXTURE.replace(
            b"https://creativecommons.org/licenses/by-sa/4.0/",
            b"https://creativecommons.org/licenses/by/4.0/",
        )
        second = scan_file(self.write("b.xml", changed_fixture), self.root, "SRC-TEST", 1024 * 1024)
        summary = build_summary("SRC-TEST", [first, second])

        self.assertEqual(summary["input_file_count"], 2)
        self.assertEqual(summary["parsed_file_count"], 2)
        self.assertEqual(
            summary["files_by_licence_target"],
            {
                "https://creativecommons.org/licenses/by-sa/4.0/": 1,
                "https://creativecommons.org/licenses/by/4.0/": 1,
            },
        )
        self.assertTrue(any("not a legal determination" in item for item in summary["limitations"]))

    def test_discovery_is_recursive_case_insensitive_and_sorted(self) -> None:
        self.write("z.xml", TEI_FIXTURE)
        self.write("folder/A.XML", TEI_FIXTURE)
        self.write("ignore.txt", TEI_FIXTURE)
        paths = [path.relative_to(self.root).as_posix() for path in discover_xml_files(self.root)]

        self.assertEqual(paths, ["folder/A.XML", "z.xml"])

    def test_cli_writes_csv_and_summary_outside_input_root(self) -> None:
        self.write("one.xml", TEI_FIXTURE)
        csv_path = self.base / "reports" / "audit.csv"
        json_path = self.base / "reports" / "summary.json"

        code = main([
            "--root", str(self.root),
            "--source-id", "SRC-TEST",
            "--csv", str(csv_path),
            "--summary-json", str(json_path),
        ])

        self.assertEqual(code, 0)
        with csv_path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        summary = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual(len(rows), 1)
        self.assertEqual(summary["source_id"], "SRC-TEST")
        self.assertEqual(summary["parsed_file_count"], 1)

    def test_cli_returns_nonzero_when_a_file_needs_technical_review(self) -> None:
        self.write("good.xml", TEI_FIXTURE)
        self.write("broken.xml", b"<TEI><broken>")
        csv_path = self.base / "report.csv"
        json_path = self.base / "summary.json"

        code = main([
            "--root", str(self.root),
            "--source-id", "SRC-TEST",
            "--csv", str(csv_path),
            "--summary-json", str(json_path),
        ])

        self.assertEqual(code, 1)
        summary = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual(summary["non_parsed_file_count"], 1)

    def test_cli_rejects_report_paths_inside_input_corpus(self) -> None:
        with self.assertRaises(SystemExit) as caught:
            main([
                "--root", str(self.root),
                "--source-id", "SRC-TEST",
                "--csv", str(self.root / "report.csv"),
                "--summary-json", str(self.base / "summary.json"),
            ])

        self.assertEqual(caught.exception.code, 2)

    def test_cli_does_not_overwrite_existing_reports_without_flag(self) -> None:
        self.write("one.xml", TEI_FIXTURE)
        csv_path = self.base / "existing.csv"
        json_path = self.base / "existing.json"
        csv_path.write_text("keep", encoding="utf-8")
        json_path.write_text("keep", encoding="utf-8")

        with self.assertRaises(SystemExit) as caught:
            main([
                "--root", str(self.root),
                "--source-id", "SRC-TEST",
                "--csv", str(csv_path),
                "--summary-json", str(json_path),
            ])

        self.assertEqual(caught.exception.code, 2)
        self.assertEqual(csv_path.read_text(encoding="utf-8"), "keep")
        self.assertEqual(json_path.read_text(encoding="utf-8"), "keep")

    def test_cli_empty_directory_returns_explicit_failure(self) -> None:
        csv_path = self.base / "empty.csv"
        json_path = self.base / "empty.json"

        code = main([
            "--root", str(self.root),
            "--source-id", "SRC-TEST",
            "--csv", str(csv_path),
            "--summary-json", str(json_path),
        ])

        self.assertEqual(code, 2)
        self.assertEqual(json.loads(json_path.read_text(encoding="utf-8"))["input_file_count"], 0)


if __name__ == "__main__":
    unittest.main()
