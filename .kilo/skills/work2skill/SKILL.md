---
name: work2skill
description: Induce and author reusable AI agent skills from human GUI demonstrations, operation recordings, and multimodal task evidence using the Work2Skill methodology. Connects human UI actions (mouse, keyboard, window states) and visual traces with structured skill induction, separating reusable operational invariants from episode-specific noise. Use when recording user workflows, converting GUI traces into portable skill definitions, analyzing human computer-use patterns, or pairing with WorkRecorder.
metadata:
  version: "1.0"
  source: china-qijizhifeng/Work2Skill
  license: MIT
---

# Work2Skill: GUI Demonstration to Reusable Agent Skill Induction

Work2Skill connects human GUI demonstrations with reusable agent skills through operation recording, multimodal evidence inspection, and agentic skill induction (arXiv:2610.12984).

## Overview

The intended workflow is:
**Record demonstrations → Export task evidence → Induce reusable skills → Evaluate on downstream tasks**.

1. **Demonstration Capture**: Use WorkRecorder (`workrecorder-context` skill or native daemon) to capture human GUI operations (clicks, scrolls, key events, active window metadata, and frame checkpoints).
2. **Multimodal Evidence Inspection**: Inspect action sequences (`actions.jsonl`), keylogs (`keylog.jsonl`), and visual screenshots/video frames.
3. **Agentic Skill Induction**: Abstract the observed behavior into a self-contained skill folder (`SKILL.md` + supporting scripts/references) that any coding/computer-use agent can execute with fresh inputs.

## Skill Induction Rules

- **Preserve Modality & Invariants**: Maintain the application's actual interaction semantics. Do not replace UI controls with hidden API mutations unless explicitly part of the target task.
- **Extract Operational Rules, Not Episodic Traces**: Strip out transient timing delays, accidental miss-clicks, absolute window pixel offsets, and personal user data. Extract semantic selectors, UI state preconditions, verification steps, and recovery routines.
- **Self-Contained Execution**: Put correctness-critical logic directly into `SKILL.md`. Ensure that required tools, scripts, and format contracts are completely documented.
- **Evidence-Linked Grounding**: Link inducted rules to recorded evidence checkpoints (action index or frame timestamp) during authoring for traceability.

## References

- Overview & Architecture: [overview.md](references/overview.md)
- Induction Setup & Guide: [induction_guide.md](references/induction_guide.md)
- System Prompt Template: [system_prompt.md](references/system_prompt.md)
- WorkRecorder Context Skill: see `workrecorder-context`

