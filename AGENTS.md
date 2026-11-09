# AGENTS.md — Plane Tracker & Workspace Guidelines

> This document is the single source of truth for AI agents operating in this repository. All future agents interacting with Plane via Plane MCP, REST API, or Python automation scripts MUST strictly adhere to the conventions defined below.

---

## 1. Security & Secrets Policy

- **Environment Variables**:
  - `PLANE_API_KEY`: API authentication key. Never hardcode plaintext keys in scripts, commits, or chat logs.
  - `PLANE_WORKSPACE_SLUG`: Workspace identifier (default: `panupong`).
- **Secret Files**: Any `.env`, `.env.local`, `secrets.*`, or credential JSONs are ignored by git and must NEVER be read into context or committed.
- Scripts must load configuration via `os.getenv('PLANE_API_KEY')` with safe local fallbacks only when authorized.

---

## 2. Plane Workspace Architecture & Projects

Workspace: **`panupong`** (`https://api.plane.so`)

| Project Identifier (Code) | Project Name | Scope & Purpose |
| :---: | :--- | :--- |
| **`LAND`** | Knowledge Intelligence (กรมที่ดิน) | ระบบ AI Knowledge, กฎหมายที่ดิน, LightRAG Engine, Schema, Prompt, Q&A และงาน Rollout |
| **`POST`** | ไปรษณีย์ไทย (Thailand Post) | การปรับแต่งเฉพาะสำหรับระบบไปรษณีย์ไทย (UI Display & CSV Export) |
| **`PANUP`** | Panupong | งานจัดการภายใน (Internal), สิทธิ์การเข้าถึง (VPN/Access), และระบบโครงสร้างพื้นฐาน (Infra) |
| **`MA26`** | MOCA - Bootcamp 2026 | โครงการนวัตกรรม MOCA ตามกระบวนการ Stage-Gate และ Six Thinking Hats |

---

## 3. Work Item Naming Conventions & Rules

When creating or updating issues in Plane, agents **MUST** follow these naming rules:

### A. Hierarchy Architecture (Parent vs Sub-item)
- **Parent Work Item**: Represents an **Epic** or major functional domain.
- **Sub-item**: Represents an actionable **Task** or specific requirement ticket.

### B. Parent Item Naming Pattern
```text
[Category/Type] ชื่องานภาษาไทยอย่างเป็นทางการ (English System Domain)
```
- **Examples**:
  - `[Q&A] รวบรวมและตอบข้อซักถามการทำงานของระบบ (Knowledge Intelligence Questions)`
  - `[Bug Fixes] แก้ไขและติดตามข้อผิดพลาดของระบบ & Engine (System & Engine Bugs)`
  - `[Enhancement] ปรับปรุงการจัดการ Schema & Metadata Fields`
  - `[Operations] แผนงานเตรียมการส่งมอบ อบรม และ Rollout กรมที่ดิน`

### C. Sub-item Naming Pattern
```text
[Prefix #Number] Action Verb + Target Component/Feature + Condition/Error Message
```
- **Allowed Prefixes**:
  - `[Q&A #X]`: ประเด็นข้อสงสัย ข้อซักถามพฤติกรรม AI / เกณฑ์ระบบ
  - `[Bug #X]`: ข้อบกพร่อง, Error message, หรือ Service ล่ม
  - `[Feature #X]`: ขีดความสามารถใหม่ / ความต้องการเพิ่มเติม
  - `[UI #X]`: การปรับแต่ง Frontend, Layout, Scroll, ปุ่ม หรือ Freeze header
  - `[Ops]`: แผนปฏิบัติการ, การจัดอบรม, การทดสอบระบบ (ใช้ลำดับเลข `101+`)
  - `[MOD-NN]`: โมดูลสถาปัตยกรรมระบบ (เช่น โครงการ MOCA `[MOD-01]` ถึง `[MOD-05]`)

