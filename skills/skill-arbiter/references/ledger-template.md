# Candidate ledger template

One file per signal: `.scratch/skill-candidates/<slug>.md`. Fill every field; a field you can't fill honestly is a DROP reason.

```markdown
# skill-candidate: <kebab-slug>

**Captured:** <YYYY-MM-DD> — <which session/feature>
**Verdict:** OPEN | DROP | CANDIDATE | PLANNER | IMPROVE-NOW (<skill>)

## Signal
<one of: repeated-dance | workaround | skill-bypassed | recurring-failure | user-friction>

## Evidence
<concrete, from THIS project: the 2+ occurrences, the detour, the quote, the corrections>

## Proposed direction
<one line: what an improvement/new skill would do — not the full design>

## Disposition
<what happened: edited <skill> v<x.y> (edit summary, audit result, revert conditions) |
 handed to /skill-planner on <date> | swept on <date> → <outcome> | declined because ...>
```

## Filled example

```markdown
# skill-candidate: contract-refresh-dance

**Captured:** 2026-09-12 — user-auth feature session
**Verdict:** OPEN

## Signal
repeated-dance

## Evidence
Twice in this project I regenerated the TS client from the OpenAPI spec by
hand (user-auth feature: typing out `npx openapi-typescript ...` from memory;
plane-plan feature: same, plus re-checking drift by diffing two files).

## Proposed direction
The /api-contract skill probably already has a regen step — bypassed both
times because I didn't remember it existed.

## Disposition
_(open)_
```

Note the example: "skill bypassed" signals usually resolve as an **IMPROVE-NOW description fix** (add trigger phrases), not a new skill — the arbiter's cheapest high-value outcome.
