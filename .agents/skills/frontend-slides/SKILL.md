---
name: frontend-slides
description: Convert content into zero-dependency, animation-rich HTML presentations (slides for talks, pitches, or demos). Single self-contained HTML file with a fixed 16:9 stage scaled to the viewport, inline CSS/JS, style-preset discovery by previewing rather than asking abstract questions. Use when the user asks for slides, a presentation, a pitch deck, to convert content/markdown into HTML slides, or says "นำเสนอ"/"เล่มพรีเซนต์".
---

# Frontend Slides

Build a presentation as **one self-contained HTML file**: inline CSS/JS, no npm, no build step — double-click to run. The artifact is shareable and deployable with `/ship-it` later.

## Non-negotiable: fixed 16:9 stage

Every deck uses a 1920×1080 slide canvas scaled as a whole to the viewport, so slides stay 16:9 on every screen including phones. Never use per-slide responsive reflow. The scale is computed once on load/resize:

```css
html, body { margin: 0; background: #000; overflow: hidden; }
.deck { width: 1920px; height: 1080px; position: absolute; left: 50%; top: 50%;
        transform-origin: center; }
.slide { width: 1920px; height: 1080px; display: none; }
.slide.active { display: block; }
```

```js
function fit() {
  const s = Math.min(innerWidth / 1920, innerHeight / 1080);
  document.querySelector('.deck').style.transform =
    `translate(-50%, -50%) scale(${s})`;
}
addEventListener('resize', fit); fit();
```

Navigation: arrow keys, click zones, swipe (touchstart/touchend delta), and `?n` deep links. Show a small page counter. No navigation UI that overlaps slide content.

## Process

### 1. Read the content first

Identify the material to convert: markdown, a doc, a spec (`.scratch/<slug>/spec.md` is a common source), or free-form text the user pastes. Derive a slide outline: one idea per slide, title + a few bullets or a visual — never paragraph dumps. Target a count from the material, not a default.

### 2. Pick a style by previewing, not asking

"Do you want dark or light?" is a banned question. Instead, build the outline once and render **2–3 full first-slide previews as small cards** in the same HTML (switchable by a floating preview bar), each a complete aesthetic: preset colors, fonts, signature element. The user picks by seeing it, then the full deck inherits that style. If the project has a `design.md`, treat it as the default preset and preview alternatives beside it.

No generic "AI slop": no default blue/purple gradients, no centered hero with emoji, no font defaulting to system-ui as a *choice* (only as an explicit fallback). Every deck must feel custom-crafted.

### 3. Generate the deck

- Semantic structure per slide: `<section class="slide">` with a real `<h1>`/`<h2>` hierarchy.
- Animations are CSS-first (fade/slide/stagger via `animation-delay`), triggered on `.active`. Keep total animation budget light: entrance effects, not busy motion.
- Images use **relative paths** (so the file moves with its directory); remote images are fine when a URL is given.
- Speaker notes: `<aside class="notes">` inside each slide, toggled with `s`, hidden by default.
- If a chart is needed, Chart.js from CDN is allowed (the only permitted external script); set `?export`-style static mode when PDF/screenshots are expected.

### 4. Verify before handing off

- **Overflow check**: for each slide, confirm no content extends past the 1920×1080 stage — measure `scrollHeight > 1080` (or `scrollWidth > 1920`) per `.slide` in a headless browser if available; otherwise reduce content density and state the check was manual.
- Screenshot the first and a mid slide for visual proof when a browser tool is available.
- All content present: diff the outline against the slides; no silently dropped section.

## Deliver

Report: file path, slide count, chosen style, navigation summary, and how to open/share (double-click, or `/ship-it` to get a URL). If the user wants PDF, export via headless-browser print of `.slide.active` pages (one page per slide, 1920×1080) and note animations flatten to their final visual state.
