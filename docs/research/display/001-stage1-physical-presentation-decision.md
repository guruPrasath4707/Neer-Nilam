# Neer-Nilam — Stage 1: Physical Presentation Decision

Date: 2026-10-07 · Status: INPUT TO VALIDATION (not a final decision) · Proposed decision ID: D-001

Method note: every number below comes from search-result extracts (not full page reads) unless marked *engineering estimate*. Prices are the seller's currency; INR conversions use an **assumed ₹87/USD, before duty/GST — vendor quote required**.

---

## 1. Verdict

1. **Do not buy any display yet.** Every exotic option costs ₹1.3 lakh to ₹30+ lakh and none has been shown to pass your own experience test.

2. **Build the scene system first and run it on a plain monitor.** That is the real asset, and it is also your permanent fallback.

3. **First physical build: a Pepper's-Ghost-style cabinet on a bright 27" monitor, gated by a ₹3–12k cardboard proof.** The ghost layer shows monument + terrain + water + state. **Evidence text goes on a separate ordinary touch screen**, not in the ghost.

4. **Light-field (Looking Glass), eye-tracked (Sony/Samsung) and transparent OLED are Tier C**: rent or borrow a unit for one day before buying.

5. **Reject for this project:** LED fans, hologram-box "pyramids", Hololuminescent (HLD) displays, volumetric (Voxon). Reasons in §3.

6. **Stay in React + Three.js / R3F.** Looking Glass supports it via WebXR (W064–W067), so a future display swap needs no second engine. Unity/Unreal are not justified yet.

---

## 2. What the display must satisfy (derived from your experience test)

| Need | Consequence for display choice |
|---|---|
| Temple + terrain + water in one view | Wide, bright 3D-ish scene; some depth cue helps, true volume not required |
| Time selector with discrete states | Rotary control + a visible "no supported state" screen |
| Evidence, source, confidence | **Needs readable text** → dense text cannot live on a floating/ghost layer |
| Known vs reconstructed vs uncertain | Visual grammar must work on the chosen optics (see §7) |
| Offline, student budget, small team | Commodity parts, same renderer on fallback screen |

**Two physics facts that decide a lot** (general optics/engineering knowledge, not tied to one source):

- A Pepper's Ghost reflection is **additive light**. Black = nothing = see-through. You cannot draw shadows, dark fills, or "faded = transparent" uncertainty. The usual "more transparent = less certain" idea **fails here**; use line style and hatching instead.

- A Pepper's Ghost (and any flat panel image) has **no motion parallax**. The depth you get is apparent depth, from the dark chamber and any physical props. Do not call it 3D to the audience.

---

## 3. Technology comparison

Legend: ● good ◐ partial ○ poor. "Text" = can it show readable evidence panels.

| # | Technology | Principle | Real depth / parallax | Viewers | Room light | Text | Neer-Nilam fit | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | **Pepper's Ghost / beamsplitter** | Monitor reflected in 45° glass/film (W045, W049, W052) | Apparent depth only, no parallax | Many, front arc | ○ needs dim hood | ◐ | Good for monument+terrain+water diorama | **Tier A/B, after optical proof** |
| 2 | Holographic pyramid | Four-sided reflection of one panel | Apparent only | 360° but small image | ○ | ○ | Poor: tiny image, scene is directional | Reject |
| 3 | Transparent OLED | Self-emissive see-through panel; LG 55" FHD, 38–43% transparency, 200/600–400 nits listed (W027, W031) | Apparent, shows real object behind | Many, wide (178° listed) | ◐ | ● | Excellent over a physical model; ₹ out of reach | Tier C/D, vendor quote |
| 4 | Transparent LCD box | LCD with open backlight; LG itself cites ~10% for LCD vs 38% OLED (W031); 21.5" box products exist (W103) | Apparent | Many | ◐ | ● | Small; can hold a prop + overlay | Optional small variant |
| 5 | LED holographic fan | Spinning LED blades, persistence of vision; ~640×640 class, 224 LEDs on a 42 cm unit (W040); ₹9,999–12,500 (W038, W041) | Floating 2D | Many | ○ weak in light | ○ | Wrong: low-res, moving blades, safety | Attract-loop only, no |
| 6 | Projection mapping (flat) | Projector on surface | None | Many | ○ dark room | ◐ | Not stated here: **not researched this session** | Defer |
| 7 | **Projection mapping on physical relief model** | Projector paints a terrain/temple model | Real physical depth | Many, all angles | ○ dark room | ○ | Strong for water/land/time *layers*; cannot change building geometry between states | **Candidate Tier B alt; not researched for products** |
| 8 | Light-field display (Looking Glass) | 45–100 views through lenticular optics, no headset (W012, W013) | Real parallax, ~53° cone on 32" (W015) | Multiple | ◐ | ○ detail split across views | Great depth, small size, text weak | Tier C; rent first |
| 9 | Volumetric (Voxon VX2) | Swept LED volume 256×256 mm, 8 M voxels, 30 vols/s, US$6,800 ex-duty (W088) | True volume | 360° | ○ | ○ | Volume too small for a landscape; moving parts | Reject |
| 10 | Eye-tracked spatial (Sony ELF-SR2, Samsung Odyssey 3D) | Lenticular + face tracking; 4K 27" (W018, W097) | True stereo for tracked viewer | 1–2 | ◐ | ◐ | Sony needs RTX 2070 Super-class PC (W022); Samsung 3D runs through its Windows app, SBS input (W092, W099) | Reject for exhibition |
| 11 | **HLD (Looking Glass Hololuminescent)** | Fixed holographic volume inside the stack, shows 2D video with depth (W071, W077, W080) | Fixed, not a live 3D scene | Many | ● | ○ | It plays video; it does not render your scene | Reject |
| 12 | VR headset (Quest 3/3S) | Stereo HMD; US$349.99 (3S 128 GB) after Apr 2026 hike (W063) | Full | 1 | ● | ● | Not a shared installation; India official channel UNKNOWN | Side-demo only |
| 13 | AR / MR | Phone or headset overlay | Full | 1 each | ● | ● | Good later as a second client; not the first install | Post-MVP |
| 14 | **Plain 4K screen** | Ordinary monitor/TV | Rendered depth cues only | Many | ● | ● | Where the evidence UI lives; permanent fallback | **Always built** |
| 15 | Hybrid: ghost + physical prop | Ghost image over a laser-cut/printed terrain relief | Real parallax from prop | Many | ○ | ◐ | Strongest cheap depth cue; tests the "is it a gimmick" question | **Test 2b** |

