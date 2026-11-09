---
name: harden
description: Audit and fix the security POSTURE of a deployed or locally-running web app — the configuration layer the code scanners can't see — then prove access-denial dynamically against a URL the app actually serves (localhost by default; BaaS checks target the real BaaS project URL). Covers BaaS policies (Supabase RLS, Firebase rules), storage bucket publicity, CORS, admin route guards, rate limits on expensive endpoints, and security headers. Ends with live proof — requests without tokens must get 401, direct database queries must be policy-blocked. Use when the user asks "is my app secure", wants to harden the app, checks Supabase/Firebase security settings, or after /security-review or /security-audit findings mention access control. Not for source-code vulnerability scanning (use /security-review) or deep exploit audits (use /security-audit).
---

# Harden

The code scanners cover the source. This skill covers what they can't see: **the configuration layer that decides who gets in**, and the **live proof** that denial actually works. Three rounds, each a gate.

Skill split (already installed, escalate or delegate as noted):
- **/security-review** — source-code vulnerability scan (injection, secrets, deps)
- **/security-audit** — deep adversarial exploit audit of source
- **owasp-security** — the standards these posture fixes map to (A01 Broken Access Control, A02 Misconfiguration)
- **ship-it** — proves function (flows work, status 200); this skill proves **denial**

## Round 1 — Exposure map (gate: every entry point classified)

From the repo's evidence (manifests, config files, migration SQL, route registrations — not assumptions), build a table of every entry point:

| Entry point | Who can reach it | Auth enforced where | Data it touches |
| --- | --- | --- | --- |

Then classify the sensitive surfaces:
- **BaaS policies** — Supabase: `RLS enabled?` per table + read the actual policies; Firebase: rules file read and evaluated; storage buckets: public/private per bucket
- **API routes** — which mutations (create/update/delete, anything billed: LLM calls, email, SMS) have auth middleware, and where it's enforced (central middleware vs per-route vs nowhere)
- **Admin/staff surfaces** — what guards them beyond hiding links in the UI
- **Cross-origin surface** — CORS config, webhook signature checks, session/cookie flags (Secure, HttpOnly, SameSite)

Present the map with a plain-language verdict per row: **protected / unprotected / unknown**. "Unknown" is a finding — go read until it isn't.

## Round 2 — Posture fixes (gate: every P0 unprotected → protected)

Fix by tier, cheapest damage first, one explicit user confirmation before any change to a live project's policies:

- **P0 — strangers touching sensitive data:** enable RLS with deny-by-default policies on every Supabase table holding user data; Firebase rules deny-then-allowlist per path; storage buckets private unless the content is genuinely public assets; any unauthenticated route that mutates or bills gets auth middleware.
- **P1 — trust-boundary fixes:** admin routes guarded server-side (session check, not hidden links); CORS allowlist instead of `*` for credentialed endpoints; rate limits on expensive/billable endpoints (platform feature or middleware); webhook signatures verified.
- **P2 — hygiene:** security headers (HSTS, X-Content-Type-Options, X-Frame-Options/frame-ancestors, CSP baseline), cookie flags, verbose error suppression on client-facing responses, dependency audit via /security-review Step 2.

Map every fix to the OWASP requirement it satisfies (cite owasp-security's quick reference) and write it down — the fixes must outlive the conversation, so record anything architectural in an ADR via /grill-with-docs conventions.

## Round 3 — Dynamic proof (gate: denial demonstrated, not claimed)

Against a URL the app actually serves — **localhost by default** (boot the app locally; the app must be running, not just built). BaaS checks (Supabase/Firebase/storage) still target the **real BaaS project URL** — that exists without deploying anything. Production-URL proof happens only after an explicit go live via /ship-it:

1. **Unauthenticated mutation** — `curl` the most sensitive write endpoint with no token: expect 401/403. Show the actual status and body.
2. **Direct data access** — for BaaS: query the exposed table/API directly (the public project URL, no app in between): expect policy-denied. This is THE Supabase check — RLS in the dashboard means nothing until this returns blocked.
3. **Admin surface** — visit the admin route without a session: expect redirect/401, not rendered content.
4. **Expensive endpoint abuse** — no-token/bad-token calls to the billable endpoint: expect 401 then rate-limit if repeated.
5. **Headers check** — response headers from the home page match the Round 2 list.

Local-mode example (adjust to the repo's real endpoints — the commands are the pattern):

```bash
# 1) unauthenticated mutation → expect 401/403
curl -i -X POST http://localhost:3000/api/orders -H "Content-Type: application/json" -d '{}'
# 2) direct BaaS access (real project URL, no app) → expect policy-denied
curl -i "https://<project-ref>.supabase.co/rest/v1/profiles?select=*" -H "apikey: <anon-key>"
# 3) admin route without a session → expect redirect/401, not rendered HTML
curl -i http://localhost:3000/admin
# 5) headers from home page → match the Round 2 list
curl -I http://localhost:3000/
```

Every check: command + actual response. A check you couldn't run is reported as UNVERIFIED — with what's needed to verify it — never as pass.

## Deliver

Report: the exposure map (before/after), fixes applied with their OWASP mapping, the dynamic-proof log, and what remains UNVERIFIED or deferred. Offer the follow-up pair: /security-audit for the deep source-code exploit hunt, and a note that posture drifts — re-run this after adding any new table/route/bucket.

## References

- [references/platform-posture.md](./references/platform-posture.md) — per-platform evidence to read, posture checks, and dynamic proofs (Supabase, Firebase, storage, API routes, headers, rate limits). Load the section matching the repo's stack.

## Guardrails

- One explicit confirmation before changing policies on a live project's data — a wrong RLS policy can lock the app's own users out; state who keeps access before applying.
- Never apply deny-everything then walk away: after deny-by-default, verify the app's own normal flows still work (the app must keep working for its real users — that check is the difference between hardening and an outage).
- Report protection failures verbatim; an unprotected surface is never narrated as fixed.
- Don't scan source for injection/taint/secrets here — that's the scanners' job; keep this skill's scope on posture and denial proof.
