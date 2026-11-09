---
name: design-explorer
description: Explore and evaluate multiple structured design options before committing to design tokens in design.md. Generates at least 3 distinct sub-specifications with varied macrostructures and visual directions, assigns typicality scores per arXiv:2609.15078, renders standalone HTML preview artifacts for user visual selection, and writes the selected direction to design.md. Companion to /design-md implementing ADR-0010 Steps 1-2. Use when exploring UI layout ideas, deciding aesthetic directions, evaluating design choices, or when design.md has open questions.
metadata:
  version: "1.0"
  author: local
---

# Design Explorer (Multi-Spec Exploration & Visual Preview)

Design Explorer is an interactive design exploration companion to `/design-md` and `/frontend-design`, implementing Steps 1–2 of ADR-0010 based on empirical diversity principles from arXiv:2609.15078. Instead of locking into the first prompt completion or asking abstract questions, Design Explorer synthesizes **at least 3 structured sub-specifications with distinct macrostructures**, calculates their typicality scores, renders standalone interactive HTML previews, and lets the user choose visually before committing choices to `design.md`.

## Boundary & Relationships

- `/design-md`: Holds the single source of truth for repository design tokens, theme, and guardrails.
- `/frontend-design`: Owns component-level build craft and anti-slop execution during feature implementation.
- `/design-explorer`: Companion that generates exploratory variants and standalone HTML previews *before* tokens are locked into `design.md`.

## 5-Step Exploration Loop

```
1. Identify Open Design Slots ─► 2. Generate ≥3 Variants ─► 3. Compute Typicality
                                                                       │
5. Lock Winner into design.md ◄── 4. Render HTML Previews ◄────────────┘
```

### 1. Identify Open Design Slots

Inspect `design.md` or the feature request to identify unresolved choices:
- Visual personality (corporate utility vs editorial vs technical high-density)
- Color scheme & dark/light contrast balance
- Navigation macrostructure (sidebar collapsible vs top breadcrumb vs split command pane)
- Typography pairings (neutral sans vs technical monospace vs serif accents)

### 2. Synthesize ≥3 Distinct Variants

Construct 3 divergent specifications. Never vary only colors; change the **macrostructure**:

- **Variant A (Conventional / High Typicality):** Safe, highly familiar layout (e.g. standard left sidebar, top header, clean tabular view). Minimum cognitive overhead.
- **Variant B (Expressive / Editorial):** Asymmetrical balance, distinct typography, prominent hero cards, intentional whitespace.
- **Variant C (Dense / Power-User):** High information density, keyboard-first command bars, inline inspectors, split-pane multi-column views.

### 3. Compute Typicality & Trade-Offs

Rate each variant on typicality (0.0 = completely novel/unconventional, 1.0 = standard industry pattern) per arXiv:2609.15078:

| Variant | Typicality | Primary Strength | Primary Risk |
| --- | --- | --- | --- |
| **A (Standard)** | 0.85 | Instantly familiar, zero onboarding friction | May feel generic if anti-slop rules are ignored |
| **B (Editorial)** | 0.45 | Memorable brand identity, strong visual hierarchy | Less suited for dense CRUD data entry |
| **C (Compact)** | 0.65 | Maximum throughput for domain specialists | Steeper initial learning curve |

### 4. Render Standalone HTML Previews

Produce a self-contained preview artifact (e.g., `.scratch/design-previews/variant-{a,b,c}.html`):
- Single-file HTML with inline CSS.
- Zero external build dependencies or heavy CDNs.
- Real rendered components: header, main content, cards, action buttons, and sample data.
- Include a switcher bar at the top allowing the user to toggle between variants instantly.

### 5. Lock Winner into `design.md`

Once the user selects a variant:
1. Extract chosen colors, typography, spacing tokens, and structural rules.
2. Update `design.md` at the repo root.
3. Clean up scratch previews or archive them into `.scratch/design-previews/`.

## Guardrails

- **Enforce Anti-Slop Universally:** Every variant must strictly obey the anti-slop rules (`/anti-slop`) — no generic purple gradient heroes, no centered emoji lists, no unstyled default badges.
- **No Invisible Options:** Always render visual HTML previews rather than asking the user to imagine layouts from text descriptions.
- **Local Rendering:** Previews must load immediately in any local browser without requiring internet access or npm dev servers.

