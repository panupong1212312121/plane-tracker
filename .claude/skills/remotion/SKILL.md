---
name: remotion
description: Create, animate, preview, and render programmatic video in React using Remotion. Build compositions, sequences, spring physics, audio sync, dynamic text, and data-driven video exports.
---

# Remotion: Programmatic Video in React

Use Remotion to build videos, animated graphics, and dynamic motion content using React components and web standards.

## Core Concepts

1. **Composition (`<Composition />`)**: The top-level video declaration.
   - Defines `id`, `component`, `durationInFrames`, `fps`, `width`, and `height`.
   - Always declare compositions in your root entrypoint (`src/Root.tsx`).

2. **Frame Navigation & Timing**:
   - `const frame = useCurrentFrame();` — get the current frame number (0-indexed).
   - `const { fps, durationInFrames, width, height } = useVideoConfig();` — retrieve canvas dimensions and frame rate.
   - Prefer computing animations from `frame` rather than CSS transitions or `setTimeout`.

3. **Sequencing & Layering**:
   - `<Sequence from={30} durationInFrames={60}>` — delays children by 30 frames and clips them to 60 frames.
   - `<Series>` — chains sequences one after another automatically.
   - Use standard React flexbox, grid, and absolute positioning for layouts.

4. **Interpolation & Spring Physics**:
   - `interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' })` — smooth value remapping.
   - `spring({ frame, fps, config: { damping: 12, mass: 0.5, stiffness: 100 } })` — natural physics-based motion.

5. **Audio & Media Integration**:
   - `<Audio src={staticFile("audio/track.mp3")} />` — perfectly synced audio playback.
   - `<Video src={staticFile("video/clip.mp4")} />` — embed video clips with volume and trim controls.
   - Static assets live in `public/` and are resolved with `staticFile()`.

## CLI Commands

```bash
# Preview studio
npx remotion preview

# Render video
npx remotion render src/index.ts <composition-id> out/video.mp4

# Render still image
npx remotion still src/index.ts <composition-id> out/thumbnail.png
```

## Best Practices

- **Zero Layout Shift**: Fix the root container to the video resolution (`1920x1080`, `1080x1920`, etc.).
- **Pure Functions**: Ensure components render deterministically at any given frame.
- **Preload Fonts & Assets**: Use `continueRender()` and `delayRender()` when waiting for web fonts or dynamic data.
- **Reference**: See [video layout reference](references/video-layout.md) and [composition guidelines](references/composition-best-practices.md).
