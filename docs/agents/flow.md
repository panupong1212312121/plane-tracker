# Vibe-coding workflow

The default pipeline for feature work in this repo, and which skill owns each stage. The spine is fixed; specialist skills enter by task type, not as extra stages.

## The spine

```
Idea (rough is fine)
   │
   ▼
/feasibility-study    — OPTIONAL gate for new product ideas BEFORE grilling:
   │                    is it worth building at all (users, impact, market,
   │                    ทำใหม่ไปทำไม)? BUILD/EXTEND/WONTFIX verdict first.
   ▼
/grill-with-docs      — interview until the plan is sharp; record domain
   │                    decisions as ADRs + glossary (CONTEXT.md)
   ▼
/design-md            — FIRST RUN OF A UI-BEARING REPO ONLY: interview the
   │                    design system into design.md at the repo root.
   │                    Skip when design.md already exists (update mode later)
   │                    or the work has no UI. Never before grilling.
   ▼
/to-spec              — synthesize the conversation into a spec at
   │                    .scratch/<feature-slug>/spec.md (no interview).
   │                    Implementation Decisions may cite design.md tokens;
   │                    tickets with many input combinations get flagged
   │                    for /pict-test-designer at build time.
   ▼
/to-tickets           — tracer-bullet vertical slices with blocking edges at
   │                    .scratch/<feature-slug>/issues/NN-<slug>.md.
   │                    Wide refactors are sequenced expand–contract and
   │                    execute through the /migration skill.
   ▼
/implement            — one ticket at a time. /tdd at pre-agreed seams;
                        close each ticket with /code-review + /review-metrics + /verify-and-stop.
   ▼</slug>
/ship-it              — LOCAL by default: pre-flight → boot the production
   │                    build locally → smoke + screenshots, stop there.
   │                    Deploy + verify against a real URL only on an
   │                    explicit "go live" (Phase 3-4).
   ▼
/grill-ship           — OPTIONAL blunt post-completion critique of the artifact
                        (what's missing, broken, or overbuilt) — the reverse of
                        /grilling: interrogate the result, not the plan.
```

## Branch rule + rollback plan (delivery steps 2 และ 6)

**Branch rule** — ทุกการเปลี่ยนแปลงมีประวัติและย้อนตรวจได้:

- แต่ละ ticket จาก `/to-tickets` ถูกสร้างบน branch ของตัวเอง `NN-<slug>` ตัดจาก main; commit ข้างในเป็นก้อนเล็กที่อ้างเลข ticket ทุกครั้ง
- merge เข้า main เมื่อ `/code-review` + `/verify-and-stop` เขียวบน branch นั้นเท่านั้น; เมื่อ `/ci-cd` ถูก wire แล้ว main ได้ประตูเดียวกันตอน push
- `prototype/<name>` คงกติกาเดิม (throwaway แต่มีประวัติ); wide refactor วิ่ง expand–contract ของ `/migration` บน branch ของตัวเอง
- ข้อยกเว้นเดี่ยว: ถ้า user สั่งชัด ๆ ให้ลง main ตรง ๆ — จดลง ticket ทุกครั้ง ห้ามทำเงียบ ๆ

**Rollback plan** — deploy LIVE โดยไม่มีคำตอบว่า "ย้อนยังไง" = deploy ยังไม่เกิด:

- รายงาน `/ship-it` Phase 3 (LIVE) ต้องระบุวิธี rollback คู่กับ deploy: ถอยไป build/image ก่อนหน้าได้ด้วยคำสั่งเดียว และฝั่งฐานข้อมูลระบุชัดว่าจุดไหนเป็น expand (ถอยได้ — build เก่ายังรันได้) จุดไหนเป็น contract (จุดไม่ย้อนกลับ) ตาม `/migration`
- migration ที่ทำลายข้อมูล (drop/retype/backfill ย้อนไม่ได้) — รวมถึงงานฐานข้อมูล/การชำระเงินใด ๆ ในอนาคต — ต้องมี user ยืนยันชัดเจน + snapshot/backup ก่อน deploy ทุกครั้ง; ไม่มี snapshot ไม่ deploy
- "ยังอยู่ไหม" วัดด้วยหลักฐานเดียวกับตอน go live: smoke ของ Phase 4 + `/monitoring` — แดงหรือมีแจ้งเตือน = rollback ทันที ไม่รอสรุป