Items not source-verified this session: projection mapping products, depth cameras, hand-tracking SDKs, Unity/Unreal licensing, Apple Vision Pro, HYPERVSN, Holoxica, pyramid products. Labelled UNKNOWN until a Stage 1b pass.

---

## 4. Real products worth investigating

| Product | Maker | Key facts | Price evidence | India | Role |
|---|---|---|---|---|---|
| Spatial Display 16" | Looking Glass | 4K, 45–100 views, Unity/Unreal/Blender/WebXR plugins (W012, W013) | From US$4,000 (US$3,000 limited promo, 2024) | UNKNOWN: VENDOR CONFIRMATION REQUIRED | Tier C rental/trial |
| 27" Light Field Display | Looking Glass | 4K, 100+ views (W011) | US$10,000 list at Apr 2025 launch | UNKNOWN | Too costly |
| HLD 16" / 27" / 86" | Looking Glass | Ships May/June 2026 per vendor page (W077) | US$2,000 (16"), US$20,000 (86") (W077, W078) | UNKNOWN | Rejected for fit, still listed |
| ELF-SR2 | Sony | 27", 4K, eye tracking, 14 ms response (W018), PC: i5 6-core + RTX 2070 Super-class (W022) | ₹7,00,000 (Croma article, launch era, W017); US$5,000 US (W018, W023) | Sold via authorised distributors per W017; confirm current | Tier D |
| Odyssey 3D G90XF | Samsung | 27" 4K, eye-tracked, SBS input (W092) | ₹1,27,299 listed at India launch (W097) | Official India launch (W097, W093) | Cheap stereo testbed only |
| 55EW5G / 55EW5P-M | LG | 55" FHD transparent OLED, 38–43% transparency (W027, W031) | US$17,333–36,851 (US resellers) | UNKNOWN: VENDOR CONFIRMATION REQUIRED | Tier D |
| 3D hologram fan 42–46 cm | Many (Chinese OEM, IndiaMART traders) | 150° view (W043), WiFi app upload | ₹9,999–12,500 (W038, W041); ₹2,699 for 11 cm (W044) | Many traders | Not recommended |
| VX2 | Voxon | See §3 | US$6,800, ex duty, 10–12 wk lead (W088) | UNKNOWN | Reject |
| Quest 3S | Meta | — | US$349.99 (W063) | Official India price UNKNOWN; grey-market blogs (W055–W061) rejected as evidence | Optional |
| Looking Glass WebXR library | Looking Glass (open source) | Three.js v141+, R3F demos, needs Bridge running (W064–W070) | Free | n/a | Future-proofing |
| 21.5" IR touch (industrial) | Chennai supplier on IndiaMART | — | ₹21,000 listing (W107) | Local, TN | Evidence screen candidate |

---

## 5. Experience-test scoring (1 = fails, 5 = excellent; my judgement, to be tested)

| | Temple centre | Terrain+settlement | Water | Time | Links | Evidence text | Uncertainty | Total /35 |
|---|---|---|---|---|---|---|---|---|
| Plain 4K screen | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 32 |
| **Pepper's Ghost (ghost + 2nd screen)** | 4 | 4 | 4 | 5 | 4 | 5* | 3 | 29 |
| Projection on relief model | 3 | 5 | 5 | 4 | 3 | 2 | 4 | 26 |
| Light-field 16" | 4 | 3 | 3 | 5 | 3 | 2 | 4 | 24 |
| Transparent OLED + model | 4 | 3 | 3 | 5 | 4 | 5 | 4 | 28 (cost fails) |
| Fan / pyramid / HLD / Voxon | 2 | 1 | 1 | 3 | 1 | 1 | 1 | ≤10 |

* evidence lives on the second screen. The plain screen wins on content. The ghost wins only on **impact**, so the optical proof must show that impact is real, not assumed.

---

## 6. Interaction ranking

Scores 1–5 per criterion (reliability, latency, learnability, robustness, cost, visual impact). Judgement, not measured.

| Rank | Method | R | L | Learn | Robust | Cost | Impact | Note |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **Rotary encoder with detents** | 5 | 5 | 5 | 5 | 5 | 3 | One USB HID microcontroller; detent = one historical state |
| 2 | Physical buttons (layers, reset) | 5 | 5 | 5 | 5 | 5 | 2 | 3–4 big buttons |
| 3 | **Touch screen (evidence)** | 4 | 4 | 5 | 4 | 3 | 3 | Fixed panel, not a visitor's phone |
| 4 | External tablet | 3 | 3 | 5 | 2 | 3 | 3 | Theft, battery, pairing |
| 5 | Phone controller | 2 | 3 | 4 | 2 | 5 | 3 | Needs local WiFi; fails offline unless hosted locally |
| 6 | Depth camera / hand tracking | 2 | 3 | 3 | 2 | 2 | 5 | Lighting/occlusion; optional later |
| 7 | Webcam gestures / CV | 2 | 2 | 2 | 1 | 4 | 4 | Fragile in crowds |
| 8 | Voice | 1 | 1 | 4 | 1 | 4 | 3 | Noisy hall, Tamil/English mix; skip |
| 9 | Gaze | 1 | 2 | 1 | 1 | 2 | 4 | Skip |

Choice: **rotary encoder (primary) + 3 buttons + touch evidence screen (secondary).** Gestures are a documented future experiment, not MVP.

---

## 7. Optical design — Tier B cabinet (all dimensions are *engineering estimates* to verify with a cardboard mock-up)

**Geometry** (viewer in front; monitor mounted face-down at the top, glass tilted 45° with its top edge away from the viewer):

- The viewer sees a **virtual image the same size as the monitor, vertical, behind the glass**, mirrored on one axis. Treat the mirror axis as a render flag (`mirrorX` / `mirrorY`) found in Test 2.

- Monitor: 27" 16:9 ≈ 60 × 34 cm active area.

- Glass/film sheet: ≈ 65 cm wide × ~64 cm sloped length (monitor depth × √2 plus margin).

- Interior: ≈ 70 W × 55 D × 55 H cm, matte black everywhere (flock cloth), no shiny edges.

- Viewing: eye height near the centre of the virtual image, about 1.5–2.5 m away; vertical tolerance is tight (±10–15° is a hypothesis to test), horizontal arc wider.

**Parts and positions**

| Item | Position / spec |
|---|---|
| Screen | Bright 4K IPS/VA panel, top, face down; brightness limit is the key risk — spec UNKNOWN until chosen; sheet-bought nits claims must be photographed (Test 4) |
| Beamsplitter | Candidates: clear 3 mm acrylic/glass (dim, ~8% per surface *general physics*), two-way-mirror acrylic, beamsplitter film. India supplier: VENDOR CONFIRMATION REQUIRED (not verified) |
| Chamber floor/back | Matte black; optional dim LED strip for a physical relief prop |
| Hood | Shade top and sides so room light does not wash the glass; front arc open |
| Evidence screen | 21.5" IR touch, separate, landscape, on the front fascia, left of the encoder for right-handed use; mirror the layout in a variant |
| Encoder + buttons | Table-top control box, ≈ 90 cm height, reach zone wheelchair-compatible (≤ 1.1 m, forward reach) |
| Sensor | None in MVP; optional depth camera later behind the glass opening |
| Cables | Cable channel on the rear wall, power and USB hubs at the back panel |
| Ventilation | Monitor top with 5 cm gap, rear vents, filtered fans if enclosed, no fan noise audible at 2 m |
| Power | One UPS (≥ 600 VA *estimate*), PC + monitor + touch screen on a single surge-protected strip |

**Scene preparation for the ghost layer**

- Render at 2560×1440 or 3840×2160 to the full monitor; pure black `#000000` background.
- Fixed perspective camera, FOV ≈ 25–35°, orbit **disabled**; permit at most a small scripted yaw to hint at depth.
- Nothing dark: minimum fill luminance high enough to survive the beamsplitter loss; use bright outline linework for structure.
- No long text in the ghost layer: icons and 1–2 word labels only; sentences live on the evidence screen.
- Mirror flag in the renderer; calibration grid scene for alignment.

---

## 8. Historical representation on this display

Evidence classes (your A–E) need non-colour-only coding that **works on additive light**:

| Class | Meaning | Ghost layer style | Evidence-screen badge |
|---|---|---|---|
| A | Directly documented | Solid surface, bright, crisp edge | A + source ID |
| B | Archaeologically supported | Solid, slightly dimmer fill, thin outline | B + source ID |
| C | Scholarly interpretation | Outline + sparse hatching | C + scholar/source |
| D | AI-assisted / provisional | Dotted outline, no fill, "P" mark | D + review status |
| E | Speculative / uncertain | Outline only, flickering banned; dashed | E + "speculative" |

Rules: no tweening between states (a step change with a short cut, not a morph); selecting a period with no supported reconstruction shows a **full-scene state** with the text **NO SUPPORTED RECONSTRUCTION FOR THIS PERIOD** (Tamil + English) and the nearest *documented* evidence listed, never the nearest model. Every object must open a record: source, evidence class A–E, confidence, review status, valid time vs document time. Placeholder records must be tagged `UNREVIEWED`.

---

## 9. Pre-purchase tests

| # | Test | Setup | Cost | Duration | Pass / fail | Informs |
|---|---|---|---|---|---|---|
| 1 | **Software-only** | R3F scene on laptop, 3 states + gap state, water layer, evidence panel, fallback layout | ₹0 | 5–7 days | Runs ≥ 30 fps on your RTX 3050-class laptop at 1440p; state switch < 200 ms; gap state shows correct text | Whether to proceed at all; renderer choice |
| 2 | **Optical proof** | Existing monitor (face-down on a frame), cheap clear acrylic at 45°, cardboard/ply/black cloth; photo with phone | ₹3–8k *estimate* | 2–3 days | Virtual image visible and legible at 2 m in dim room, no double image distraction, correct orientation | Is Pepper's Ghost visually worth it |
| 2b | Prop test | Add a laser-cut/3D-printed relief or temple model in the chamber | ₹1–4k | 1–2 days | Viewers say they see "depth" in ≥ 3 of 5 hall tests | Whether a physical prop is needed |
| 3 | **Interaction proof** | Pro Micro/Arduino + encoder + 3 buttons as USB HID | ₹1–2k | 2 days | Dial turn → new state on screen < 100 ms measured by 240 fps phone slow-mo; 20 turns, 0 missed detents | Control hardware and latency budget |
| 4 | **Brightness / visibility** | Lux meter app, room at 3 light levels, photograph ghost at each | ₹0 | 1 day | Legible linework at ≤ ~150 lux with a hood *threshold is a hypothesis*; record monitor nits needed | Whether a brighter monitor/film is required |
| 5 | **Scene readability** | Print 5 screenshots of the ghost; 5 people, 10 s each, ask what temple/water/time they saw | ₹0 | 1 day | ≥ 4 of 5 identify temple; ≥ 4 identify water; ≥ 4 distinguish "evidence" vs "uncertain" | Visual grammar, label size |
| 6 | **Long-run stability** | Auto-start, kiosk Chromium, 4 h soak, forced kill and restart | ₹0 | 1 day | 4 h, 0 crashes; auto-recovery < 30 s after kill | Fallback logic, GPU margin |
| 7 | **Visitor usability** | 10 college visitors, no instructions | ₹0–500 | 1–2 days | ≥ 8 of 10 change state within 30 s unaided; ≥ 7 open evidence; ≥ 7 can say whether a shown state was documented or reconstructed | Whether hardware is learnable; uncertainty comprehension |

Optional **Test 8: borrow or rent a Looking Glass 16" for one day** (VENDOR CONFIRMATION REQUIRED in India) to compare against Test 2 on the same scene via WebXR.

---

## 10. Tiers and cost (INR, rough; *engineering estimates* unless sourced)

| | Tier A — proof | Tier B — exhibition prototype | Tier C — advanced |
|---|---|---|---|
| Display | Existing monitor | New bright 27" 4K monitor | Looking Glass 16" or transparent OLED over a model |
| Optics | Clear acrylic at 45° | Two-way mirror acrylic/film in hooded cabinet | Native light-field or transparent OLED |
| Computer | Existing laptop | Existing RTX 3050-class laptop; consider a mini-PC later | PC with RTX-class GPU as vendor specifies (Sony wants 2070 Super-class, W022) |
| Interaction | Encoder + buttons | Encoder + buttons + 21.5" IR touch (₹21,000, W107) | Plus optional depth camera |
| Audio | Laptop speakers | Small powered speakers, narration optional | Directional audio |
| Enclosure | Cardboard/ply | Local carpenter, MDF, flocked black | Professional fab |
| Cost | ₹3–12k | ₹0.8–1.8 lakh | ₹3.5 lakh+ (Looking Glass 16" ≈ US$4,000, W013, plus duty) up to ₹15 lakh+ (LG transparent OLED, W027, W031) |
| Time | 1–2 weeks | 4–8 weeks | 3–6 months |
| Portability | Hand-carry | Two people + case | Crate |
| Audience | 1–5 | 5–15 / hour guided | Multiple |

Cheapest credible route: **Tier A → Tier B**, hardware spend under ₹2 lakh. The ₹10–25 lakh figure is not required for a first demo.

---

## 11. Fallback

| Failure | Response |
|---|---|
| Encoder fails | Touch screen + on-screen arrows |
| Touch screen fails | Encoder + buttons only; evidence text shown in a side column of the main screen |
| Ghost optics washed out | Switch the same scene to a full-screen plain mode (`mode=flat`) |
| GPU crash / hang | Watchdog restarts kiosk; scene pack reloads from local disk < 30 s |
| Internet / backend down | Everything served from a local scene pack (JSON + GLB + textures); no live calls |
| PC dies | Second laptop with the same pack, tested monthly |
| Display dies | Spare monitor or a pre-recorded 3-minute video loop |

---

## 12. Final decision (proposed, subject to Tests 1–7)

**DISPLAY:** Bright 27" 4K monitor (specific model: VENDOR CONFIRMATION REQUIRED), plus a 21.5" IR touch screen for evidence

**OPTICS:** 45° beamsplitter (two-way mirror acrylic/film), hooded matte-black cabinet, optional physical relief prop

**COMPUTER:** Your existing RTX 3050-class Windows laptop for Tests 1–7; mini-PC after the gate

**GPU:** Existing GPU; spend nothing on new GPU before Test 6

**PRIMARY INTERACTION:** Rotary encoder with detents (one detent = one historical state)

**SECONDARY INTERACTION:** 3 buttons + touch evidence screen

**SENSOR:** None in MVP; depth camera deferred to a labelled experiment

**AUDIO:** Off by default; optional short narration, clearly labelled as a modern voice-over

**ENCLOSURE:** Local carpenter, MDF/ply, ≈ 70×55×55 cm chamber plus fascia

**SOFTWARE:** React + Three.js / R3F in a Chromium kiosk; Electron only if kiosk behaviour requires it

**SCENE FORMAT:** Versioned JSON scene description + GLB (glTF 2.0) assets, loaded from a local pack

**ESTIMATED COST:** Tier A ₹3–12k, Tier B ₹0.8–1.8 lakh

**TARGET VIEWERS:** Small groups at a StartupTN / college booth, one operator

**EXPECTED DEVELOPMENT TIME:** 4 weeks to the goal below

**MAIN RISK:** Ghost brightness and legibility in a lit hall; visual grammar failing on additive light

**FALLBACK:** Same scene in flat mode on a plain monitor with the encoder; if optics fail, you still demonstrate the evidence/time system

**Why this and not the others**

- Plain screen alone is the best content carrier but gives no "physical installation".
- Light-field gives real parallax but costs ≥ ~₹3.5 lakh, is small, and splits resolution across views; unsuitable for text.
- Eye-tracked displays serve 1–2 viewers and carry PC/software dependencies.
- Transparent OLED is the best optics but costs ₹15 lakh+ before duty.
- Fans/pyramids look like advertising; HLD plays video, not your scene; Voxon's volume is too small.
- Unity/Unreal add a second stack with no gain until a vendor SDK demands it.

---

## 13. The one goal

**By 5 November 2026 (4 weeks):** one unassisted visitor, offline, turns a dial to any of **3 supported Brihadisvara states** and **1 "no supported reconstruction" state**; each state shows the ghost scene plus a small water-context layer; the visitor taps any object and sees **source, evidence class A–E, confidence and review status**; **dial-to-photon latency < 100 ms** (measured at 240 fps), **≥ 30 fps**, and **4 hours unattended with zero crashes** and **< 30 s auto-recovery** after a forced kill. At least 3 evidence records per state, real sources registered, each tagged `UNREVIEWED` until an expert signs off.

---

## 14. Four-week schedule (Day 1 = 8 Oct)

| Week | Dates | Deliverables |
|---|---|---|
| 1 | 8–14 Oct | Validate this report; register sources; scene-pack JSON v0; Test 1 scaffold; decide first 3 states with a historian-advisor |
| 2 | 15–21 Oct | Test 1 complete on plain monitor; evidence panel; gap-state; mirror/flat render modes |
| 3 | 22–28 Oct | Tests 2, 2b, 3, 4; encoder HID; photograph optical proof; go/no-go on ghost |
| 4 | 29 Oct–5 Nov | Tests 5, 6, 7; kiosk autostart; fallback modes; recorded demo; goal measurement |

---

## 15. Open items to verify

- Indian availability/price: Looking Glass, LG transparent OLED, beamsplitter sheet, bright 27" monitor — all VENDOR CONFIRMATION REQUIRED.
- Sony ₹7,00,000 is a launch-era article (W017); current price UNKNOWN.
- Projection mapping on relief, depth cameras, hand tracking, Unity/Unreal costs: not researched this stage.
- Whether the Looking Glass WebXR route works with your exact R3F version: test before buying.
- Legal/licensing: nothing in this report touches data rights.

---

## 16. COMPLETE WEBSITE INDEX (Stage 1)

How I accessed pages: via a search tool returning page extracts. I did not open full pages except the GitHub URL. Spec claims should be re-confirmed on the official page before purchase. Category codes: MFR = manufacturer, RET = retailer, NEWS = trade/news, PAT = patent, DOC = developer docs, ACAD = academic, FORUM = list/forum, MKT = marketplace. Rights: "Unknown/ToS apply" unless stated; all material was only read, nothing reproduced.

| ID | URL | Organization | Cat | Finding | Status |
|---|---|---|---|---|---|
| W007 | github.com/guruPrasath4707/Neer-Nilam | You | — | 404 (private) | RESTRICTED |
| W008 | 3dnews.ru/1109192-looking-glass-predstavila-kompaktniy-golograficheskiy-6dyuymoviy-displey-go-za-300 | 3DNews | NEWS | Looking Glass Go US$299 (Russian) | REFERENCE |
| W009 | …/print variant of W008 | 3DNews | NEWS | Same article | DUPLICATE |
| W010 | jonpeddie.com/?p=45726 | Jon Peddie Research | NEWS | 16"/32" displays, gesture sensors | REFERENCE |
| W011 | moguravr.com/?p=267148 | Mogura VR | NEWS | LG 27" US$10,000, 100+ views, Apr 2025 | USEFUL |
| W012 | mixed-news.com/en/looking-glass-first-holo-displays-are-sent-to-customers/ | MIXED | NEWS | Shipping; 45–100 views; US$4,000 | USEFUL |
| W013 | mixed-news.com/en/looking-glass-16-32-spatial-displays/ | MIXED | NEWS | US$3,000 promo; plugins | USEFUL |
| W014 | looking-glass.helpscoutdocs.com/category/218-looking-glass-32 | Looking Glass | DOC | FAQ index only | REFERENCE |
| W015 | displaydaily.com/?p=381232 | Display Daily | NEWS | 32": 53° cone, 45–100 views | USEFUL |
| W016 | techcrunch.com/2024/05/14/looking-glass-launches-new-3d-displays | TechCrunch | NEWS | 16" US$4,000; 32" no public price | USEFUL |
| W017 | croma.com/unboxed/sony-spatial-reality-display-lets-you-view-3d-content-without-glasses-or-a-vr-headset | Croma | RET | ELF-SR2 ₹7,00,000 | USEFUL (date unclear) |
| W018 | almoproav.com/productdetails/SONYD/ELFSR2 | Almo Pro A/V | RET | MSRP US$5,000; 14 ms | USEFUL |
| W019 | exertisalmo.com/productdetails/SONYD/ELFSR2 | Exertis Almo | RET | Same listing as W018 | DUPLICATE |
| W020 | fonearena.com/blog/404245/sony-elf-sr2-price-india-features.html/amp | Fone Arena | NEWS | India launch, Unity/Unreal, OpenXR | USEFUL |
| W021 | adiglobaldistribution.pr/Product/61-ELFSR2 | ADI Global | RET | Distributor listing, no price | REFERENCE |
| W022 | lowyat.net/2023/298085/sony-second-generation-spatial-reality-display | Lowyat.NET | NEWS | PC requirement RTX 2070 Super-class | USEFUL |
| W023 | channelxr.com/products/sony-spatial-reality-display-4k-27-inch | Channel XR | RET | US$5,000 | REFERENCE |
| W024 | deploydepot.ca/products/sony-pro-bravia-elf-sr2… | Deploy Depot | RET | CAD 6,360, sold out | REFERENCE |
| W025 | creationnetworks.net/products/sony-elf-sr2-27-inch-4k-spatial-reality-display | Creation Networks | RET | US$4,750 | REFERENCE |
| W026 | displaydaily.com/?p=58883 | Display Daily | NEWS | LG 55" transparent OLED 40%, 400 nits | REFERENCE |
| W027 | fullcompass.com/prod/638659-lg-electronics-55ew5p-m-55-transparent-oled-commercial-display | Full Compass | RET | 43%, 200/600 nits, US$17,333 | USEFUL |
| W028 | displaydaily.com/lg-starts-with-transparent-oled/ | Display Daily | NEWS | Same article as W026 | DUPLICATE |
| W029 | adorama.com/loc55ew5tfa.html | Adorama | RET | 55EW5TF-A 33% with touch | USEFUL |
| W030 | displaydaily.com/?p=32607 | Display Daily | NEWS | Planar transparent OLED 45% | REFERENCE |
| W031 | commercialdisplay.sg/?p=12708 | Commercial Display SG | RET | 55EW5G 38%, US$36,851, LCD ~10% | USEFUL |
| W032 | shi.com/product/44575544/… | SHI | RET | 55EW5PG-S, 400 cd/m² | REFERENCE |
| W033 | displaydaily.com/planar-shows-off-transparent-oled-variants/ | Display Daily | NEWS | Same as W030 | DUPLICATE |
| W034 | commercialdisplay.sg/digital-signage/lg-55ew5g/ | Commercial Display SG | RET | Same as W031 | DUPLICATE |
| W035 | publicsector.shidirect.com/product/44575544/… | SHI | RET | Same as W032 | DUPLICATE |
| W036 | m.indiamart.com/dkunique-production | DK Unique Production | MKT | Fan sizes, "call for price" | REFERENCE |
| W037 | newegg.com/p/0FC-065A-008H3 | Newegg | RET | Fan 42–115 cm, US$294.99 | REFERENCE |
| W038 | aajjo.com/product/3d-hologram-fan-input-voltage-24-v-in-delhi-the-reptile-company | Aajjo | MKT | ₹9,999 | REFERENCE |
| W039 | aajjo.com/product/3d-holographic-fan-in-delhi-the-reptile-company | Aajjo | MKT | POV explanation, no price | REFERENCE |
| W040 | syncee.com/product/197078_57874_7133338042554/3d-hologram-fan-projector-light | Syncee | MKT | 640×640, 224 LEDs | REFERENCE |
| W041 | indiamart.com/redwolfmedia/3d-holographic-fan.html | Red Wolf Media | MKT | ₹12,500, 46 cm | USEFUL |
| W042 | m.indiamart.com/impcat/holographic-display.html | IndiaMART | MKT | Category listing (seen again in a later query, same page) | REFERENCE |
| W043 | newegg.com/p/0FC-065A-00378 | Newegg | RET | 150° viewing angle, US$152.99 | REFERENCE |
| W044 | magicdrop.in/drops/3d-hologram-fan | Magicdrop | MKT | ₹2,699 (11 cm, Amazon) | REFERENCE (Tier 4) |
| W045 | patents.google.com/patent/US8692738 | Google Patents | PAT | Pepper's Ghost at ~45° | USEFUL |
| W046 | twowaymirrors.com/?p=609576 | TwoWayMirrors | RET | Beamsplitter overview | REFERENCE (commercial) |
| W047 | twowaymirrors.com/peppers-ghost-illusion | TwoWayMirrors | RET | Same as W046 | DUPLICATE |
| W048 | google.co.uk/patents/US9132361 | Google Patents | PAT | Beamsplitter layout | REFERENCE |
| W049 | patents.google.com/patent/US12298537 | Google Patents | PAT | Display + beamsplitter geometry | USEFUL |
| W050 | hajim.rochester.edu/optics/undergraduate/senior-design/pdf/fall16/rmsc_prd_161217_final.pdf | Univ. of Rochester | ACAD | Student exhibit design | REFERENCE |
| W051 | patents.google.com/patent/US9211481 | Google Patents | PAT | High-gain beamsplitter | REFERENCE |
| W052 | patents.justia.com/patent/20120313839 | Justia | PAT | Mask + beam splitter | USEFUL |
| W053 | artanddesign.aut.ac.nz/2021/student-work/house-of-illusions | AUT | ACAD | Student project | REJECTED (irrelevant) |
| W054 | patents.justia.com/patent/10108020 | Justia | PAT | High-gain beamsplitter | REFERENCE |
| W055 | comgateway.com/ja/blogs/the-meta-quest-3s-price-discrepancy-between-us-and-indian-markets/ | comGateway | MKT | Grey-market markup claims | REJECTED (promotional) |
| W056 | comgateway.com/sv/blogs/is-the-current-price-of-the-meta-quest-3s-in-india-an-unnecessary-financial-burden/ | comGateway | MKT | Same theme | REJECTED |
| W057 | comgateway.com/es/blogs/is-the-indian-grey-market-price-for-the-meta-quest-3s-a-total-glitch-vs-importing-from-the-us/ | comGateway | MKT | Same theme | REJECTED |
| W058 | comgateway.com/ja/blogs/bypassing-local-price-hikes-on-the-meta-quest-3s-for-indian-gamers/ | comGateway | MKT | Same theme | REJECTED |
| W059 | comgateway.com/zh-cn/blogs/amazon-us-vs-indian-retailers-the-meta-quest-3s-price-gap-analyzed/ | comGateway | MKT | Same theme | REJECTED |
| W060 | comgateway.com/it/blogs/is-the-meta-quest-3s-significantly-more-affordable-when-sourced-directly-from-us-retailers/ | comGateway | MKT | Same theme | REJECTED |
| W061 | erp.blackboxoperations.com/blog/meta-quest-3-price-in | Blackbox Ops | MKT | Generic, no figures | REJECTED |
| W062 | meta.com/ja-jp/blog/update-meta-quest-pricing/ | Meta | MFR | Japanese-language pricing notice | DUPLICATE (content of W063) |
| W063 | meta.com/blog/update-meta-quest-pricing/ | Meta | MFR | US$349.99 / 449.99 / 599.99 from 19 Apr 2026 | USEFUL |
| W064 | npmjs.com/package/@lookingglass/webxr | npm | DOC | Looking Glass WebXR library | USEFUL |
| W065 | lfdocs.lookingglassfactory.com/software/creator-tools/webxr | Looking Glass | DOC | Three.js v141+, needs Bridge | USEFUL |
| W066 | cdn.jsdelivr.net/npm/@lookingglass/webxr@0.6.0/README.md | jsDelivr | DOC | Same library README | DUPLICATE |
| W067 | lookingglassfactory.com/tutorial/webxr | Looking Glass | DOC | Three.js tutorial | USEFUL |
| W068 | lfdocs.lookingglassfactory.com/software/looking-glass-bridge-sdk.md | Looking Glass | DOC | Bridge SDK | USEFUL |
| W069 | docs.lookingglassfactory.com/developer-tools/webxr | Looking Glass | DOC | Older docs of W065 | DUPLICATE |
| W070 | lfdocs.lookingglassfactory.com/software/overview | Looking Glass | DOC | Unity/Unreal/Blender/WebXR ecosystem | USEFUL |
| W071 | lookingglassfactory.com/hld-overview | Looking Glass | MFR | HLD vs Pepper's Ghost vs LFD | USEFUL |
| W072 | channelxr.com/products/looking-glass-hololuminescent-display-hld | Channel XR | RET | HLD US$2,000 | REFERENCE |
| W073 | ravepubs.com/?p=291725 | rAVe | NEWS | HLD announcement | REFERENCE |
| W074 | itc.ua/news/looking-glass-predstavyaet-gololyumynestsentnye-dyspley-hld… | ITC.ua | NEWS | HLD from US$1,500 (Russian) | REFERENCE |
| W075 | itc.ua/ua/novini/looking-glass-predstavlyaye-gololyuminestsentni-dyspleyi-hld… | ITC.ua | NEWS | Ukrainian version | DUPLICATE |
| W076 | looking-glass.helpscoutdocs.com/category/385-hld | Looking Glass | DOC | HLD FAQ index | REFERENCE |
| W077 | checkout.lookingglassfactory.com/products/hld-displays-early-access | Looking Glass | MFR | May/June 2026 shipping; no speakers | USEFUL |
| W078 | checkout.lookingglassfactory.com/products/86-hld-preorder | Looking Glass | MFR | 86" US$20,000, IR touch | USEFUL |
| W079 | auganix.org/?p=17569 | Auganix | NEWS | Announcement 16 Sep 2025 | REFERENCE |
| W080 | 3dtested.com/monitors/looking-glass-demos-hololuminescent-display-monitors-sizes-range-from-16-to-85-inches-starting-at-usd1-500 | 3DTested | NEWS | Commenter says HLD is optical illusion | REFERENCE (comment is Tier 4) |
| W081 | en.wikipedia.org/wiki/Volumetric_display | Wikipedia | REF | VX1 18×18×8 cm | REFERENCE |
| W082 | www.wikipedia.org/wiki/Holovision | Wikipedia mirror | REF | Same text as W081 | DUPLICATE |
| W083 | techeblog.com/voxon-vx1-hologram-table/ | TechEBlog | NEWS | VX1 US$9,800 | REFERENCE |
| W084 | interaction-lab.wiki.utwente.nl/_export/raw/xr:vx1_volumetric_display | Univ. of Twente | ACAD | VX1 lab description | REFERENCE |
| W085 | voxon.co/demonstration-voxon-vx1-3d-volumetric-display/ | Voxon | MFR | Principle explanation | REFERENCE |
| W086 | interaction-lab.wiki.utwente.nl/xr:vx1_volumetric_display | Univ. of Twente | ACAD | Same as W084 | DUPLICATE |
| W087 | handwiki.org/wiki/Volumetric_display | HandWiki | REF | Same text as W081 | DUPLICATE |
| W088 | voxon.co/product-page/voxon-vx2 | Voxon | MFR | VX2 US$6,800, 256 mm, 8 M voxels | USEFUL |
| W089 | voxon.co/?p=3261 | Voxon | MFR | Marketing | REFERENCE |
| W090 | samsung.com/sg/monitors/gaming/odyssey-3d-g90xf-27-inch-165hz-uhd-ls27fg900xexxs | Samsung SG | MFR | Eye-tracking, view mapping | REFERENCE |
| W091 | ushl.samsung.com/sa_en/monitors/gaming/odyssey-3d-g90xf-27-inch-ls27fg900xmxue | Samsung | MFR | Regional duplicate of W090 | DUPLICATE |
| W092 | mail.cgl.ucsf.edu/mailman/archives/list/chimerax-users@cgl.ucsf.edu/thread/C4BNC6ZSHEBV4S2O7JFPNURTR4GZM3OP/ | UCSF ChimeraX list | FORUM | Expert view: Samsung SBS, single viewer | REFERENCE (Tier 3/4) |
| W093 | news.samsung.com/in/tag/odyssey-g9/feed | Samsung India | MFR | India availability of Odyssey 3D | USEFUL |
| W094 | ushl.samsung.com/ch_fr/monitors/gaming/odyssey-3d-g90xf-27-inch-165hz-uhd-ls27fg904xuxen | Samsung CH | MFR | Regional duplicate | DUPLICATE |
| W095 | ushl.samsung.com/ph/monitors/gaming/odyssey-3d-g90xf-27-inch-165hz-uhd-ls27fg900xexxp | Samsung PH | MFR | Regional duplicate | DUPLICATE |
| W096 | mail.cgl.ucsf.edu/mailman/archives/list/chimerax-users@cgl.ucsf.edu/message/C4BNC6ZSHEBV4S2O7JFPNURTR4GZM3OP | UCSF ChimeraX list | FORUM | Same message as W092 | DUPLICATE |
| W097 | mediainfoline.com/techno/samsung-unveils-odyssey-gaming-monitors-first-ever-glasses-free-3d-4k-oled-in-india | MediaInfoline | NEWS | ₹1,27,299 listing | USEFUL |
| W098 | galaxus.at/de/page/jetzt-im-shop-samsungs-3d-bildschirm-odyssey-3d-g90xf-37563 | Galaxus | RET | German retailer note | REFERENCE |
| W099 | mail.cgl.ucsf.edu/mailman/archives/list/chimerax-users@cgl.ucsf.edu/message/OTVSIRSNTOI6W6A45XWN4EAORJ33ULSY/ | UCSF ChimeraX list | FORUM | Tracking runs on PC CPU | REFERENCE (Tier 4) |
| W100 | m.indiamart.com/impcat/lcd-computer-monitor.html | IndiaMART | MKT | Generic LCD monitors | REJECTED (irrelevant) |
| W101 | m.indiamart.com/akola/lcd-computer-monitor.html | IndiaMART | MKT | Same category | REJECTED |
| W102 | dir.indiamart.com/bharuch/lcd-monitor.html | IndiaMART | MKT | Same category | REJECTED |
| W103 | ipros.com/en/cg2/Display Box/ | IPROS | MKT | 21.5" transparent LCD box | USEFUL |
| W104 | m.indiamart.com/proddetail/transparent-led-display-21-5-2852809994362.html | Advance Technology Inc | MKT | ₹2,55,000; headline 8K vs description 1080p | CONTRADICTORY |
| W105 | mono.ipros.com/en/cg2/Lou Display/ | IPROS | MKT | Same product as W103 | DUPLICATE |
| W106 | m.indiamart.com/proddetail/lcd-computer-monitor-2857786553530.html | Sandesh Enterprises | MKT | Basic monitor | REJECTED |
| W107 | m.indiamart.com/nrjautomationtechnology/products-and-services.html | NRJ Automation (Chennai) | MKT | 21.5" IR touch ₹21,000 | USEFUL (local TN lead) |

*End of Stage 1.*