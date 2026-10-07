# Project Log

## Purpose

This is the chronological, append-only record for major Neer-Nilam project decisions and ideas.

We log:
- major concepts
- prompts sent to external AI/research systems
- important outputs and conclusions
- decisions and rationale
- assumptions
- rejected approaches
- milestones
- current project state

We do **not** log every coding command, dependency install, typo fix, or routine implementation step.

---

# 001 — Holographic / Immersive Neer-Nilam Concept

**Date:** 2026-10-07  
**Status:** Exploration → architecture direction

## Origin

The Neer-Nilam platform concept was expanded with the idea of presenting historical heritage through an immersive physical display.

The initial motivating experience is:

> Show the Thanjavur Brihadisvara Temple through historical time as an interactive 3D/holographic-style experience.

The intended result is not a decorative rotating 3D model. The experience should connect:

**time → monument → landscape → water systems → people/events → evidence**

## Key idea

A visitor should be able to select a historical period and see an evidence-aware representation of the relevant historical state.

Potential interactions discussed:
- timeline control
- physical rotary encoder
- gesture/depth-camera interaction
- external tablet/controller
- future AR/MR extensions

## Important constraint

The holographic installation should consume the same underlying Neer-Nilam data and API as the web platform rather than becoming a separate data silo.

## Historical integrity requirement

The project must distinguish:
- directly documented evidence
- archaeologically supported reconstruction
- scholarly interpretation
- AI-generated/provisional reconstruction
- speculative/uncertain representation

Historical uncertainty must be visible rather than hidden.

## DeepSeek research

DeepSeek was asked to deeply evaluate the concept across:
- holographic display technologies
- system architecture
- time engine design
- 3D asset pipeline
- interaction hardware
- evidence/provenance
- MVP
- prototype tiers
- budget
- risks
- innovation

See:
- `docs/ai-research/deepseek/001-prompt.md`
- `docs/ai-research/deepseek/001-output-summary.md`

## Current working conclusions from the DeepSeek analysis

1. The core innovation should be the **historical intelligence + evidence system**, not the optical display itself.
2. A Pepper's Ghost-style installation is a practical first physical prototype.
3. The physical installation should be a client of the same backend used by the main platform.
4. A physical rotary encoder is a stronger primary exhibition control than relying entirely on gestures.
5. Gesture/depth sensing can remain a secondary interaction mode.
6. The MVP should start with **one monument**, a few historical states, a small evidence set, and a small water layer.
7. True volumetric/light-field technology should not be promised as the pilot implementation.
8. Continuous historical morphing should generally be avoided when there is no evidence for the intermediate state.
9. The project should avoid blockchain and other technology added only for buzzword value.

## Decision status

These are **working directions, not final engineering decisions**.

They must be validated through:
- technical prototyping
- actual hardware testing
- source verification
- domain-expert review
- cost/availability checks

## Current state

**Concept:** approved for further investigation  
**Prototype:** not yet built  
**Hardware:** not yet purchased  
**Historical dataset:** not yet assembled  
**3D temple asset:** not yet selected  
**Backend/time engine:** not yet implemented  
**Expert validation:** not yet established

## Next major decision

Determine the first physical prototype architecture and validate the optical experience with the smallest possible proof-of-concept before committing significant budget.

---

*This log records project evolution, not a claim that every external AI recommendation is correct.*
