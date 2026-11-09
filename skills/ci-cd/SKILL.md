---
name: ci-cd
description: Author and wire the repo's automated pipeline — install → build → test → deploy on push/merge — so a push lands on a working production URL with no manual go-live, then prove it by watching one real pipeline run to green and smoking the deployed URL. Calls the recipes that already exist (justfile, package.json scripts, uv) — never invents new build commands; secrets go through the platform secret store, never the repo or the log output. Use when the user asks to set up CI/CD, GitHub Actions, a pipeline, "auto-deploy ตอน push", "ทำ workflow ให้ repo", or wants merge-to-deploy automation. Not for a one-time deploy right now (use /ship-it — its Phase 3–4 deploy by hand on explicit go live), bootstrapping a new repo (/scaffold-fullstack), or security posture (/harden).
---

# CI-CD

Turn "deploy" from a manual ritual into a property of the repo: push to the named branch → pipeline verifies → deploys → URL serves. Split of labor:

- **/ship-it** — the one-time run: pre-flight, build, deploy by hand, verify. This skill authors what makes it automatic afterward.
- **/scaffold-fullstack** — creates the justfile recipes this pipeline calls; if the repo has no recipes yet, scaffold or hand-write them first.
- **/wizard** — human-only provisioning (connecting the repo to a platform, first platform login, org-level permissions) gets a wizard, not a script.
- **/harden** — posture and denial proof after go live; orthogonal to the pipeline.

## Process

### Phase 0 — Confirm inputs (gate: platform, branch, recipes all named)

Ask (or infer from `CONTEXT.md`/ADRs) before writing anything:

1. **Deploy platform** — Vercel/Netlify/Fly/Cloudflare/container host; pick by stack the same way /ship-it does (its `references/deploy-platforms.md` is the decision table). State the cost tier; confirm before creating anything paid.
2. **Trigger** — which branch deploys (default: the branch the user names; never assume one), whether PRs get build-only verification, whether PR previews are wanted.
3. **Recipes exist** — read the `justfile` / `package.json` scripts / `pyproject.toml`. A missing recipe is added to the repo's orchestrator (Phase 1), not inlined into the workflow.
4. **Human-only steps** — repo not yet connected to the platform, or secrets need a dashboard? Route those steps through /wizard with the exact actions.
5. **Local-only repo (no remote yet)** — the pipeline has nothing to run on: report `/ci-cd` as blocked at Phase 0, hand off to /ship-it (LOCAL mode) plus `just check` as the interim gates, and re-run this skill once the remote and platform exist.

### Phase 1 — Recipe audit (gate: every pipeline step maps to an existing command)

| Pipeline step | Source of truth |
| --- | --- |
| install | `just install` (or `bun install` / `uv sync` when no justfile exists) |
| check/lint | `just check` (or the stack's equivalents already configured) |
| test | `just test` (or the test runner already configured) |
| build | the production build the repo already uses — same as /ship-it Phase 2 |
| deploy | the platform's own deploy integration/CLI when one exists |

- A step with no recipe: add the recipe to the justfile first (repo-side change), then call it from the workflow. The workflow never re-states a command a recipe already owns.
- Pre-flight parity: the verify job must fail on what /ship-it Phase 1 fails on (red build, missing env docs, debug prints in production paths). If `.env.example` drifts from what the app reads, fix that before wiring.

### Phase 2 — Author the workflow (gate: YAML references only real recipes)

Default GitHub Actions; the same shape transfers to GitLab CI / Cloudflare / platform-native CI:

```yaml
name: ci
on:
  push:
    branches: [<named-branch>]
  pull_request:
  workflow_dispatch:
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5    # python side — only when the stack uses uv
      - uses: oven-sh/setup-bun@v2     # TS side — only when the stack uses bun
      - run: just install
      - run: just check
      - run: just test
  deploy:
    needs: verify
    if: github.ref == 'refs/heads/<named-branch>' && github.event_name != 'pull_request'
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - run: just deploy               # or the platform's deploy action/CLI step
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

- Cache with the ecosystem lockfile (the setup actions cache natively) — never hand-roll cache steps.
- Production migrations inside the deploy job stay behind an explicit step and get one user confirmation at authoring time — same rule as /ship-it Phase 3.
- Keep the file honest: every `run:` mirrors a recipe or a documented platform step. No step duplicates what a recipe owns.

### Phase 3 — Secrets (gate: nothing sensitive in the repo or the output)

One entry per var the app reads from `.env.example`:

```bash
gh secret set DATABASE_URL     # prompts for the value; nothing lands in the repo
gh secret set AUTH_SECRET
gh secret list                 # verify the set CI will actually see
```

- Values come from the user's own environment or typed input — never echoed, never committed, masked in all output.
- Client-visible keys are a leak (same rule as /ship-it Phase 1): a key importable in browser code stops the wiring until fixed.

### Phase 4 — Prove the pipeline (gate: one green run + the URL responds)

```bash
gh run watch                           # trigger with a push (or workflow_dispatch), follow to completion
gh run view --log-failed               # red? show the failing lines verbatim
curl -i https://<deployed-url>/        # main-path smoke — same evidence rules as /ship-it Phase 4
```

- A red run is reported red with the failing log excerpt — never summarized into "deployed".
- After the run: smoke the 2–3 critical flows against the deployed URL (HTTP status, DOM assertion, or API response body) and screenshot key pages when a headless browser is available.

## Deliver

Report: workflow path, trigger branch, platform + cost tier, the run (link/number, duration, result), the deployed URL with smoke evidence, and anything left manual (DNS, dashboard-only env vars, PR preview settings). If any phase's gate is red, stop there — an unproven pipeline is not a wired one.

## Guardrails

- Never echo secret values; mask them in all output.
- Destructive or irreversible actions (production migrations, domain changes, deleting environments) require explicit user confirmation at the moment of action.
- Free-tier awareness: state the expected cost before provisioning; don't enable paid features unasked.
- The deploy job runs only on the branch the user named — no surprise deploys from other branches or forks.
- Everyday "deploy ตอนนี้ / go live" requests still belong to /ship-it; this skill owns the wiring, not the ritual.

