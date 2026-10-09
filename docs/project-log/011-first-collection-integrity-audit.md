# Project Log 011 — First Collection Integrity Audit Passed

Date: 2026-10-09
Status: File-integrity checks passed; epigraphy rights review remains open

## Verified from the user's PowerShell output

The user ran the read-only audit against collection run `20261009-111437`.

### Collection event log

Counts in `06_logs\collection-20261009-111437.jsonl`:
- BEGIN: 1
- DOWNLOADED: 4
- CHECKSUM: 1
- EXTRACTED: 1
- GENERATED: 2
- COMPLETE: 1

The audit found no `FAILED`, `BLOCKED`, `PARTIAL_RETAINED`, `REVIEW_REQUIRED`, or `CHECKSUM_FAILED` events in this run log.

### SHA-256 file integrity

- Checksum-manifest rows: 581
- Hashes verified against present files: 581
- Missing files: 0
- Hash mismatches: 0

This verifies that the 581 files included in the generated manifest match their recorded hashes at audit time. It does not establish historical accuracy, completeness of the source datasets, or correctness of source metadata.

### Epigraphy XML licence inventory

- Total XML inventory rows: 553
- `REVIEW_EACH_RECORD`: 507
- `UNDECLARED_REVIEW_REQUIRED`: 46

The 507 rows had one or more licence target declarations detected by the collector; each record still requires record-level rights review. The 46 rows had no matching XML licence target found by the collector and remain explicitly unresolved. Do not redistribute, republish, train on, or treat these records as rights-cleared until their terms and required attribution/share-alike obligations are examined.

## Interpretation

The first local collection and initial integrity audit succeeded. The correct status is **raw files collected and checksummed; rights and scientific review pending**, not “fully validated data lake.”

OSM remains a current mapped-geography extract and HydroRIVERS a generalized modern network. Neither should be treated as direct historical proof. The two DHARMA repositories must remain linked to their recorded commit SHAs; raw snapshots should not be silently updated after downstream records are built.

## Next action

Produce a licence-review summary from the inventory that:
1. groups rows by exact `licence_url` value and repository;
2. lists all 46 undeclared rows for review;
3. inspects representative XML metadata and source documentation for ambiguous entries;
4. records a human-reviewed disposition separately from the raw inventory.

After rights triage, build a scoped Brihadisvara evidence slice and preserve source → evidence → entity → historical state → scene-pack provenance. Do not bulk-normalize or assume every downloaded record is usable.

## Project direction

Continue software-first data-lake work following the guidance relayed after pitching to Judy ma'am. She is exploring a path for physical representation; the implementation choice remains open.
