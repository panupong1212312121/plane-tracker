---
name: gsap
description: Official GreenSock Animation Platform (GSAP) patterns for web animations, timelines, ScrollTrigger, and React useGSAP() lifecycle safety. High-performance 60fps DOM, SVG, and canvas motion without layout thrashing.
---

# GSAP: GreenSock Animation Platform

GSAP is the standard high-performance JavaScript animation engine. Use this skill when building web animations, UI transitions, explorable blueprints, timelines, or scroll-driven interactions.

## Core Rules

1. **Hardware-Accelerated Properties**:
   - Animate `x`, `y`, `scale`, `rotation`, and `opacity`.
   - **Never** animate `top`, `left`, `width`, `height`, or `margin` directly (causes layout recalculation and jank).
   - Use `xPercent` and `yPercent` for responsive offsets.

2. **Core Tweens**:
   - `gsap.to(target, { x: 100, duration: 0.6, ease: "power2.out" })`
   - `gsap.from(target, { opacity: 0, y: 20, stagger: 0.1 })`
   - `gsap.fromTo(target, { scale: 0.8 }, { scale: 1, ease: "back.out(1.7)" })`

3. **Timelines (`gsap.timeline()`)**:
   - Group and sequence tweens with exact relative timing using the position parameter (`"<"`, `"+=0.2"`, `"-=0.1"`).
   - Set defaults on timelines: `const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });`

4. **ScrollTrigger**:
   - Pin sections and tie playback to scroll progress (`scrub: true`).
   - Clean up ScrollTrigger instances when unmounting components.
   - Reference: see [ScrollTrigger reference](references/scrolltrigger.md).

5. **React & Modern Framework Safety (`useGSAP()`)**:
   - Always use `@gsap/react`'s `useGSAP()` hook inside React components instead of raw `useEffect`.
   - Pass `{ scope: containerRef }` so selectors are scoped to the component and auto-cleaned on unmount.
   - Wrap callbacks with `contextSafe()` to prevent dangling execution after unmount.

```javascript
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);

export function AnimatedCard() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.from(".card-item", {
      opacity: 0,
      y: 30,
      stagger: 0.1,
      ease: "power2.out"
    });
  }, { scope: container });

  return (
    <div ref={container}>
      <div className="card-item">Item 1</div>
      <div className="card-item">Item 2</div>
    </div>
  );
}
```

## Detailed References

- [Timeline sequencing & nesting](references/timeline.md)
- [ScrollTrigger & pinning](references/scrolltrigger.md)
- [Plugins (Flip, Draggable, MotionPath)](references/plugins.md)
- [Performance & avoiding layout thrashing](references/performance.md)