## Ordering rule: grill before design

Product decisions shape design decisions, rarely the reverse. `/grill-with-docs` output (audience, brand, stack in `CONTEXT.md`/ADRs) is exactly the signal the `/design-md` interview consumes. `design.md` must exist before `/to-spec` and `/implement` so specs can cite tokens and UI tickets follow the file automatically.

Exceptions: design-only work (restyle/redesign with no new domain decisions) may run `/design-md` alone; a repo that already has a current `design.md` skips straight to grilling.

## Inside /implement — which specialist fires

| Situation | Skill |
| --- | --- |
| Starting a repo from zero (uv backend + TS frontend) | `/scaffold-fullstack` (separated layout, justfile orchestration, verified boot) |
| Defining/syncing the Python↔TS API seam | `/api-contract` (OpenAPI-first, typed client gen, drift verdicts; pairs with `/verify-and-stop` for endpoint proof) |
| Building UI | read `design.md` first (automatic via `AGENTS.md`); build-time craft via `/frontend-design` (direction, anti-slop, bounded browser verify) |
| คู่มือ/manual/demo video/slides/report ให้ app | `/enablement-kit` (director: routes to frontend-slides/manim-video/archify/codebase-diagram, captures real screenshots, verified cross-links, caveman style) |
| Expose app capabilities as MCP tools (FastMCP) | `/fastmcp-server` (analyze → confirm table → scaffold → verify every tool via fastmcp CLI → wire mcp.json) |
| Feature work at overbuilding risk | `/lean-build` (scope discipline; `/implement` stays the orchestrator) |
| Bug with ambiguous cause | `/investigate-first` — evidence before edits |
| Bug cause known, fix time | `/surgical-patch` — narrowest layer + regression proof |
| Structural change mid-ticket | `/safe-refactor` — behavior preserved |
| Persisted/public shape changes | `/migration` |
| Listing tests for existing code | `/generate-test-cases` (cases only, then review) |
| Writing unit tests for existing code | `/generate-tests` |
| Many-parameter input combinations (form/config/API) | `/pict-test-designer` |
| Proving acceptance without scope growth | `/verify-and-stop` |
| Recording review metrics after /code-review closes | `/review-metrics` (companion: review-latency + escape-ratio per playbook) |
| Going live / check production readiness | `/ship-it` (LOCAL default: pre-flight → local production run → smoke; deploy + verify live only on explicit "go live") |
| Automate deploy on push (build → test → deploy pipeline) | `/ci-cd` (calls existing justfile recipes; secrets via platform store; proves one green run + responding URL; one-time deploys stay with `/ship-it`) |
| Watch production after go-live (error tracking, uptime, alerts) | `/monitoring` (free-tier sensors; proof = test-error event ID + green uptime check; sensors feed `/investigate-first`) |
| Design a database (system-analyst work: access patterns → ER → physical schema) | `/database-design` (consumes the `/domain-modeling` glossary; proves every pattern with real queries; hands DDL to `/migration`, ER to `/diagram-design`, mapping to `/api-contract`) |
| Move data between systems (data-engineer work: ETL/ELT design + build) | `/data-pipeline` (edge contracts, idempotent stages, in = out proof + no-op rerun; diagram via `/archify` dataflow, failure signals to `/monitoring`) |
| Quick source-code vuln scan ("is my code secure?") | `/security-review` |
| Deep adversarial exploit audit of source | `/security-audit` (heavy: subagent phases; run sparingly) |
| Writing/keeping code idiomatic (classes, type hints, docstrings, decorators, async, immutability, code smells) | `/code-style` (writes/refreshes `CONVENTIONS.md`, loads per-language references, code-smell pass per ticket, wires ruff/mypy + eslint/tsc into `just check`; feeds `/code-review` Standards axis) |
| PRD for stakeholders (Lean / Comprehensive / Amazon PR-FAQ / Google) | `/prd-template` (companion to `/to-spec`; fills only from existing grill/spec/ADR output; review checklist; `.scratch/<feature>/prd.md` or a Plane page) |
| Security standards while writing/reviewing code | `owasp-security` (loads OWASP/ASVS knowledge) |
| Posture of the deployed stack + proof that denial works | `/harden` (Supabase RLS, Firebase rules, CORS, admin guards; 401/403 proofs against the live URL) |
| Drafting a project timeline / acting as PM | `/pm-planner` (draft → plane-plan.md with **Element Details ครบ 6 หมวด** (Work items/Cycles/Modules/Views/Pages/Intake); materialize into Plane only on explicit trigger + 4-gate) |
| Go/no-go before building a new product idea | `/feasibility-study` (verdict first: BUILD/EXTEND/WONTFIX + cheapest-test) |
| Blunt critique after shipping ("/implement", "/ship-it" done) | `/grill-ship` (audit artifact → grill gaps → record verdict) |
| Noticed mid-project: same dance twice, workaround, "ทำอย่างนี้ทุกทีเลย" — probably a missing/improvable skill | `/skill-arbiter` (capture to `.scratch/skill-candidates/` → triage IMPROVE-NOW/CANDIDATE/PLANNER/DROP; PLANNER routes to `/skill-planner`) |
| Real-session skill distillation (/learn, capture durable lessons with evidence quotes) | `/autoharness` (session transcript distillation, evidence quotes, auto-pruning) |
| Master engineering orchestrator ("go deep first", learning before editing, strict verification) | `/poteto-mode` (orchestrates `/investigate-first`, `/lean-build`, `/safe-refactor`, `/surgical-patch`, `/verify-and-stop`) |
| Reverse-engineer binaries, Electron/ASAR, or external JS bundles without source code | `/reverse-engineer-anything` (decompilation, evidence graphs, artifact inspection) |
| Programmatic video creation in React (compositions, sequences, springs) | `/remotion` (React video framework, preview studio, render CLI) |
| HTML/CSS seekable timeline videos and keyframe animation for agents | `/hyperframes` (seekable timeline, motion doctrine, scene blocks) |
| Industrial web animation, timelines, ScrollTrigger, and React useGSAP() lifecycle safety | `/gsap` (hardware-accelerated transforms, timelines, ScrollTrigger, context cleanup) |
| Animated PR diffs, data-flow diagrams, and ELI5 architecture walkthroughs | `/pr-lens` (JSON graph doc, `@coldtea/pr-lens-cli` validation, animated SVG) |
| 100% code motion design (no external licenses: HTML + Canvas + Playwright + FFmpeg) | `/motion-design` (seek(t) engine, log camera moves, closed-form springs, tmix motion blur) |
| Context window conservation & sandboxing large tool outputs (>20 lines) | `/context-mode` (execute inline analysis scripts, SQLite FTS5 continuity, avoid bloat) |
| Multi-domain anti-slop defense (UI, code comments, copywriting, 4-block delivery gate) | `/anti-slop` (38 rules R-01..R-38, liveliness dials, delivery gate; feeds `/frontend-design`) |
| Real browser driving & authenticated session reuse (borrow-tab model) | `/browserskill` (live session smoke tests, production UI inspect, anti-denial checks) |
| High-fidelity synthetic datasets & enterprise corpora | `/data-designer` (statistical distributions, multi-column correlations, bilingual records) |
| Multi-spec design exploration & HTML previews (ADR-0010) | `/design-explorer` (≥3 macrostructure variants, typicality scoring, visual HTML previews) |
| 3-tier validation and benchmarking suite for agent skills | `/skill-evaluator` (Tier 1 deterministic gates, Tier 2 semantic overlap, Tier 3 live benchmarks) |
| Autonomous agent skill self-repair and regression loop | `/skillhone` (trace analysis, bounded instruction/script repair, immutable decision ledger) |
| Open agent skill discovery and search-before-build | `/skillnet` (registry discovery, capability matching, supply-chain vetting before import) |
| Agent skill security scanner & supply-chain auditor | `/skillspector` (static AST/regex/YARA analysis, mandatory `--no-llm`, category triage) |
| Slides / pitch deck / content-to-HTML presentation | `/frontend-slides` (single-file, 16:9 stage; deploy via `/ship-it`) |
| Mock/synthetic data for tests and demos | `/mock-data` (schema inference, seeded generators, PII-safe) |
| Math/animation videos (.mp4/.gif) for embedding or standalone | `/manim-video` |
| Interactive visual objects for the web (canvas/WebGL) | `/interactive-web-objects` (embeddable snippet or single HTML) |
| Full-screen real-time WebGL/WebGL2 experiences | /webgl-experience (shaders, 3D scenes, single self-contained HTML) |
| GPU particle galaxy / point clouds | /webgl-particle-galaxy (GPU-computed orbits in vertex shader) |
| Running local models on free-tier GPU (Kaggle/Colab) | `/free-gpu-models` |

