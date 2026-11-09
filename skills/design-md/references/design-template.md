# design.md template

Copy this skeleton when drafting `design.md`. The YAML token block carries exact values with no prose; the prose sections carry the *why* for every key. A coverage check must pass: every YAML key has a prose entry, and every prose entry cites `{token.refs}`.

````markdown
# design.md — <Product / Brand Name>

Design system for agents and humans. Read this before generating or editing any UI.

## Tokens

```yaml
meta:
  name: ""                      # product/brand name
  version: 1
  updated: YYYY-MM-DD
colors:
  canvas: "#FFFFFF"             # page background
  surface-card: "#FFFFFF"       # card/plate surfaces
  ink: "#0A0A0A"                # primary text
  ink-muted: "#666666"          # secondary text
  primary: "#0070F3"            # brand action color
  on-primary: "#FFFFFF"
  primary-active: "#0060D1"
  accent: "#FF5B4F"             # secondary highlight + the job it does
  success: "#0CAF60"
  warning: "#F5A623"
  danger: "#E5484D"
  hairline: "#EAEAEA"           # 1px borders
typography:
  font-display: "Inter"         # headings
  font-body: "Inter"            # body
  scale-px: [12, 14, 16, 20, 24, 32, 48, 64]
  tracking-display: "-0.02em"   # and why
rounded:
  sm: 6px
  md: 10px
  lg: 16px
spacing:
  unit: 4px
  scale-px: [4, 8, 12, 16, 24, 32, 48, 64, 96]
shadows:
  card: none                    # or "0 1px 2px rgba(0,0,0,0.05)"
motion:
  duration-fast: 150ms
  duration-base: 250ms
  easing: "cubic-bezier(0.2, 0, 0, 1)"
components:
  button-primary: { bg: "{colors.primary}", text: "{colors.on-primary}", radius: "{rounded.md}" }
  button-secondary: { bg: "transparent", border: "1px {colors.hairline}", text: "{colors.ink}" }
  card: { bg: "{colors.surface-card}", radius: "{rounded.lg}", border: "1px {colors.hairline}" }
  input: { bg: "{colors.canvas}", border: "1px {colors.hairline}", radius: "{rounded.sm}" }
```

## Visual Theme & Atmosphere

<mood words; density (airy/compact); the philosophy in one sentence, e.g.
"Minimalism as engineering principle"; 2–3 reference products and what exactly
is borrowed from each — the feel, never the pixels.>

## Color Palette & Roles

<One entry per color: name, hex, the job it does, and why. Example shape:
"`#FF5B4F`, ship red — reserved for the production deploy flow, because
shipping should feel urgent." Include the semantic set and the dark-mode
decision (yes/no; if yes, the canvas/ink swap).>

## Typography Rules

<Font pairing and where each style goes and why. Include the hierarchy table
(style / size / weight / line-height / tracking / used for) and any quirks
(e.g. "display sizes get -2.4px tracking because headlines should feel like
minified code", tabular numerals in tables).>

## Component Stylings

<One prose entry per key in the YAML `components:` block — 1:1. Each entry
describes surface, typography, padding, radius, and states, citing
`{token.refs}` instead of inline values. Example shape:
"**`button-primary`** — the signature CTA. Background `{colors.primary}`,
text `{colors.on-primary}`, padding 10px × 18px, radius `{rounded.md}`.
Press state shifts to `{colors.primary-active}`. No hover state documented.">

## Layout Principles

<Spacing scale and how it is applied; grid/columns per surface; container
max-widths; the whitespace philosophy in one sentence.>

## Depth & Elevation

<Shadow system vs 1px borders; surface hierarchy (canvas → plate → overlay);
corner-radius scale and when each radius is used.>

## Do's and Don'ts

<Guardrails and banned anti-patterns, as concrete rules. Example shape:
"No purple-blue gradients — the brand reads engineered, not decorative."
"Do: 1px hairline borders instead of shadows for separation."
Accessibility floor: minimum contrast, focus rings, touch-target minimum.>

## Responsive Behavior

<Breakpoint table (name / width / key changes), touch targets with the WCAG
level claimed, and the collapsing strategy for nav, grid, spacing, forms.>

## Agent Prompt Guide

<Quick token reference (canvas / ink / primary / font one-liner) and 2–3
ready-to-use prompts the user actually types, e.g. "Build a pricing page
following design.md — hairline borders, no shadows, Inter throughout.">

## Known Gaps

<Explicit list of what is NOT yet decided or covered — animation timings,
error/success state visuals, dark-mode variants, sub-brands. Stating gaps
keeps the contract honest. Items marked `agent-recommended` in the interview
are listed here too, so the user can revisit them.>
````
