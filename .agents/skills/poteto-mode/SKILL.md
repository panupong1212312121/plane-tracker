---
name: poteto-mode
description: Master engineering orchestrator for rigorous AI development. 'Go deep first', learning before editing, strict non-negotiables, verified work, and seamless routing across investigate-first, lean-build, safe-refactor, surgical-patch, and verify-and-stop.
---

# Poteto Mode: Rigorous Engineering Orchestration

Poteto mode coordinates the suite of engineering discipline skills in this repository. It enforces evidence-first problem solving, minimal invasive edits, and deterministic verification.

## The Non-Negotiables

1. **Go Deep First (Understand Before Touching)**:
   - Never write code based on assumptions. Inspect existing types, domain rules, and error traces before modifying any file.
   - Route ambiguous bugs to `/investigate-first`.

2. **Classify Questions Before Asking**:
   - If an answer can be settled by running an experiment, writing a quick script, or checking test output, **do not ask the user**.
   - Reserve human questions only for genuine product decisions and preference forks.

3. **Surgical Scope & Preservation**:
   - Fix bugs at the narrowest responsible layer (`/surgical-patch`).
   - When building features, prevent scope creep with `/lean-build`.
   - When refactoring, bracket changes with verification to guarantee zero behavior drift (`/safe-refactor`).

4. **Proof of Delivery**:
   - Close every task with tangible, reproducible proof (`/verify-and-stop`):
     - Unit / integration test run (green).
     - Type check / lint run (clean).
     - Explicit verification of boundary conditions.

## Orchestration Routing

| Trigger / Need | Target Specialist Skill |
| --- | --- |
| Ambiguous failure / unknown cause | `/investigate-first` |
| Known cause / targeted bug fix | `/surgical-patch` |
| New capability with overbuilding risk | `/lean-build` |
| Structural consolidation or code cleanup | `/safe-refactor` |
| Persisted data or public contract migration | `/migration` |
| Acceptance verification & stopping criteria | `/verify-and-stop` |