### D. Traceability Rule (`#Number`)
- Every technical item derived from a client/stakeholder requirement sheet **MUST** retain its original serial number (`#1`, `#2`, `#11`, `#25`).
- **Why**: Allows instant cross-referencing between meetings, client Excel sheets, and Plane cards without ambiguity.
- Internal/Operations tasks must use the `101+` range (e.g. `101`, `102`) to prevent collision with client requirement numbers.

### E. Action-Oriented Phrasing
- Work item titles must always begin with an explicit action verb:
  - ✅ `[Bug #12] Error RETRIEVAL_ENGINE_UNAVAILABLE (LightRAG ล่ม)`
  - ✅ `[Ops] ปรับแต่ง Prompt สกัดข้อมูล เน้นตอบคำถามให้ถูกต้องตรงประเด็น`
  - ❌ `[Bug] LightRAG` (Unacceptable: passive and vague)

### F. Bilingual Technical Precision
- Keep official technical and architectural terms in English to prevent mistranslation:
  - *LightRAG, Retrieval Engine, Schema/Metadata, Freeze Header, Floating Button, Drag & Drop, Array, Text vs Textarea, CSV/JSON*.

---

## 4. Module & Label Conventions

### A. Module Ordering Rules
Modules must be prefixed with a 2-digit zero-padded number to enforce lifecycle sorting:
```text
01. ข้อซักถามและเกณฑ์ระบบ (Q&A)
02. ข้อผิดพลาดและ Engine (Bug Fixes)
03. การจัดการ Schema & ฟิลด์ (Schema Management)
04. การนำเข้า/ส่งออกข้อมูล (Data Import & Export)
05. การแสดงผล UI & ประสบการณ์ใช้งาน (UI/UX)
06. แผนงานและปฏิบัติการ กรมที่ดิน (Operations & Rollout)
```

### B. 2-Dimensional Label System
Every work item must have at least **two labels** attached:
1. **Dimension 1 — Work Type**:
   - `คำถาม` (Blue)
   - `Bug` (Red)
   - `สิ่งที่อยากให้ปรับปรุง` (Green)
   - `งานปฏิบัติการ / แผนงาน` (Purple)
2. **Dimension 2 — Technical Subsystem**:
   - `สกัดข้อมูล/Prompt`
   - `LightRAG/Engine`
   - `Schema/Field`
   - `Export/Data`
   - `UI/UX`
   - `Training/Onboarding`
   - `Verify/QA`

---

## 5. Issue Description Structure

Every work item created or updated must contain structured HTML in `description_html`:

### For Q&A Items:
```html
<p><b>คำถาม:</b> [ข้อสงสัยหรือโจทย์จากผู้ใช้งาน]</p>
<p><b>วิธีแก้ไข / ชี้แจง (Solution) หรือ เป้าหมาย:</b> [คำอธิบายกลไกการทำงานหรือการปรับแต่งระบบ]</p>
```

### For Bug Items:
```html
<p><b>อาการ:</b> [พฤติกรรมผิดปกติ หรือ Error code ที่พบ พร้อมบริบท]</p>
<p><b>วิธีแก้ไข (Solution) หรือ เป้าหมาย:</b> [แนวทางแก้ไข หรือ การตรวจสอบ Bug]</p>
```

### For Feature & UI Items:
```html
<p><b>รายละเอียด:</b> [ความต้องการและ User Story]</p>
<p><b>เป้าหมาย / Solution:</b> [เกณฑ์การยอมรับ (Acceptance Criteria)]</p>
```

---

## 6. Skills Management in this Repository

- Canonical skills hub: `skills/`
- Target agent platforms: `.agents/skills`, `.claude/skills`, `.kilo/skills`
- To propagate and synchronize skills:
  ```powershell
  powershell -File scripts\sync-skills.ps1
  ```
- To audit skills health against `skills-lock.json`:
  ```powershell
  powershell -File scripts\audit-skills.ps1
  ```
