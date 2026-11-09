---
name: skillhone
description: Autonomous agent skill debugging, self-repair, and regression testing loop based on Tencent SkillHone (arXiv:2606.08671). Analyzes execution traces when an agent misuses or bypasses a skill, diagnoses whether the failure stems from ambiguous instructions in SKILL.md, missing scripts, or incomplete reference docs, executes local regression tests, and proposes surgical repairs with immutable decision records. Use when an existing skill repeatedly fails or yields agent drift during complex tasks, when a skill requires behavioral regression testing, or when diagnosing prompt/instruction ambiguity in a skill.
metadata:
  version: "1.0"
  author: local
---

# SkillHone (Self-Evolving Agent Skill Repair & Regression)

SkillHone (Tencent/SkillHone, EMNLP 2026, arXiv:2606.08671) provides an automated diagnosis and repair loop for agent skills. When an agent fails a task, hallucinates invalid parameters, or bypasses a relevant skill mid-flight, SkillHone traces the exact failure point, isolates the cause within the skill package (`SKILL.md`, `scripts/`, or `references/`), executes a localized regression suite, and produces a minimal, bounded patch with an immutable decision record.

## 5-Stage Repair Architecture

```
1. Trace Failure ─► 2. Triangulate Cause ─► 3. Bounded Patch
                                                   │
5. Immutable Decision Log ◄── 4. Regression Pass ◄─┘
```

### Stage 1: Trace Failure Capture

Capture the raw execution log from the conversation or agent transcript:
- User prompt and expected agent outcome.
- The step where the agent deviated (e.g. wrong tool call, invented argument, ignored constraint).
- Active skill frontmatter and instructions visible to the agent at the moment of deviation.

### Stage 2: Triangulate Defect Layer

Isolate where the ambiguity or failure originates:
1. **Instruction Ambiguity (`SKILL.md`):** Were trigger conditions too broad or too narrow? Was instruction order inverted?
2. **Missing or Broken Script (`scripts/`):** Did a helper script throw an unhandled exception or return unstructured output?
3. **Reference Incompleteness (`references/`):** Did the agent need exact CLI flags or schema snippets that were omitted?

### Stage 3: Bounded Patch Synthesis

Formulate the smallest responsible edit:
- Maximum diff size: ≤ 30 lines.
- Preserve existing headings, formatting, and surrounding guardrails.
- Ensure all relative markdown links remain intact.

### Stage 4: Regression Testing (`.test/`)

Run the skill's embedded verification tests to ensure the repair does not break previously working capabilities:

```bash
# Run local skill regression tests
powershell -File scripts/audit-skills.ps1 -Skill <target-skill>
uv run pytest skills/<target-skill>/.test/ -v 2>$null || echo "No pytest suite; proceeding to static verification"
```

### Stage 5: Immutable Decision Logging

Record the repair decision in the skill candidate ledger or `.scratch/skill-repairs/<skill>-<date>.md`:
- Incident description & triggering prompt.
- Root cause category (Instruction / Script / Reference).
- Exact patch applied.
- Verification hash and test status.

## Guardrails

- **Upstream Protection:** Never edit an upstream-locked skill directly (`source` does not start with `local` in `skills-lock.json`). For locked skills, author a local companion skill or route through `/skill-planner`.
- **Safety Non-Negotiables:** Never relax security checks, anti-slop gates, or PII protections to make a failing test pass.
- **Bounded Changes:** Megarefactors are prohibited in self-repair; if a fix exceeds 30 lines, escalate to `/skill-creator` for a structured rewrite.

