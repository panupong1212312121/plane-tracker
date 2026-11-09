---
name: pr-lens
description: Visualize code diffs, pull requests, and architectures as animated SVG data-flow diagrams. Includes ELI5 simplified explainability mode and graph schema validation.
---

# PR Lens: Animated Architecture & Diff Visualizer

PR Lens draws code changes, pull requests, and architecture systems as animated, self-contained SVG diagrams that render cleanly on GitHub PR comments and web pages.

## Operating Manual

1. **Read the Diff or System Boundary**:
   - For pull requests: `git diff --find-renames <base>...<head>` (using merge-base).
   - For architecture explanations: inspect the module boundaries and contracts.

2. **Generate the Graph Document**:
   - Write `.pr-lens/graph.json` specifying:
     - `lanes`: horizontal or vertical groupings (e.g. Frontend, API, Database).
     - `nodes`: services, components, tables, or modified files.
     - `edges`: calls, dependencies, or data flows.
     - `flows`: step-by-step sequential message exchanges with payloads.

3. **Validate the Graph**:
   ```bash
   npx @coldtea/pr-lens-cli@latest validate .pr-lens/graph.json
   ```
   - The CLI pinpoints the exact JSON field if invalid, enabling rapid self-correction.

4. **Render Animated SVG**:
   ```bash
   npx @coldtea/pr-lens-cli@latest render .pr-lens/graph.json --out out/architecture.svg
   ```

5. **ELI5 Mode (Explain Like I'm 5)**:
   - For non-engineers or high-level stakeholders, use ELI5 mode to strip technical jargon and highlight the user-facing outcome of the change.
   - Reference: see [ELI5 guide](references/eli5.md).

## Synergy with Existing Workflow

- Pairs with `/code-review`: generate an animated diff canvas to accompany the review report.
- Pairs with `/diagram-design`: use PR Lens when animated step-by-step traffic or data-flow animation is superior to static Mermaid diagrams.
