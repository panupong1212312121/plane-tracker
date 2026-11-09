# Renderer handoff — choosing and driving the diagram renderer

Decision table and the exact handoff contract for each renderer skill. `codebase-diagram` owns exploration and modeling; the renderer owns artifact quality.

## Decision table

| Reader's question | Type | Renderer | Notes |
| --- | --- | --- | --- |
| What are the parts and how do they connect? | architecture | archify | Components, boundaries, external services |
| What happens when a user does X? | workflow | archify | Steps with branches/failures |
| Order of calls between services for one request? | sequence | archify | One flow, actors as columns |
| Where does data come from and go? | dataflow | archify | Pipelines, ETL, lineage |
| Lifecycle of an order/job/ticket through states? | lifecycle | archify | State machine |
| Who owns what / reporting lines? | org chart | diagram-design | `type-org-chart` |
| Entities + relationships in the database? | ER / data model | diagram-design | `type-er` |
| What does a user feel across stages? | user journey | diagram-design | `type-journey` |
| Timeline of work / milestones? | Gantt / timeline | diagram-design | `type-gantt`, `type-timeline` |
| Value chain / build-vs-buy evolution? | Wardley map | diagram-design | `type-wardley` |
| Stack layers / environments? | layer stack | diagram-design | `type-layers` |
| Anything else on the 39-type list | per its selection table | diagram-design | Read its SKILL.md table |
| Diagram must live inline in markdown | Mermaid | direct emit | Both skills can redraw `.mmd` later |

Tiebreaker: interactivity/explorable HTML or brand marks → archify; print/slides/static editorial art or non-listed types → diagram-design.

## Handoff A — archify

Working directory: the archify skill folder (its CLI is `node bin/archify.mjs`, Node ≥ 18, no `npm install` needed — validators are vendored).

1. Choose the type; read **only** `schemas/<type>.schema.json`, `schemas/common.schema.json`, and one matching file in `examples/`.
2. Author the candidate JSON from the evidence summary: fresh stable IDs, domain wording from the codebase, one clear main path, ≤ 12 primary nodes, `meta.quality_profile: "showcase"`.
3. Validate after every edit and before handoff:
   `node bin/archify.mjs validate <type> <candidate.json> --quality showcase --json`
4. Final acceptance:
   `node bin/archify.mjs deliver <type> <candidate.json> <output.html> --quality showcase --json`
5. A non-zero exit is never "success". Repair only the diagnosed subject; a passing delivery freezes the spec — no edits afterward.

Brand marks are opt-in: only with a user-provided official URL (`node bin/archify.mjs brands capture "<url>" --json`). Never infer a brand from a role like "database".

## Handoff B — diagram-design

1. Read its `SKILL.md` selection table and pick the type; load only the matching `references/type-*.md`.
2. Brief it with the evidence summary (components, flows, boundaries, assumptions) — not with code dumps.
3. Its first-run style-guide gate will ask about brand tokens; let it run. For a non-tech audience ask for the editorial default (4/10 density) and jargon-translated labels.
4. Output is a self-contained HTML (SVG/PNG via its scripts when requested).

## Mermaid fallback

When the artifact must live inside markdown (README, PR, ticket):

- Architecture: `graph LR/TD` with subgraphs per boundary
- Sequence: `sequenceDiagram`
- State: `stateDiagram-v2`

Keep it ≤ 15 nodes; a diagram that needs scrolling is two diagrams. Either renderer skill can redraw the `.mmd` into a styled artifact later.

## Evidence summary template (paste into the handoff)

```
Components: <name — role — evidence file> (…)
Main flows: <1. …> <2. …> <3. …>
Boundaries: <what talks to what, and through what>
Assumptions: <explicitly unverified, with the reason>
Audience: <non-tech | dev | self> → density/jargon posture
```
