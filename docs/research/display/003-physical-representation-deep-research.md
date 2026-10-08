# Physical Representation Deep Research 001 — Neer-Nilam

Date: 2026-10-08
Status: Research conclusion / prototype architecture hypothesis
Scope: Physical presentation of the Neer-Nilam heritage-time experience

## 1. Research question

What physical representation can make Neer-Nilam feel materially different from an ordinary web GIS while preserving the project's real value:

time → place → monument → landscape → water → people/events → evidence

The display must support a shared public experience, not a private headset workflow. It must survive exhibition conditions, run offline, and keep the historical evidence model visible.

## 2. Main conclusion

A single "hologram" technology is not the best representation of the complete Neer-Nilam concept.

The strongest current architecture hypothesis is a **multi-modal heritage theatre**:

1. **Physical relief / terrain substrate**
   - gives genuine physical depth
   - gives all-viewer spatial reference
   - makes land, river, tank and settlement relationships tangible

2. **Projection-mapped dynamic layers**
   - changes water, roads, settlement footprint, boundaries, routes and other time-varying contextual layers
   - supports a shared audience without headsets
   - can use physical/tactile controls

3. **Optional Pepper's Ghost / optical overlay**
   - creates the floating "holographic" hero moment
   - can emphasize the temple, a monument state, event annotations or a focal reconstruction
   - should remain an interchangeable presentation client, not the data system

4. **Separate evidence interface**
   - touch screen or side display
   - carries source, evidence class, confidence, review status, dates, notes and uncertainty
   - prevents dense evidence UI from contaminating the physical scene

This is **not a final hardware purchase decision**. It is the architecture to test first.

## 3. Why the physical relief matters

Pepper's Ghost creates apparent depth but does not give ordinary binocular or motion-parallax behavior for a single flat image. A physical relief creates an actual spatial object that the audience can inspect from different positions.

For Neer-Nilam, that distinction is important because the project's subject is a **landscape**, not only a building.

A relief can physically encode:
- terrain
- river corridor
- settlement relationship
- temple position
- tanks / canals
- roads / routes
- approximate elevation structure

Projection can then encode changing or analytical layers on top of that physical base.

## 4. Why projection mapping deserves equal status with Pepper's Ghost

Museum and digital-heritage research has demonstrated projection mapping on physical or 3D-printed historical models, including interactive/tangible controls and audience evaluation. This is much closer to Neer-Nilam's landscape-oriented narrative than a decorative hologram fan.

The key advantage is semantic:

**physical geometry = relatively stable spatial substrate**

**projected content = time/state/layer information**

That separation maps naturally to the Neer-Nilam data model.

The main weakness is geometry change. Projection can recolor/highlight existing geometry, but it cannot physically rebuild a demolished/expanded structure unless the installation adds:
- interchangeable model pieces
- separate physical overlays
- multiple model states
- or another optical layer

Therefore projection mapping is strongest for landscape/context/time, while an optical overlay can handle selected monument-state emphasis.

## 5. Three first-build candidates

### Candidate A — Pepper's Ghost theatre

Architecture:
- 27-inch display
- 45-degree optical surface
- matte-black hood
- rotary encoder + buttons
- separate evidence display

Strength:
- cheapest path to the desired "floating" visual hook

Weakness:
- apparent depth only
- sensitive to optical alignment and ambient light
- weak for dense evidence
- landscape depth must be faked or supplemented

Status:
**Leading low-cost optical proof candidate.**

### Candidate B — Projection-mapped physical relief

Architecture:
- 3D-printed / laser-cut relief
- short-throw or ultra-short-throw projector
- calibrated projection
- rotary/buttons or tangible controls
- separate evidence display

Strength:
- physical depth
- shared audience
- excellent fit for landscape/water/settlement layers
- strong museum precedent

Weakness:
- room-light sensitivity
- projector alignment/calibration
- projected detail varies with surface geometry
- physical geometry does not automatically change across historical states

Status:
**Co-equal first physical proof candidate.**

### Candidate C — Hybrid relief + projection + optical overlay

Architecture:
- physical terrain/urban relief
- projection-mapped environmental/historical layers
- Pepper's Ghost-style floating monument/annotation layer
- evidence screen
- rotary control

Strength:
- combines the strongest semantic role of each medium

Weakness:
- highest calibration and fabrication complexity
- more components and more failure modes
- requires careful optical separation between projected and reflected light

Status:
**Most promising exhibition architecture, but only after A and B prove their individual value.**

## 6. Technologies that should remain later-stage

### Light-field

