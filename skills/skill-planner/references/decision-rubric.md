# Decision rubric

## Overlap classes

**COMPETING** — run the trigger test: if the user said the request out loud to an agent with only skill descriptions loaded, would the existing skill plausibly fire? If yes for the *same job*, it is COMPETING. Competing + local → extend it. Competing + upstream-locked → companion.

**ADJACENT** — some shared steps or vocabulary, but the trigger phrases differ (e.g. `security-review` "scan this code" vs `harden` "is my deployed app safe"). Adjacency is decided by triggers, not by topic similarity alone.

**ORTHOGONAL** — no shared trigger, no shared procedure.

## Thresholds

- **EXTEND** when: same trigger family AND the new content is ≤ ~30% of the resulting skill AND the skill stays one job. An extension that needs its own table of contents is really two skills.
- **CREATE NEW** when: orthogonal; or the extension would push the skill past one trigger family; or the delta is > ~30%.
- **COMPANION** when the match is upstream-locked: wrap, don't fork. The companion may *read* the locked skill's files and add local behavior (verification steps, platform notes) but must restate nothing it can reference.

## Edge cases

1. **Existing skill never fires** — usually a description problem, not a missing skill. Verdict: EXTEND-description (smallest possible edit: add trigger phrases + negative triggers), not a new skill.
2. **Competing local skills already exist** — propose consolidation (merge into the stronger one) before creating a third skill.
3. **Capability = existing skill + platform variation** (e.g. deploy locally vs deploy to GitHub later) — prefer an EXTEND with a mode/phase, not a parallel skill, unless the platform steps are more than half the workflow.
4. **Capability is knowledge, not procedure** — a `references/*.md` file inside the nearest relevant skill beats a new knowledge-only skill.
5. **User insists on a skill for a one-off** — build it, but record in the brief that it failed the gate; `/skill-doctor` will revisit it with real evidence later.

## Anti-patterns

- **Mega-skill** — many trigger families stapled together; splitting is almost always right.
- **Wrapper-for-wrapper** — a companion that only restates the locked skill; worthless.
- **Doc-as-skill** — a skill whose only act is "read this file"; put the file in `docs/` and link it instead.
- **Skill-for-everything** — if 5+ consecutive requests each produced a new skill, run `/skill-doctor` instead; the hub is drifting.

## Worked example (this skill's own creation)

Request: "a skill to decide create-new vs extend-existing" (inspired by luongnv89/asm's `find-me-skills` + the `should-this-exist` gate in its `skill-creator`).

- **Inventory**: `skill-creator` (anthropics/skills — **upstream-locked**) covers authoring/improving with an "update existing skill" footnote; `skill-doctor` (warpdotdev — locked) grades skills from conversation history; `find-me-skills` exists upstream in asm only, not installed here.
- **Classification**: the decide-step is ADJACENT to `skill-creator`'s update subpath, but that subpath is a footnote in a locked ~20KB file — extending means editing a locked file; `skill-doctor` needs conversation evidence, not a forward-looking request. No local skill owns "decide before authoring".
- **Verdict**: **CREATE NEW** (`skill-planner`) — different trigger (decide before authoring), both near neighbors upstream-locked, natural handoff chain: planner decides → creator authors → doctor grades.
