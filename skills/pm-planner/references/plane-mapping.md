# plane-plan.md template + Plane mapping

Template for the DRAFT artifact and the exact object mapping + creation sequence for MATERIALIZE.

## plane-plan.md template (DRAFT output, repo root)

```markdown
# Plane Plan — <Project Name>

> **เป้าหมาย:** <1-2 ประโยค ผลลัพธ์สุดท้ายที่เป็นรูปธรรม>
> **เดดไลน์:** <จากผู้ใช้ หรือ "relative estimates ยังไม่ตั้งวัน">
> **ทีม:** <ผู้ใช้เดี่ยว + agents (default)>
> **สถานะ:** draft — สร้างใน Plane ยังไม่เกิดขึ้น

## Phases

| # | เฟส | สิ่งที่ส่งมอบเมื่อจบเฟส | ช่วงเวลา | วัตถุใน Plane (หลัง materialize) |
| --- | --- | --- | --- | --- |
| 1 | Plan & Design | grill docs + design.md + spec | สัปดาห์ 1 | module `plan-and-design` |
| 2 | Build (tracer-bullet slices) | เดโมได้ทีละสไลซ์ | สัปดาห์ 2-4 | module `build` |
| 3 | Ship & Harden | URL จริง + posture proof | สัปดาห์ 5 | module `ship-and-harden` |

## Milestones

| ชื่อ | target_date (หรือ relative) | สังเกตเมื่อ |
| --- | --- | --- |
| First demoable slice | … | สไลซ์แรกวิ่งจริงตั้งแต่ต้นจนจบ |
| Feature complete | … | ทุกสไลซ์ผ่าน verify-and-stop |
| Live & hardened | … | ship-it ผ่าน + harden 401-proof ผ่าน |

## Work Items (tracer-bullet slices)

| # | ชื่องาน | Blocked by | Phase | Priority | สิ่งที่เดโมได้เมื่อจบ |
| --- | --- | --- | --- | --- | --- |
| 1 | … | — | build | medium | … |
| 2 | … | 1 | build | medium | … |

## Risks & Assumptions

- <ความเสี่ยง — สัญญาณเตือน — แผนสำรอง>

## Element Details (บังคับครบทั้ง 6 หมวด — ห้ามว่างเงียบ ๆ)

### Work items
<รายการงานทั้งหมด: ชื่อ + จำนวน + phase + priority + blocked-by — ยกจากหมวด Work Items ด้านบน>

### Cycles
<จะสร้างอะไร: เช่น "1 cycle สำหรับเฟส build ปัจจุบัน (สัปดาห์ 2-4)" หรือ "ไม่ใช้ — เพราะ …">

### Modules
<จะสร้างอะไร: ชื่อ module ต่อเฟส เช่น `plan-and-design`, `build`, `ship-and-harden` + จำนวน>

### Views
<จะสร้างอะไร: default 2 อัน `All Work` + `Build Board` หรือ "ไม่ใช้ — เพราะ …">

### Pages
<จะสร้างอะไร: 1 page สรุป plane-plan.md ของ project (body HTML) หรือ "ไม่ใช้ — เพราะ …">

### Intake
<สถานะ: เปิด feature พร้อมใช้ (triage queue — ของจะเข้าเมื่อมีคน raise ไม่ใช่สร้างเอง) หรือ "ไม่เปิด — เพราะ …">

## Plane

<หมวดนี้ว่างใน DRAFT — MATERIALIZE จะเติม: initiative/project identifier, รายการ objects ที่สร้างพร้อม id>
```

## Object mapping

