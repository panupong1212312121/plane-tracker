---
name: api-contract
description: OpenAPI-first contract work between a Python backend and a TypeScript (or other-language) frontend — interview and draft the API contract as the single source of truth, scaffold an OpenAPI spec, generate a typed TS client from it, verify the backend code against the spec, and flag drift. Use when the user asks for an API contract, "contract ระหว่าง backend กับ frontend", TS client generation from OpenAPI, spec/code drift check, or cross-language API alignment.
---

# API Contract

The contract between two languages is not code on either side — it is the spec. When Python and TypeScript disagree, the spec is the truth; code that diverges is drift to be fixed, not a new truth.

## Workflow

1. **Interview the contract (new APIs).** If no spec exists: interview like `/grill-with-docs` but scoped to the API — resources, verbs, auth, pagination, error shape, IDs (string vs number), datetime format (ISO 8601 only), empty-list vs null semantics. Record decisions as one entry per endpoint. If a spec exists, extract it instead of interviewing.
2. **Write the OpenAPI spec first.** One file (e.g. `openapi.yaml`) at the repo root or the agreed location, before writing backend handlers or frontend calls. Single source of truth for: paths, request/response schemas, error responses (`4xx` shape documented, not assumed), auth scheme. Prefer `$ref` components over inline schemas so the same schema serves both sides.
3. **Generate the typed TS client from the spec.** Use the project's existing generator if configured; otherwise pick one and state why (`openapi-typescript` for types-only, `@hey-api/openapi-ts` for client+types). The generated file is a build artifact: commit decision must match the project's existing pattern, and regeneration must be one scripted command (e.g. `bun run gen:api`) — never hand-edit generated output.
4. **Verify the backend against the spec.** FastAPI: derive its OpenAPI output (`uv run python -c "from app.main import app; import json; print(json.dumps(app.openapi()))"`) and diff it against the committed spec — every path, schema name, and required field must match. Non-FastAPI backends: exercise each endpoint and assert actual responses satisfy the spec (status codes, required fields, types). A mismatch is a finding, not a silent fix.
5. **Wire the frontend to the generated types.** Handlers/fetchers consume the generated types — no hand-written response interfaces beside them. One response shape living twice (hand-written + generated) is the classic drift source; delete the hand-written one.
6. **Report drift with a verdict per endpoint.** For each finding: which side is wrong relative to the spec, the minimal fix, and who owns it. Changing the spec to match code is allowed only when the code is the desired behavior — then the spec change is the deliverable, and the TS client regenerates in the same pass.

## Guardrails

- The spec is checked into version control and changes go through the same review as code — a contract change is a breaking-change event for the other language.
- Never reconcile drift by editing the generated client or by quietly widening a backend response.
- IDs: string or number — pick once in the spec; JS `number` loses precision above 2^53, so big IDs are strings.
- If the stack is not Python+TS, the skill still applies: keep step 3's target language flexible (e.g. Rust/Go generators) and the rest is unchanged.
- Pair with `/verify-and-stop` for acceptance proof of the endpoint against the contract.