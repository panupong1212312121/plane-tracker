---
name: frontend-design
description: Build-time design craft for any UI work — act as the design lead when a landing page, dashboard, product UI, app shell, component, form, settings, or onboarding is actually built. Reads design.md tokens as constraints, grounds aesthetic direction in the product's subject matter, bans templated/"AI slop" tells (default gradients, system-ui as a choice, one-word accents, all-caps labels), and verifies the built surface in bounded browser passes (desktop + mobile together, batched fixes). Complements design-md (interviews the design system into design.md) — this skill is the craft at build time. Use when building or reshaping UI, making a bland surface bolder, or when the user says ออกแบบหน้าจอ/ทำให้สวย/ไม่เอา template. Not for backend-only work or non-UI tasks.
metadata:
  version: "1.1"
  author: local
---

# Frontend Design

Two design skills own different moments: `design-md` interviews the design system into `design.md` before grilling finishes; **this skill is the design lead at the moment UI is built**. Same client, same bar — a studio known for giving every product a distinct identity that is not mistaken for anyone else's.

## 1. Ground in the subject matter

Distinctive choices come from the product's world, not from design preferences. Before the first markup, name the subject, the audience, and the surface's primary job. If the brief doesn't identify them, derive them as a proposal and confirm. A toy's page and a financial dashboard must be aesthetically unrecognizable from each other — materials, industry vernacular, and the audience's job decide palette, type, and signature element. Build with the real content throughout (see Guardrails on lorem-ipsum).

## 2. Direction before markup

Write a one-paragraph aesthetic direction before the first component: palette personality, type personality, signature element, motion budget. If the optional `ui-ux-pro-max` CLI is available (`npx ui-ux-pro-max-cli`), query its database for style/palette/font-pairing candidates for the stack and adapt — never paste raw. Without the CLI, derive from the subject's world. **State which path was used** in the deliver report. If `design.md` exists, treat its tokens as the default direction (see Guardrails on conflicts).

## 3. Anti-slop — banned tells of a generated page

These are facts, not preferences — they are the commonest tells that a page was generated (governed by the universal rules in `anti-slop`):

- Default blue/purple gradients, centered hero with emoji, `system-ui` reached for as a *choice* (only as an explicit, stated fallback).
- Accenting one word/phrase in a headline (italic/bold/color); unnecessary all-caps for labels; unnecessary typographic labels above content.
- The default hero treatment (big number + small label + supporting stats + gradient accent) only when genuinely the best option.
- Type: one or two families, clearly distinct if two; a real type scale with intentional weights; line length < 80 characters (serif slightly longer, slightly more line-height); type as an active part of the design, never a neutral delivery vehicle.
- For the full 38-rule checklist (Hard Gates, Purpose Gates, Quality Locks) and the 4-block Delivery Gate, consult the `anti-slop` skill.

When a whole new surface is being shaped, render **2–3 complete first-screen aesthetic previews** (pattern shared with `frontend-slides`) and let the user pick by seeing. Single-surface work inside an existing system gets the direction paragraph; diverging from `design.md` needs user confirm (Guardrails).

## 4. Structural variety — vary the bones, not just the skin

Two pages built from two briefs must not share the same hero → 3-feature → CTA → footer rhythm (the tell of one template reskinned). Before markup, pick a **macrostructure** for this brief and name it in the direction paragraph (e.g. stat-led, editorial-led, doc-led, chat-led, map-led, split-rail) — the brief's primary job picks it, not habit. Cross-brief check: if this surface's section rhythm equals the last surface built in this project, re-pick. The content inventory decides section order; never copy a previous page's skeleton.

## 5. Pre-emit slop self-critique

After building, before showing the result, re-read the markup once against §3 and §4 and fix what trips: default rhythm, template cadence, gradient-by-default, accent-by-italic. Then run the bounded browser verification below.

## 6. Build, then verify in bounded passes

One batched browser pass — desktop and mobile together — checking: overflow, contrast, hierarchy, real content renders, signature element present. Batch every defect into one fix round, confirm with at most one more pass, then **stop**. Open-ended self-polish burns the user's money; this mirrors `verify-and-stop`'s no-scope-growth discipline, applied to aesthetics.

**Deterministic slop detection (when available):** `npx impeccable detect <target>` — 61 rules (side-tab borders, purple gradients, bounce easing, dark glows, line length, cramped padding, small touch targets, skipped headings). Run it on the built surface when the package is reachable; report the findings count + notable rules tripped. Ignore individual rules only for a named brand reason, recorded in the deliver report. Unavailable (no network) → state "impeccable detect skipped: offline" and rely on the manual pass. A clean run is evidence, not proof — it does not replace looking at the rendered page.

## Deliver

Report: the direction paragraph, macrostructure pick, tokens used/added (new tokens update `design.md` via `design-md` update mode), preview/screenshot paths, verification results per pass, slop self-critique result, impeccable detect findings (or skipped note), the design-database path used (CLI/local), and surfaces built. If the surface is new and going live, hand off to `ship-it`.

## Guardrails

- `design.md` tokens win by default — diverging needs user confirm; surface the conflict, never silently pick.
- Lorem-ipsum is banned as final content — placeholder only while real content is absent, stated in the report.
- Verification is bounded (≤ 2 passes total) — unlimited polish is banned.
- Never overwrite `design.md` silently — new tokens go through `design-md` update mode.
- Backend-only or non-UI work is not this skill.

## Provenance

- Extended v1.1 (2026-09-21) with deltas from `nutlope/hallmark` (MIT: structural variety / macrostructure pick, pre-emit slop self-critique) and `pbakaus/impeccable` (Apache-2.0: `npx impeccable detect` as optional deterministic verification). Neither upstream skill is imported in full — see the catalog note in `docs/agents/skills.md`.
