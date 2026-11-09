# Deploy platforms — pick by stack

Decision table for Phase 2. Default to the row that matches the repo's evidence (manifests, config files). Confirm platform + tier with the user before provisioning.

## Selection table

| Evidence in the repo | Platform | How | Notes |
| --- | --- | --- | --- |
| Next.js / Nuxt / Remix / SvelteKit / Vite SPA | **Vercel** | `vercel` CLI or connect repo | Zero-config for the frameworks it knows; preview URLs per branch; env vars via `vercel env add` |
| Static site / plain HTML / docs build | **Netlify** or Cloudflare Pages | `netlify deploy` / `wrangler pages deploy` | Cheapest path for static output |
| Node API / Express / Fastify, needs a long-running server | **Fly.io** or Railway | `fly launch` / Railway repo connect | Vercel functions have timeouts; long-lived sockets/queues need a real server |
| Python backend (FastAPI/Django/Flask) | Railway or Fly.io | repo connect / Dockerfile | Railway: simplest; Fly: needs a Dockerfile (they generate one) |
| Containerized (Dockerfile in repo) | **Fly.io** | `fly launch --dockerfile` | Region + scale flags; check free allowance |
| Supabase / Neon / managed DB already in use | keep it; deploy only the app | — | Get the pooled connection string for serverless hosts |
| `wrangler.toml` / Workers | **Cloudflare Workers** | `wrangler deploy` | Bindings ≠ env vars; KV/R2/D1 stay as configured |

Tiebreaker: the user already has an account/CLI with one of these → use it. Unknown stack → ask one question; don't guess hosting.

## Platform gotchas (check before declaring success)

- **Vercel/Netlify (serverless):** cold starts + execution timeouts — long cron jobs and websockets need the platform's queue/cron feature or a real server. Env vars must be re-set per environment (preview vs production).
- **Fly.io:** first deploy needs `fly launch`, subsequent `fly deploy`; health checks must respond on the port in `fly.toml`; free Postgres requires explicit attach.
- **Railway:** services in one project share private networking; public domains must be generated per service.
- **Cloudflare Pages:** functions live in `functions/` dir; build output dir must match the dashboard setting.
- **Databases on serverless hosts:** use connection pooling (serverless-friendly driver) — raw TCP connection per request exhausts limits fast.

## Migration checklist (Phase 2 step 3)

1. `migrate status` (or equivalent) against prod — confirm from where.
2. Backup/snapshot exists before the first schema change (platform snapshot or `pg_dump`).
3. Run migrations; read back a row from a touched table.
4. Never rename/drop columns without the expand–contract pattern (see `/migration` skill) — production data has no undo.

## Smoke test patterns (Phase 3)

- Simplest: `curl -s -o /dev/null -w "%{http_code}" <url>` per page + one API call with expected body substring.
- Headless browser (if Playwright/Puppeteer available): load home, assert selector; run the main flow; capture console errors; screenshot viewport + mobile viewport.
- Always: one wrong-URL visit expecting a rendered 404/fallback, and a scan for asset 404s in the network log or console.
