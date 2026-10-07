# Neer-Nilam — Stage 1 Validation 001

Date: 2026-10-07
Status: PARTIAL VALIDATION — physical hardware decision not yet final

## Purpose

Validate the Stage 1 physical-presentation report against current primary/technical sources before any hardware purchase.

## Executive result

The Stage 1 strategy is directionally sound, but several statements must be corrected before becoming engineering requirements.

Current gate:

**NO EXPENSIVE HARDWARE PURCHASE.**

The strongest immediate path remains:

**software-first → low-cost Pepper's Ghost optical proof → compare against projection-mapped physical relief → only then approve a Tier B cabinet.**

Pepper's Ghost remains a candidate, not a confirmed final display architecture.

## Findings

### 1. Pepper's Ghost principle is confirmed, but some wording in Stage 1 was too absolute

Current technical/educational references confirm the standard arrangement uses a semi-transparent/semi-reflective surface around 45°, with a dark/background-controlled environment to make the reflected image visible. The effect is a reflection/transmission illusion rather than a true free-space volume. [W108, W109, W112, W113]

Correction:

- Keep the 45° geometry as the starting hypothesis.
- Keep the dark hood/background requirement.
- Do not state that dark pixels literally create transparency. Better wording: dark image regions contribute little reflected display light, so they do not reliably provide an opaque/filled visual layer against whatever is visible through the beamsplitter.
- Do not use transparency/fade alone to encode uncertainty.
- A single-view Pepper's Ghost setup does not provide normal multi-view motion parallax.

### 2. The Stage 1 "~8% per surface" acrylic reflection figure is NOT a safe design requirement

The exact reflection/transmission of a beamsplitter depends on substrate, coating, angle, wavelength, polarization and construction. Thorlabs currently offers coated plate beamsplitters optimized for 45° with explicit 10:90, 30:70, 50:50, 70:30 and 90:10 split ratios; wedged back surfaces are used to reduce unwanted ghost reflections. [W111]

Correction:

**REMOVE the generic "~8% per surface" figure from the engineering specification.**

For Test 2, compare:
1. clear acrylic
2. clear glass
3. commercial two-way mirror acrylic/film
4. a purpose-built beamsplitter if affordable

Record actual visible brightness, double-image artifacts, haze and viewing angle.

### 3. 45° does NOT by itself guarantee final image position/scale

45° is the starting optical geometry, but the virtual image position and practical cabinet dimensions depend on the physical relationship among display, reflector, viewer and scene. Educational and academic sources support the 45° arrangement, but the final geometry still needs calibration. [W108, W109, W114]

Correction:

Treat all Stage 1 cabinet dimensions as prototypes, not production dimensions.

### 4. Looking Glass Light Field is more capable than an older Stage 1 extract suggested

Current Looking Glass product information lists the 16" Light Field Display at **US$3,000**, with 4K resolution, 60 Hz, up to 100 views and a **60° optimal viewing cone**. The company also documents WebXR, custom renderer integration and current software support. [W122, W131, W132, W133]

Correction:

The report's approximately ₹3.5 lakh figure is not a direct current product price. At the report's assumed ₹87/USD, US$3,000 is about ₹2.61 lakh before import taxes and duties. Final landed India cost remains UNKNOWN until a vendor quote.

This makes Light Field a credible borrowed/rented comparison candidate, but not an immediate purchase.

### 5. Looking Glass WebXR compatibility direction is credible

Looking Glass currently documents WebXR and custom renderer/Bridge workflows, and its tooling explicitly supports web-based 3D workflows. [W131, W132]

Correction:

Keep React + Three.js/R3F as the first software renderer. Before purchase, run a compatibility test using the exact project versions.

### 6. HLD is NOT accurately described as "video only"

This is an important correction.

Looking Glass currently describes HLD as a hybrid display with a fixed holographic depth layer. Its official material allows content to originate from video, images and supported 3D assets, and lists Unity/Unreal among optional creation workflows. Deployment is still centered on prepared playback media rather than a normal live light-field 3D viewport. [W126, W128, W129]

Correction:

Do not say "HLD cannot use 3D."

Use:

> **HLD can present spatialized prepared media and supported 3D-origin content, but it is not the same kind of live, multi-view, interactive 3D display architecture we need as the primary Neer-Nilam scene client.**

HLD remains a poor fit for the first build because the project needs live scene-state interaction, source-aware object selection and evidence-driven state changes.

### 7. Transparent OLED specification is broadly verified, but price is not

LG India currently lists the 55EW5P at FHD 1920×1080, 200/600 nit brightness depending on APL, 43% transparency, 178° viewing angle and 120 Hz refresh. [W123]

Correction:

Keep the technical specification.

Remove any implication that ₹15 lakh+ is a verified current India price. The current LG India page is a contact/sales route, not a public India price.

