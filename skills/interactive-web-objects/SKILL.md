---
name: interactive-web-objects
description: Build interactive visual objects for the web that the user can interact with — generative art, simulations, particle systems, data-playgrounds, 3D scenes — as an embeddable snippet or single HTML, using canvas 2D, p5.js, or three.js. Use when the user asks for an interactive object/visual/playground on a web page, "ของเล่น interactive", "particle/3D/p5.js/three.js on my site", a canvas toy, or an explorable visual rather than a static image.
---

# Interactive Web Objects

The differentiator from a static page: the object **responds to input**. An object with a render loop but no input handlers is a video, not an interactive object — it doesn't satisfy this skill.

## Pick the renderer

| Need | Renderer | Note |
| --- | --- | --- |
| 2D generative art, particles, playgrounds | **p5.js** (CDN) | Fastest to author; built-in input (`mouseX`, sliders) |
| Custom 2D perf (thousands of particles), minimal deps | **canvas 2D** (vanilla) | No CDN; hand-rolled loop |
| 3D scenes, models, orbiting cameras | **three.js** (CDN) | Needs WebGL fallback message |

Single dependency rule: the object is self-contained — one CDN script max (or zero with vanilla canvas), inline CSS/JS, no build step. It must run by double-click and embed by copy-paste.

## Workflow

1. **Define the interaction contract first.** Before code, write what input does: drag → rotate/add force, click → spawn, scroll/slider → change parameter, keyboard → pause/reset. Include at least one **continuous** interaction (hover/drag), not just buttons. The contract is the acceptance criteria — the object ships when the contract works.
2. **Author as snippet or page.**
   - *Embeddable snippet*: a `<div id="obj-root">` + scoped script that discovers its root by id (no `document.body` assumptions), sized to its container (`ResizeObserver`), so it drops into any page including a `/frontend-slides` deck.
   - *Single page*: full-viewport object with a minimal control bar.
   - Handle `devicePixelRatio` for crisp canvas; cap the particle/render budget and degrade gracefully (fewer particles on small screens); `requestAnimationFrame` with delta-time so speed is framerate-independent.
3. **Touch is input, not an afterthought.** Every pointer interaction has a touch equivalent (pointer events over mouse events). An object that dies on mobile is a finding, not a footnote.
4. **Verify against the contract.** In a headless browser if available: the loop runs (frame count increases), each contract interaction produces its effect (dispatch events, assert state change), no console errors, resize doesn't break it. Without a browser tool: reduce assumptions and state the verification was manual.
5. **Deliver.** Embeddable: root div + snippet + CDN tag, with the exact drop-in instructions. Page: file path + how to open, and that `/ship-it` can put it on a URL.

## Guardrails

- Ship by the interaction contract — "it renders" is never the done-state.
- No `alert/confirm` for in-object feedback; visual state changes are the feedback.
- Pause the loop when the tab is hidden (`document.visibilityState`) — background CPU burn is a defect.
- Performance is a contract: if the object targets 60fps, state the measured fps; a stuttering object ships with the stutter reported, not hidden.
- Keep the source as the artifact; note which CDN version the snippet pins (pin the major version, don't float on `@latest`).
