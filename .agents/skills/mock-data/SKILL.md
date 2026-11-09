---
name: mock-data
description: Generate realistic mock/synthetic data for testing, demos, and development — infer the schema from code/types/docs (or the user's description), generate with a seeded deterministic script, validate against constraints, and export to JSON/CSV/SQL/TypeScript fixtures. Use when the user asks for mock data, test data, sample data, seed data, fake users/orders/records, "ข้อมูลจำลอง", or wants a dataset for a demo without real data.
---

# Mock Data

Generate data that **passes the app's own validation** — mock data that the schema rejects is worse than no data. Everything flows from reading the real constraints first.

## Workflow

1. **Infer the schema from evidence.** In order: TypeScript interfaces / Pydantic / Prisma or SQL schema / Zod-Joi validators / API handlers / existing seed scripts / README. List every field with its real constraints (required, min/max, regex, enum, FK relationships, cross-field rules). Constraints found in code are facts; constraints you assume are labeled guesses in the output.
2. **Plan the shape, not just rows.** Decide before generating: how many records (default 50–100; honor an explicit user number), what edge cases must exist (empty strings, unicode/Thai text, boundary values, nulls where allowed), and the relationship topology (1:1, 1:N, cyclic refs, orphan rows for testing joins). A dataset of 500 happy-path rows tests nothing.
3. **Generate with a seeded script.** Write a small script (the project's language when known, else Python with `Faker`, else Node) with a **seed argument** so re-runs reproduce the same data. Use a real fake-data library for names/emails/addresses — never invent transliterated junk by hand. Respect PII: no real-looking national IDs, phone numbers, or card numbers unless explicitly requested and clearly fake.
4. **Validate the output.** Run the generated data through the project's own validator/schema if one exists (Zod schema, Pydantic model, DB constraint migration) — a load attempt into a scratch DB is the strongest proof. Fix the generator, not the data, when validation fails.
5. **Export where it's consumed.** Default `./fixtures/` or the project's existing seed location. Formats: JSON/JSONL, CSV, SQL INSERTs, or typed TS fixtures — match how the consuming code reads data. If the project has a seed command, wire the file to it rather than inventing a new one.

## Deliver

Report: file path(s), record counts per entity, the seed number, edge cases included, validation method (which schema passed), and how to regenerate ("`node scripts/mock-data.mjs --seed 42 --count 200`"). The generator script is the artifact — the data file is disposable; keep both in sync.

## Guardrails

- Never source fields from real personal data or scrape real users.
- Constraints read from code win over the user's summary when they conflict — surface the conflict, don't silently pick.
- Don't fabricate domain values that look real but break logic (e.g. a "paid" order with `paid_at: null`); generate state-consistent records.
- For ML/training datasets (SFT/DPO), this skill is not it — that pipeline has different quality gates.
