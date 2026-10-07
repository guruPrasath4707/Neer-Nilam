# Claude Planning Prompt 001 — Choose the Neer-Nilam Holographic Presentation System

Act as a senior immersive-display architect, 3D graphics engineer, museum-exhibition designer, hardware integration engineer, digital-heritage architect, product strategist and technical project planner.

This is a real build-planning exercise. Challenge assumptions. Do not hype the word “hologram”.

PROJECT:
Neer-Nilam — a source-aware, spatiotemporal digital heritage intelligence platform for Tamil Nadu.

PILOT:
Thanjavur–Kumbakonam–Cauvery heritage corridor.
First deep physical case: Brihadisvara Temple, Thanjavur.

CORE PLATFORM:
- PostgreSQL/PostGIS
- temporal historical states/events
- provenance/confidence/verification
- knowledge graph
- AI-assisted manuscript/inscription pipeline with human verification
- React/Next.js
- CesiumJS/Three.js/R3F
- FastAPI
- selective 3D/photogrammetry
- source registry + data rights layer

PHYSICAL EXPERIENCE:
A visitor sees an immersive 3D representation of a heritage site and can explore supported historical states, water/landscape context, people/events/text, evidence and uncertainty.

Previous DeepSeek analysis proposed:
- Pepper’s Ghost
- rotary encoder
- optional depth camera
- event/discrete time states
- evidence-first visualization
- Unity as a later installation client

Do not accept that recommendation without re-evaluating it.

CURRENT RESEARCH SOURCES ALREADY REVIEWED:
W001 https://bhuvan-app1.nrsc.gov.in/2dresources/bhuvanstore2.php
W002 https://overpass-turbo.eu/
W003 https://tngis.tn.gov.in/apps.html
W004 https://bhuvan.nrsc.gov.in/home/index.php/newsletter.php
W005 https://bhuvan.nrsc.gov.in/forum/ucp.php?mode=terms&s_forum_id=ef804d61fb0810a00be9ded85883fa74
W006 https://tngis.tn.gov.in/apps/cumta/

RULE:
EVERY website you visit during this research must be tracked and assigned a source ID. Include useful, rejected, restricted and reference-only sites. Do not omit websites merely because their conclusions are negative.

IMMEDIATE QUESTION:
Which physical presentation model should we build first?

Compare current 2026 options:
1. Pepper’s Ghost / beamsplitter
2. holographic pyramid
3. transparent OLED
4. transparent LCD
5. LED holographic fan
6. projection mapping on a physical 3D model
7. light-field display
8. volumetric display
9. AR/MR
10. other credible current commercial/research options
11. hybrid combinations

RESEARCH REQUIREMENT:
Use current sources. Prefer manufacturer pages, official documentation, technical datasheets and reputable Indian suppliers/distributors for availability/pricing. Do not invent prices, specifications or availability.

FOR EACH OPTION EVALUATE:
- actual optical/display principle
- whether it has real depth/parallax
- viewing cone
- brightness and contrast
- image resolution
- screen size
- indoor lighting sensitivity
- number of simultaneous viewers
- interaction possibilities
- tracking requirements
- latency
- GPU requirement
- software/API integration
- safety
- heat/noise
- maintenance
- portability
- setup/calibration
- reliability
- Indian availability
- indicative INR cost
- total prototype cost
- development difficulty
- failure modes
- suitability for Neer-Nilam
- best use case

THEN DESIGN THE EXPERIENCE:
Visitor approaches.
Visitor sees the temple/landscape.
Visitor changes time.
The scene changes only according to supported evidence.
Water/land/settlement layers can be toggled.
Related people/events/text can be selected.
Evidence and confidence appear without destroying the visual experience.
Unsupported periods are explicitly labeled.

INTERACTION:
Compare:
- rotary encoder
- buttons
- touch controller
- external tablet
- depth camera
- hand tracking
- phone controller
- voice
- gaze
- computer vision
Rank by exhibition reliability. Do not prefer a futuristic interaction merely because it looks impressive.

HISTORICAL INTEGRITY:
Separate:
- directly documented
- archaeologically supported
- scholarly interpretation
- AI-assisted/provisional
- speculative/uncertain

Do not invent intermediate states.
Do not silently use the nearest historical state when evidence is absent.
Separate historical validity time, observation time, source/document time and ingestion time.

ARCHITECTURE:
Design:
external source
→ source registry/rights
→ connectors
→ restricted/raw plane
→ normalization/QA
→ canonical PostGIS + knowledge graph
→ evidence engine
→ temporal engine
→ scene composer
→ presentation client

The hologram should not query external websites or raw government datasets on every frame.

RENDERER:
Assess whether the first proof should use:
- browser kiosk + React/Three.js/R3F
- Unity
- Unreal
- Electron
- native application

Do not introduce a second renderer unless it creates a real benefit.

PROTOTYPE TIERS:
Design:
A. low-cost proof
B. serious exhibition MVP
C. advanced museum/research prototype

For each provide:
- physical dimensions
- display/optics
- computer/GPU
- sensors
- controller
- enclosure
- audio
- wiring/power
- setup
- approximate INR range
- development timeline
- reliability
- portability

PRE-PURCHASE TESTING:
Define the cheapest tests that prove:
1. visual effect
2. optical geometry
3. scene readability
4. interaction
5. brightness/contrast
6. stability
7. audience usability

Create hard pass/fail criteria.

FAILURE/FALLBACK:
Design offline operation, cached scenes, controller fallback, backup display/video, automatic startup, crash recovery and safe shutdown.

INNOVATION:
Be brutally honest about:
- common technology
- genuinely differentiated components
- gimmick risks
- research opportunities
- startup value
- what judges will likely challenge

MVP:
Define exactly what must be real and what can be mocked for a one-monument proof.

MOST IMPORTANT:
The display is replaceable.
The Neer-Nilam temporal/evidence/scene system is the core asset.

FINAL OUTPUT:
1. Executive verdict
2. Best terminology for the system
3. Technology comparison matrix
4. Real current products worth investigating
5. Recommended physical architecture
6. Interaction architecture
7. Hardware bill of materials
8. Software architecture
9. Optical/display geometry
10. Historical/evidence UX
11. 3–5 minute demo
12. Testing plan
13. Fallback architecture
14. Risks
15. Innovation assessment
16. MVP boundary
17. 30-day implementation plan
18. Specific final architecture

FINISH WITH:
CLEAR GOAL
State one measurable goal for the team’s next milestone.

Also give:
FIRST 10 ACTIONS
exactly what we should do, in order, starting Day 1.

At the end provide a complete list of every website you visited, categorized and numbered, so it can be added to the Neer-Nilam master website index.