# Platform posture playbook — BaaS-specific checks and fixes

The config-layer checks per platform, with the exact evidence to read and the dynamic proof to run. Read the section matching the repo's evidence.

## Supabase

**Evidence to read:** migration SQL (`supabase/migrations/*.sql`) for `CREATE TABLE` / `ENABLE ROW LEVEL SECURITY` / `CREATE POLICY`; `supabase/config.toml` for exposed schemas.

**Posture checks (Round 1):**
- Every table holding user data: `ENABLE ROW LEVEL SECURITY` present? (default is **off** — a table without it is fully readable by anyone with the public anon key)
- Policies: deny-by-default present? (`FOR SELECT USING (auth.uid() = user_id)` shape per table) — a `FOR SELECT USING (true)` policy on a user-data table is public data
- Exposed schemas: only `public` should be exposed; `auth`/`storage` schema exposure is a finding
- Service-role key: server-only (never imported in frontend code, never in client-visible env vars)

**Dynamic proof (Round 3):** query the table through the public REST URL with the anon key and no session: `curl "$PROJECT_URL/rest/v1/<table>?select=*" -H "apikey: $ANON"` — expect an empty array or 401/permission error, NOT user rows. Then the same query with the app's own session (its normal flows must still work — hardening that locks real users out is an outage).

## Firebase

**Evidence to read:** `firestore.rules` / `storage.rules` / `database.rules.json`; `firebase.json` for hosting rewrites and headers.

**Posture checks:**
- Rules start with deny: `match /<path>/{doc} { allow read, write: if false; }` then per-path allowlist — not `if true` defaults
- Per-user scoping in rules: `request.auth.uid == resource.data.ownerId` shape on user documents
- Storage: read rules per bucket path; write rules tighter than read for user uploads; content-type limits on uploads
- Client config (`apiKey` in the web bundle is normal for Firebase) — the *rules* are the security, never the config secrecy

**Dynamic proof:** run the app's own SDK unauthenticated against a user document: expect permission-denied, not data. `firebase emulators` can run rules offline if the project isn't deployed yet.

## Storage buckets (any provider)

- Per bucket: public or private, and why (public = genuinely static assets only: images of products, fonts — never user uploads, exports, or anything with user identifiers)
- URL-guessability: public user content must not be enumerable (random IDs / signed URLs), because "public" + guessable = scrapeable
- Upload path: content-type allowlist + size limit + (ideally) server-side scan before serving user uploads back

## API routes (Express/Next/Fastify/...)

- **Centralize auth middleware** for the protected prefix (`app.use('/api', requireAuth)`) — per-route auth is where gaps hide; list every route OUTSIDE the central middleware and justify it
- Billable endpoints (LLM, email, SMS, payments) get: auth + rate limit + input length caps. An unauthenticated LLM endpoint is a wallet with the PIN taped to it
- Webhooks: verify signatures (Stripe/Shopify/CLoudflare headers) before processing; reject unsigned
- Admin: server-side session/role check on the route, not UI navigation; audit the admin prefix as its own zone in the Round 1 map

## Headers & cookies (any host)

- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` (or CSP `frame-ancestors 'none'`)
- CSP baseline: `default-src 'self'` + explicit allowlist for CDN/analytics; `upgrade-insecure-requests`
- Cookies: `Secure; HttpOnly; SameSite=Lax` (or Strict) — session cookies never without HttpOnly
- CORS: credentialed endpoints get an explicit origin allowlist; `Access-Control-Allow-Origin: *` with credentials is a P1 finding

## Rate limits (platform features first)

- Vercel: platform WAF/rate limiting or middleware-based; Netlify: edge functions; Fly/Railway: app-level (express-rate-limit or the framework's equivalent)
- Tier: billable endpoints strictest (per-user + per-IP), auth endpoints (login/reset) against stuffing, public reads loosest
- Rate limiting at the CDN is a valid architecture (per owasp-security / cf anti-patterns) — the check is that SOME layer enforces it, and the dynamic proof shows 429 after the configured threshold
