# CGWB Tamil Nadu–Puducherry Groundwater Year Book 2024–2025 — Access Review

**Review date:** 2026-10-10  
**Dataset ID:** DLA-021 (cross-reference DLA-020 in the critical-session log)  
**Status:** Official publication listing confirmed; PDF acquisition and rights review remain open.

## Official catalogue evidence

The Central Ground Water Board (CGWB), Ministry of Jal Shakti, lists the publication:

- **Title shown in catalogue:** Groundwater Year Book, Tamilnadu UT of Puducherry (2024 - 2025)
- **Catalogue record:** https://cgwb.gov.in/cgwbpnm/public/publication-detail/2023
- **Tamil Nadu yearbook search:** https://cgwb.gov.in/cgwbpnm/search?cat_id=4&search=search&state_id=33&type=2
- **Related official monitoring page:** https://www.cgwb.gov.in/ground-water-level-monitoring
- **Catalogue metadata found in the current search result:** author CGWB; year of issue 2026. The public catalogue listing was shown as posted on 25 March 2026. Catalogue counters are dynamic and are not evidence of file validity.

The catalogue record is sufficient to establish that the yearbook is officially listed. It does **not** establish that a downloadable response is a valid PDF or that any particular redistribution licence applies.

## Previous local acquisition failure

The 10 October 2026 critical-session log records two failed attempts for DLA-021/DLA-020. The attempted URLs were:

- https://cgwb.gov.in/cgwbpnm/public/download/2023
- https://cgwb.gov.in/cgwbpnm/public/media

The collector reported that the returned payload was not a valid PDF and preserved the invalid/partial responses under the Seagate quarantine folder. The files must remain quarantined until a successful acquisition has been independently validated. They are not yearbook assets.

## Required acquisition and validation steps

1. Open the official catalogue record above and use its **Download** action in a normal browser session.
2. Save the response to a temporary filename outside the canonical yearbook path first. Do not trust the extension or HTTP status alone.
3. Confirm PDF magic bytes `%PDF-`, a plausible non-trivial file size, successful PDF parsing, and a document title/year matching the 2024–2025 Tamil Nadu–Puducherry groundwater yearbook. Confirm the relevant contents, reporting period, station/district coverage, tables, methods and page numbering.
4. If the link returns HTML, a login/interstitial page, an error document, or a partial transfer, preserve it under quarantine with a timestamp and record the response URL/status. Do not overwrite a previously validated file.
5. Only after validation, place the PDF at `01_RAW_DATA/05_GROUNDWATER/CGWB/Groundwater-Year-Book-Tamil-Nadu-Puducherry-2024-2025.pdf`, calculate SHA-256 and size, and append a new acquisition manifest/audit row.
6. Review document-specific terms and attribution before extracting or republishing tables. Do not upload the full PDF to the public GitHub repository without rights review.

## Interpretation constraints

This is a modern groundwater observation source. It may provide contemporary environmental context for the Thanjavur–Cauvery pilot; it is not direct evidence of Chola-era groundwater levels. Preserve dates, station IDs, units, methods, report/table/page locators, and uncertainty for any downstream use.

## Evidence status

- Official catalogue listing: **CONFIRMED**
- Direct PDF endpoint: **NOT YET CONFIRMED**
- Local PDF acquisition: **NOT ACQUIRED**
- PDF content validation: **PENDING**
- Rights/redistribution determination: **PENDING**