Security trigger split: "scan/review this code" → `/security-review` (mid-weight, patches proposed); "audit/pen-test this codebase" → `/security-audit` (heavy, exploit-only findings; upstream refreshed 2026-09-15 — default = guidance mode, full audit เปิดเฉพาะสั่ง audit/pen-test ชัด ๆ); "is my app safe online / harden it / check Supabase/Firebase settings" → `/harden` (posture + dynamic denial proof). Standards questions map to `owasp-security`'s reference files, which any of the three loads on demand.

## Doc division of labor

- **`CONTEXT.md` + `docs/adr/`** (via `/grill-with-docs`): domain concepts, glossary, product/architecture decisions.
- **`design.md`** (via `/design-md`): visual theme, colors, typography, components, layout, elevation, guardrails, responsive rules.
- **`research/`** (via `/arxiv-deep-researcher`): the arXiv evidence ledger behind architecture/design decisions — newest-first chains with `supports`/`refutes`/`extends`/`bounded-by` relations and cite-ready blurbs to paste into UI for credibility.

Never put hex values in ADRs or business rules in `design.md`.

## Diagram routing (design-phase artifacts)

After `/grill-with-docs`, system-design diagrams route by need — all drawn through `/diagram-design` (39 types; also redraws Mermaid `.mmd` / `.drawio` sources) or `/archify` (explorable HTML):