### 8. Samsung Odyssey 3D is officially available in India

Samsung India currently lists the Odyssey 3D G90XF as a 27" 4K IPS monitor with 350 cd/m² typical brightness, 165 Hz refresh, eye tracking and view mapping. Samsung India also published a launch price of ₹1,27,299. [W136, W137]

Correction:

This product is real and locally available, but its strategic fit is weaker than a shared-view installation because its 3D experience depends on tracked viewing. It should not be called "bad technology"; it is simply not the primary shared-display architecture for Neer-Nilam.

### 9. Sony ELF-SR2 is still a real Indian product path, but the ₹7 lakh figure is not current evidence

Sony India currently documents the ELF-SR2 as a 27" glasses-free spatial display with 400 nit brightness and eye tracking. Sony India's current support materials include a 2026 operating manual. [W138, W139, W140]

Correction:

Treat ₹7,00,000 as a historical/secondary price reference only. Current India price remains UNKNOWN until Sony/distributor quotation.

### 10. Voxon VX2 specifications are current, but the current official page does not establish the earlier quoted price

Voxon's current official product page confirms a 256 mm diameter × 256 mm tall display volume, 30 volumes/s, 8 million voxels, Windows PC connectivity and Unity/C/C++ SDK options. [W121]

Correction:

Keep the physical-volume objection. Mark the previously cited US$6,800 price as **UNVERIFIED CURRENT PRICE** unless confirmed from a current purchase quote/page.

### 11. Projection mapping on a physical relief is a serious competitor and was under-researched

This is the largest Stage 1 gap.

Academic museum work has demonstrated interactive projection mapping onto 3D-printed historical-settlement models, including tangible controls and iterative museum evaluation. Another heritage exhibition study describes projection mapping on physical cultural objects for concurrent audience engagement. [W116, W117]

A current Indian case-study source also describes a relief map used to present Shahjahanabad through mapped animation, including monument outlines, streets, water channels and bilingual interpretation. [W120]

Correction:

**Projection mapping on a physical relief must remain a live Tier-B candidate.**

It should receive its own proof test rather than being deferred.

### 12. Bright 27" 4K panels are technically available

Current manufacturer material shows 27" 4K displays with approximately 1000 nit-class peak/SDR/HDR brightness exist, including ASUS ProArt OLED models in India and Philips professional mini-LED documentation. [W151, W153, W154]

Correction:

The report is correct that monitor brightness is a major optical risk. However, "bright 27-inch 4K" should not become a specific purchase until the exact panel, coating, heat, mounting orientation and reflected-image performance are tested.

## Revised Stage 1 conclusion

### Keep

- Do not purchase an expensive exotic display yet.
- Build the scene system first.
- Keep a plain-screen fallback.
- Use physical controls as the default exhibition interaction hypothesis.
- Keep evidence text outside the ghost image.
- Keep the renderer presentation-neutral.
- Use discrete, evidence-supported historical states.
- Keep React + Three.js/R3F for the first software proof.
- Use a low-cost physical optical proof before cabinet fabrication.

### Change

1. Replace "Pepper's Ghost is the final display choice" with "Pepper's Ghost is the leading physical prototype candidate."
2. Replace the generic 8% reflection assumption with measured/commercial beamsplitter performance.
3. Treat projection-mapped relief as a first-class competitor.
4. Correct the HLD description.
5. Update Looking Glass current figures.
6. Separate current product price from historical/secondary pricing.
7. Treat all cabinet dimensions as provisional until Test 2 measurement.
8. Do not claim accessibility compliance from a single reach-height number.

## New validation gate

Before approving the Tier-B cabinet, complete:

**Gate A — Software proof**
- historical states
- unsupported period
- evidence panel
- local scene pack
- flat fallback

**Gate B — Pepper's Ghost optical proof**
- 45° starting geometry
- at least two reflector materials
- measured brightness/readability
- double-image check
- viewing-angle check

**Gate C — Relief projection comparison**
- same historical content
- same physical footprint target
- same interaction hardware
- compare visitor comprehension and impact

**Gate D — Interaction**
- encoder
- three buttons
- touch evidence
- measured event-to-visible-response latency

**Gate E — Exhibition robustness**
- 4-hour soak
- forced-kill recovery
- power loss/restart
- local/offline operation

## Current status

**Physical architecture:** OPEN — Pepper's Ghost leading prototype candidate; projection-mapped relief added as a serious alternative.

**Purchase:** BLOCKED until proof gates.

**Software architecture:** PROPOSED — React + Three.js/R3F, presentation-neutral scene pack.

**Canonical decision register:** D001–D017 remain historical working/proposed decisions. The Stage 1 report's "D-001" is not a new canonical decision ID.

## Immediate next engineering step

Start **Gate A — Software-only proof**.

No display purchase.

