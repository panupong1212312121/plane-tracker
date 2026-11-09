---
name: skill-arbiter
description: Capture and triage self-improvement signals DURING real work — a manual step repeats twice, a workaround betrays a missing capability, a skill fires wrongly or gets bypassed, or a just-finished multi-step pattern will recur — then decide one of IMPROVE-NOW (small evidence-backed edit to a LOCAL skill), CANDIDATE (record for the periodic review), PLANNER (escalate to /skill-planner for a create-vs-extend verdict), or DROP. Use when you catch yourself doing the same dance twice in a project, the user says "ทุกทีเลย" / "why do I keep having to", or right after completing a recurring dance that deserves capture. Don't use when the user outright proposes a skill idea (that is /skill-planner), for periodic whole-hub grading from conversations (/skill-doctor), or for authoring SKILL.md content (/skill-creator).
metadata:
  version: "1.0"
  author: local
---

# Skill Arbiter

The hub improves itself through evidence, not vibes. This skill is the evidence faucet: it runs **during** ordinary work (vibe coding, `/implement`, anything), catches improvement signals at the moment they occur, and routes each one — cheap fix now, deferred candidate, planner escalation, or drop. An improvement observed is an improvement half-done; an improvement *captured* is never lost.

Signal rubric and provenance: [references/signal-rubric.md](references/signal-rubric.md) — read it when unsure whether something is a signal. Candidate ledger format: [references/ledger-template.md](references/ledger-template.md).

## Step 1 — Recognize the signal

A signal is real when it satisfies one of these **and** has concrete evidence from this project:

| Signal | Example |
| --- | --- |
| **Repeated dance** | Same 3+ manual steps done twice in this project (screenshot workflow, contract refresh, demo data reset) |
| **Workaround** | Doing something via detour because no skill owns it (hand-copying values, re-deriving a command from memory) |
| **Skill bypassed** | An installed skill covered this but was ignored — or fired on the wrong request |
| **Recurring failure** | Same mistake corrected twice (missed empty states, forgot `uv run` prefix, wrong directory) |
| **User friction** | "ทำอย่างนี้ทุกทีเลย", "why do I keep having to ask" |

**Not a signal:** one-off steps, user preference (→ `AGENTS.md`/`design.md`), project facts (→ `CONTEXT.md`/ADR), anything whose repetition you cannot evidence — say so honestly and drop it.

## Step 2 — Capture before deciding

Write the candidate to the ledger — one file per signal at `.scratch/skill-candidates/<slug>.md` (create the directory on first write), following [references/ledger-template.md](references/ledger-template.md). The capture is the minimal unit of progress: **a captured signal is a valid outcome even if the verdict is DROP.** Never hold a signal in memory across turns.

## Step 3 — Triage (first match wins)

1. **DROP** — fails the rubric, or the evidence is one-off. Mark the ledger file's verdict and stop.
2. **CANDIDATE** — real, but not now: mid-sprint context, needs evaluation you can't run, or repetition count is low. Leave the file for the **end-of-project sweep** (Step 5) and continue working. This is the correct default under momentum — "vibe coding ไปเจอทีหลังว่าควรมี skill" lands here.
3. **PLANNER** — the signal implies a *capability-level* ask (new skill, or heavy extend of an existing one). Invoke `/skill-planner` with the ledger file as input.
4. **IMPROVE-NOW** — all of: the fix targets an **existing LOCAL skill** (`local` source in `skills-lock.json`), the edit is small (≤ ~30 changed lines, same trigger family, no new sections), and the evidence is from this very session. Then Step 4.

Never IMPROVE-NOW an upstream-locked skill — route via PLANNER (companion skill). Never create a new skill directly from the arbiter — that decision belongs to `/skill-planner`.

## Step 4 — IMPROVE-NOW protocol

Apply SkillAdam's rule — only changes that survive verification land:

1. Read the skill's full `SKILL.md`; edit only what the evidence justifies (a trigger phrase added to the description, a missing step, a command to encode).
2. Bump `metadata.version` (patch).
3. Recompute the lock entry: `computedHash` = SHA256 of the edited `SKILL.md`; keep `source` string, append "(improved <date>: <one line>)" if the line changes materially.
4. Run `powershell -File scripts\audit-skills.ps1 -Skill <name>` — a FAIL result reverts the edit; a WARN is reported, not hidden.
5. Run `powershell -File scripts\sync-skills.ps1` so every agent directory sees the improvement.
6. Update the ledger file: verdict, edit summary, revert conditions. Report to the user what changed and why, in one paragraph.

## Step 5 — End-of-project sweep

When the user asks to review accumulated candidates (or at project close per `docs/agents/flow.md`):

1. Read every file in `.scratch/skill-candidates/` with verdict `CANDIDATE`.
2. Re-triage each against the rubric — repetition counts may have grown since capture.
3. Batch the PLANNER escalations (at most one new skill per sweep — let `/skill-planner` enforce it) and the IMPROVE-NOWs (with user confirmation for each edit).
4. Aggregate hub-level patterns (many bypasses of one skill = description problem; many candidates in one area = maybe one real capability) — for a graded, whole-hub verdict, this is where `/skill-doctor` runs.

## Guardrails

- **Capture is mandatory, improvement is conditional.** Evidence in the ledger first; edit only what survives verification.
- **Local skills only** for IMPROVE-NOW; locked skills route through `/skill-planner` (companion).
- **Small diffs:** an arbiter edit is a patch, not a rewrite — anything larger becomes a PLANNER escalation.
- **One capability, one candidate:** merge duplicated ledger files instead of stacking near-duplicates.
- The ledger never auto-deletes; DROP keeps the file with its verdict, so the sweep can see what was declined and why.
