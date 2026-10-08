# Physical Proof Experiment Plan 001

Date: 2026-10-08
Status: Proposed
Purpose: Compare the two strongest low-cost physical representation tracks before Tier-B fabrication.

## 1. Experimental rule

Use the **same Neer-Nilam scene content** in every prototype.

Do not change the historical narrative to make one display look better.

The experiment is about presentation, not about changing the underlying evidence.

## 2. Track P1 — Pepper's Ghost

### Build
- existing monitor/laptop
- inexpensive clear reflector as baseline
- second reflector material if available
- rigid 45-degree frame
- matte-black hood
- printed calibration target
- simple physical controller

### Scene
- black background
- temple focal object
- terrain/context silhouettes
- water layer
- three supported-state placeholders only after the state records are approved
- explicit gap-state
- short labels only

### Measurements
Record:
- ambient illumination
- display brightness setting
- reflector type
- reflector dimensions
- reflector angle
- camera/viewer distance
- useful horizontal viewing arc
- useful vertical viewing range
- perceived image brightness
- double-image severity
- glare
- alignment error
- calibration time
- observer comprehension

### P1 pass criteria
The numbers below are experimental targets, not established facts:

- recognizable focal monument at target viewing distance
- water layer identifiable by most test viewers
- state change understandable without operator explanation
- optical image does not show distracting double images
- calibration repeatable by a second person
- evidence UI remains readable on the separate screen
- no dangerous exposed moving parts or unstable structure

## 3. Track P2 — Projection-mapped relief

### Build
- small physical Thanjavur/temple-area relief
- short-throw or ultra-short-throw projector
- projector mount
- darkened test surface/background
- physical controller
- separate evidence screen

### Physical model design
Do not start with a perfect architectural replica.

Start with the spatial structures required for the story:
- terrain
- temple footprint
- river/water context
- selected routes
- settlement massing

Optional details come later.

### Projection layers
Keep layers semantically separated:

L1 terrain
L2 water
L3 settlement
L4 routes
L5 monument/context
L6 event markers
L7 uncertainty/reconstruction treatment

### Measurements
Record:
- ambient illumination
- projector brightness setting
- throw distance
- focus condition
- projected alignment error
- surface occlusion
- readability
- setup/calibration time
- state-switch latency
- audience comprehension
- accidental shadows
- maintenance burden

### P2 pass criteria
Experimental targets:

- visitor understands that the physical object is the landscape
- visitor recognizes the temple location
- visitor recognizes water context
- state change is understood as a historical-state change
- projection remains usable for the planned exhibition lighting
- setup can be repeated without the original builder

## 4. Track P3 — Hybrid

Do only after P1 and P2.

Combine:
- physical relief
- projection layers
- optional Pepper's Ghost focal layer
- evidence display
- physical controls

The hybrid passes only if the optical layer provides a measurable comprehension or impact benefit large enough to justify added complexity.

## 5. Audience protocol

Each participant should be tested without a verbal explanation.

Ask:
1. What place are you looking at?
2. What changed?
3. What is the water layer showing?
4. Is the displayed reconstruction directly documented, interpreted, or uncertain?
5. Can you find the evidence record?

Record answers separately from operator observations.

## 6. Experiment log fields

experiment_id
date
hardware
scene_pack_version
software_commit
model_version
room_lux
display/projector settings
optical geometry
calibration version
operator
participant_count
observations
measurements
photos/video refs
failures
result
next_action

## 7. Stop conditions

Stop the experiment and redesign when:
- the structure is physically unstable
- heat/ventilation is unsafe
- exposed optics can cause injury
- projector/display hardware is being damaged by the mounting arrangement
- viewers consistently misinterpret uncertainty
- optical alignment changes during normal operation

## 8. Decision output

The experiment does not directly choose a product.

It produces:

P1 score
P2 score
P3 score

Then the team chooses:
- Pepper's Ghost
- relief projection
- hybrid
- flat-screen-only fallback

The same scene pack remains the source of truth.
