---
name: skill-evaluator
description: Run the 3-tier validation and benchmarking suite for agent skills using NVIDIA SkillEvaluator. Tier 1 executes keyless, deterministic quality gates (schema, pii, license, quality, unicode, lint); Tier 2 performs semantic overlap detection across skill libraries; Tier 3 runs synthetic eval dataset generation and live behavioral benchmarking against agent models. Use during skill creation (/skill-creator) and optimization (/skill-optimize) to guarantee skill quality before locking and syncing. Use when validating new or updated skills, running quality benchmarks, or checking for semantic skill overlap.
metadata:
  version: "1.0"
  author: local
---

# SkillEvaluator (3-Tier Agent Skill Evaluation & Quality Gates)

NVIDIA SkillEvaluator is a comprehensive evaluation framework for AI agent skills. It establishes an evidence-based quality ladder for skills across three tiers, moving from fast, keyless deterministic checks to semantic overlap auditing and live behavioral agent benchmarks.

## 3-Tier Quality Architecture

```
▲  Tier 3: Synthetic Eval Datasets & Live Agent Benchmarks (Quota-Gated)
│  Tier 2: Semantic Overlap & Redundancy Detection (Embeddings / Provider)
│  Tier 1: Deterministic Quality Gates (Keyless, Free, Run on Every Change)
```

### Tier 1: Deterministic Quality Gates (Mandatory & Keyless)

Fast static checks that require zero external credentials or network calls:

- **Schema Check:** Validates YAML frontmatter, required keys (`name`, `description`), and field types.
- **PII Guard:** Scans for hardcoded emails, phone numbers, secret keys, or identifiable personal records.
- **License Compliance:** Confirms license identifiers match repo policy.
- **Quality & Format:** Assesses markdown structure, heading hierarchies, code block tags, and brevity (<400 lines for SKILL.md).
- **Unicode & Lint:** Checks for illegal non-printable control characters, BOM artifacts, and line ending hygiene.

```bash
# Run Tier 1 quality checks on a specific skill
uv run skillevaluator validate skills/<skill-name> \
  --checks schema,pii,license,quality,unicode,lint \
  --no-dedup
```

### Tier 2: Semantic Overlap Detection (Provider Required)

Analyzes semantic similarity against all existing skills in `skills/` to prevent capability fragmentation and redundant skill proliferation:

```bash
# Check if a proposed skill duplicates existing capabilities
uv run skillevaluator check-overlap \
  --candidate skills/<candidate-name> \
  --catalog skills/ \
  --threshold 0.85
```

### Tier 3: Synthetic Eval Datasets & Live Agent Benchmarks

Generates realistic task prompts and executes them against an agent harness to measure whether the skill actively improves task success rates:

```bash
# Generate synthetic evaluation tasks
uv run skillevaluator create-eval-dataset \
  --skill skills/<skill-name> \
  --num-samples 10 \
  --output .scratch/evals/<skill-name>-eval.json

# Run live benchmark execution
uv run skillevaluator benchmark \
  --skill skills/<skill-name> \
  --dataset .scratch/evals/<skill-name>-eval.json \
  --harness local-agent
```

## Integration with Hub Lifecycle

- **Pre-Commit Gate:** Every new or edited skill must pass Tier 1 checks before updating `skills-lock.json`.
- **Optimization Loop (`/skill-optimize`):** Bounded edits to `SKILL.md` are accepted only when SkillEvaluator metrics strictly improve or remain equal with justified repairs.
- **Companion to `scripts/audit-skills.ps1`:** While `audit-skills.ps1` checks repo-specific links and lock states, SkillEvaluator inspects inner agent instructability and linguistic quality.

## Guardrails

- **Keyless by Default:** Tier 1 is mandatory for all skill changes and must never require API keys or network requests.
- **Quota Confirmation:** Tiers 2 and 3 consume provider API credits — always obtain explicit user confirmation before executing Tier 2/3 commands.
- **No Gate Softening:** Never disable or weaken Tier 1 check flags to force a failing skill to pass; fix the underlying document or formatting defect.

