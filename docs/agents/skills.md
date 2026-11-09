# Skill hub

This repo is a skills hub: `skills/` is the canonical copy, synced into every agent directory, with upstream imports pinned by hash.

## Layout

- `skills/<name>/SKILL.md` — canonical skill; the `name:` field must match the folder name.
- `skills/<name>/references/`, `scripts/`, etc. — progressive disclosure; SKILL.md links out instead of growing past ~400 lines.
- `skills-lock.json` — provenance + integrity: `source` (e.g. `mattpocock/skills`), `skillPath`, `computedHash`. A `source` starting with `local (built: …)` marks a locally authored skill — the only kind that may be edited in place.
  - **Hash scheme (`sha256-lf`)** — SHA-256 of the canonical `SKILL.md` as UTF-8 text with CRLF/CR normalised to LF and any BOM stripped. Line-ending normalisation is what keeps the lock stable across Windows working copies.
  - `computedHash` is the **current baseline**; `scripts/rebash-lock.ps1 -Check` reports drift and `scripts/rebash-lock.ps1` re-baselines it.
  - `importHash` (optional) preserves the value recorded by the **original importer**. Those legacy values predate the documented scheme and are not reproducible byte-for-byte, so they are kept as an audit trail only — never as a verification target.
  - Upstream drift is a *content* question, not a hash question: `scripts/verify-upstream-skills.ps1` fetches each upstream-sourced skill and compares local content against the live upstream `HEAD` (report `LOCK-OK` / `LOCK-STALE` / `LOCAL-DRIFT`).
- Agent dirs (`.claude/`, `.agents/`, `.kilo/`, …) — stamped copies produced by `scripts/sync-skills.ps1`. Never edit them directly.

## Lifecycle

```
/skill-arbiter            — DURING real work: catch self-improvement signals
   │                        (repeated dance, workaround, skill bypassed, user
   │                        friction), capture to .scratch/skill-candidates/,
   │                        triage: IMPROVE-NOW | CANDIDATE | PLANNER | DROP
   ▼
/skill-planner            — decide: NEW skill, EXTEND existing, COMPANION for an
   │                        upstream-locked skill, or NO-SKILL (docs note instead)
   ▼
/skill-creator            — author/eval the skill from the planner's brief
   ▼
scripts/audit-skills.ps1  — static health audit (frontmatter, dead links,
   │                        actionability, platform markers, lock status)
   ▼
scripts/sync-skills.ps1   — propagate skills/ into every agent directory
   ▼
/skill-doctor             — grade skills from real conversations; evidence
   ▼                        feeds back through /skill-arbiter → /skill-planner
```

## Mid-project rule (the "vibe coding ไปเจอทีหลังว่าควรมี skill" case)

Skill-shaped needs discovered mid-project go through `/skill-arbiter`, never straight to `/skill-creator`: capture the signal to the ledger (mandatory), triage, and only escalate when the rubric justifies it. CANDIDATE is the default while a ticket is half-finished; the **end-of-project sweep** re-triages the ledger with fresh repetition counts and batches the planner escalations.

## Rules

1. Skill-shaped needs discovered mid-project go through `/skill-arbiter` first — capture to `.scratch/skill-candidates/`, then triage; CANDIDATE is the default while a ticket is open.
2. New skill ideas go through `/skill-planner` — one capability in, one verdict out (NO-SKILL / EXTEND / COMPANION / CREATE NEW).
3. Never edit an upstream-locked `SKILL.md` (non-`local` source in `skills-lock.json`); build a local companion skill that references it (precedent: `codebase-diagram` → `archify`).
4. Every new or changed skill updates its `skills-lock.json` entry and finishes with `scripts/sync-skills.ps1`, or it did not happen. Recompute the baseline with `scripts/rebash-lock.ps1` (never hand-edit a hash) and confirm with `scripts/audit-skills.ps1`.
5. `scripts/audit-skills.ps1 -Inventory` is the single source of truth for "what skills exist" — read it before proposing anything skill-shaped.
6. Importing or refreshing an upstream skill is a two-gate move: `skillspector scan <path> --no-llm` before it lands (supply-chain check), then `scripts/verify-upstream-skills.ps1` afterwards to record that local content matches upstream `HEAD`. Re-baseline the lock for that skill in the same change.
7. Read a SkillSpector score as **triage, never as a verdict**. The score is dominated by literal pattern matches on example content — a skill shipping HTML/SVG examples with comments or OAuth walkthroughs scores 100/100 `DO_NOT_INSTALL` while carrying no real defect. Triage by category instead: `Prompt Injection` / `Anti-Refusal` on `assets/` or examples = false positive (read the line, confirm it); `analysis-evasion` = the scanner could not fully inspect a referenced file (a coverage gap, not a finding) — re-scan with the whole skill directory; `MCP Least Privilege` / `Output Handling` / `Rogue Agent` / `Excessive Agency` = hygiene notes worth fixing in frontmatter or wording. Record the triage (category counts + which lines) in the candidate ledger; never re-import just because the score is high.
8. Production-oriented skills stay LOCAL-first: concrete, ordered, gated steps that run on this machine. The deployment-automation capabilities exist now — `/ci-cd` (pipeline: push → build → test → deploy) and `/monitoring` (post-deploy sensors), both planner-approved CREATE NEW (2026-09); any further deployment-platform skills (e.g. a new deploy target) still go through `/skill-planner` first. LOCAL-first is a gate order — prove on this machine before pushing — not a local-only restriction: once a git remote exists, `/ci-cd`'s pipeline and `/ship-it` LIVE are the first-class continuation.

