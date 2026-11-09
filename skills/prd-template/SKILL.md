---
name: prd-template
description: Turn a sharpened plan into a Product Requirements Document using the right-sized template — pick among Lean PRD (small features), Comprehensive PRD (standard features), Amazon PR/FAQ (new products, working backwards), and Google PRD (data-driven, metrics-first) — fill it only from what /grill-with-docs and /to-spec already produced, attach the review checklist, and publish to .scratch/<feature>/prd.md (or a Plane page via /pm-planner materialization). Use when the user asks for a PRD, "เขียน PRD", a PR/FAQ document, or a requirements doc for stakeholders — after the plan is sharp. Not for the interview itself (/grill-with-docs), the implementation spec (/to-spec), the go/no-go verdict (/feasibility-study), or the project timeline (/pm-planner).
---

# PRD Template

A PRD is a communication artifact, not a working spec — it carries the problem, metrics, requirements, and scope for people outside the implementation loop. The thinking already happened in `/grill-with-docs` (ADRs + `CONTEXT.md`) and `/to-spec` (`spec.md`); this skill shapes that output into the right document.

Split of labor:

- **/grill-with-docs** — interviews until the plan is sharp; this skill only packages its output.
- **/to-spec** — the implementation-facing spec at `.scratch/<feature>/spec.md`; the PRD cites it, never duplicates it.
- **/feasibility-study** — the go/no-go verdict; a PRD assumes BUILD was decided.
- **/pm-planner** — materializes the PRD as a Plane page when stakeholders work there.

## Process

### Phase 1 — Pick the template (gate: size + audience named)

| Template | Use for | Length | Audience |
| --- | --- | --- | --- |
| Lean PRD | small features, enhancements, well-understood problems | 1–2 pages | engineering team |
| Comprehensive PRD | standard features, customer-facing changes | 3–5 pages | cross-functional team |
| Amazon PR/FAQ | new products, major bets, pitching up | 1–2 page PR + 2–4 page FAQ | customer-first review |
| Google PRD | data-driven products, cross-team initiatives | 5–10 pages | teams + leadership |

Default: Lean when in doubt — start lean, expand only the sections that need depth. Skip the PRD entirely for trivial changes, throwaway prototypes, and one-person side projects — a `/to-spec` spec or a single issue is enough there.

### Phase 2 — Fill from existing decisions (gate: no new decisions invented)

Every section is filled from what already exists — problem from `/feasibility-study` + grilling, domain terms from `CONTEXT.md`, technical constraints from ADRs, scope from `/to-tickets`. Inventing new scope here is a red flag: route it back through `/grill-with-docs`.

Core sections every template keeps (the floor):

- **Problem statement** — who hurts, how much, evidence (or flagged assumptions).
- **Goals + success metrics** — specific and measurable; non-goals for the Google style.
- **Solution summary** — the user flow at a readable altitude, citing `design.md` tokens when UI-bearing.
- **Requirements** — each testable, with acceptance criteria (they become `/to-tickets` checks).
- **Out of scope** — explicit; scope creep after approval requires a PRD amendment.
- **Launch plan + risks** — what ships when, and what could break.

### Phase 3 — Review checklist (gate: every box checked or consciously waived)

- [ ] Problem clearly stated with evidence or flagged assumptions
- [ ] Success metrics specific and measurable
- [ ] Requirements testable with acceptance criteria
- [ ] Out of scope explicit
- [ ] Decisions + rationale captured (ADR links, not inline essays)
- [ ] A new teammate could read it cold and understand the what + why

### Phase 4 — Publish

- Write to `.scratch/<feature-slug>/prd.md`, next to the spec it summarizes.
- When stakeholders work in Plane: materialize as a project page via /pm-planner's materialization trigger, cross-linked to the tickets.
- Skeletons: [references/templates.md](references/templates.md) — the four templates, copy-paste-ready.

## Guardrails

- No new product decisions inside a PRD — decisions belong to /grill-with-docs and ADRs.
- Never fabricate evidence or metrics; unknowns are flagged assumptions to validate.
- The PRD never replaces `spec.md` — different audience (see /to-spec).
- Templates adapt to context; problem statement, metrics, and out-of-scope are never removable.
