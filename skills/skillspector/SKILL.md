---
name: skillspector
description: Security scanner and supply-chain auditor for AI agent skills using NVIDIA skillspector. Runs static analysis (AST, regex, YARA) across SKILL.md, scripts, assets, and references to detect prompt injection, privilege escalation, anti-refusal patterns, dangerous tool executions, and security hygiene issues. Enforces the --no-llm offline execution rule and categorization triage guidelines documented in docs/agents/skills.md Rule 6-7. Use when importing new upstream skills, refreshing existing skills, performing security reviews of skills, or auditing agent capabilities for supply-chain risks.
metadata:
  version: "1.0"
  author: local
---

# SkillSpector (Agent Skill Security & Supply-Chain Audit)

NVIDIA SkillSpector is a static security analysis tool purpose-built for AI agent skills. As research indicates over 25% of public agent skills possess security vulnerabilities or excessive agency (Liu et al., 2026), SkillSpector acts as the **mandatory supply-chain gate** (Rule 6 in `docs/agents/skills.md`) before any external skill is admitted into the repository's canonical skill hub.

## CLI Execution & Mandatory Flags

All scans must use `--no-llm` by default to prevent sending local repository contents or skill instructions to external LLM providers:

```bash
# Standard supply-chain scan for an incoming skill (offline, zero-exfiltration)
uv run skillspector scan skills/<skill-name> --no-llm

# Output structured JSON for logging and audit trail
uv run skillspector scan skills/<skill-name> --no-llm --format json > .scratch/security-scans/<skill-name>.skillspector.json

# Rescan against a baseline suppressing known false positives
uv run skillspector scan skills/<skill-name> --no-llm --baseline .scratch/security-scans/<skill-name>.baseline.yaml
```

## Triage Rubric (Rule 7 from `docs/agents/skills.md`)

A SkillSpector score must be read as **triage, never as a verdict**. The overall numeric score (0–100) is easily inflated by literal pattern matches on benign HTML examples, mock data, or SVG comments:

| Category | Typical Example | Triage Action |
| --- | --- | --- |
| **Prompt Injection (PI)** | `<!-- comment in example HTML -->` | **False Positive** if located inside `assets/` or example blocks. Verify line and suppress. |
| **Anti-Refusal (AR)** | "NO WARNING" text in UI mockup image | **False Positive** if part of UI copy or design preview. Confirm context. |
| **analysis-evasion** | `is_complete=false`, partial file parse | **Coverage Gap**, not an attack finding. Re-scan pointing directly to file. |
| **Privilege Escalation** | `os.system()`, raw shell execution | **Investigate immediately.** Require structured `subprocess.run(shell=False)` or reject. |
| **MCP Least Privilege** | Missing `allowed-tools` in frontmatter | **Hygiene note.** Add explicit tool whitelist to frontmatter where appropriate. |

## Workflow: Importing Upstream Skills

```
1. Fetch Candidate ─► 2. Run skillspector --no-llm ─► 3. Category Triage
                                                              │
5. Lock & Baseline ◄── 4. Fix Hygiene / Suppress FP ◄─────────┘
```

1. **Scan:** Run `skillspector scan <path> --no-llm`.
2. **Review JSON:** Inspect individual findings by category and exact file line.
3. **Remediate:** If genuine risks exist (e.g. unsafe shell commands, hardcoded API endpoints), reject or patch.
4. **Baseline:** If high scores are driven by documentation examples, record baseline in `.scratch/security-scans/<skill-name>.baseline.yaml`.
5. **Record Ledger:** Record the scan summary and triage notes in the candidate ledger before committing to `skills-lock.json`.

## Guardrails

- **Mandatory Offline Mode:** The `--no-llm` flag is mandatory. Never execute scans in cloud LLM mode without explicit human authorization.
- **Never Rely on Score Alone:** Never reject a legitimate skill solely based on a high numerical score without opening and checking the reported lines.
- **No Binary Pass/Fail in CI:** Do not block CI on raw score thresholds; gate on genuine findings (Privilege Escalation, Unsanitized Shell Execution) after triage.

