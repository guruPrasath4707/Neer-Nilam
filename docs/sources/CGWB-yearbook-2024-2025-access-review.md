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


## Follow-up lookup — 2026-10-12

A fresh search-index result from the official CGWB publications repository reconfirms the exact listing title **“Groundwater Year Book, Tamilnadu UT of Puducherry (2024 - 2025)”**, year of issue 2026, state Tamil Nadu, and a district listing that includes Thanjavur. The official state-filtered results also list the 2023–2024 Ground Water Year Book as a separate older item. These are catalogue metadata observations only; a download counter and a visible “Download” label are not evidence that a valid PDF was retrieved.

An automated direct-open attempt against the official publication-detail page returned **502 Bad Gateway** in this check. The search-index result did not expose a verified final PDF URL or PDF bytes. This does not establish what a normal browser session on the operator's Windows machine will receive. No file was acquired, validated, moved from quarantine, or registered. Next step remains a normal browser click on the exact 2024–2025 catalogue item's Download control with DevTools Network capture enabled.

Reference URLs:
- Official record: https://cgwb.gov.in/cgwbpnm/public/publication-detail/2023
- Official Tamil Nadu yearbook search: https://cgwb.gov.in/cgwbpnm/search?cat_id=4&search=search&state_id=33&type=2


## Follow-up catalogue check — 2026-10-13

A fresh public search-index check still lists **“Groundwater Year Book, Tamilnadu UT of Puducherry (2024 - 2025)”** in the official CGWB publications repository. The record continues to identify Tamil Nadu and includes Thanjavur in its district metadata. The official state-filtered result also displays this 2024–2025 yearbook separately from the older 2023–2024 edition. These observations reconfirm catalogue discovery only.

A direct open of the official publication-detail URL again returned **502 Bad Gateway** through the automated page-fetch path. No verified final PDF download URL, response bytes, or completed browser download were obtained. Search snippets expose the listing and a Download label, but not the actual downloadable PDF resource. No local file, PDF signature, page count, title page, content coverage or SHA-256 was examined by this recheck.

Disposition remains **NOT ACQUIRED / PENDING**. Do not create a checksum/manifest row for an unacquired PDF, promote quarantined error payloads, or treat Thanjavur's presence in catalogue metadata as proof that the report contains pilot-relevant well observations. The next evidence-bearing step remains a normal browser click on the exact item's Download control with DevTools Network capture enabled.

Official links:
- https://cgwb.gov.in/cgwbpnm/public/publication-detail/2023
- https://cgwb.gov.in/cgwbpnm/search?cat_id=4&search=search&state_id=33&type=2
