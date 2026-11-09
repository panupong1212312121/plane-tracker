---
name: design-md
description: Interview the user step by step to capture their project's own design system — theme, colors, typography, components, layout, elevation, guardrails — and save it as design.md at the repo root for the user and agents to read before any UI work. Use when the user wants to create, update, or review a design.md / DESIGN.md file, asks to document their design system, or says "design interview".
---

# design-md

Create or update `design.md` at the repo root: a semantic design-system document that both the user and AI agents read before writing any UI.

This implements the DESIGN.md concept introduced by Google Stitch and popularized by [getdesign.md](https://getdesign.md/what-is-design-md): a plain markdown file that describes a design system semantically. Not a token list, not a Figma export. It reads like a designer explaining a brand's visual language to a developer seeing it for the first time. The differentiator is that **token, rule, and rationale live in the same file** — a token says what to use, a rule says where, and the rationale lets an agent make the right call in a situation the file never covers.

**Core rule: nothing generic survives.** "Modern and clean" is banned as an answer. Every answer must end up as a concrete value (hex, px/rem, a named font) or a concrete behavior, plus a reason. When the user has no preference, derive a recommendation from their brand and project signals, propose it, and mark it `agent-recommended` in the file.

## Output contract

- File: `design.md` at the repo root (lowercase).
- Structure: follow [references/design-template.md](./references/design-template.md) exactly — a YAML token block followed by prose sections. Every YAML key gets a prose entry; every prose entry cites `{token.refs}`.
- Every section is either filled with concrete values or explicitly listed under `## Known Gaps` as not yet decided. Never leave silent holes.
- If a `design.md` or `DESIGN.md` already exists, switch to **update mode**: diff what is there, interview only about gaps and outdated parts, and preserve user-written rationale verbatim.

## Process

### 1. Gather signals (before asking anything)

Read what the project already says, so you only ask what you cannot discover:

- Existing `design.md` / `DESIGN.md`, `AGENTS.md`, `CONTEXT.md`, README
- `package.json` (or equivalent manifests) for UI dependencies: tailwind, shadcn/ui, MUI, styled-components, framer-motion, etc.
- Global CSS / CSS variables / tailwind config for tokens already defined
- Fonts in use, existing components, brand assets, screenshots

Present a short summary of the signals found, then start the interview. Never ask for a value the repo already answers — confirm the discovered value instead ("Found `#0070F3` as your link color — keep?").

### 2. Interview in rounds

Ask **2–4 questions per round**, in the user's language, one section at a time, in this order:

| Round | Section | Ask about |
| --- | --- | --- |
| 1 | Visual Theme & Atmosphere | 3–5 mood words; density (airy vs compact); the design philosophy in one sentence; 2–3 products/sites whose *feel* they want |
| 2 | Color Palette & Roles | canvas/background, ink/text, primary **and the job it does**, accent, semantic colors (success/warning/danger), dark mode yes/no |
| 3 | Typography | display/body font pairing, size hierarchy, tracking quirks, numeral style |
| 4 | Component Stylings | buttons (primary/secondary/ghost + states), cards, inputs, navigation voice |
| 5 | Layout Principles | spacing scale, grid/columns, container widths, whitespace philosophy |
| 6 | Depth & Elevation | shadows vs 1px borders, surface hierarchy, corner-radius scale, motion feel |
| 7 | Do's and Don'ts | anti-patterns to ban (purple-blue gradients? centered heroes? emoji?), accessibility floor |
| 8 | Responsive Behavior | breakpoints, touch-target sizes, collapsing strategy for nav/grid/forms |
| 9 | Agent Prompt Guide | confirm the quick token reference; collect 2–3 ready-to-use prompts the user actually types |

Interview rules:

- Lead every question with a recommended answer derived from the signals, so the user can accept it in one word.
- Offer multiple choice where possible; free text is always allowed.
- When an answer is vague ("clean", "professional"), ask exactly one follow-up that converts it into a value: "clean — meaning flat surfaces with 1px borders instead of shadows, like Vercel? or generous whitespace with large type, like Linear?"
- Keep going until **all 9 sections** have concrete answers or explicit agent-recommended defaults. Do not stop early because the user seems tired — instead offer to mark the remaining sections as agent-recommended and list which ones those are.
- Track answers as you go; never re-ask something already answered.

### 3. Draft and confirm

Assemble the full `design.md` from the template. Show the complete draft, highlight every agent-recommended default so the user can veto them individually, and let them edit before anything is written.

### 4. Write and wire

1. Write `design.md` at the repo root.
2. If `AGENTS.md` or `CLAUDE.md` exists, add or update a one-line pointer under `## Agent skills` telling agents to read `design.md` before UI work. Edit whichever one already exists; never create both.
3. Tell the user: any agent that reads the repo root (Claude Code, Cursor, Windsurf, ...) will now follow the file; they can edit `design.md` by hand at any time, and re-running this skill refreshes it in update mode.

## References

- [references/design-template.md](./references/design-template.md) — the exact output structure; copy this skeleton when drafting.
