---
name: codebase-diagram
description: Turn a real codebase into a professional diagram a non-technical reader (or the vibe-coder themself) can absorb — system architecture, data flow, request sequence, deployment topology, or any editorial type. Explores the repo for evidence, derives a component/flow model, picks the right diagram type for the audience, then renders it through /archify (validated interactive HTML) or /diagram-design (editorial HTML/SVG/PNG). Use when the user asks to visualize or diagram a codebase, explain "how this app works", onboard onto an unfamiliar repo, or produce architecture visuals for docs or stakeholders.
---

# Codebase Diagram

Bridge a real codebase to a finished diagram. Neither reading code forever nor drawing from vibes: **evidence first, then model, then render through the specialist skill that fits.**

Two renderer skills are installed in this hub and this skill never draws pixel-level output itself:

- **`/archify`** — architecture / workflow / sequence / dataflow / lifecycle as interactive standalone HTML, built from a typed JSON spec with a 9-check validation gate. Needs Node ≥ 18.
- **`/diagram-design`** — 39 editorial diagram types (org chart, ER, journey, Gantt, Wardley, layers, …) as self-contained HTML/SVG/PNG with a brand style-guide gate.

## Process

### 1. Frame the question

One short question, only if the request is ambiguous: **who reads this** (non-tech stakeholder / new developer / the user themself) and **what should it show** (the whole system at a glance, or one specific flow). Default: whole system, non-tech-friendly.

### 2. Evidence sweep (read-only, timeboxed)

Orient, don't audit. Read only what answers "what are the parts and how do they talk":

- README, manifests (`package.json`, `go.mod`, `pyproject.toml`, `requirements.txt`, `pom.xml`), workspace configs
- Entry points, route/controller registrations, background-job definitions
- Folder topology (2 levels deep is usually enough), `docker-compose`/infra files, `.env.example` for external services

Cap this at ~15 minutes of tool calls. Track what you read: every component and connection in the model must cite a file, or be explicitly labeled an assumption.

### 3. Derive the model (before any drawing)

Write a 5–8 line evidence summary: the components (frontend / backend / jobs / databases / external services), the 2–3 main flows, and the boundaries. Show it to the user for a sanity check when the repo is large or the stakes are high. Distinguish clearly:

- **Evidence** — "Express routes registered in `src/server.ts` mount `/api/*` to the orders module"
- **Assumption** — "Postgres assumed from `DATABASE_URL` in `.env.example`; no query code read yet"

### 4. Pick the renderer

Follow [references/renderer-handoff.md](./references/renderer-handoff.md). The short version:

| The question is… | Renderer |
| --- | --- |
| "How is the system structured / how do requests flow / what happens when X" (architecture, workflow, sequence, dataflow, lifecycle) and interactivity is welcome | **archify** |
| Any of the 39 editorial types (org chart, ER/data model, journey, Gantt, Wardley, kanban, layers, …), or a hand-crafted branded look for print/slides | **diagram-design** |
| User explicitly wants diagram-as-text inside markdown | emit **Mermaid** directly (both skills can redraw it later) |

### 5. Non-tech pass (default on for non-tech audiences)

- Translate jargon to product language in labels ("auth middleware" → "ประตูตรวจสิทธิ์" / "login gatekeeper") — keep the technical term as secondary text where the renderer allows it.
- Respect the density ceilings: archify ≤ 12 primary nodes (`quality_profile: showcase`); diagram-design targets 4/10 density — the highest-quality move is deletion.
- Append a 3-bullet "how to read this diagram" caption next to the delivered file.

### 6. Deliver

Report: file path, how to open it (browser), what to look at first, and which claims were assumptions. Offer the natural follow-up: "want to zoom into flow X as a sequence diagram?"

## Guardrails

- Never present an assumption as a fact; the model step marks them.
- Do not bypass the renderer skills' own quality gates (archify's `validate` → `deliver` receipt; diagram-design's style-guide gate). Their word is final on artifact quality.
- If the codebase is too large to orient in the timebox, diagram the one subsystem the user cares about and say so.
