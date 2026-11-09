---
name: skill-planner
description: Decide whether a requested capability should become a NEW skill, an EXTENSION of an existing skill, a thin local COMPANION to an upstream-locked skill, or no skill at all — before anything is written. Scans the local skills inventory (skills/*/SKILL.md + skills-lock.json), classifies overlap against every existing skill, then hands off a written brief to /skill-creator. Use when the user proposes adding a skill, asks "should I create a new skill or extend an existing one", or has a fuzzy capability idea heading for /skill-creator. Don't use for writing or editing SKILL.md files (that is /skill-creator), grading skills from real conversations (/skill-doctor), or invoking skills to do product work.
metadata:
  version: "1.0"
  author: local
---

# Skill Planner

The gate before the workshop. One capability in, one verdict out — **NO-SKILL**, **EXTEND**, **COMPANION**, or **CREATE NEW** — backed by the actual inventory, not vibes. Cheapest correct outcome wins: a docs note beats a skill; extending a living skill beats a near-duplicate; a thin local companion beats editing an upstream-locked file.

## Step 1 — Capture the capability

Answer three questions from the user's request; ask only what the conversation doesn't already answer:

1. **What does it do** — the repeatable procedure or knowledge, in one sentence.
2. **When does it fire** — the user phrases / situations that should trigger it, and the near-misses that should NOT.
3. **What varies between runs** — inputs, artifacts, environment. If the answer is "nothing, it's a one-off", it is not a skill yet.

Red flags that mean "not a skill" on their own: it will be done once; it is a preference rather than a procedure (belongs in `AGENTS.md` or `design.md`); it is a fact about this project (belongs in `CONTEXT.md` or ADRs).

## Step 2 — Inventory scan

Run from the repo root:

```powershell
powershell -File scripts\audit-skills.ps1 -Inventory
```

This prints `name :: description :: lock-status` for every canonical skill. If the script cannot run (non-Windows shell), fall back to reading the frontmatter (`name:` + `description:`) of each `skills/*/SKILL.md` — descriptions only; full text comes later.

Build a shortlist of skills whose **purpose** or **trigger phrases** overlap the capability. Read the full `SKILL.md` of shortlisted skills only — never the whole hub.

For the shortlist, also read `skills-lock.json`: a `source` starting with `local` means free to edit; anything else (`github`, …) is **upstream-locked** — its `SKILL.md` must not be edited locally, because the next import would clobber the edit (the hash is pinned).

## Step 3 — Classify overlap

For each shortlisted skill, classify the capability against it:

| Class | Meaning | Test |
| --- | --- | --- |
| **COMPETING** | Same job, same trigger family | The existing skill's description would plausibly fire on the user's request |
| **ADJACENT** | Shares territory, different trigger | Some steps or phrases overlap, but the center of gravity differs |
| **ORTHOGONAL** | No meaningful overlap | Nothing in its description or workflow matches |

Record the class plus the lock status for every near neighbor. Full rubric and edge cases: [references/decision-rubric.md](references/decision-rubric.md).

## Step 4 — Verdict

Apply in order — first match wins:

1. **NO-SKILL** — the capability is one-off/conversational, or Step 1 hit a red flag. Write the guidance where it belongs (`AGENTS.md` note, `docs/agents/*.md`, ADR) and stop. A docs note is a valid, complete outcome.
2. **EXTEND** — a shortlisted skill is COMPETING (or ADJACENT with ≤ ~30% delta), the same trigger family genuinely fits, AND it is `local` in `skills-lock.json`. The brief specifies exactly which sections/commands to add; keep the existing name, bump `metadata.version`, keep the description one trigger family.
3. **COMPANION** — the matching skill is upstream-locked but the delta is real. Build a thin local skill that references the locked one (precedent: `codebase-diagram` bridges exploration to `archify`/`diagram-design`), or extend a neighboring local skill. Never edit the locked file.
4. **CREATE NEW** — the capability is ORTHOGONAL, or COMPETING-with-a-different-trigger-family that would bloat the existing skill. Pick a name that does not collide; the brief defines the boundary against every near neighbor it will be confused with.

Never output two new skills for one request. If the capability genuinely has two trigger families, say so and let the user split it.

## Step 5 — Handoff brief

Fill [references/handoff-brief.md](references/handoff-brief.md) and show it to the user for confirmation. Then, when they approve:

- **NO-SKILL** → write the docs note directly.
- **EXTEND / COMPANION / CREATE NEW** → invoke `/skill-creator` with the brief (it owns drafting, evals, and description optimization).
- After any skill lands: add or refresh its `skills-lock.json` entry (`source: "local (built: …)"`, recomputed `computedHash`) and run `powershell -File scripts\sync-skills.ps1` so every agent directory sees it.

## Guardrails

- Never edit an upstream-locked `SKILL.md` (non-`local` source in `skills-lock.json`).
- One capability in, one verdict out — resist scope creep into authoring; that is `/skill-creator`'s job.
- Duplicate or near-duplicate names are rejected: check the inventory before proposing.
- Every skill change ends with a `skills-lock.json` entry + `sync-skills.ps1`, or it did not happen.
