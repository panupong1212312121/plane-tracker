---
name: hyperframes
description: Build seekable HTML/CSS timeline videos and animations for AI agents with HyperFrames. Supports keyframe animation, motion doctrine, scene transitions, and deterministic rendering.
---

# HyperFrames

HyperFrames is an open-source framework designed for AI coding agents to write HTML/CSS, animate with seekable timelines, and render high-quality video deterministically.

## Execution Model

1. **Deterministic HTML Video Engine**:
   - Every animation is driven by a time parameter `window.seek = async (t) => { ... }`.
   - Never use timers (`setTimeout`, `setInterval`) or non-deterministic state.
   - Declare layout in HTML/CSS with em units or explicit viewport scaling.

2. **Motion Doctrine**:
   - **No Frozen Frames**: Keep micro-settles or subtle drifts alive across shots.
   - **Directional Continuity**: Entering shots should inherit the motion vector of the exiting shot.
   - **Eased Spring Dynamics**: Use closed-form step responses or cubic curves (`cubic-bezier`).

3. **Keyframe Workflow**:
   - Plan scene duration and beat markers before writing layout.
   - Group visual elements into reusable blocks (overlays, titles, captions, product demos).
   - Render draft passes (30 fps, low res) to verify rhythm and pacing before final high-res output.

## CLI Usage

```bash
# Check usage and status
npx hyperframes usage --json

# Preview composition
npx hyperframes preview

# Render video
npx hyperframes render <input.html> --out <out/video.mp4>
```

## Agent Guidelines

- When prompted to generate video using HTML/CSS or web components, propose a clear storyboard with timestamps.
- Validate layout with viewport captures before invoking final rendering passes.