## Upstream source catalog (for future /skill-planner runs)

Curated external pools to consult **per capability** when a real need appears — never bulk-import (anti-pattern: skill-for-everything); each candidate still passes the planner rubric + audit + lock.

- `alirezarezvani/claude-skills` (GitHub) — 380-skill catalog (engineering, product, PM, marketing, finance, compliance). Harvest selectively: product/PM ideas → compare against `/to-spec`, `/pm-planner`, `/prd-template` first; engineering ideas → compare against the specialist table in `flow.md`.
- `slgoodrich/agents` — `prd-templates` skill, consumed 2026-09 as the local `/prd-template` companion (templates + checklist live there now).
- `affaan-m/ECC` — `coding-standards` skill, consumed 2026-09 into `/code-style` (immutability, code smells, AAA tests, verb-noun naming, perf guardrails).
- `khendzel/skills-janitor` — health/fix/value/security TUI suite for installed skills; evaluated 2026-09: report/security duplicate `audit-skills.ps1` + `skillspector` (NO-SKILL); `janitor-value` (token-cost vs usage per skill) kept as an idea — revisit only when a real repetition signal appears via `/skill-arbiter`.
- `ruc-datalab/SkillAdam` (arXiv:2609.08944) — skill evolution loop (test → revise from failures → validate-gated acceptance); consumed 2026-09 into `/skill-optimize`'s acceptance discipline (skill is local, so EXTEND was legal).
- `FrancyJGLisboa/agent-skills-platform` — skill factory + governed marketplace; evaluated 2026-09 as NO-SKILL (duplicates creator/audit/lock stack); idea to revisit: `every_expected_is_reachable` gate in `/skill-creator` eval design.
- `nutlope/hallmark` + `pbakaus/impeccable` — anti-AI-slop design; consumed 2026-09 as deltas into `/frontend-design` v1.1 (structural variety, pre-emit slop self-critique, `npx impeccable detect`), not imported whole (hallmark MIT, impeccable Apache-2.0).
- `morluto/rea` — Reverse Engineer Anything; consumed 2026-10 into `/reverse-engineer-anything` for native binaries, Electron/ASAR, and JS bundle analysis.
- `remotion-dev/remotion` (`remotion-dev/skills`) — React-based programmatic video framework; consumed 2026-10 into `/remotion`.
- `heygen-com/hyperframes` — seekable HTML/CSS timeline video and motion framework; consumed 2026-10 into `/hyperframes`.
- `greensock/gsap-skills` — official GreenSock animation skills (core, timelines, ScrollTrigger, React `useGSAP()`); consumed 2026-10 into `/gsap`.
- `tigerless-labs/autoharness` — real-session skill distillation, evidence chains, and auto-pruning; consumed 2026-10 into `/autoharness`.
- `coldteadotai/pr-lens` — animated architecture and PR diff visualizer (SVG diagrams, ELI5 mode); consumed 2026-10 into `/pr-lens`.
- `howseen-ai/claude-motion-design` — 100% code motion design via HTML + Canvas + Playwright + FFmpeg; consumed 2026-10 into `/motion-design`.
- `mksglu/context-mode` — context window optimization, tool output sandboxing (`ctx_execute`), and SQLite session continuity; consumed 2026-10 into `/context-mode`.
- `cursor/plugins/pstack` + `backnotprop/pstack` — Poteto's rigorous AI engineering orchestrator; consumed 2026-10 into `/poteto-mode` unifying existing leaf skills (`investigate-first`, `lean-build`, `safe-refactor`, `surgical-patch`, `verify-and-stop`).
- `miqdadbadjuber/anti-slop` — 38 mandatory anti-slop rules, 4-block Delivery Gate, liveliness dials; consumed 2026-10 into `/anti-slop`.
- `Tencent/BrowserSkill` — real browser driving & authenticated session reuse (borrow-tab model); consumed 2026-10 into `/browserskill`.
- `NVIDIA-NeMo/DataDesigner` — high-fidelity synthetic enterprise datasets with statistical distributions; consumed 2026-10 into `/data-designer`.
- `arXiv:2609.15078` / ADR-0010 — multi-spec design exploration, typicality scoring, and visual HTML previews; consumed 2026-10 into `/design-explorer`.
- `NVIDIA/SkillEvaluator` — 3-tier validation and benchmarking suite for agent skills; consumed 2026-10 into `/skill-evaluator`.
- `Tencent/SkillHone` (arXiv:2606.08671) — self-evolving agent skill repair loop, execution trace analysis, and regression; consumed 2026-10 into `/skillhone`.
- `zjunlp/SkillNet` (arXiv:2603.04448) — open agent skill discovery, semantic search, and composition; consumed 2026-10 into `/skillnet`.
- `NVIDIA/skillspector` — static security analysis & supply-chain scanner for agent skills; consumed 2026-10 into `/skillspector`.
- local/webgl-experience — real-time WebGL/WebGL2 full-screen animated shaders, 3D scenes, and generative visuals; consumed 2026-11 into /webgl-experience.
- local/webgl-particle-galaxy — real-time GPU particle galaxy, orbiting vertex shader point clouds; consumed 2026-11 into /webgl-particle-galaxy.
- `QingYunA/answer-me-with-html` — one-page visual HTML explainer engine; consumed 2026-11 into `/answer-me-with-html`.
- `china-qijizhifeng/Work2Skill` (arXiv:2610.12984) — human GUI demonstration capture and agentic skill induction; consumed 2026-11 into `/workrecorder-context` and `/work2skill`.
- `ShadowSwaps/REA-Reconstruction-Companion` — evidence-based software reconstruction companion for `/reverse-engineer-anything`; consumed 2026-11 into `/rea-reconstruction-companion`.
- `obra/superpowers` — software development methodology and agent skills framework; consumed 2026-11 into 15 skills (`/brainstorming`, `/diagnosing-superpowers`, `/dispatching-parallel-agents`, `/executing-plans`, `/finishing-a-development-branch`, `/receiving-code-review`, `/requesting-code-review`, `/subagent-driven-development`, `/systematic-debugging`, `/test-driven-development`, `/using-git-worktrees`, `/using-superpowers`, `/verification-before-completion`, `/writing-plans`, `/writing-skills`).
- `oil-oil/oil-ui` — UI design exploration, multi-style comparison views, and screenshot-based visual refinement; consumed 2026-11 into `/oil-ui`.
- `Jakubantalik/transitions.dev` — UI motion agent and crafted transition recipes; consumed 2026-11 into `/transitions-dev`, `/transitions-polish`, `/transitions-ui-generation`, `/transitions-agent`.
- `caru-ini/stack-diagram` — cloud-architecture-style diagrams of tech stacks and infrastructure topologies with real brand logos; consumed 2026-11 into `/stack-diagram`.
- `hugohe3/ppt-master` — AI-driven presentation workflow generating native editable PPTX decks, animations, and narrated slides; consumed 2026-11 into `/ppt-master`.
- `NiazMorshed2007/reanimate` — frame-by-frame animation reverse engineering and replication verifier; consumed 2026-11 into `/reanimate`.
- `heydamir/unslop` — anti-AI-slop interface design, typography, spacing, and craft refinement; consumed 2026-11 into `/unslop`.
- `blader/humanizer` — prose humanizer removing AI writing patterns, forced triads, staged openers, and stock phrasing; consumed 2026-11 into `/humanizer`.
- `shadcn-ui/ui` — official component framework, registry, CLI integration, and Base UI migration; consumed 2026-11 into `/shadcn` and `/migrate-radix-to-base`.
- `nateherkai/scroll-craft` — premium, immersive, scroll-driven websites, 8 page grammars, timeline video scrub, bespoke signature moves, and Playwright verification; consumed 2026-11 into `/scroll-craft`.



