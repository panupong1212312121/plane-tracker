---
name: enablement-kit
description: Produce the complete pack of materials that make our app easy to adopt — user manual, quick-start, slide presentation, demo video, web docs, summary report — as one linked enablement pack. Composes existing skills instead of duplicating them (frontend-slides, manim-video, archify, codebase-diagram, mock-data, frontend-design, ship-it), captures real app screenshots and embeds them, cross-links every deliverable ("ดูเพิ่มเติม: <url>" with verified links), and enforces caveman style — infographic-first (flowchart/chart/diagram leads every section), prose never longer than ~3 lines. Use when the user asks for คู่มือ, manual, docs for the app, demo video, presentation to teach the app, report สรุป, "ทำเอกสารสอนใช้", "สรุปวิธีใช้", or wants the app explained professionally for end users/clients.
---

# Enablement Kit

One pack, many deliverables, all linked. Core rule: **never write what another skill already does well — route to it and embed its output.** This skill is the director, not the one-person band.

## 1. Scope the pack (menu, not a guess)

Present the deliverable menu with a recommended default and let the user tick:

| Deliverable | Owner skill | Default |
| --- | --- | --- |
| คู่มือ (HTML manual) + quick-start 1 หน้า | this skill | ✅ default |
| Slide presentation | `frontend-slides` | optional |
| Demo video | `manim-video` (concept animation) or screen-recording script (app walkthrough) | optional |
| Report สรุปผล/ตัวเลข | this skill | optional |
| Publish เป็นเว็บ | `ship-it` | optional — local first |

Confirm the audience (ผู้ใช้ปลายทาง / client / ทีมใหม่) — it decides vocabulary and depth.

## 2. Gather evidence from the app

Read the app itself: README, `design.md`, `CONTEXT.md`, entry points, main flows. Derive the **top 5 tasks** users actually do — these become the manual's chapters and the demo video's beats. If the app has no data and empty states would look broken, generate demo data via `mock-data` first (stated as demo data, never implied real).

## 3. Caveman style — visuals lead, prose follows

Non-negotiable:
- **Every section LEADS with a visual** — flowchart, sequence/flow diagram, chart, screenshot, or annotated image. Prose follows, never longer than ~3 lines per section. ถ้าอธิบายยาวได้ แปลว่ายังไม่มีภาพที่ใช่
- Chapter-opening diagrams come from `archify` (architecture/workflow/sequence/dataflow) — invoke it per diagram type, embed its HTML/SVG/exports into the pack assets.
- Codebase explanation pages route to `codebase-diagram`.
- Charts use real numbers with the source labeled under the chart. No decorative charts.
- Captions carry the teaching: what the user does, where to click, what they should see.

## 4. Capture the real app

Screenshots are of the **running app**, not mockups. Bounded method, first that works:

```powershell
# 1) Edge headless (Windows, no install)
msedge --headless=new --disable-gpu --window-size=1920,1080 --screenshot="assets/01-home.png" "http://localhost:PORT/"
# 2) Playwright fallback
npx playwright screenshot --viewport-size=1920,1080 "http://localhost:PORT/" assets/01-home.png
```

Start the app locally first (dev or production build — state which). Verify each capture exists and is >10KB; retake failed shots once, then report what failed. Capture the key states: home, main flow mid-step, main flow result, error state, mobile viewport for the top 2 screens.

## 5. Write the deliverables

- Manual/report: one self-contained HTML per document (inline CSS, relative `assets/` paths), styled with `design.md` tokens via `frontend-design` rules — subject-grounded, anti-slop, no lorem-ipsum.
- Quick-start หน้าเดียว: install → run → first task, ≤ 10 steps, every step has a screenshot.
- Slides/video/diagrams: produced by their owner skills from the same outline and asset pool, so every deliverable tells the same story with the same visuals.

## 6. Link the pack (professional cross-referencing)

Every deliverable cross-links the others, both directions:

```html
<p class="more">ดูเพิ่มเติม: <a href="./manual.html#deploy">คู่มือฉบับเต็ม — หัวข้อ Deploy</a> · <a href="https://<deployed-url>">เว็บแอป</a></p>
```

**Every link is verified before delivery**: file targets must exist (relative paths, never absolute), URL targets must respond (`curl -I` / status check). A broken link is a broken deliverable — fix or remove it, never ship a dead "ดูเพิ่มเติม".

## 7. Publish (optional, local-first)

The pack opens by double-click from `docs/enablement/`. Publishing to a URL happens only when the user asks — route the folder through `ship-it`, then replace relative links with deployed URLs and re-verify all links.

## Deliver

Report: pack folder path, deliverables produced (with owner skills used per artifact), screenshots captured (count + app URL they came from), diagrams embedded (per archify run), link-check results (every link PASS/FAIL), and what remains optional (slides/video/publish).

## Guardrails

- Route, don't duplicate: if `frontend-slides`/`manim-video`/`archify`/`codebase-diagram`/`mock-data` can produce the artifact, they produce it — this skill composes and links.
- Caveman style is a contract: any section the user could call "ยาวพรืด" is a finding to fix, not a style preference.
- Screenshots of real screens only — never fabricate UI images the app can't produce; state demo-data usage explicitly.
- No absolute paths, no dead links, no unverified "ดูเพิ่มเติม".
- Never publish (ship-it) unasked — local pack is the default delivery.
