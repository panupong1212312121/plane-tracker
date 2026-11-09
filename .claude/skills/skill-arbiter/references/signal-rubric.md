# Signal rubric

## What counts (with evidence requirements)

| Signal | Evidence requirement | Typical first verdict |
| --- | --- | --- |
| Repeated dance (≥2x) | Point at both occurrences in this project | CANDIDATE (2x) → IMPROVE-NOW/PLANNER (3x+) |
| Workaround for missing capability | Name the detour and the direct path that does not exist | CANDIDATE — capability-level |
| Skill bypassed/fired wrongly | Name the installed skill + the request that ignored/misused it | IMPROVE-NOW (description fix) |
| Recurring failure corrected twice | Both corrections in the conversation/repo | IMPROVE-NOW (missing step/command) |
| User friction phrase | Quote it | Capture, then re-triage with rubric |

## What never counts

- One-off steps with no repetition evidence — DROP (honest drop, kept in ledger).
- User preferences ("I like dark themes") — belongs in `AGENTS.md`/`design.md`, not a skill.
- Project facts ("this app uses Supabase") — belongs in `CONTEXT.md`/ADRs.
- Hypothetical repetition ("someone might do this") — no evidence, no signal.

## Triage depth

- **IMPROVE-NOW** needs all three: LOCAL skill, ≤ ~30 lines, same trigger family, evidence from this session. Miss one → downgrade, don't negotiate.
- **PLANNER** when the ask is capability-level: "a skill for X" rather than "skill X is missing a step".
- **CANDIDATE** is the default under momentum — never interrupt a half-finished ticket to improve the hub; capture and move on.

## Concept provenance (adapted, markdown-light)

- **OpenSpace** — "evolve under control in real tasks": evolution signals arise from execution, routed through review. → the capture-first faucet.
- **SkillAdam** — test, learn, apply only validated changes. → IMPROVE-NOW protocol (edit + audit-gate + revert on FAIL).
- **skills-janitor** — janitor-value/janitor-swipe: skills carry a value assessment, declines stay visible. → ledger never auto-deletes; sweep re-triages with fresh counts.
- **SkillEvaluator** — tiered evidence: deterministic checks first, behavioral proof later. → audit-skills.ps1 as the cheap gate; `/skill-doctor` as the deep tier.
- **SkillHone** — prd → synthesis → evaluation → optimization as separate stages. → arbiter (capture) ≠ planner (decide) ≠ creator (author) ≠ doctor (grade).
- **agent-skills-platform** — governance: evidence, approvals, rollback. → user confirmation per edit; revert conditions in every ledger file.
- **AREX-Skill** — routing over a taxonomy with progressive disclosure. → boundary table below keeps each stage's trigger family distinct; hub review is per-area, not one mega-review.
- **SkillNet** — skill bundles stay SKILL.md + references. → this skill's format matches the hub's own conventions.

## Boundary

- vs **skill-planner**: arbiter *observes and triages* during work; planner *decides create/extend* from a user-facing ask. Arbiter's PLANNER verdict hands over the ledger file as planner's Step-1 input.
- vs **skill-doctor**: arbiter = lightweight, continuous, per-signal; doctor = heavy, on-demand, whole-hub, from real conversation history. Doctor's findings can seed arbiter-ledger entries.
- vs **skill-creator**: arbiter never authors; the handoff brief and lock entry are planner's/arbiter's, the writing is creator's.
