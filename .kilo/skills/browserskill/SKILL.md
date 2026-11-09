---
name: browserskill
description: Real browser driving and session reuse for AI coding agents using BrowserSkill (Tencent/BrowserSkill). Allows agents to attach to existing authenticated user browser sessions (borrow-tab model) via bsk CLI and extension, performing live smoke testing, production UI inspection with actual user permissions, post-deploy live verification (/ship-it Phase 4), and anti-denial security checks (/harden). Complements headless Playwright testing by testing against real authenticated browser tabs without mock credentials. Use when live authenticated browser interaction is required, during post-deploy verification on production, or when inspecting session-gated UI.
metadata:
  version: "1.0"
  author: local
---

# BrowserSkill (Real Browser Driving & Session Reuse)

BrowserSkill (Tencent/BrowserSkill) connects AI coding agents to real, already-authenticated browser tabs via a lightweight CLI (`bsk`) and browser companion extension. Unlike headless Playwright runners that boot fresh, unauthenticated incognito sessions, BrowserSkill operates on the **borrow-tab model**: the agent interacts with existing browser tabs containing real human logins, cookies, and state.

## Boundary: BrowserSkill vs Playwright

| Dimension | Playwright (`/tests`, `/ci-cd`) | BrowserSkill (`/browserskill`, `/ship-it`) |
| --- | --- | --- |
| **Execution Mode** | Headless, isolated, deterministic | Live user browser, headful |
| **Authentication** | Seeded test tokens / fixtures | Active human session / SSO |
| **Environment** | Local unit/E2E test suite, CI pipelines | Staging & Production live verification |
| **Primary Owner** | Automated testing & CI gates | Post-deploy smoke test, access audits |

## CLI Commands

The `bsk` CLI interacts with the BrowserSkill daemon and extension:

```bash
# Verify connection to browser daemon
bsk status

# List open browser tabs available for inspection
bsk tabs list

# Attach to an active tab by URL pattern or ID
bsk attach --url "https://app.example.com/*"

# Capture visual snapshot of the current viewport
bsk screenshot --output .scratch/browser-snapshots/smoke-prod.png

# Query DOM state or read active accessibility tree
bsk dom inspect --selector "#user-profile-card"

# Trigger synthetic interaction on target tab
bsk click "#verify-billing-btn"
bsk type "#notes-input" "Automated verification pass"
```

## Workflows

### 1. Post-Deploy Live Smoke Verification (`/ship-it` Phase 4)

1. Verify deployment cutover has completed.
2. Run `bsk status` to confirm user has opened the target staging/production URL.
3. Attach to the tab using `bsk attach --url "<target-url>"`.
4. Inspect key dashboard elements, API response status codes in network tab, and session cookies.
5. Take a verification screenshot and record visual evidence in the deployment report.

### 2. Live Access Control & Anti-Denial Audit (`/harden`)

1. Inspect how role-based UI elements behave under real user authentication.
2. Verify that restricted action buttons or administrative menus remain hidden or correctly disabled for non-admin accounts.
3. Validate session timeout notifications and CSRF tokens in actual browser storage.

## Guardrails

- **Zero Credential Theft:** Never extract, dump, or log sensitive user session tokens, passwords, private keys, or raw cookies into conversation logs or files.
- **Explicit Confirmation for Destructive Actions:** Never execute state-mutating clicks (e.g. "Delete Project", "Transfer Funds", "Cancel Subscription") without explicit interactive user approval.
- **URL Sanity Check:** Always verify the active tab URL before issuing click or keyboard commands to ensure actions are not executed on unintended personal tabs.
- **Fallback to Headless:** When running in automated CI environments or unattended background tasks, always route to headless Playwright.

