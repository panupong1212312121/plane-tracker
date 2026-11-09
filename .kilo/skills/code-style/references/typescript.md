# TypeScript reference

Loaded by `code-style` Phase 2 when the stack is TypeScript.

## tsconfig baseline

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "moduleResolution": "bundler"
  }
}
```

## Naming

- `PascalCase` types/classes/components; `camelCase` functions/variables; `UPPER_SNAKE` constants.
- Files `kebab-case`; tests colocated as `*.test.ts` / `*.spec.ts`.
- Functions read as verb–noun: `fetchMarketData`, `calculateSimilarity`; predicates read as questions: `isValidEmail`, `hasAccess`.
- Booleans read as predicates: `isLoading`, `hasAccess`, `canSubmit`.

## Types

- `interface` for object shapes, `type` for unions and utilities; never `any` — `unknown` plus narrowing.
- Discriminated unions for state machines:

```ts
type FetchState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "ok"; data: T }
  | { status: "error"; error: AppError };
```

- Zod (or the repo's existing validator) at boundaries; infer types from schemas instead of hand-maintained twins.
- `satisfies` for config objects; `as const` for literal sets.

## Doc comments (JSDoc, mandatory on exported surface)

```ts
/**
 * Retry `fn` with exponential backoff.
 * @param fn - The operation to retry.
 * @param opts - Attempt count and base delay.
 * @returns The first successful attempt's value.
 * @throws {RetryExhaustedError} After `opts.attempts` failures.
 * @example
 * ```ts
 * const value = await withRetry(load, { attempts: 3 });
 * ```
 */
export async function withRetry<T>(fn: () => Promise<T>, opts: RetryOptions): Promise<T>
```

## Async

- `async/await` over raw `.then` chains; `Promise.all` for independent work — never an awaited call inside a loop unless order matters.
- A timeout on every external call; `AbortController` for cancellable work.
- No floating promises: handle rejection, or `void` prefix when intentionally detached.

## OOP & structure

- Classes only for genuine stateful services or framework requirements; prefer functions, closures, and discriminated unions.
- One export surface per module; barrel files only at package boundaries.

## Errors

- Custom `Error` subclasses carrying a `code`; never throw strings.
- Result-style (`{ ok: true; data } | { ok: false; error }`) at domain boundaries; exceptions for programmer errors.
- No empty `catch` — log with context, then rethrow or convert.

## Immutability defaults

```typescript
// PASS: build new values with spread — never mutate shared state
const updatedUser = { ...user, name: "New Name" };
const updatedItems = [...items, newItem];
const sorted = [...markets].sort((a, b) => b.volume - a.volume); // sort mutates in place — copy first

// FAIL
user.name = "New Name";
items.push(newItem);
```

## Code smells (pass before closing a ticket)

- **Long functions** — > ~50 lines → split by step (validate → transform → save).
- **Deep nesting** — 5+ levels → early returns:

```typescript
// PASS
if (!user) return;
if (!user.isAdmin) return;
if (!market?.isActive) return;
// do the work
```

- **Magic numbers** — named constants: `const MAX_RETRIES = 3;` `const DEBOUNCE_MS = 500;`

## Performance guardrails

- Memoize expensive computations/callbacks in React (`useMemo` / `useCallback`).
- `lazy()` + `Suspense` for heavy components.
- Queries select the needed columns with a `limit` — never `select('*')`.

## Test style

- AAA: Arrange–Act–Assert blocks in every test.
- Names describe behavior: `returns empty array when no markets match query` — never `works` / `test search`.

## Tooling (wired into `just check`)

```bash
bunx eslint . --fix
bunx prettier --write .
bunx tsc --noEmit
```
