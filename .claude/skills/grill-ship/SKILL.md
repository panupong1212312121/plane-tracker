---
name: grill-ship
description: Hard, blunt post-completion critique of a finished product, build, or feature — audit what shipped and grill what is missing, broken, or overbuilt. This is the reverse of /grilling (which interrogates a *plan* before building): this interrogates the *artifact* after building. Use when the user asks "ตรวจผลงาน", "จี้งานที่เสร็จแล้ว", "what did we miss", "critique the result", "ผลงานเสร็จแล้วมีข้อเสนอแนะอะไรบ้าง", or wants a blunt gap review after /ship-it or /implement.
---

# Grill Ship

The work claims to be done. Your job is to prove or disprove that with evidence and blunt questions — not polite review. **Critique the artifact, never the person.**

## Phase 1 — Audit silently (evidence first)

Never grill from vibes. Read the deliverable and gather findings before asking anything:

- What the user asked for vs. what exists — every dropped requirement is a finding.
- Run it / open it if runnable (build, tests, the HTML, the URL). A failure is a finding, verbatim.
- The gap surface: error states, empty states, mobile, accessibility, missing README, missing `.env.example`, leftover debug code, hardcoded values, TODO on shipped paths.
- Claims made anywhere (report, comments, chat) that the artifact cannot back up.
- What is **overbuilt** — features nobody asked for, abstraction with one caller, config nobody sets. Overbuilt is as off-target as missing.

Sort findings: 🔴 broken (blocks the purpose), 🟡 missing/overbuilt (worth doing soon), 🟢 fine (say so briefly — blunt does not mean only-negative).

## Phase 2 — Grill in rounds

Work like `/grilling`: ask the whole **frontier** in one round, numbered, each with your recommended answer, then wait. A question whose answer depends on another open question waits for the next round. Facts you can look up in the repo are never questions — find them yourself.

Each question must be **jeep** (จี้): pointed at a gap with a decision hanging on it, e.g.

- "🔴 เมื่อ user กด submit โดยที่ input ว่าง — UI รายงาน success ทั้งที่ไม่มีอะไรเกิดขึ้น แก้เป็น inline validation ตอนนี้เลยไหม? ➡️ ใช่ แก้ก่อนอย่างอื่น"
- "งานนี้ไม่มี empty state เมื่อ list ว่าง — เดโมได้จริงไหมถ้า user ใหม่มาเจอหน้าว่าง? ➡️ ไม่ ต้องเพิ่ม empty state ก่อน ship"
- "มี feature X ที่ไม่มีใครขอ 3 วัน dev ต่อ — ตัดทิ้งหรือเก็บไว้? ➡️ ตัด ย้ายไป backlog"

A round covers, in order: 🔴 broken first, then 🟡 gaps (missing > overbuilt), then scope honesty ("ถ้าต้องเดโมให้ลูกค้าจริงพรุ่งนี้ อะไรต้องเพิ่มทันที อะไรตัดทิ้งได้"). Three rounds maximum — after that, remaining items go to the backlog instead of endless questions.

## Phase 3 — Record and act

- Append a `## Comments` section to the feature's issue file per `docs/agents/issue-tracker.md`: verdict, 🔴/🟡 findings with file references, and the user's decisions. If there is no `.scratch/<feature-slug>/` directory, create the record file there first.
- 🔴 broken items found: offer to fix now (in act mode) with `/surgical-patch` or `/implement` — never silently fix opinionated things.
- 🟡 items: add to the backlog as issue files, or fold into the spec if the user wants them in-scope.
- End with a verdict in one paragraph: what the artifact is ready for, what blocks it, what was explicitly decided out.

## Guardrails

- Blunt, not cruel: critique code and decisions with file references, never the user.
- Never soften a 🔴 into "minor issue" — report failures verbatim.
- Never declare "looks complete" on a phase you didn't audit; a gap you didn't check is a 🟡 finding about your own audit.
- Facts are yours, decisions are theirs: put every 🔴/🟡 disposition to the user and wait.
