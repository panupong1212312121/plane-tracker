---
name: database-design
description: Design a database like a system analyst — interview access patterns first (which queries, at what volume, growing how), then produce the conceptual ER model and the physical schema (tables/collections, columns/types, keys, constraints, indexes) that answers every stated query, and hand off the artifacts to the executors (ER content to /diagram-design or /archify for drawing, DDL + migration plan to /migration, entity mapping to /api-contract). The store choice (relational/document/key-value) is a deliberate trade-off recorded as an ADR when hard to reverse. Use when the user asks to design a database, schema design, "ออกแบบ database/ตาราง", make an ER model, or decide how data should be stored. Not for vocabulary and glossary work (/domain-modeling owns CONTEXT.md), executing a shape change (/migration), drawing the diagram (/diagram-design), or the API seam (/api-contract).
---

# Database Design

Schema follows usage, not intuition. Interview how the data will be read and written before drawing a single table, then design so every stated access pattern is answerable — and hand the result to the executors that already exist.

Split of labor:

- **/domain-modeling** — owns the glossary (`CONTEXT.md`). This skill consumes its vocabulary and never contradicts it; a term resolved there is binding here.
- **/migration** — executes shape changes compatibly. This skill produces the target shape and the migration plan; never edits live schemas directly.
- **/diagram-design**, **/archify** — draw the ER/dataflow artifacts after this design exists.
- **/api-contract** — the API seam; pair when endpoints expose the modeled entities.
- **/mock-data** — seeds the designed schema for tests and demos.

## Process

### Phase 1 — Access-pattern interview (gate: patterns listed before any table exists)

Ask until every row is concrete:

| Query (in app words) | Frequency | Volume now → in 1 yr | Latency need |
| --- | --- | --- | --- |

- Include writes too: what gets inserted/updated, how often, in which transaction group.
- Red flag to reject: "design it first, we'll figure out usage later" — a design that answers nobody is not a design.

### Phase 2 — Conceptual ER (gate: entities resolve against the glossary)

- Entities, relations (cardinality: 1-1, 1-N, M-N), and the business rules the relations encode.
- Every entity name comes from `CONTEXT.md` — a missing or conflicting term stops here and resolves through /domain-modeling first.
- State the store choice with its trade-off (relational vs document vs key-value); record as an ADR when it passes /domain-modeling's bar (hard to reverse, surprising without context, real trade-off).

### Phase 3 — Physical schema (gate: every access pattern is answerable)

- Tables/collections, columns with types, primary keys, foreign keys, constraints (unique, check, not-null), and indexes.
- Normalize to the level the access patterns justify; an intentional denormalization is a written decision, not an accident.
- **The proof step — for every access-pattern row, write the actual query the app will run and show the schema answers it (key path or covering index).** A pattern with no supporting path is a design failure: go back to Phase 2.

```bash
# the proof is real queries against the drafted schema, e.g.
psql "$DATABASE_URL" -c "EXPLAIN ANALYZE SELECT ... FROM orders WHERE customer_id = ..."
```

### Phase 4 — Handoff package (gate: the executors have what they need)

1. **ER content** → /diagram-design (ER/data-model type) or /archify — entities + relations in their input form.
2. **DDL + migration plan** → /migration — target shape plus the compatible path from the current one (the expand–contract sequencing it owns).
3. **Entity mapping** → /api-contract — which endpoints expose which entities, so the typed client and the schema agree.
4. Update `docs/adr/` with the store choice and any intentional denormalization.

## Deliver

Report: the access-pattern table, the ER summary, the physical schema artifact (path), the store-choice ADR, and the proof log (query → index/plan used per pattern). Anything unanswered in Phase 3 is reported UNRESOLVED — never shipped as "designed".

## Guardrails

- Never contradict `CONTEXT.md` vocabulary — a conflicting term goes back through /domain-modeling.
- Schema edits on live data belong to /migration, never to this skill.
- Intentional denormalization and store choice get written down (ADR) — unrecorded cleverness rots.
- Volumes implying sharding/partitioning are surfaced as explicit design items, never deferred silently.
