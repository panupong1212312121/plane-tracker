---
name: autoharness
description: Self-learning skill layer. Distills lessons, workarounds, and user preferences from real agent conversations into durable skills with traceable evidence quotes, automated merging, and pruning.
---

# AutoHarness: Self-Learning Skill Distillation

Use AutoHarness to review conversation sessions and distill durable, reusable agent capabilities directly into the project's skill repository.

## When to Trigger

- User says `/learn`, "จำวิธีนี้ไว้", "อย่าทำแบบนี้อีก", or "สรุปเป็น skill ให้หน่อย".
- A complex non-trivial technique was successfully discovered after multiple iterations.
- An unexpected error required a specific workaround that future agent runs will hit.

## Distillation Discipline

1. **Extract Class-Level Lessons**:
   - Focus on reusable patterns, library idiosyncrasies, and architectural conventions.
   - Ignore one-off data typos or transient network failures.

2. **Verbatim Evidence Anchoring**:
   - Every distilled rule MUST link to a verbatim conversation quote or command output proving why the rule exists.
   - "Rule without evidence is speculation; rule with evidence is institutional memory."

3. **Cross-Check Existing Skill Hub**:
   - Read `skills/` first. If an existing skill covers the domain, propose an `EXTEND` or `PATCH` rather than creating a near-duplicate.
   - Follow the `/skill-planner` rubric in `docs/agents/skills.md`.

4. **Reconcile Conflicts & Prune**:
   - If a new lesson supersedes an old convention, identify the obsolete instructions and update them so the new rule wins cleanly.
   - Run `scripts/audit-skills.ps1` and `scripts/sync-skills.ps1` after modifying skills.