Useful for:
- real parallax
- direct interactive 3D
- future research/demo station

Problem for first installation:
- relatively small physical image for the cost
- view-dependent presentation
- text/evidence remains better on a conventional interface
- installation economics are currently weaker than a custom physical theatre

### Transparent OLED

Useful for:
- elegant overlay on a physical model
- museum-grade industrial design
- future permanent installation

Problem:
- current price/availability require vendor confirmation
- the display is still a display surface; it does not replace the historical data/evidence system

### Eye-tracked spatial displays

Useful for:
- one-person expert visualization
- 3D review
- model inspection

Problem:
- tracking/viewer constraints are poorly matched to walk-up group exhibition.

### Volumetric

Useful for:
- specialist research demonstrations

Problem:
- small volume relative to the landscape scale
- higher cost
- mechanical/optical complexity
- evidence text remains an external UI problem

### LED hologram fans / small pyramids

Useful mainly as:
- attention-getting signage or attract loops

Problem:
- low semantic density
- weak fit for evidence-rich landscape storytelling
- safety/robustness concerns for fan systems

## 7. Physical representation should be a layered semantic system

| Physical channel | Neer-Nilam meaning |
|---|---|
| Physical relief | stable spatial reference |
| Projection | temporal/contextual state |
| Optical floating layer | focal reconstruction / narrative emphasis |
| Evidence display | provenance + uncertainty |
| Physical controls | deterministic navigation |
| Optional audio | narration only; never substitute for evidence |

This avoids trying to make one optical surface perform every job.

## 8. Recommended experience

Visitor approaches.

The relief immediately establishes the Thanjavur landscape.

A visible rotary control is labelled with the currently selected historical state.

Turning the control causes a **state change**, not an invented continuous historical morph.

Projected layers change:
- water context
- roads/routes
- settlement context
- selected historical annotations

The optical layer can bring the temple/focal structure forward.

Visitor selects an object or layer.

The evidence screen shows:
- what is being claimed
- evidence class
- confidence
- source
- source date
- valid time
- document time
- verification state
- expert review
- data/asset rights

Selecting an unsupported period produces an explicit:
NO_SUPPORTED_RECONSTRUCTION

The installation never silently substitutes another state.

## 9. Physical calibration model

Calibration should be treated as data, not as an undocumented workshop adjustment.

Record:
- display pose
- reflector pose
- projector pose
- relief origin
- scale
- homography / calibration transform
- camera/projector intrinsics where applicable
- scene version
- calibration date
- operator
- calibration asset/version
- measured residual/error

A calibration package should be versioned and tied to the physical installation ID.

## 10. Test plan

### P1 — Pepper's Ghost optical proof

Measure:
- visibility at several room-light levels
- useful viewer arc
- vertical tolerance
- double-image/ghosting
- black-level behavior
- line readability
- image registration
- time to calibrate

### P2 — Relief projection proof

Use exactly the same Neer-Nilam scene data.

Measure:
- projected alignment error
- readability at visitor distance
- room-light sensitivity
- setup/calibration time
- audience comprehension
- state-switch comprehension
- water/settlement recognition

### P3 — Hybrid proof

Only after P1 and P2.

Measure:
- whether the optical layer adds meaningful comprehension or only spectacle
- interference between projected illumination and reflected image
- total calibration burden
- maintenance burden
- failure recovery

## 11. Hard gate for the physical architecture

A technology should not enter Tier B merely because it looks impressive.

Tier B approval requires:
- measurable visitor benefit
- stable operation
- offline operation
- deterministic interaction
- readable evidence through a separate channel
- documented calibration
- recoverable failure mode
- reproducible setup by a second operator
- no unsupported historical claims introduced by the visual medium

## 12. Current physical decision

**D018 already blocks expensive hardware purchase before proof.**

Current physical hypothesis:

**A + B first, C only if the hybrid adds measurable value.**

That means:

1. build software scene first
2. build cheap Pepper's Ghost proof
3. build cheap relief-projection proof
4. compare them using the same scene and controls
5. select Tier B architecture from measured results

## 13. Important terminology

For internal engineering documents:

**Heritage Time-Travel Theatre**

For public/demo language:

**Evidence-Aware Historical Landscape Experience**

Use "hologram" only when the actual optical/display implementation justifies the term.

## 14. Research basis

Current research reviewed during this pass includes:
- academic and educational Pepper's Ghost work
- commercial beamsplitter specifications
- museum projection mapping on historical/3D-printed models
- current display manufacturer information
- current Indian product/availability references

See W108 onward in the master website index.
