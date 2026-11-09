---
name: monitoring
description: Wire the minimal observability set into a deployed app — error tracking, uptime checks, and one alert destination — free-tier first, then prove events actually flow: a deliberately triggered test error shows up in the tracker with an event ID, and the uptime check is green against the real URL. The sensor half of go-live — /ship-it proves the app works once at deploy; this keeps watching after. Use when the user asks to set up monitoring, error tracking, observability, uptime checks, "อยากรู้ตอน production พัง", or "แจ้งเตือนเมื่อล่ม". Not for deploying (/ship-it), security posture (/harden), diagnosing a known bug (/investigate-first), or the one-time post-ship critique (/grill-ship).
---

# Monitoring

An app nobody watches fails silently. This skill adds the sensor layer after go live and ends only with proof that events flow — never with "should work now".

Split of labor:

- **/ship-it** — proves function once, at deploy time. This skill makes failures visible continuously.
- **/harden** — proves denial (401/403); unrelated to health signals.
- **/investigate-first**, **/diagnosing-bugs** — consume the error events this skill produces.
- **/wizard** — human-only signups (tracker org, uptime service account) get a wizard, not a script.

## Process

### Phase 1 — Sensor selection (gate: one stack, user-confirmed)

| Sensor | Default (free tier) | Alternatives |
| --- | --- | --- |
| Error tracking | Sentry (5k errors/mo) | GlitchTip (self-host), Rollbar |
| Uptime | UptimeRobot (50 monitors, 5-min interval) | BetterStack, healthchecks.io |
| Alerts | the tracker's own email → user's inbox | Slack / Discord webhook if the user already lives there |

Present the table with one recommendation; confirm before creating any account. Signups the user must do by hand → /wizard with the exact steps. If the deploy platform ships built-in monitoring, prefer wiring it over adding a second service — fewer dashboards, same proof bar.

### Phase 2 — Integrate error tracking (gate: DSN from env only)

1. **Backend** — init the SDK at app entry, before route registration; capture unhandled exceptions and rejections.
2. **Frontend** — error boundary around the app root plus global handlers; ignore browser-extension noise.
3. **Config** — DSN via env var only; add it to `.env.example`; never committed, never bundled.
4. **Release tagging** — if the repo has a version (from the build or git tag), attach it so each error maps to a build.

```bash
grep -rn "DSN" .env*               # DSN lives only in env files, never in source
git grep -i "dsn="                 # and nothing committed
```

### Phase 3 — Uptime + alerts (gate: real URL registered, destination confirmed)

1. Register the deployed URL: the home page plus one cheap route (health endpoint if the app has one).
2. Interval: free tiers poll every 5 minutes — state that this is the fastest detection at the tier, not a promise of instant paging.
3. Alert destination: confirm with the user where alerts land (their email, their Slack). Never subscribe a channel without asking.
4. If the platform has built-in monitoring, wire its alerts into the same destination instead of a second checker.

Local-only note: with no public URL, error tracking still works (the SDK ships events to the cloud from localhost), but external uptime checkers cannot reach localhost — register monitors only when a public URL exists, and keep /ship-it's local smoke as the interim health check.

### Phase 4 — Prove events flow (gate: event ID seen + uptime green)

```bash
curl -i https://<deployed-url>/              # app is serving
curl -i https://<deployed-url>/__test-error  # dev-only route that throws — removed after the proof
```

- Find the test error in the tracker and record the **event ID** in the report. No event ID = not proven.
- Uptime check green on both monitors; fire one manual test alert to confirm the destination actually receives it.
- Remove the test route afterward — it is dev-only and must not ship enabled.

## Deliver

Report: sensors chosen (with tier limits), where the DSN lives, monitor URLs + intervals, alert destination, the test-error event ID, and the ADR note location. Re-run this skill whenever a new deploy target or app surface appears.

Record the wiring in an ADR (via /grill-with-docs conventions): what's monitored, thresholds, where alerts land — the setup must outlive the conversation.

## Guardrails

- Never commit a DSN or echo one; mask it in all output.
- Free-tier awareness: state the tier limits before creating anything; don't enable paid features unasked.
- Don't leave the test-error route enabled in production paths.
- Don't mute or downgrade real alerting while testing — the test alert goes to the real destination.
- An unverified sensor is reported UNVERIFIED with what's missing to verify it — never narrated as done.