| Design-phase need | Route to |
| --- | --- |
| Architecture / components / deployment | `/diagram-design` architecture · layer stack · deployment · dependency graph, or `/archify` architecture |
| Process / activity / flowchart | `/diagram-design` flowchart · process · swimlane, or `/archify` workflow |
| API / object interaction | `/diagram-design` sequence, or `/archify` sequence |
| State machines | `/diagram-design` state machine, or `/archify` lifecycle |
| Data storage (ER, schema) | `/database-design` first (access patterns → ER → physical), then `/diagram-design` ER/data model · database schema |
| Data movement (DFD, pipelines) | `/data-pipeline` designs the flow, then `/archify` dataflow renders it |
| Existing codebase (as-built) | `/codebase-diagram` (bridges to both renderers) |

UML vocabulary maps into the same routes: use case → story map / user journey / process; component → architecture / layer stack; activity → flowchart / process.

## Meta loop (periodic, not per-feature)

```
/skill-arbiter  — runs DURING ordinary work: catches self-improvement signals
   │             (repeated dance, workaround, skill bypassed, user friction),
   │             captures each to .scratch/skill-candidates/, then triages:
   ▼             IMPROVE-NOW (small local edit) | CANDIDATE (defer) |
                 PLANNER (escalate) | DROP
/skill-planner  — decide FIRST when a capability idea appears: new skill, extend
   │             an existing one, companion to an upstream-locked skill, or
   ▼             no skill (docs note) — hands /skill-creator a written brief; การ import skill จากต้นทางภายนอกใหม่ต้องผ่าน `skillspector scan` ก่อนเสมอ (tool ติดตั้งแล้ว — `skillspector scan <path> --no-llm`)
/skill-creator  — authors or edits the skill from the brief; evals +
   │             description optimization
   ▼
/skill-optimize  — bounded improve–validate loop for LOCAL skills (arXiv:2605.23904
   │             adapted): one evidence-backed edit per cycle, accepted only when
   ▼             SkillEvaluator gates improve — never edit past records
scripts/audit-skills.ps1 — static health audit of skills\ (frontmatter, dead
   │             links, actionability, platform markers, lock status)
   ▼
scripts/sync-skills.ps1  — propagate skills\ into every agent directory
   ▼
/skill-doctor  — periodic whole-hub grading from real conversations; its
   │             findings seed arbiter-ledger entries
   ▼
/skill-creator — applies the evidence-backed edits or creates new skills
```
