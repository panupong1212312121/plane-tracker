---
name: code-style
description: Write convention-conforming, idiomatic code and keep the repo's documented coding standards alive — first run interviews the stack and writes CONVENTIONS.md (naming, structure/OOP balance, type hints, docstrings, decorators, async rules, error handling, immutability, test style, code smells), then every implementation session loads the per-language reference (Python or TypeScript) and applies it while writing, runs a code-smell pass before closing a ticket, and wires format+lint+typecheck into `just check`, so /code-review's Standards axis has a documented target and /implement tickets produce orderly code by default. Use when the user asks to set up coding standards, "เขียน docstring/type hints ด้วย", "make code follow PEP 8 / standard style", "ตรวจ code smell", complains code is inconsistent, or starts implementing in a repo with no CONVENTIONS.md. Not for reviewing a diff (/code-review), orchestrating tickets (/implement), test-first discipline (/tdd), or security standards (owasp-security).
---

# Code Style

The reviewer can only check against a written standard. This skill writes that standard, loads the right idioms for the stack while code is being written, and keeps lint wired so order is enforced by the machine, not by mood.

Split of labor:

- **/code-review** — consumes `CONVENTIONS.md` on every review (Standards axis); this skill authors and updates it.
- **/implement** — orchestrates tickets; this fires during the writing for style decisions.
- **/tdd** — test-first discipline; style rules apply to test code too (same doc).
- **owasp-security** — same loading pattern, security domain; on conflict, security beats style.

## Process

### Phase 1 — Standards gate (first run in a repo, or when the doc drifted)

1. Detect the stack: languages, frameworks, existing lint config (`pyproject.toml`, `eslint.config`, `justfile`).
2. If `CONVENTIONS.md` exists: read it and propose updates only where the code disagrees with it (a drift report). If not: draft it in one pass covering —
   - **Naming** — files, classes, functions, variables, test files.
   - **Structure** — when classes vs plain functions; module layout; deep modules over shallow.
   - **Types** — where annotations are mandatory; the strictness level.
   - **Docs** — one docstring/doc-comment style for the house; what must be documented (public surface).
   - **Async** — when async is required; what must never block.
   - **Errors** — exception/error-result policy; what is never swallowed.
   - **Principles** — readability first, KISS/DRY/YAGNI; immutability as the default; self-documenting code preferred over comments.
   - **Tests** — test style: AAA structure (Arrange–Act–Assert), behavior-describing test names, same doc as product code.
   - **Code smells** — the smell checklist the team rejects: long functions, deep nesting, magic numbers.
   - **Format/lint** — the tools and their config, wired into `just check`.
3. Confirm the draft with the user before writing the file — standards are the team's, not the agent's.

### Phase 2 — Load the language reference (every writing session)

- Python → [references/python.md](references/python.md) — PEP 8 layout, type hints, Google-style docstrings, decorators, async idioms, dataclasses/pydantic, exception policy, ruff + mypy commands.
- TypeScript → [references/typescript.md](references/typescript.md) — strict tsconfig, naming, async/await idioms, error policy, JSDoc, eslint + prettier + tsc commands.
- A stack with no reference file yet: derive the style from the existing code plus the ecosystem standard, write it into `CONVENTIONS.md`, and note the gap for a future reference file.

### Phase 3 — Apply while writing (paired with /implement and /tdd)

- New code conforms by construction; a deviation is a conscious choice recorded in the ticket or PR description.
- Public surface (exported functions, class methods) carries docstrings with types — not optional.
- A **code-smell pass** closes every ticket: functions stay ≤ ~50 lines with early returns, no magic numbers (named constants), and shared state is never mutated where the doc requires immutability.
- Re-styling existing code rides along with a refactor only when /safe-refactor brackets the change.

### Phase 4 — Enforce (gate: `just check` green)

```bash
just check        # the wired gate: format + lint + typecheck (ruff/mypy, eslint/tsc)
```

- A style rule that can be checked by a tool gets wired in; only what a tool cannot check stays doc-only.
- Docstring presence on the public surface is spot-checked at review time by /code-review against the doc.

## Deliver

Report: `CONVENTIONS.md` path (created or drift-fixed), the reference loaded, the `just check` result, and any style deviations taken consciously. The doc is the artifact — everything else follows from it.

## Guardrails

- Standards are proposed, never imposed — the user confirms before `CONVENTIONS.md` lands.
- Never fight the existing style mid-ticket without /safe-refactor bracketing.
- Security rules (owasp-security) outrank style rules on conflict.
- The doc stays language-level; project-specific business rules belong in `CONTEXT.md`/ADRs.
