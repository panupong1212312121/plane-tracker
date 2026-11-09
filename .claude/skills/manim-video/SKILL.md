---
name: manim-video
description: Create math/algorithm/explainer animation videos with Manim (.mp4 or .gif) — scene authoring from a bounded outline, render, frame verification, and optimization for embedding into HTML or delivery as a standalone file. Use when the user asks for an animation, math video, explainer video, .gif/.mp4 for a page, "วิดีโอประกอบ", "ทำ motion อธิบาย", or a visual walkthrough of an algorithm/equation.
---

# Manim Video

Produce an animation with Manim that is **verified frame by frame** — a render that exits 0 proves nothing about readability. Requires Python and Manim (`pip install manim` plus ffmpeg; check `manim --version` first and give install instructions when missing).

## Workflow

1. **Bounded outline first.** From the user's request, write the scene beats in 5–10 numbered steps (what appears, what moves, what the viewer should conclude at each step). Beats not in the outline don't get rendered; an outline the user didn't confirm for long/deep topics is stated as an assumption. Long explanations split into separate videos, not one 5-minute scene.
2. **Author the scene.** One `Scene` class per video in one file under `animations/` (or the project's existing location). Rules that keep renders honest:
   - `self.play` only where the outline says motion; `self.wait` beats where the viewer reads.
   - Text via `Text`/`MathTex`, never screenshot images; keep text within frame bounds (`to_edge`/`scale` explicitly).
   - Add `self.next_section()` markers between beats so failed sections are debuggable.
   - A 60s video at 1080p can take minutes to render — author at `-ql` (480p) while iterating, final render at `-qh` (1080p) only once.
3. **Render.** `manim -ql animations/<file>.py <SceneName>` for iteration; `-qh` for delivery. Report the actual output path Manim prints.
4. **Verify.** Don't trust a 0 exit code:
   - Open the output path and confirm duration and size are sane (an 0-byte or 2-frame file is a failure).
   - Extract 3–4 frames at the beats from the outline (`ffmpeg -ss <t> -i out.mp4 -frames:v 1`) and check them against the outline beats — text within bounds, no overlapping elements, each beat visible.
   - If a beat's frame doesn't match, fix the scene at that `next_section`, not the whole file.
5. **Embed or deliver.** For HTML embedding: copy the .mp4 next to the consuming HTML, add `<video>` with `controls preload="metadata"` (or muted+autoplay+loop for background motion), and use relative paths so the artifact moves with its directory. For GIF delivery: convert via `ffmpeg` (palettegen/paletteuse two-pass for quality) and note GIFs are large — >10MB for >15s at 1080p is normal, prefer .mp4 in HTML. Presentations can embed the video directly into a `/frontend-slides` deck.

## Deliver

Report: outline beats, render quality, output path + duration + size, frames checked (with which beats), and the embed snippet when embedding. State what was verified visually vs. what was only a 0-exit-code.

## Guardrails

- Never deliver a video whose frames you didn't check against the outline.
- Never re-render 1080p per iteration — one quality bump at the end, stated.
- A render failure is reported verbatim (the failing Manim/ffmpeg error), never summarized as "rendered with issues".
- Keep `animations/` files as the source of truth; the .mp4 is a build artifact. A re-render from source must reproduce it.
