---
name: skillnet
description: Discover, search, evaluate, and compose public agent skills from external skill networks and open repositories based on zjunlp/SkillNet (arXiv:2603.04448). Enables searching existing open-source agent capabilities before deciding to CREATE NEW, semantic matching against problem briefs, multi-skill orchestration, and supply-chain safety screening via skillspector before import. Companion to /skill-planner enforcing the "Search before Build" discipline. Use when exploring external skills for a new capability, searching public skill hubs, evaluating third-party skill quality, or composing multi-skill pipelines.
metadata:
  version: "1.0"
  author: local
---

# SkillNet (Open Agent Skill Discovery & Composition)

SkillNet (zjunlp/SkillNet, arXiv:2603.04448) provides a semantic discovery, evaluation, and composition layer for AI agent skills across open-source ecosystems. In a skill hub, authoring a new skill from scratch when a mature, battle-tested implementation already exists wastes effort and fragments standards. SkillNet enforces the **"Search before Build"** discipline: before `/skill-planner` issues a `CREATE NEW` verdict, SkillNet queries curated external pools and public skill registries to identify potential candidates for adoption or companion authoring.

## Discovery & Adoption Lifecycle

```
1. Formulate Need ─► 2. Semantic Search ─► 3. Supply-Chain Scan
                                                    │
5. Lock & Sync Hub ◄── 4. Planner Decision ◄────────┘
```

### 1. Formulate Capability Need

Extract the core capability brief from user requirements or `/skill-arbiter` candidate notes:
- Primary task domain (e.g. cloud deployment, database migration, canvas rendering, data cleaning).
- Required tools or execution environments (CLI, MCP, Python libraries).
- Specific platform constraints (Windows PowerShell compatibility, offline execution).

### 2. Semantic Search Across Catalogs

Query known upstream catalogs (including those listed in `docs/agents/skills.md` Upstream Source Catalog) or public skill indices:

```bash
# Search public registries by capability description
uv run skillnet search "timeseries anomaly detection BigQuery" \
  --limit 5 \
  --min-stars 50

# Inspect metadata and skill structure of a candidate
uv run skillnet inspect "github:owner/repo/skills/anomaly-detect"
```

### 3. Mandatory Supply-Chain Security Scan

Before any external skill is imported or downloaded to local storage, it must undergo offline static analysis via `skillspector` (Rule 6 in `docs/agents/skills.md`):

```bash
# Scan downloaded candidate without sending files to external LLMs
skillspector scan .scratch/downloaded-candidates/<candidate-name> --no-llm
```

Review findings against the triage rubric: pattern false positives on assets/examples are triaged; actual remote execution or privilege escalation halts adoption.

### 4. Planner Harmonization & Verdict

Submit the candidate to `/skill-planner`:
- **NO-SKILL:** Candidate duplicates existing tools or native repo scripts.
- **EXTEND:** Capability naturally belongs in an existing local skill.
- **COMPANION:** Candidate addresses a need alongside an upstream-locked skill.
- **CREATE NEW / IMPORT:** Candidate is unique, clean, and fills an unmet repo need.

### 5. Ingestion, Lock, and Sync

If approved:
1. Copy into canonical `skills/<skill-name>/`.
2. Compute hash baseline and register in `skills-lock.json`.
3. Run `scripts/audit-skills.ps1 -Skill <skill-name>`.
4. Propagate across agent directories via `powershell -File scripts/sync-skills.ps1`.

## Guardrails

- **Zero Uninspected Ingestion:** Never import an external skill directly into `skills/` without running `skillspector scan --no-llm` first.
- **Anti-Catalog Hoarding:** Never bulk-import whole repositories or massive skill dumps. Ingest only the specific capability required by real tasks.
- **Provenance Integrity:** Always record the exact git commit, upstream repository URL, and license in `skills-lock.json`.

