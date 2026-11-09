---
name: ship-it
description: Take a finished feature or app from localhost to a working production URL, then prove it works there — but LOCAL-FIRST by default. Modes — LOCAL (default) runs pre-flight checks, boots the production build locally, proves the main path with smoke tests and screenshots, and STOPS there; LIVE (explicit "go live"/deploy/put it online only) adds deploy to the platform that fits the stack (Vercel/Netlify/Fly/Cloudflare/container hosts) with env vars and migrations handled, and verification against the real URL. Use when the user asks to deploy, ship, publish, go live, put the app online, or check the production build is okay. Not for CI/CD pipeline design or long-running ops work.
---

# Ship It

Close the last gap: an app that works on the user's machine means nothing until **someone else can open a URL and use it**. Two modes — **LOCAL** (default: Phase 1 → Phase 2, stop there) and **LIVE** (only on an explicit go live: + Phase 3 → Phase 4). Each phase is a gate — never start a phase while the previous one is red, never declare success on a phase you didn't run.

## Process

### Phase 1 — Pre-flight (gate: clean checklist)

Run every check; report each as PASS / FIX / WARN with the file involved. Fix what is safe and mechanical; ask before anything opinionated.

**Secrets & config**
- No committed secrets: grep the working tree (not `.env.example`) for high-entropy strings, `sk-`, `AKIA`, `-----BEGIN`, hardcoded passwords, connection strings with credentials.
- `.env*` variants are gitignored; `.env.example` exists and lists every var the app reads — no missing entries, no stray ones.
- Third-party keys are read from env only; no client-visible key in frontend bundles (a key importable in browser code is a leak, flag it).

**Junk & rough edges**
- No `console.log`/`print` debugging statements in production paths (structured logging stays).
- No TODO/FIXME with unfinished logic on the paths being shipped; no dead feature flags defaulting off; no commented-out code blocks.
- Error states exist: 404 page (or router fallback), unhandled-rejection handler, form validation messages, empty states for lists.

**Works as built**
- Production build passes (`npm run build` / equivalent) — dev-mode-only success does not count.
- The production build boots and the main path works locally against the built artifact, not the dev server.

### Phase 2 — Local run (default stop point; gate: main path proven on the built artifact)

The default end state is a **verified local production run** — deploy only when the user explicitly says go live.

1. **Production build** — `npm run build` (or the stack's equivalent); report build time and output size. A red build is reported red with the failing log excerpt — never summarized away.
2. **Boot the built artifact** — the way production would run it (`npm start`/`node dist/index.js`/`python -m app`/container run), **not the dev server**.
3. **Smoke the main path on localhost** — the 2–3 critical flows, proved with actual checks (HTTP status, DOM assertion via headless browser, or API response body) using the same evidence rules as Phase 4.
4. **Screenshot key pages** — home + main-flow end state + the error page, against `design.md` tokens when it exists.
5. **Report** — what was verified locally (with evidence), WARN items deferred, and the next step in one line: "พร้อม go live เมื่อ user สั่ง — deploy ยังไม่เกิด"

Stop here unless the user explicitly asks to deploy. A LOCAL pass is a complete, shippable state — not a failure to deploy. With `/ci-cd` wired, these local gates are exactly what the pipeline runs on push — a LOCAL pass is the pre-push proof, and the pipeline's green run with a responding URL is the automated continuation of this phase.

### Phase 3 — Deploy (explicit go live only; gate: real URL responds)

Pick the platform from [references/deploy-platforms.md](./references/deploy-platforms.md) by stack; confirm the choice (and its cost tier) with the user before creating anything. Then:

1. **Provision** — create the project/service; connect the repo or use the platform CLI.
2. **Config** — set env vars from `.env.example` values the user provides (never paste user secrets into command output; use the platform's secret command or dashboard via `/wizard` if manual steps are needed).
3. **Data** — for databases: create the resource, run migrations against it, and confirm with a read-back. Migrations on production data get one explicit confirmation from the user first, always.
4. **Deploy** — trigger the build; watch it to completion. A red build is reported as red with the failing log excerpt — never summarized as "deployed".
5. **Custom domain** — only if the user asks; otherwise report the platform URL.

Report: URL, platform, build number/time, anything the user must do by hand (remaining env vars, DNS records).

### Phase 4 — Verify live (gate: smoke evidence, not vibes)

Against the **deployed URL**, not localhost:

- **Smoke the main path** — the 2–3 critical flows (e.g. load home → sign up → do the core action → see the result). Prove each with an actual check: HTTP status, DOM assertion via a headless browser if available, or API response body.
- **Screenshot key pages** — home and the main flow's end state. If the user has a `design.md`, compare against its tokens and responsive rules; report drift (wrong colors, broken mobile layout) as findings, not opinions.
- **Check the error surface** — visit a deliberately wrong URL; confirm the 404/fallback renders instead of a stack trace.
- **Resource check** — no 404 on bundled assets in the network log (or console); no mixed-content warnings if HTTPS.

### Deliver

End with a ship report: URL, what was verified and how, screenshots taken, WARN items deferred (with why), and what's still manual (e.g. DNS, third-party dashboard config). If any phase failed, stop there and fix before proceeding — a shipped-but-broken URL is worse than a delayed one.

## Guardrails

- Never echo secret values; mask them in all output.
- Destructive or irreversible actions (prod migrations, domain changes, deleting services) require explicit user confirmation at the moment of action.
- Report failures verbatim (status codes, log excerpts); a failed phase is never narrated as success.
- Free-tier awareness: state the expected cost tier before provisioning; don't enable paid features unasked.
