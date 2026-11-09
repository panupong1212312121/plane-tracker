---
name: fastmcp-server
description: Turn our app into an MCP server with FastMCP — analyze the app to decide which capabilities should become tools that other agents/apps can call, scaffold a typed FastMCP server (tools/resources/prompts with thin wrappers over real app functions), run and verify every tool with the fastmcp CLI (list/call, happy path + error case), then wire it into editor configs (mcp.json). Use when the user asks to สร้าง MCP server, expose app capabilities as MCP tools, "ให้ agent อื่นเรียกใช้ app เราได้", connect the app to Claude/Cursor via MCP, or mentions FastMCP. Not for consuming other people's MCP servers as a client (use the fastmcp-client-cli pattern directly) or for non-tool API design.
---

# FastMCP Server

An MCP server is the app's **control surface for agents**: the same capabilities the UI offers, as typed tools a model can call safely. Requires Python 3.10+ with `fastmcp` installed (`pip install fastmcp` — verify with `fastmcp version` first and give install steps when missing).

## 1. Analyze the app for tool candidates (evidence, not imagination)

From the repo's real entry points — route handlers, service methods, CLI commands, background jobs — list what the app can actually **do**: queries, mutations, exports, status checks. Then propose a tool list:

| Tool | Wraps (real function) | Kind | Destructive? |
| --- | --- | --- | --- |
| `get_order_status` | OrderService.get_status | read | no |
| `create_order` | OrderService.create | mutation | no |
| `purge_cache` | Cache.purge_all | mutation | **yes** |

Rules for the list:
- **Thin wrappers**: a tool body delegates to the app's existing function — no business logic duplicated inside the MCP layer.
- **Read-only first**: ship queries before mutations; destructive tools are listed but explicitly gated (Step 3).
- **Small surface**: start with ≤ 10 tools the demo story needs; grow on request. Every tool has `verb_noun` naming, typed parameters, and a docstring that says what it returns — docstrings become the tool descriptions agents read.

Present the table for user confirmation before scaffolding — which tools to expose is a product decision, not a technical one.

## 2. Scaffold the server

One `server.py` (plus the app imports) in the project, `FastMCP` instance named after the app:

```python
from fastmcp import FastMCP

mcp = FastMCP(name="myapp")

@mcp.tool
def get_order_status(order_id: str) -> dict:
    """Return order status and ETA for an order id."""
    return OrderService.get_status(order_id)  # thin wrapper — real logic lives in the app

if __name__ == "__main__":
    mcp.run()  # stdio by default; use transport="http", port=8000 for a networked server
```

- Typed parameters and return types on every tool (they become the JSON schema).
- Async functions where the app is async; no blocking calls inside `async def`.
- Secrets come from environment variables — never tool parameters; a tool that would need a secret as an argument is a design failure, re-think it.
- Resources (`@mcp.resource`) for readable state ("app://stats"), prompts (`@mcp.prompt`) only when a canned prompt is genuinely reusable.

## 3. Run and verify (every tool, both cases)

```bash
fastmcp dev server.py            # interactive inspector while iterating
fastmcp list server.py --json    # every listed tool must match the confirmed table
fastmcp call server.py get_order_status order_id=ORD-1      # happy path
fastmcp call server.py get_order_status order_id=DOES-NOT-EXIST   # error case
```

The gate: **every tool called once happy-path and once error-case** via the CLI (the `fastmcp-client-cli` pattern — list, then call). An error case must return a clean, informative message — never a stack trace to the agent. Type coercion is automatic (`limit=5` → int), so verify the schema, not string handling.

## 4. Destructive tools get a gate

Any tool flagged destructive in Step 1 takes a `dry_run: bool = True` parameter (or equivalent confirm step) and logs the action. The tool's description must state the blast radius plainly ("purges all caches — takes sites offline for ~seconds"). An agent calling it blind is the threat model: assume the caller read only the description.

## 5. Wire into the editor config

Add the server to the project `mcp.json` (and the user's editor config on request — Claude Code, Cursor, etc.):

```json
{ "mcpServers": { "myapp": { "command": "python", "args": ["path/to/server.py"] } } }
```

Then verify end-to-end: `fastmcp discover` shows it, `fastmcp list myapp` lists the tools from a clean shell. Record the exposed surface in an ADR (via `grill-with-docs` conventions) — what the app exposes to agents is an architecture decision.

## Deliver

Report: confirmed tool table vs. shipped tools, verification results per tool (happy + error), transport used, config files changed, and ADR path. State anything manual (editor restart to load the config).

## Guardrails

- Nothing ships that wasn't in the confirmed table — scope creep on an agent-facing surface is a security decision made silently.
- No secrets in tool parameters, tool output, or committed configs; mask in all reports.
- Destructive tools are gated and honestly described — a missing gate is a P0 finding, not a nice-to-have.
- Verification is via the fastmcp CLI against the real server, not "the code looks right" — a tool nobody called did not ship.
- Client-side usage of other servers is not this skill — follow the `fastmcp-client-cli` workflow (discover → list → call) directly.
