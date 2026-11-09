---
name: skill-optimize
description: Run the bounded self-optimization loop for LOCAL skills — propose one small evidence-backed edit, validate it with SkillEvaluator gates (Tier 1 at minimum), and accept the edit only when the held-out score improves — then bump version, lock, and sync. Use when /skill-planner hands off a brief that includes optimizing an existing local skill, when /skill-arbiter IMPROVE-NOW grows beyond a one-line patch, or when the user asks to optimize/ปรับ skill ด้วยหลักฐาน. Not for authoring new skills from scratch (/skill-creator), grading from conversations (/skill-doctor), deciding whether a skill should exist (/skill-planner), or anything touching upstream-locked skills (route via /skill-planner companion instead).
metadata:
  version: "1.1"
  author: local
---

# Skill Optimize

SkillOpt's discipline (arXiv:2605.23904), adapted to this hub: the skill document is external state of a frozen agent; the agent proposes **bounded edits**; an edit lands **only when a held-out score improves**. Feelings are not scores. SkillAdam (arXiv:2609.08944) adds the acceptance discipline this loop inherits: test the current skill on representative tasks first, derive the revision from observed failures (not taste), apply the smallest change that addresses them, and keep a revision only when it passes the same validation as the baseline.

## Loop (bounded — max 3 cycles per session)

1. **Inputs** — a planner brief or arbiter ledger file + the target LOCAL skill (local in skills-lock.json). Upstream-locked target? Stop and route via /skill-planner.
2. **Baseline** — run SkillEvaluator on the skill and record the gates/score:
   `skillevaluator validate skills/<name> --checks schema,pii,license,quality,unicode,lint --no-dedup`
   Tier 1 is keyless and free. No eval set yet? `skillevaluator create-eval-dataset` (needs a provider — confirm quota with the user before spending).
3. **Propose** — ONE bounded edit per cycle (add/delete/replace a section, ≤ ~30 lines), justified by the ledger evidence. Multiple ideas = multiple cycles, not one mega-edit.
4. **Validate** — re-run the exact same command. **Accept only when the score/gates improve** — or when equal, only for an explicitly justified repair (e.g. dead-link fix). Otherwise revert and record the rejected edit.
5. **Record** — append to the ledger file: diff summary, before/after scores, accept/reject. Append-only; never edit past records.
6. **Ship** — bump `metadata.version`, recompute `computedHash` in skills-lock.json, run `scripts/audit-skills.ps1 -Skill <name>`, then `scripts/sync-skills.ps1`.

## Guardrails

- Accept-only-on-improvement is the whole point; "feels better" is not a score.
- Never weaken a skill's guardrail/safety sections to make gates easier to pass — a gate that gets cheaper to pass is a finding, not a win.
- Tier 1 is free and mandatory; Tier 2/3 spend provider quota — user confirmation required first.
- Upstream-locked skills are out of scope entirely.
- If 3 cycles can't produce an accepted edit, stop and report the trajectory — persistent failure is information for /skill-planner, not fuel for a 4th cycle.
