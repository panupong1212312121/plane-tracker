# PRD templates

Copy-paste skeletons for `/prd-template`. Fill from existing decisions only — no new scope invented here (SKILL.md Phase 2).

## Lean PRD (1–2 pages)

```markdown
# PRD — <Feature>

## Problem
**Who**: <segment>  **Pain**: <from their perspective>  **Impact**: <cost if unsolved>
**Evidence**: <data/quotes — or "assumptions flagged below">

## Success metrics
- <metric> reaches <target> by <date>

## Solution
<2–4 sentences + the user flow>

## Requirements
| # | Requirement | Acceptance criteria |
|---|---|---|

## Out of scope
- <explicitly not building>

## Launch
<what ships, when>
```

## Comprehensive PRD (3–5 pages)

Same floor as Lean, plus:

```markdown
## Background
<context: why now, what came before, ADR links>

## User stories
As a <role>, I want <capability>, so that <benefit>.
- Acceptance criteria: <checkable conditions>

## Non-functional requirements
<performance, security, accessibility, data-retention>

## Risks + mitigation
| Risk | Mitigation | Owner |
|---|---|---|

## Open questions
<each with who decides and by when>
```

## Amazon PR/FAQ (1–2 page PR + 2–4 page FAQ)

```markdown
# <Product> — press release (imagined, written first)

**<Headline>** — <one-sentence summary>

**The problem:** <customer pain, from their perspective>
**The solution:** <what ships, customer-visible>
**Customer quote:** <imagined user, concrete>
**Getting started:** <first step a customer takes>

## FAQ
- Who is the customer, and what is their real problem?
- Biggest risk, and how do we know it is survivable?
- How do we know they will adopt (or pay)?
- What does it cost to build and run?
- What would we cut first?
```

## Google PRD (5–10 pages)

Same floor as Comprehensive, plus:

```markdown
## Objectives
**Goals:** <outcomes, not features>
**Non-goals:** <explicitly not pursuing — drains scope creep>

## User benefits
<per benefit: the measurable user-visible delta>

## Success criteria
| Criterion | Baseline | Target | Measured by |
|---|---|---|---|

## Technical design summary
<link ADRs; constraints the implementation must respect>

## Cross-team dependencies
<who blocks whom, by when>

## Scalability plan
<what breaks first at 10x, and the plan for it>
```

## Review checklist (same gate as SKILL.md Phase 3)

- [ ] Problem stated with evidence or flagged assumptions
- [ ] Success metrics specific and measurable
- [ ] Requirements testable with acceptance criteria
- [ ] Out of scope explicit
- [ ] Decisions + rationale captured (ADR links)
- [ ] A new teammate could read it cold and understand the what + why
