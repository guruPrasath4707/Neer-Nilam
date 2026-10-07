# Project Log 003 — Stage 1 Display Report Archived + Validation Started

Date: 2026-10-07
Status: Stage 1 validation in progress

## What happened

The team supplied the full external Stage 1 physical-presentation report.

The report was archived unchanged as:

docs/research/display/001-stage1-physical-presentation-decision.md

The report remains explicitly marked as **INPUT TO VALIDATION**, not a final hardware decision.

## Repository bookkeeping

The report proposed decision ID "D-001". The canonical Neer-Nilam decision register already contains D001–D017, so the report ID is not treated as a new canonical decision.

D018 was added:

> Do not purchase an expensive physical display before low-cost proof gates validate the presentation geometry and experience.

Status: Proposed.

## Validation work started

Current-source validation was performed for:

- Pepper's Ghost optics
- commercial beamsplitter specifications
- Looking Glass Light Field
- Looking Glass HLD
- LG transparent OLED
- Samsung Odyssey 3D
- Sony ELF-SR2
- Voxon VX2
- projection mapping on physical relief models
- high-brightness 27-inch display availability

## Important validation corrections

1. The generic "~8% per surface" reflector number is not acceptable as an engineering requirement. Actual beamsplitter behavior depends on optic/coating/angle and must be tested.
2. Pepper's Ghost remains the leading low-cost physical candidate, but not a final decision.
3. Projection-mapped physical relief is a serious Tier-B competitor and must receive its own proof test.
4. HLD is more capable than the original report stated: Looking Glass documents video, images and supported 3D-origin content, but its deployed workflow is media/playback oriented rather than the live multi-view scene client desired here.
5. Current Looking Glass 16-inch Light Field pricing/specification was rechecked from the manufacturer and differs from some older secondary-source figures.
6. LG, Samsung, Sony and Voxon specifications were rechecked against current manufacturer material where available.
7. Hardware purchase remains blocked.

## Current gate

Next engineering gate:

**Gate A — software-only proof**

No new display purchase.

## Source tracking

Every new website/page visited during validation was assigned a new W-ID in docs/sources/WEBSITE_INDEX.md, continuing from the Stage 1 report's W007–W107 through W166.