| แนวคิดของผู้ใช้ | Plane object | เหตุผล/หมายเหตุ |
| --- | --- | --- |
| "workspace ใหม่" | **Initiative** (`plane__initiative create`) | Plane MCP scoped กับ workspace เดียว — Initiative คือกลุ่มระดับ workspace ที่ตรงเจตนา; บอกผู้ใช้ทุกครั้ง |
| ตัว product | **Project** (`plane__project create`) | ตั้ง `identifier` สั้น `[A-Z]+` เช่น `MYAPP` — ใช้ค้นหา/อ้างตลอดชีพ อย่าตั้งซ้ำกับที่มีอยู่ |
| เฟส | **Module** (`plane__module create`, status `planned`) | ชื่อ slug เช่น `plan-and-design`, `build`, `ship-and-harden` |
| เดดไลน์กลาง | **Milestone** (`plane__milestone create`, `target_date`) | เฉพาะเมื่อผู้ใช้ให้วันจริง |
| งานย่อย | **Work Item** (`plane__workitem create` พร้อม module, priority) | ชื่อ + description สั้น: สิ่งที่เดโมได้เมื่อจบ |
| งานที่ต้องรองานอื่น | **Relation** (`plane__workitem_relation create`, `relation_type: blocking`) | สร้าง work item ครบก่อน แล้วผูกทีเดียว; blocked_by เท่านั้น |
| ป้ายกำกับกลุ่มงาน | **Label** (`plane__label create`) | เช่น `infra`, `ui`, `security` — สร้างเฉพาะที่ใช้จริง |
| ช่วง build ปัจจุบัน | **Cycle** (`plane__cycle create`) | เฉพาะเมื่อผู้ใช้ใช้ cycles — สร้าง 1 cycle สำหรับเฟส build ปัจจุบัน (status จะเป็น current เองเมื่อวันเริ่มถึง) อย่าสร้างไล่ทุกเฟส; ห้าม complete/archive ใน skill นี้ |
| มุมมองงาน | **View** (`plane__view create`) | สร้าง 2 default: `All Work` (ทุกงานเปิด) และ `Build Board` (เปิด จัดกลุ่มตาม module) — ใช้เองได้ทันทีหลัง materialize |
| แผนฉบับอ่านง่าย | **Page** (`plane__page create`, มี `project_id`) | ยก plane-plan.md ย่อ (เป้าหมาย/เฟส/milestone/งาน) เป็น page ของ project — body เป็น HTML (`<p>/<h2>/<table>`) ไม่ใช่ markdown ดิบ |
| คิวของข้อเสนอใหม่ | **Intake** (เปิด feature เท่านั้น) | Intake คือ triage queue — ของจะเข้าเมื่อมีคน raise ไม่ใช่สร้างเอง; skill นี้แค่เปิด feature พร้อมใช้ |

> **บังคับก่อน MATERIALIZE:** plane-plan.md ต้องมีหมวด **Element Details** ครบทั้ง 6 องค์ประกอบ (Work items, Cycles, Modules, Views, Pages, Intake) — หมวดไหนแผนไม่ใช้ต้องเขียนเหตุผล "ไม่ใช้ — เพราะ …" ไว้ในหมวดนั้น ห้ามว่างเงียบ ๆ ไม่ครบ = ห้าม call plane mcp (gate ชั้นที่ 4 ใน SKILL.md)

## Creation sequence (MATERIALIZE)

```
0. plane__workspace get_features  → initiatives เปิด? ปิด = ข้าม + แจ้งผู้ใช้
1. plane__project list            → duplicate guard ชื่อ/identifier
2. plane__initiative create       → (ถ้าผู้ใช้ขอ) + plane__initiative add_projects หลังสร้าง project
3. plane__project create          → จำ project_id + identifier
3b. plane__project update_features → เปิด per-project features ที่แผนใช้:
                                     views, pages, intakes (default ทั้งสาม);
                                     cycles (เฉพาะผู้ใช้ใช้ cycles);
                                     epics/workitem_types (เฉพาะแผนใช้) — modules เปิดอยู่แล้ว
4. plane__module create (ต่อเฟส)  → จำ module_id
5. plane__milestone create        → (เฉพาะมีวันจริง)
5b. plane__cycle create           → (เฉพาะเปิด cycles) 1 cycle เฟส build ปัจจุบัน
5c. plane__view create (2 default) → `All Work` + `Build Board`
5d. plane__page create            → สรุป plane-plan.md เป็น page ของ project (body HTML)
6. plane__workitem create (ต่องาน, ระบุ project, module)
7. plane__workitem_relation create (ทีเดียวหลังสุด, relation_type: blocking)
8. plane__label create + workitem manage_label (เฉพาะที่ใช้)
9. รายงาน: identifier + รายการ MYAPP-1..N + page/cycle/view ids + อัปเดต plane-plan.md หมวด ## Plane
```

## Gotchas

- **UUID ต้องมาจากการสร้างจริง** — relation และ module links อ้าง id ที่ได้จาก create responses เท่านั้น ห้ามเดา
- **create ไม่ dedupe** ยกเว้นบาง endpoint — duplicate guard ต้องทำเอง (step 1)
- **target_date ไม่มี = ไม่ตั้ง** — relative estimates ค้างอยู่ใน draft จนผู้ใช้ให้วันจริง
- **ห้าม complete/archive** อะไรใน skill นี้ — สร้างอย่างเดียว; สถานะเดินหน้าเมื่องานจริงจบ (โดย agent ทำงานจริง)
- **workitem ids ใน report** ใช้รูป `IDENTIFIER-N` (เช่น `MYAPP-3`) อ่านง่ายกว่า UUID สำหรับมนุษย์
