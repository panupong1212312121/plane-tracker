# Python reference

Loaded by `code-style` Phase 2 when the stack is Python.

## Layout & naming (PEP 8)

- 4-space indent; `snake_case` functions/variables/modules; `PascalCase` classes; `UPPER_SNAKE` constants; `_leading_underscore` for module-internal.
- One concern per module; imports in three sorted blocks — stdlib, third-party, local (ruff isort enforces).

## Type hints

- Public functions always annotated; `from __future__ import annotations` at the top for forward references.
- `X | None` instead of `Optional[X]`; built-in generics `list[int]`, `dict[str, int]`; `Sequence`/`Mapping` in signatures, concrete types at construction.
- Pydantic `BaseModel` at boundaries (API schemas, config); `@dataclass` for internal value objects; `typing.Protocol` for structural interfaces.
- Strictness: `mypy --strict` on new modules; a legacy suppression is `# type: ignore[code]  # reason` — never bare.

## Docstrings (Google style, mandatory on public surface)

```python
def transfer_funds(src: AccountId, dst: AccountId, amount: Decimal) -> TransferReceipt:
    """Move `amount` between accounts and return the receipt.

    Args:
        src: Source account id.
        dst: Destination account id.
        amount: Positive decimal amount.

    Returns:
        The transfer receipt carrying the new balances.

    Raises:
        InsufficientFunds: If `src` cannot cover `amount`.
    """
```

- A one-line docstring only when the signature is fully self-explanatory; `Args/Returns/Raises` otherwise.

## OOP & structure

- Classes when state + behavior travel together; plain functions for pure transforms.
- Prefer composition and small protocols over deep inheritance; `ABC` only for a genuine interface contract.
- Decorators for cross-cutting concerns only (auth, retry, logging, caching), named `@verb_noun`, always `@functools.wraps`-wrapped.

## Async

- I/O-bound → `async def` end to end; blocking calls (`requests`, `time.sleep`) are forbidden inside async — `httpx` and `asyncio.sleep` instead.
- CPU-bound → stay sync; offload at the boundary with `asyncio.to_thread`.
- `uvicorn` / `asyncio.run` at the outermost layer only — never mid-stack.

## Errors

- Domain exceptions (`class InsufficientFunds(Exception)`), never bare `Exception`.
- Catch only what you handle; `except:` and `except Exception: pass` are forbidden.
- Log with context (`logger.exception`) at the boundary, then re-raise typed.

## Immutability defaults

- Return new structures instead of mutating a caller's list: `items = [*items, new]` beats `items.append(...)` on shared state.
- Value objects are frozen: `@dataclass(frozen=True)` / `NamedTuple`; pydantic models `model_config = ConfigDict(frozen=True)` at boundaries.

## Code smells (pass before closing a ticket)

- **Long functions** — > ~50 lines → split by step (parse → validate → persist).
- **Deep nesting** — 5+ levels → early returns (`if not user: return`).
- **Magic numbers** — named constants: `MAX_RETRIES = 3`, `DEBOUNCE_SECONDS = 0.5` (UPPER_SNAKE).
- **Comments** — self-documenting code preferred; a comment explains *why*, never restates the *what*.

## Test style

- AAA: Arrange–Act–Assert blocks in every test.
- Names describe behavior in plain English: `test_transfer_rejects_insufficient_funds` — never `test_works` / `test_transfer_1`.

## Tooling (wired into `just check`)

```bash
uv run ruff format .
uv run ruff check --fix .
uv run mypy .
```
