---
name: data-pipeline
description: Design and build a data pipeline like a data engineer — map sources → transforms → sinks with a contract on every edge (shape, frequency, volume, SLA), decide batch vs streaming and ETL vs ELT with written reasons, then build it with every stage idempotent and observable, and prove it end-to-end: sample data flows source to sink with in = out reconciled and a rerun that changes nothing. Hands the finished flow spec to /archify (dataflow renderer) for the diagram and persisted shape changes to /migration. Use when the user asks for a data pipeline, ETL/ELT, "ดึงข้อมูลจาก X ไป Y", "ออกแบบการไหลของข้อมูล", or moving data between systems on a schedule. Not for CI/CD of code (/ci-cd moves code, this moves data), drawing an existing dataflow (/archify, /codebase-diagram), schema shape transitions (/migration), or database modeling (/database-design).
---

# Data Pipeline

Data that moves without a contract fails on the first bad batch. Design the flow as edges with promises, build every stage idempotent, and prove the whole path with counts before calling it done.

Split of labor:

- **/ci-cd** — deploys code; this moves data. "Pipeline" overlaps as a word, not as an object.
- **/database-design** — models the stores at either end; this designs the movement between them.
- **/migration** — executes the persisted shape changes this pipeline's evolution forces.
- **/archify** — renders the designed flow as a dataflow diagram after the fact.
- **/mock-data** — seeds sample input when real data is not available yet.
- **/monitoring** — consumes the failure events and freshness signals this pipeline emits.

## Process

### Phase 1 — Edge contracts (gate: every edge has a promise)

| Edge | Shape | Frequency | Volume | SLA (freshness) |
| --- | --- | --- | --- | --- |

- Sources: who owns the data, how it may be read (full scan, CDC, webhook, API), and what breaks if its shape changes.
- Sinks: who reads downstream and the freshness they actually need — that answer decides batch vs streaming, not fashion.

### Phase 2 — Flow design (gate: decisions written with reasons)

1. **Batch vs streaming** — the freshness SLA from Phase 1 decides; a streaming stage nobody watches is a liability.
2. **ETL vs ELT** — transform at the edge or in the destination; prefer the destination when it can express the transform (cheaper to re-run).
3. **Idempotency + recovery** — every stage is safe to re-run: deterministic keys, upsert-or-replace writes, checkpoint per stage so partial failure resumes instead of duplicating.
4. Record the batch/streaming choice as an ADR when reversing it is expensive.

### Phase 3 — Build (gate: stages observable, stack-native)

- Implement with the repo's existing stack and scheduler conventions (the cron/queue/workflow tool already present — never import a new one silently).
- Every stage emits counts (read, written, rejected) and a failure signal /monitoring can route.
- Transformations are pure functions of input where possible — testable without the source.

### Phase 4 — Prove end-to-end (gate: in = out, rerun is a no-op)

```bash
just pipeline-run        # or the repo's own run command, seeded via /mock-data
just pipeline-check      # reconcile: sink count == source count - rejected
just pipeline-run        # a second run changes nothing — that is the idempotency proof
```

- Reconcile: sink count == source count − rejected; spot-check sample rows for shape conformance.
- Re-run the whole pipeline a second time: final state unchanged (no duplicates, no drift).
- Backfill note: how a missed window replays (the checkpoint makes it a range re-run, not a full resend).

### Phase 5 — Handoff

- Flow spec (edges + contracts + stages) → /archify `dataflow` renderer for the diagram.
- Persisted shape changes discovered while building → /migration.
- Failure signals + freshness checks → /monitoring wiring.

## Deliver

Report: the edge-contract table, the design decisions with reasons, stage observability (what counts/failures emit where), the end-to-end proof (counts + idempotent rerun), and the artifacts handed off. Missing reconciliation or a duplicate-y rerun is a red result — never narrated as shipped.

## Guardrails

- No stage ships without idempotency — a pipeline that duplicates on retry is not a pipeline.
- Never widen a source's read privileges to make a pipeline work; ask for a narrower contract instead.
- Secrets for sources/sinks come from env only, masked everywhere (same rule as /ci-cd and /ship-it).
- The second run changing anything is a failure, reported verbatim with the counts.
