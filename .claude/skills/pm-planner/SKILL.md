---
name: pm-planner
description: Act as the project manager for a vibe-coding project — interview-lite, then draft a phased timeline (phases, milestones, work items with blocking dependencies, dates, risks) saved as plane-plan.md at the repo root. Only on an explicit go-ahead in act mode (e.g. "สร้าง project ใหม่ใน Plane พร้อมร่างแผนผ่าน plane mcp" / "create it in Plane") materialize the same plan into Plane via the Plane MCP — initiative/project, modules, milestones, work items with blocking edges. Use when the user asks to plan a project timeline, draft a roadmap, act as PM, or wants the plan pushed into Plane.
---

# PM Planner

Two-mode PM: **draft everything, create nothing** until the user explicitly says push it to Plane. The draft is plan-mode safe; materialize is act-mode only.

| Mode | When it fires | Output |
| --- | --- | --- |
| **DRAFT** (default) | คำขอวางแผน/ร่าง timeline/ร่าง roadmap รวมถึง plan mode ทุกครั้ง | `plane-plan.md` ที่ repo root — ไม่แตะ Plane เลย |
| **MATERIALIZE** | act mode + คำสั่งชัดเจนที่ตั้งชื่อว่า Plane ("สร้างใน Plane", "push to Plane", "สร้าง project ใหม่พร้อมร่างผ่าน plane mcp") | วัตถุจริงใน Plane ตาม mapping ด้านล่าง + รายงานพร้อม identifier |

## DRAFT mode

1. **Interview-lite** (ไม่เกิน 6 คำถาม, ทุกข้อมี default ที่เสนอนำ): เป้าหมาย product คืออะไร / เดดไลน์หรือระยะเวลา / ทีมกี่คน (มัก = ผู้ใช้เดี่ยว + agents) / stack ที่ตัดสินใจแล้ว / งานค้างอื่นที่แย่งเวลาไหม / ความเสี่ยงที่กังวลที่สุด
2. **Derive phases จาก spine ของ hub** (`docs/agents/flow.md`): grill → design → spec → tickets → implement (tdd + specialists) → ship → harden — ยุบ/ขยายให้ fit กับ scope: โปรเจกต์เล็กมักเหลือ 3 เฟส (Plan → Build → Ship), โปรเจกต์เต็มอาจแยก Security/Harden ออกจาก Ship
3. **แตกงานเป็น work items แบบ tracer-bullet** (แนวเดียวกับ `/to-tickets`): งานละสไลซ์ที่เดโมได้จริง, ขนาดพอดี context window เดียว, ทุกงานระบุ blocked-by
4. **เขียน `plane-plan.md`** ตาม template ใน [references/plane-mapping.md](./references/plane-mapping.md) แล้วให้ผู้ใช้รีวิว — จบโหมดนี้ที่ไฟล์เดียว
5. **Element details ครบก่อนจบ draft (บังคับ):** draft ต้องมีหมวดรายละเอียดขององค์ประกอบทั้ง 6 — **Work items, Cycles, Modules, Views, Pages, Intake** — แต่ละหมวดระบุสิ่งที่จะสร้างจริง (ชื่อ + จำนวน + เงื่อนไข/ค่า default) ไม่ใช่แค่กล่าวถึง; องค์ประกอบที่แผนไม่ใช้ต้องมีหมวดเขียนเหตุผลว่า "ไม่ใช้ — เพราะ …" อย่างชัดเจน ห้ามปล่อยว่างเงียบ ๆ

## MATERIALIZE mode

**Gate สี่ชั้นก่อน call แรก:** (1) act mode, (2) คำสั่งชัดเจนตั้งชื่อว่า Plane, (3) แสดงรายการสิ่งที่จะสร้าง (ชื่อ + จำนวน + วันที่) ให้ผู้ใช้ยืนยันก่อน, (4) **element-details check:** `plane-plan.md` ต้องมีรายละเอียดครบทั้ง 6 องค์ประกอบ (**Work items, Cycles, Modules, Views, Pages, Intake**) — ทุกหมวดต้องมีรายละเอียด ไม่ว่าง และไม่ว่างเงียบ ๆ (ไม่ใช้ = มีเหตุผลเขียนไว้ในหมวดนั้น) — ไม่ครบ = กลับไป DRAFT เติมให้ครบก่อน ห้าม call plane mcp ใด ๆ

0. **Pre-check:** ถ้าไม่มี `plane__*` tools ใน workspace → บอกผู้ใช้ว่าต้องเพิ่ม Plane MCP server ก่อน แล้วหยุด — ห้ามเดา config
1. **Duplicate guard:** `plane__project list` หาชื่อ/identifier ซ้ำ + `plane__workspace get_features` ดูว่า initiatives เปิดไหม (ปิด = ข้าม initiative และบอกผู้ใช้)
2. **สร้างตามลำดับ** (ตาม mapping ใน references/plane-mapping.md): Initiative (ถ้าผู้ใช้ขอ "workspace ใหม่" — อ่านหมายเหตุด้านล่าง) → Project (ตั้ง identifier สั้น เช่น `MYAPP`) → Modules (status `planned`) → Milestones (target_date) → Work items (priority, module) → **Relations ทีหลังสุด** (workitem_relation `relation_type: blocking` อ้าง UUID ของ work item ที่สร้างแล้วเท่านั้น) → Labels
3. **Report:** identifier + รายการ objects ที่สร้าง (เช่น `MYAPP-1`…`MYAPP-12`) + อัปเดต `plane-plan.md` ให้มีหมวด `## Plane` ชี้ไปยัง objects

**หมายเหตุ "workspace ใหม่":** Plane MCP ถูก scope กับ workspace เดียว (ตั้งค่ามาพร้อม server) — สร้าง workspace ที่สองไม่ได้ สิ่งที่ตรงความหมายของผู้ใช้คือ **Initiative** (กลุ่มระดับ workspace) บอกผู้ใช้อย่างตรงไปตรงมาเมื่อ mapping นี้เกิดขึ้น

## Guardrails

- DRAFT เป็นค่าเริ่มต้นเสมอ — MATERIALIZE ยังไม่รวมอยู่ในการเรียกวางแผนธรรมดา
- ห้ามลบ/แก้ Plane objects ที่มีอยู่ — skill นี้**สร้างอย่างเดียว**; การแก้ให้ผู้ใช้ทำใน UI หรือสั่งรายวัตถุ (id หรือ identifier) อย่างชัดเจน
- ทุก `target_date` ต้องมาจากผู้ใช้ หรือ derived จากเดดไลน์ที่ผู้ใช้ให้ — ห้ามกุ deadline เอง; ถ้าผู้ใช้ไม่ให้เดดไลน์ ใช้เป็น relative estimates ("สัปดาห์ 1-2") ใน draft และ**ไม่ตั้ง target_date ตอน materialize**
- Work item ที่ blocked ต้องสร้างครบทุกตัวก่อน แล้วค่อยผูก relation ทีเดียว — อย่าผูกไล่ตัวต่อตัว
- ผู้ใช้เดี่ยวเป็น default: ไม่ assign ให้ใครจนผู้ใช้บอก; ไม่ตั้ง priority ตัวเองเกินกว่าข้อมูลที่มี (default `medium`, urgent เฉพาะที่ผู้ใช้ชี้)

## References

- [references/plane-mapping.md](./references/plane-mapping.md) — plane-plan.md template, Plane object mapping, creation sequence, gotchas (identifier rules, features check, blocking edges)
