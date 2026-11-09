---
name: feasibility-study
description: Evaluate whether a project/idea is worth building at all — real users, impact, existing market alternatives, differentiation, and cost of building — and deliver a blunt build/extend/wontfix verdict with evidence. Runs AFTER an idea exists but BEFORE any build (before /pm-planner or /to-spec). Use when the user asks "ควรทำไหม", "มีคนใช้จริงไหม", "มีในตลาดแล้วทำไมทำใหม่", "feasibility", "worth building", or wants a go/no-go before investing effort.
---

# Feasibility Study

Answer one question bluntly: **ถ้าควรทำ ทำให้ดีกว่าของเดิมอย่างไร — ถ้าไม่ควร หยุดตอนนี้**. A study that says "everything is fine" is worthless.

## Step 1 — Pin the claim

Before researching, record what the project claims, in one paragraph: who it is for, what job it does, and what success looks like. If the user can't state this, that IS the first finding — interview-lite (≤5 questions, each with a recommended answer) until the claim is pinable.

## Step 2 — Research with evidence

For each axis, research then record evidence — market facts from web search, project facts from the repo, and estimates only where marked as estimates:

| Axis | What to establish | Evidence |
| --- | --- | --- |
| **Real users** | Who exactly uses this, how they do the job today, how painful it is | Interviews/user count the user provides; search for communities asking for the job |
| **Impact** | Time/money saved per user per week; frequency of the job | Estimate with stated assumptions |
| **Market** | Existing tools/services for the job, their pricing, stars/adoption, top complaints | Web search — name at least 3 alternatives or record "none found" as a finding |
| **Differentiation** | The honest answer to "ทำใหม่ไปทำไม": what this does that alternatives don't | One paragraph; if it's "same thing but free" or "mine", that's usually a wontfix signal |
| **Cost of building** | Effort (weeks via the repo's `/pm-planner` spine), running cost, maintenance burden | Estimate via repo spine, range not point |

Cite sources for market facts (URLs in the study file). Never invent adoption numbers or pricing.

## Step 3 — Verdict

Score the five axes honestly, then deliver exactly one of:

- **BUILD** — differentiated on at least one axis that matters to the user, cost fits, users reachable. State the one paragraph of "ทำไมทำใหม่ได้" a skeptic would accept.
- **EXTEND** — an alternative exists but misses a concrete gap; the cheaper move is building on/alongside it. Name the gap and the extension.
- **WONTFIX** — no differentiation, unreachable users, or cost dwarfs impact. State the strongest single reason and what would change the verdict.

A borderline BUILD must come with a **cheapest-test**: the smallest 1–2 day throwaway experiment (often a `/prototype`) whose result flips the verdict — with the flip condition stated ("ถ้าเทสแล้วไม่มีใครคลิกต่อ ยุบ").

## Step 4 — Record

Write `.scratch/<feature-slug>/feasibility.md` (create the directory if needed): claim, five-axis table with evidence, verdict, cheapest-test if borderline, and research URLs. If a grilling/wayfinding session exists for the same effort, link the study from that effort's `map.md` Decisions-so-far.

## Guardrails

- Verdict first in the file and in the chat — the user should not read five pages to find "wontfix".
- Estimates are labeled estimates; market facts carry sources. A claim without either is deleted from the study, not footnoted with "maybe".
- "มีคนใช้จริงไหม" is answered by the user's own reachable users first (their team, their community) — global TAM fantasies are not evidence.
- Do not proceed to planning or building on a WONTFIX verdict unless the user explicitly overrides after reading the strongest reason.
