# Project Log 012 — DHARMA Repository and XML Licence Discrepancy

Date: 2026-10-09
Status: Discrepancy confirmed in the collected snapshots; rights clarification required before downstream reuse

## Local inventory results

The user's local summary grouped 553 XML files into four repository/licence groups:

| Repository snapshot | XML declares CC BY-SA 4.0 | No `licence target` detected |
|---|---:|---:|
| DHARMA Tamil Nadu | 340 | 16 |
| DHARMA South Indian Inscriptions | 167 | 30 |
| **Total** | **507** | **46** |

The collector's inventory regex identifies XML `<licence target="…">` declarations. “No declaration detected” means the collector did not find a matching tag; it is not, by itself, a legal conclusion that no licence applies.

## Repository-level conflict verified against exact collected commits

The two collected repository README files state that edited XML in their repository is available under CC BY 4.0:
- DHARMA Tamil Nadu snapshot commit: `ab94f9e525e2ce21938e63ac93fd80aa78a4e423`
- DHARMA SII snapshot commit: `dfa95be6729f162c0e7b70eea15c51da94520ff4`

At those exact snapshots, an inspected Tamil Nadu XML (`DHARMA_INSTamilNadu00031.xml`) and an inspected SII XML (`DHARMA_INStfaSIIv05p1i0228.xml`) have `<licence target="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</licence>`. A sampled Tamil Nadu record (`DHARMA_INSTamilNadu00192.xml`) had no licence target detected by the current inventory approach.

Relevant upstream references:
- Tamil Nadu README at collected commit: https://github.com/erc-dharma/tfa-tamilnadu-epigraphy/blob/ab94f9e525e2ce21938e63ac93fd80aa78a4e423/README.md
- SII README at collected commit: https://github.com/erc-dharma/tfa-sii-epigraphy/blob/dfa95be6729f162c0e7b70eea15c51da94520ff4/README.md
- Tamil Nadu XML sample: https://github.com/erc-dharma/tfa-tamilnadu-epigraphy/blob/ab94f9e525e2ce21938e63ac93fd80aa78a4e423/DHARMA_INSTamilNadu00031.xml
- SII XML sample: https://github.com/erc-dharma/tfa-sii-epigraphy/blob/dfa95be6729f162c0e7b70eea15c51da94520ff4/DHARMA_INStfaSIIv05p1i0228.xml
- Tamil Nadu no-tag sample: https://github.com/erc-dharma/tfa-tamilnadu-epigraphy/blob/ab94f9e525e2ce21938e63ac93fd80aa78a4e423/DHARMA_INSTamilNadu00192.xml

This is a real metadata discrepancy: the README declares CC BY 4.0 for the edited XML collection, whereas many per-file TEI metadata records declare CC BY-SA 4.0. The current inventory also reports no licence tag in 46 files. The project should not decide on its own that one declaration overrides the other.

## Decision and risk control

- Keep the raw repository snapshots and their exact commit SHAs unchanged for provenance and local inspection.
- Do not redistribute the full snapshots, publish copied XML, or incorporate record text into reusable/public derived products until the conflict is resolved.
- Preserve attribution requirements from the README in the meantime, without treating attribution alone as rights clearance.
- Ask the DHARMA maintainers to clarify the governing licence for the specific XML records, how missing `licence target` records should be treated, and whether record-level CC BY-SA declarations are intentional/current.
- Store the response and date in the source registry. Do not silently rewrite the original licence inventory; create a separately reviewed disposition table after clarification.
- Update the source registry and acquisition manifest to mark both corpora as `HOLD_LICENSE_RECONCILIATION` / `COLLECTED_HOLD_REUSE_REVIEW`.

## Next step

Prepare an audit packet for maintainers: exact repository URL, snapshot commit, the 507/46 counts, representative filenames, README wording, per-file licence URIs, and a request for written clarification. Continue only non-public local research/technical inspection until rights are reconciled. Then proceed to source-linked, evidence-scoped Brihadisvara records with attribution and confidence; modern OSM/HydroRIVERS remain contextual rather than direct historical evidence.
