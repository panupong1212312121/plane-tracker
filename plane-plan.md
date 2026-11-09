# Plane Plan — โครงการพัฒนาระบบคลังความรู้และปัญญาประดิษฐ์ กรมที่ดิน (SDP Knowledge Center & Gen AI)

> **เป้าหมาย:** พัฒนาระบบคลังความรู้กฎหมายรังวัด (Knowledge Base) และโมเดลปัญญาประดิษฐ์ (Gen AI Chatbot) ครอบคลุมการนำเข้าและสกัดเอกสารกว่า 100,000 หน้า เชื่อมต่อกับ Webchat ของ บมจ. สามารถ เพื่อให้บริการประชาชนและเจ้าหน้าที่ช่างรังวัดกรมที่ดินอย่างแม่นยำ พร้อมส่งมอบงานครบถ้วนตาม TOR ทั้ง 5 งวด  
> **เดดไลน์:** ส่งมอบงวดที่ 2 (24 พ.ย. 2569) และส่งมอบงวดสุดท้าย (งวดที่ 5) วันที่ 25 มีนาคม 2570  
> **ทีม:** คุณโบส (Boat - Handoff Owner & Tech Lead), ทีมพัฒนา Softnix (พี่ท็อป, พี่เบิ้ม, อาร์ม, เบล, ดอม, บิ๊ง), บมจ. สามารถคอมเทค, และคณะทำงานกรมที่ดิน (DOL)  
> **สถานะ:** DRAFT (เตรียม Materialize เข้า Plane Workspace: `panupong` / Project: `กรมที่ดิน` / Identifier: `DOL`)

---

## 1. การสังเคราะห์ข้อมูล 3 แหล่ง (Three-Way Synthesis)

| แหล่งข้อมูล | สิ่งที่ตรวจพบและนำมาวิเคราะห์ | ผลการ Mapping เข้าสู่โครงสร้าง Plane |
| :--- | :--- | :--- |
| **1. `C:\Users\Boat\Downloads\เอกสารกรมที่ดินสำคัญ`** | - `Timeline`: แผนส่งเอกสาร 50,000 หน้า 3 งวด (2, 16, 27 พ.ย. 69)<br/>- `TOR`: ข้อกำหนด 4.1.1–4.1.3 (นำเข้า/OCR 50,000 หน้า/แก้คำผิด), 4.2–4.5 (Audit Log, Knowledge Graph, PWA, Re-training, โควต้า 6,000 queries)<br/>- `ส่งมอบงวดที่ 2`: เอกสาร Prototype และฟอร์มช่วยตรวจคณะ 1–3<br/>- `คู่มือติดตั้ง`: Gen AI & Beszel Monitoring Hub | กำหนดรายละเอียดความต้องการทางเทคนิคของ Work Items, เอกสารส่งมอบ, ข้อมูล Acceptance Criteria ใน Description และ Sub-tasks เชิงลึก |
| **2. `https://192.168.10.46/...` (กรมที่ดิน)** | - โครงสร้างเดิม: 75 Issues (69 งานหลัก + 6 งานย่อย), 8 Modules (A ถึง H), 2 Cycles, 19 Labels<br/>- สถานะคืบหน้า: Done 4 งาน, Delayed 2 งาน, In Progress 33 งาน, Backlog 36 งาน | ใช้เป็น **Baseline 100%** ในการสร้าง Project ใหม่ ทั้งชื่อ รหัสลำดับ `[Code]`, ลำดับ Hierarchy, สหสัมพันธ์ Parent-Child, วันที่เริ่ม-สิ้นสุด และผู้รับผิดชอบ |
| **3. `http://192.168.10.31/` (Softnix PMS - DOL)** | - แถบ Timeline โครงการ DOL: Workstreams A ถึง G<br/>- ความคืบหน้าสะสม: ขอบเขตเต็ม v5 รวม ~23.5%, แผนเวลา Plan % ~24.4%<br/>- การแบ่งฝ่ายรับผิดชอบ: Softnix, สามารถ, กรมที่ดิน, Joint | ยืนยันความสอดคล้องของ Workstreams A–G เข้ากับ Modules ใน Plane และใช้เปอร์เซ็นต์ความคืบหน้าระบุใน Description |

---

## 2. Phases (Modules)

| # | เฟส / Module | ขอบเขตและสิ่งที่ส่งมอบ | ช่วงเวลา | วัตถุใน Plane |
| :-: | :--- | :--- | :---: | :--- |
| **H** | **Module H: Handoff & Immediate Action Items** | เคลียร์ Blocker ด่วน: แก้ API Upload ล่ม, คอขวด LLM Worker, เตรียมข้อมูล Intelligent, แก้ไข Prototype Feedback 3-4 ข้อ | 26 ต.ค. – 20 พ.ย. 69 | Module `Module H: Handoff & Immediate Action Items` |
| **A** | **Module A: เอกสารเก่า 48,000 หน้า (Cleansing & 15 Categories)** | ทบทวนไฟล์ OCR/JSON เดิม, Classification 15 กลุ่มตามลำดับศักดิ์กฎหมาย, สกัดวันบังคับใช้/ยกเลิก | 7 ก.ย. – 27 พ.ย. 69 | Module `Module A: เอกสารเก่า 48,000 หน้า` |
| **B** | **Module B: เอกสารใหม่ 50,000 หน้า (ETL, OCR & PDPA/PII)** | Pipeline รับเอกสาร 3 งวด (2, 16, 27 พ.ย.), OCR ไทย/อังกฤษ/ตัวเลข, PDPA Screening, ปรับปรุงคำผิด | 21 ก.ย. – 18 ธ.ค. 69 | Module `Module B: เอกสารใหม่ 50,000 หน้า` |
| **C** | **Module C: System & Data Architecture / Integration** | Data Pipeline 11 ขั้นตอน, DB Schema, Vector DB, ระบบจัดเก็บ Net Intelligence | 21 ก.ย. – 8 ม.ค. 70 | Module `Module C: System & Data Architecture` |
| **D** | **Module D: GenAI Agent, RAG & Webchat API Integration (Samart)** | Agent ตอบคำถามอิงศักดิ์กฎหมาย, Citation Links เปิดไฟล์ต้นฉบับ, Swagger API ให้สามารถ, เชื่อมต่อ Webchat | 12 ต.ค. 69 – 25 มี.ค. 70 | Module `Module D: GenAI Agent & Webchat API` |
| **E** | **Module E: ติดตั้งระบบ On-premise ณ เครื่องลูกค้า (กรมที่ดิน)** | ติดตั้งซอฟต์แวร์ 6-7 ตัวบนเครื่องกรมที่ดิน (ปากเกร็ด), ขอเปิดเน็ต/VPN, ทดสอบ Performance บนเครื่องจริง | 19 ต.ค. – 27 พ.ย. 69 | Module `Module E: ติดตั้งระบบ On-premise` |
| **F** | **Module F: TOR Compliance & System Features (4.1 - 4.5)** | Audit Log, Knowledge Graph, Feedback Loop (RLHF), Re-training Pipeline, Dashboard สถิติ, โควต้า 6,000 queries | 22 ต.ค. 69 – 19 ก.พ. 70 | Module `Module F: TOR Compliance` |
| **G** | **Module G: งวดงานและการส่งมอบ (งวด 2, งวด 5, คู่มือ, อบรม, Pen Test)** | ตรวจรับงวด 1 (Done), ส่งมอบงวด 2 (Prototype), จัดอบรม Admin/User, Pen Test ครั้งที่ 2, ส่งมอบงวด 5 | 15 ก.ย. 69 – 25 มี.ค. 70 | Module `Module G: งวดงานและการส่งมอบ` |

---

## 3. Milestones

| ชื่องวดงาน / Milestone | วันที่เป้าหมาย (Target Date) | เกณฑ์การสังเกตและผลลัพธ์ที่พิสูจน์ได้ | ผู้รับผิดชอบหลัก |
| :--- | :---: | :--- | :--- |
| **งวดที่ 1 (ตรวจรับแล้ว)** | 15 ก.ย. 2569 | แผนการดำเนินงานและสถาปัตยกรรมระบบได้รับการตรวจรับจากคณะกรรมการ | Joint |
| **ส่งมอบเอกสาร 50,000 หน้า (งวดที่ 1)** | 2 พ.ย. 2569 | กรมที่ดินส่งมอบไฟล์ PDF ชุดแรก เพื่อเข้ากระบวนการ ETL & OCR | กรมที่ดิน |
| **ส่งมอบคู่มือ Softnix & ติดตั้ง On-premise** | 6 พ.ย. 2569 | ส่งมอบคู่มือการติดตั้ง 4 เล่ม + พี่เบิ้มติดตั้งซอฟต์แวร์บนเซิร์ฟเวอร์ปากเกร็ด | Softnix |
| **ส่งมอบเอกสาร 50,000 หน้า (งวดที่ 2)** | 16 พ.ย. 2569 | กรมที่ดินส่งมอบไฟล์ PDF ชุดที่สอง | กรมที่ดิน |
| **จัดฝึกอบรมระบบ GenAI (Admin & User)** | 11 & 16 พ.ย. 2569 | จัดอบรมช่างรังวัด (11 พ.ย.) และผู้ดูแลระบบ (16 พ.ย.) พร้อมเอกสารหลักสูตร | สามารถ / Softnix |
| **ส่งมอบงานงวดที่ 2 (ส่งมอบ Prototype)** | 24 พ.ย. 2569 | เอกสาร Prototype ฉบับแก้ไข + ผลการทดสอบผ่านเกณฑ์คณะกรรมการ | Softnix / สามารถ |
| **ส่งมอบเอกสาร 50,000 หน้า (งวดที่ 3 - ครบถ้วน)** | 27 พ.ย. 2569 | กรมที่ดินส่งมอบเอกสารครบ 50,000 หน้า รวมเรื่องร้องเรียน/หารือ | กรมที่ดิน |
| **ส่งมอบ API Production + Token ให้สามารถ** | 12 ก.พ. 2570 | API Gateway, Swagger, Production Token ส่งมอบให้ทีม Webchat สามารถเชื่อมต่อ | Softnix |
| **UAT ผู้ใช้จริงผ่าน Webchat** | 19 มี.ค. 2570 | เจ้าหน้าที่กรมที่ดินทดสอบถามตอบกฎหมายผ่าน Webchat ครบถ้วนตาม Test Scenario | Joint |
| **ส่งมอบงวดที่ 5 (วันสิ้นสุดสัญญา 300 วัน)** | 25 มี.ค. 2570 | ส่งมอบระบบสมบูรณ์, รายงาน Pen Test 2 ครั้ง, Source Listing, สถาปัตยกรรมระบบ | สามารถ / Softnix |

---

## 4. Work Items (75 รายการครบถ้วนตาม Baseline)

### หมวด Module H: Handoff & Immediate Action Items (11 งาน)
| รหัส | ชื่องาน | Blocked by | Priority | ผู้รับผิดชอบ | วันที่เป้าหมาย | สถานะ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **H1** | [H1] หาสาเหตุและแก้ไขปัญหาระบบล่มของ API อัปโหลดข้อมูลและ Rate Limit | — | Urgent | Softnix | 2026-11-04 | In Progress |
| **H2** | [H2] แก้ไขปัญหาคอขวด LLM / Worker และให้คำปรึกษาเชิงสถาปัตยกรรม | — | Urgent | พี่ท็อป | 2026-11-06 | In Progress |
| **H3** | [H3] นำเข้าข้อมูลส่วนที่เหลือ (จาก ~80%) และส่งต่อให้คุณโบสทำส่วน Intelligent | — | High | อาร์ม / โบส | 2026-11-06 | In Progress |
| **H4** | [H4] ตรวจสอบกลุ่ม 15 ให้เสร็จ นำเข้ากลุ่ม 7, 9, 11 และอัปเดตโครงสร้าง 15 กลุ่ม | — | High | เบล | 2026-11-20 | In Progress |
| **H5** | [H5] จัดทำสไลด์และตารางเปรียบเทียบโครงสร้างเดิม vs 15 กลุ่มใหม่ สรุปยอดหน้ารวม | — | Medium | Softnix | 2026-11-06 | In Progress |
| **H6** | [H6] แก้ไขเอกสาร Prototype ตาม Feedback ผู้ใช้ 3-4 ข้อ | — | High | Softnix | 2026-11-06 | In Progress |
| **H7** | [H7] ประชุมหารือสามารถเรื่อง User Management และสิทธิ์ราชการหลายระดับ | — | High | Softnix/สามารถ | 2026-11-13 | In Progress |
| **H8** | [H8] ดอมเตรียมเนื้อหาอธิบาย MLOps / ML Flow และการทดสอบความแม่นยำให้ลูกค้า | — | Medium | ดอม | 2026-11-06 | In Progress |
| **H9** | [H9] พี่เบิ้มติดตั้งซอฟต์แวร์ทั้งหมด (6-7 ตัว) บนเซิร์ฟเวอร์กรมที่ดิน | — | High | พี่เบิ้ม | 2026-11-06 | In Progress |
| **H10** | [H10] จัดทำเอกสารคู่มือ Training ทั้งส่วน AI และ Net Intelligence ส่งมอบ 6 พ.ย. | — | Medium | ทีมเอกสาร | 2026-11-06 | In Progress |
| **H11** | [H11] พี่บิ๊งและคุณโบสทดสอบความถูกต้องข้อมูลต้นทาง-ปลายทาง และเตรียมทดสอบ 1-2 พ.ย. | H3 | Urgent | พี่บิ๊ง / โบส | 2026-11-02 | In Progress |

### หมวด Module A: เอกสารเก่า 48,000 หน้า (7 งาน)
| รหัส | ชื่องาน | Blocked by | Priority | ผู้รับผิดชอบ | วันที่เป้าหมาย | สถานะ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **A1** | [A1] ทบทวนไฟล์ OCR + Metadata JSON เดิม / recheck จำนวนไฟล์ | — | Urgent | Softnix | 2026-10-30 | Done |
| **A2** | [A2] กำหนดเกณฑ์จัดกลุ่มเอกสาร (16→14→15 กลุ่ม) ร่วมกับกรมที่ดิน | — | High | Joint | 2026-10-30 | Done |
| **A3** | [A3] รวบรวมไฟล์นอกชุด 48,000 ที่ตกหล่น | — | High | Softnix | 2026-10-30 | Done |
| **A4** | [A4] พัฒนา Classification (Rule/ML) ตามเกณฑ์ 14/15 ประเภท | A2 | High | Softnix | 2026-10-30 | In Progress (Delayed) |
| **A5** | [A5] รัน Classification + นำเข้าระบบ (48,000) | A4, H2 | Urgent | Softnix | 2026-11-13 | In Progress |
| **A6** | [A6] QA / สุ่มตรวจผลการจัดกลุ่ม | A5 | High | Softnix | 2026-11-20 | In Progress |
| **A7** | [A7] สกัดวันมีผลบังคับใช้/วันยกเลิก (AI) + ให้ประธานอนุมัติ | A6 | Medium | Softnix | 2026-11-27 | Todo |

### หมวด Module B: เอกสารใหม่ 50,000 หน้า (9 งาน)
| รหัส | ชื่องาน | Blocked by | Priority | ผู้รับผิดชอบ | วันที่เป้าหมาย | สถานะ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **B1** | [B1] นำเข้าไฟล์ PDF ชุดใหม่ (3 งวดภายใน พ.ย.) | — | Medium | Softnix | 2026-11-23 | In Progress (Delayed) |
| **B2** | [B2] พัฒนา ETL Pipeline (microservice/Docker/API) | — | High | Softnix | 2026-10-16 | In Progress |
| **B3** | [B3] ตั้งค่า OCR Engine (ไทย/อังกฤษ/เลขไทย-อารบิก, สี/ขาวดำ) | — | High | Softnix | 2026-10-30 | In Progress |
| **B4** | [B4] รัน OCR เอกสารใหม่ทั้งหมด (50,000 หน้า) | B1, B3 | High | Softnix | 2026-11-06 | In Progress |
| **B5** | [B5] ปรับปรุงคุณภาพข้อมูล (แก้คำผิด) ตาม 4.1.3 | B4 | High | Softnix | 2026-11-13 | In Progress |
| **B6** | [B6] จัดกลุ่มเอกสารตาม mapping ลูกค้า (15 กลุ่ม) | B5 | High | Softnix | 2026-11-20 | In Progress |
| **B7** | [B7] Export ข้อมูล JSON/CSV (ชุดข้อมูล) | B6 | High | Softnix | 2026-11-20 | In Progress |
| **B8** | [B8] เตรียมรับมอบเอกสาร 50,000 หน้า 3 งวด (2, 16, 27 พ.ย.) | — | Urgent | Softnix | 2026-11-27 | In Progress |
| **B9** | [B9] PDPA/PII Screening (ซ่อน/แทนที่ข้อมูลส่วนบุคคล - หมวดคำพิพากษา) | B5 | High | Softnix | 2026-12-18 | In Progress |

### หมวด Module C: System & Data Architecture / Integration (6 งาน)
| รหัส | ชื่องาน | Blocked by | Priority | ผู้รับผิดชอบ | วันที่เป้าหมาย | สถานะ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **C1** | [C1] พัฒนาฟังก์ชัน Export JSON/CSV (ระดับระบบ) | — | High | Softnix | 2026-10-09 | In Progress |
| **C2** | [C2] นำเข้าเอกสารประเภทเดียวกันหลายหน้าพร้อมกัน (Batch/Queue/Worker) | — | High | Softnix | 2026-10-16 | In Progress |
| **C3** | [C3] Pipeline เชื่อมกับระบบจัดเก็บ (DB/MinIO/Vector DB) | C2 | High | Softnix | 2026-11-06 | In Progress |
| **C4** | [C4] วางโครงสร้าง Vector DB และ Embedding | C3 | High | Softnix | 2026-11-13 | In Progress |
| **C5** | [C5] ข้อมูลเข้าสู่ระบบจัดเก็บ (Net Intelligence) | C4 | High | Softnix | 2026-12-04 | In Progress |
| **C6** | [C6] บูรณาการทุกส่วน (System Integration) | C5 | Medium | Softnix | 2027-01-08 | Backlog |

### หมวด Module D: GenAI Agent, RAG & Webchat API Integration (15 งาน รวม Sub-tasks)
| รหัส | ชื่องาน | Parent | Blocked by | Priority | ผู้รับผิดชอบ | วันที่เป้าหมาย | สถานะ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **D1** | [D1] พัฒนา Agent ตอบคำถามจากคลังความรู้ (Prompt/Chain/RAG) | — | C4 | High | Softnix | 2026-11-20 | In Progress |
| **D2** | [D2] สถาปัตยกรรม Agent ให้เหตุผลตามลำดับศักดิ์กฎหมาย (15 กลุ่ม) | — | D1 | High | Softnix | 2026-12-04 | In Progress |
| **D3** | [D3] พัฒนาระบบแสดงแหล่งอ้างอิง (Citation + ลิงก์เปิดไฟล์เอกสาร) | — | D1 | High | Softnix | 2026-12-11 | In Progress |
| **D3.1** | [D3.1] แก้ไขปัญหาลิงก์เปิดไฟล์ต้นฉบับ (Link Resolution & Path Mapping) | D3 | — | Urgent | Softnix | 2026-11-27 | In Progress |
| **D4** | [D4] จัดทำ API Spec (Swagger) + Sandbox ให้สามารถ | — | — | Urgent | Softnix | 2026-10-30 | In Progress |
| **D5.1** | [D5.1] สามารถ: ระบุผู้ประสานงานเทคนิค + ข้อกำหนด Auth/Security ของ Webchat | — | D4 | High | สามารถ | 2026-11-13 | In Progress |
| **D5.2** | [D5.2] ข้อกำหนด User Management / Auth / Security ของ Webchat + GenAI (ร่วมกัน) | — | D5.1 | High | Joint | 2026-11-30 | In Progress |
| **D5.3** | [D5.3] สามารถ: เชื่อม Webchat เข้ากับ Agent API | — | D5.2 | High | สามารถ | 2027-02-19 | Backlog |
| **D5.4** | [D5.4] สามารถ: แสดงผลแหล่งอ้างอิงใน Webchat (citation + เปิดไฟล์ต้นฉบับ) | — | D5.3 | High | สามารถ | 2027-02-26 | Backlog |
| **D5.5** | [D5.5] Softnix: ส่งมอบ API Production + Swagger + Token ให้สามารถ | — | D5.4 | High | Softnix | 2027-02-12 | Backlog |
| **D6** | [D6] Integration Testing บน Webchat จริง | — | D5.5 | High | Joint | 2027-03-05 | Backlog |
| **D7** | [D7] UAT ผู้ใช้จริงผ่าน Webchat | — | D6 | High | Joint | 2027-03-19 | Backlog |
| **D7.1** | [D7.1] ตรวจสอบคุณสมบัติ PWA และช่องคำถาม >= 512 ตัวอักษร | D7 | — | Medium | สามารถ / โบส | 2027-03-15 | Backlog |
| **D8** | [D8] Go-live Agent บน Webchat + ส่งมอบ (25 มี.ค. 70) | — | D7 | High | สามารถ | 2027-03-25 | Backlog |
| **D9** | [D9] Softnix: จัดทำคู่มือส่วนของ Softnix (GenAI + Knowledge Center + Net Intelligence + MLFlow) | — | — | Urgent | Softnix | 2026-11-05 | In Progress |

### หมวด Module E: ติดตั้งระบบ On-premise ณ เครื่องลูกค้า (5 งาน รวม Sub-tasks)
| รหัส | ชื่องาน | Parent | Blocked by | Priority | ผู้รับผิดชอบ | วันที่เป้าหมาย | สถานะ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **E1** | [E1] ประสานงานการเชื่อมต่อระบบภายใน / VPN (สามารถประสานงาน + ขอเปิด Internet/Remote Access) | — | — | High | สามารถ/Joint | 2026-11-13 | In Progress |
| **E1.1** | [E1.1] ติดตั้งและกำหนดค่า Beszel (GPU & System Monitoring Hub/Agent) | E1 | — | High | พี่เบิ้ม | 2026-11-10 | Todo |
| **E2** | [E2] Softnix: เข้าไปติดตั้ง Software ที่เกี่ยวข้องทั้งหมด บนเครื่อง On-premise (ปากเกร็ด) | — | E1 | Urgent | Softnix | 2026-11-06 | In Progress |
| **E3** | [E3] นำเข้าโมเดลและระบบลงเครื่องลูกค้า (เมื่อเปิดเครื่องได้) | — | E2 | High | Softnix | 2026-11-13 | Todo |
| **E4** | [E4] วัด Performance บนเครื่องลูกค้าเทียบกับเครื่องพัฒนา | — | E3 | Medium | Softnix | 2026-11-27 | Backlog |

### หมวด Module F: TOR Compliance & System Features (10 งาน รวม Sub-tasks)
| รหัส | ชื่องาน | Parent | Blocked by | Priority | ผู้รับผิดชอบ | วันที่เป้าหมาย | สถานะ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **F1** | [F1] คุณลักษณะ OCR ภาษาไทย อังกฤษ เลขไทย-อารบิก (ตาม TOR 4.1.2) | — | — | High | Softnix | 2026-11-13 | In Progress |
| **F2** | [F2] 4.2.3.4 ระบบประเมินและติดตามความพึงพอใจการใช้งาน | — | — | Medium | Softnix | 2026-12-18 | Backlog |
| **F3** | [F3] 4.2.3.5 พัฒนาปรับปรุงโมเดลอย่างต่อเนื่อง (Re-training) | — | — | Medium | Softnix | 2027-01-15 | Backlog |
| **F4** | [F4] 4.3 ระบบจัดการสิทธิ์และความปลอดภัย (Role, Audit Log) | — | — | High | Softnix | 2027-01-15 | Backlog |
| **F5** | [F5] 4.4 ระบบจัดเก็บข้อมูลความรู้ (Vector DB + Knowledge Graph) | — | — | High | Softnix | 2026-12-25 | In Progress |
| **F6** | [F6] 4.5.1 รายงานสถิติการใช้งานและการค้นหา | — | — | Medium | Softnix | 2027-01-29 | Backlog |
| **F6.1** | [F6.1] พัฒนาระบบติดตามโควต้าการใช้งานตาม SOC 26.13 (Queries, Pages, Tokens) | F6 | — | High | โบส | 2027-01-25 | Backlog |
| **F7** | [F7] 4.5.2 Dashboard วิเคราะห์ผลลัพธ์และความถูกต้อง | — | F6 | Medium | Softnix | 2027-02-05 | Backlog |
| **F8** | [F8] 4.5.3 ระบบแจ้งเตือนข้อผิดพลาดและการทำงาน | — | F7 | Medium | Softnix | 2027-02-12 | Backlog |
| **F9** | [F9] การเชื่อมต่อระบบภายนอก (ยืนยันขอบเขตเชื่อมต่อจริง) | — | — | Low | Joint | 2027-02-19 | Backlog |

### หมวด Module G: งวดงานและการส่งมอบ (11 งาน รวม Sub-tasks)
| รหัส | ชื่องาน | Parent | Blocked by | Priority | ผู้รับผิดชอบ | วันที่เป้าหมาย | สถานะ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **G1** | [G1] ส่งมอบและตรวจรับงวดที่ 1 (วันที่ 60) | — | — | High | Joint | 2026-09-15 | Done |
| **G2** | [G2] จัดฝึกอบรมการใช้งานระบบ GenAI กรมที่ดิน (User & Admin) | — | E3 | Urgent | Softnix/ร่วมกัน | 2026-11-16 | In Progress |
| **G2.1** | [G2.1] หลักสูตรอบรมผู้ดูแลระบบ (Admin Training - 0.5 วัน: สถาปัตยกรรม, Model Tuning, Beszel) | G2 | — | Urgent | สามารถ / Softnix | 2026-11-16 | Todo |
| **G2.2** | [G2.2] หลักสูตรอบรมผู้ใช้งานทั่วไป (User Training - 0.5 วัน: การถามตอบ, กฎหมายรังวัด, ตรวจสอบ Citation) | G2 | — | Urgent | สามารถ / Softnix | 2026-11-11 | Todo |
| **G3** | [G3] Penetration Testing ครั้งที่ 2 + รายงานผล | — | D6 | High | สามารถ | 2027-03-12 | Backlog |
| **G3.1** | [G3.1] แก้ไขช่องโหว่ตามผล Pen Test (ส่วน Softnix) | G3 | G3 | High | Softnix | 2027-03-19 | Backlog |
| **G4** | [G4] คู่มือปฏิบัติงานสำหรับผู้ใช้ระบบ (รวมเล่มกับสามารถ) | — | D9 | High | Joint | 2027-03-12 | Backlog |
| **G5** | [G5] Source Listing + Library ของทุกโปรแกรมที่พัฒนา | — | C6 | Medium | Joint | 2027-02-26 | Backlog |
| **G6** | [G6] Architecture Diagram ของระบบที่พัฒนา | — | C6 | Medium | Joint | 2027-01-29 | Backlog |
| **G7** | [G7] คู่มือกำหนดค่า Configuration อุปกรณ์ + System Diagram | — | E4 | Medium | Joint | 2027-02-26 | Backlog |
| **G8** | [G8] ส่งมอบงวดที่ 5 (วันที่ 300) ให้ลูกค้า | — | G3.1, G4 | High | สามารถ | 2027-03-25 | Backlog |

---

## 5. Risks & Assumptions

1. **R-001 (ความเสี่ยงการรับเอกสาร 50,000 หน้า):** กรมที่ดินอาจส่งเอกสารล่าช้ากว่ารอบ พ.ย. 2569  
   - *สัญญาณเตือน:* วันที่ 2 พ.ย. และ 16 พ.ย. ไม่ได้รับไฟล์ตามนัด  
   - *แผนสำรอง:* เตรียมหนังสือชี้แจงผลกระทบต่อ UAT ส่งมอบล่วงหน้า และนำเข้าไฟล์ markdown/text ที่มีอยู่ไปพลางก่อน
2. **R-002 (ความเสี่ยงการเชื่อมต่อ API กับ สามารถ):** Softnix ยังไม่ได้รับข้อกำหนด Auth/Session จากสามารถ  
   - *สัญญาณเตือน:* ไม่มีการกำหนด Technical Contact ภายใน 13 พ.ย.  
   - *แผนสำรอง:* ส่ง Swagger Spec กลาง และเปิด Mock/Sandbox Environment ให้ทดสอบล่วงหน้า
3. **R-003 (ความเสี่ยงสภาพแวดล้อม On-premise ปิดกั้น):** เซิร์ฟเวอร์กรมที่ดินไม่เปิดอินเทอร์เน็ต/ไม่มี VPN  
   - *สัญญาณเตือน:* ไม่สามารถดาวน์โหลด Docker Image/Model Weights ได้  
   - *แผนสำรอง:* เตรียมไฟล์ติดตั้งแบบ Offline Tarball & USB Drive นำเข้าไปลงเครื่องโดยตรง
4. **R-004 (ความเสี่ยงคอขวด OCR 50,000 หน้า):** OCR ทำงานช้าบนเครื่องพัฒนา (~2 หน้า/นาที)  
   - *สัญญาณเตือน:* ประมวลผลไม่ทันกำหนดส่งมอบงวด 2  
   - *แผนสำรอง:* กระจายคิว Worker และย้ายงาน OCR หนักขึ้น GPU เซิร์ฟเวอร์ของลูกค้าที่มีกำลังคำนวณสูงกว่า

---

## 6. Element Details (ครบถ้วนทั้ง 6 องค์ประกอบตามข้อกำหนด PM-Planner)

### 6.1 Work items (จำนวน 75 รายการ)
- **รายการงานทั้งหมด:** 75 รายการ (69 งานหลัก + 6 งานย่อย/Sub-tasks) ตามตารางหมวดที่ 4
- **การจัดกลุ่ม:** สัมพันธ์กับ 8 Modules และ 2 Cycles อย่างสมบูรณ์
- **Parent-Child Relations:** 6 คู่ความสัมพันธ์หลัก (`E1` -> `E1.1`, `D3` -> `D3.1`, `D7` -> `D7.1`, `F6` -> `F6.1`, `G2` -> `G2.1`, `G2` -> `G2.2`)
- **Blocking Dependencies:** ผูกความสัมพันธ์ `blocking` ข้ามงานตามลำดับกระบวนการจริง (เช่น `A2` blocks `A4`, `B4` blocks `B5`, `D1` blocks `D2`/`D3`)

### 6.2 Cycles (จำนวน 2 รอบ)
1. **Cycle พ.ย. 2569: ติดตามงานส่งมอบเอกสาร 5 หมื่นหน้า & ทดสอบระบบ (โบส รับช่วงต่อ)**  
   - *ช่วงเวลา:* `2026-11-01` ถึง `2026-11-30`  
   - *จำนวนงาน:* 46 งาน (เน้น Module H, A, B, C และการเตรียมสอบทาน)  
   - *เป้าหมาย:* รับมอบเอกสาร 3 งวด, แก้ API ล่ม, อบรม 11/16 พ.ย., ส่งมอบงวด 2
2. **Cycle ธ.ค. 2569 - มี.ค. 2570: พัฒนาและเชื่อมต่อ API Production สู่การส่งมอบงวด 5**  
   - *ช่วงเวลา:* `2026-12-01` ถึง `2027-03-25`  
   - *จำนวนงาน:* 29 งาน (เน้น Module D, E, F, G)  
   - *เป้าหมาย:* เชื่อมต่อ Webchat จริง, Pen Test, UAT ผู้ใช้จริง, ส่งมอบงวดสุดท้าย

### 6.3 Modules (จำนวน 8 หมวด)
1. `Module H: Handoff & Immediate Action Items (งานติดตามเร่งด่วน พ.ย. 2569)` (11 งาน)
2. `Module A: เอกสารเก่า 48,000 หน้า (Data Cleansing & 15 Categories)` (7 งาน)
3. `Module B: เอกสารใหม่ 50,000 หน้า (Pipeline ETL, OCR & PDPA/PII)` (9 งาน)
4. `Module C: System & Data Architecture / Integration` (6 งาน)
5. `Module D: GenAI Agent, RAG & Webchat API Integration (Samart)` (15 งาน)
6. `Module E: ติดตั้งระบบ On-premise ณ เครื่องลูกค้า (กรมที่ดิน)` (5 งาน)
7. `Module F: TOR Compliance & System Features (4.1 - 4.5)` (10 งาน)
8. `Module G: งวดงานและการส่งมอบ (งวดที่ 2, งวดที่ 5, คู่มือ, อบรม, Pen Test)` (11 งาน)

### 6.4 Views (จำนวน 4 มุมมอง)
1. **`All Work (มุมมองงานทั้งหมด)`**: ตารางสรุปงานทั้งหมด 75 รายการ แสดงสถานะ, ลำดับความสำคัญ, ผู้รับผิดชอบ และวันที่เป้าหมาย
2. **`By Module Board (มุมมองแยกตามหมวดงาน)`**: Kanban Board จัดกลุ่มงานตาม 8 Modules เพื่อให้ Tech Lead ตรวจสอบสถานะของแต่ละสายงาน
3. **`Delayed & Urgent Focus (งานเร่งด่วนและตกค้าง)`**: Filter เฉพาะงานที่มี Priority `Urgent` หรือติดแท็ก `🚨 Delayed (ตกค้าง)` และ `Urgent / Blocker`
4. **`Cycle พ.ย. 69 Board (โฟกัสสปริ้นท์ปัจจุบัน)`**: กรองเฉพาะงานใน Cycle พฤศจิกายน 2569 เพื่อให้คุณโบสและทีมโฟกัสงานประจำวัน

### 6.5 Pages (จำนวน 1 หน้า)
- **ชื่อหน้า:** `สถาปัตยกรรมและแผนการส่งมอบโครงการกรมที่ดิน (SDP GenAI Master Plan)`
- **เนื้อหา (HTML):** สรุปเป้าหมายโครงการ, ตารางส่งมอบงานงวด 1 ถึง 5, โครงสร้างสถาปัตยกรรมโมเดลและ RAG, ข้อกำหนดความปลอดภัยตาม TOR, รายชื่อผู้ประสานงานหลัก

### 6.6 Intake (สถานะ: เปิดใช้งาน Feature)
- **การตั้งค่า:** เปิดใช้งานฟีเจอร์ Intake ของโปรเจกต์
- **วัตถุประสงค์:** ทำหน้าที่เป็น Triage Queue สำหรับรับประเด็นข้อสงสัย ข้อผิดพลาด (Bugs) หรือข้อเสนอแนะเพิ่มเติมจากกรมที่ดินหรือ บมจ. สามารถ โดยไม่ให้กระทบกับตารางงานหลักที่วางแผนไว้จนกว่าจะผ่านการ Triage

---

## 7. Labels ที่ใช้งาน (19 ป้ายกำกับ)

| ชื่อ Label | รหัสสี | จุดประสงค์ |
| :--- | :---: | :--- |
| `Softnix` | `#0052CC` | งานที่ทีม Softnix รับผิดชอบหลัก |
| `สามารถ (Samart)` | `#FF8B00` | งานที่ บมจ. สามารถ รับผิดชอบ |
| `กรมที่ดิน (DOL)` | `#00875A` | งานฝั่งกรมที่ดิน / ลูกค้า |
| `Joint / ร่วมกัน` | `#6554C0` | งานประสานงานร่วมกัน |
| `Urgent / Blocker` | `#DE350B` | งานเร่งด่วน คอขวดวิกฤต |
| `Handoff / โบส` | `#57D9A3` | งานส่งมอบให้คุณโบสรับช่วงต่อ |
| `Data / ETL / OCR` | `#00B8D9` | งานจัดการข้อมูลและแปลงเอกสาร |
| `AI / RAG / Intelligent` | `#8777D9` | งาน AI Prompt, RAG และ Net Intelligence |
| `API / Integration` | `#4C9AFF` | งานพัฒนา API เชื่อมต่อระบบ |
| `Infra / On-prem` | `#FFAB00` | งานเซิร์ฟเวอร์, OS, VPN และเครื่องลูกค้า |
| `TOR Compliance` | `#FF5630` | ข้อกำหนดตาม TOR 4.1 - 4.5 |
| `Documentation / Training` | `#36B37E` | คู่มือและหลักสูตรฝึกอบรม |
| `งวด 1 (ตรวจรับแล้ว)` | `#10B981` | งานในงวดที่ 1 ที่ผ่านการตรวจรับแล้ว |
| `งวด 2 (24 พ.ย. 69)` | `#F59E0B` | งานที่ผูกกับกำหนดส่งมอบงวด 2 |
| `งวด 5 (25 มี.ค. 70)` | `#8B5CF6` | งานส่งมอบงวดสุดท้าย |
| `🚨 Delayed (ตกค้าง)` | `#EF4444` | งานที่ล่าช้ากว่ากำหนด |
| `⏳ Waiting Dependency` | `#EAB308` | งานที่รองานอื่นหรือรอลูกค้า |
| `🛡️ PDPA / PII` | `#3B82F6` | งานคัดกรองข้อมูลส่วนบุคคล |
| `🏢 รอสิทธิ์ลูกค้า (Customer Blocker)` | `#EC4899` | ติดปัญหาการขอสิทธิ์/เปิดเน็ตจากลูกค้า |

---

## 8. ผลการ Materialize ขึ้นสู่ระบบ Plane จริง (Live Artifacts)

> **สรุปผลการสร้าง:** ระบบได้เชื่อมต่อ Plane API และสร้างโปรเจกต์ กรมที่ดิน พร้อมวัตถุทั้งหมดครบถ้วน 100% ตามพิมพ์เขียว โดยมีรายละเอียด Entity IDs และ Sequence IDs ประจำระบบดังนี้:

### 8.1 ข้อมูลภาพรวมโครงการ (Project Overview)
- **Workspace Slug:** panupong
- **Project Name:** กรมที่ดิน
- **Project Identifier:** DOL
- **Project UUID:** d0795c71-dd1f-40c4-b204-14e14b33c880
- **Live Project URL:** [Plane Project กรมที่ดิน](https://api.plane.so/panupong/projects/d0795c71-dd1f-40c4-b204-14e14b33c880/issues/)
- **เปิดใช้งานฟีเจอร์:** Modules, Cycles, Views, Pages, Intake

### 8.2 Modules (8 Modules)
| Module Code & Name | Module UUID | สถานะ |
| :--- | :--- | :---: |
| Module G: งวดงานและการส่งมอบ (งวดที่ 2, งวดที่ 5, คู่มือ, อบรม, Pen Test) | 5b3c5cce-1a70-4aa5-a2ed-991e38e68d40 | Active |
| Module F: TOR Compliance & System Features (4.1 - 4.5) | e1a9dba7-2664-46cb-82a6-c1cecf5d44d4 | Active |
| Module E: ติดตั้งระบบ On-premise ณ เครื่องลูกค้า (กรมที่ดิน) | 9cd17bdf-7bfa-47fb-ad11-371c5c5d1752 | Active |
| Module D: GenAI Agent, RAG & Webchat API Integration (Samart) | 6d87a7fa-3489-4ef7-902c-88cee22d5c5d | Active |
| Module C: System & Data Architecture / Integration | 7499eb02-e20f-4a1e-8d12-05fc9233e862 | Active |
| Module B: เอกสารใหม่ 50,000 หน้า (Pipeline ETL, OCR & PDPA/PII) | 5b628bd3-2a4f-4379-ab92-7000dd9fa67b | Active |
| Module A: เอกสารเก่า 48,000 หน้า (Data Cleansing & 15 Categories) | fc3117bc-0d26-45f3-aa85-887b9164b095 | Active |
| Module H: Handoff & Immediate Action Items (งานติดตามเร่งด่วน พ.ย. 2569) | 970b1088-4e8c-474a-9b19-0521a664f473 | Active |

### 8.3 Cycles (2 Cycles)
| Cycle Name | Cycle UUID | ช่วงเวลาดำเนินการ |
| :--- | :--- | :---: |
| Cycle ธ.ค. 2569 - มี.ค. 2570: พัฒนาและเชื่อมต่อ API Production สู่การส่งมอบงวด 5 | 866027ab-e788-49e7-a8fb-c93bcce3c82f | 2026-12-01 – 2027-03-25 |
| Cycle พ.ย. 2569: ติดตามงานส่งมอบเอกสาร 5 หมื่นหน้า & ทดสอบระบบ (โบส รับช่วงต่อ) | d7830540-2f81-4a11-a867-18897eb84a21 | 2026-11-01 – 2026-11-30 |

### 8.4 Views & Pages
| ชนิดวัตถุ | ชื่อวัตถุ | Plane UUID |
| :--- | :--- | :--- |
| View | All Work (มุมมองงานทั้งหมด) | 4589522d-ada1-4cdf-9edb-6841af0fab77 |
| View | By Module Board (มุมมองแยกตามหมวดงาน) | a919a05-96ac-4775-958f-c44bb9de470f |
| View | Delayed & Urgent Focus (งานเร่งด่วนและตกค้าง) | da8fcaa0-9a00-49e7-ae0d-3482254c8bd0 |
| View | Cycle พ.ย. 69 Board (โฟกัสสปริ้นท์ปัจจุบัน) | 8ddefd48-2836-4822-a7f6-be97d758c781 |
| Page | สถาปัตยกรรมและแผนการส่งมอบโครงการกรมที่ดิน (SDP GenAI Master Plan) | 446fca1e-8b21-49f1-b5d7-d7b5ce23e840 |

### 8.5 Work Items Mapping (74 รายการ)
| Code | Plane Issue | ชื่องาน | Module | Plane UUID |
| :---: | :---: | :--- | :--- | :--- |
| **H1** | **DOL-62** | [H1 - ด่วนที่สุด] หาสาเหตุและแก้ไขปัญหาระบบล่มของ API อัปโหลดข้อมูลและ Rate Limit | Module H | 7ce5c0ee-ff84-487a-8b95-f309e3da16ff |
| **H2** | **DOL-63** | [H2 - สำคัญ] แก้ไขปัญหาคอขวด LLM / Worker และให้คำปรึกษาเชิงสถาปัตยกรรม | Module H | fccb7847-6848-4dc7-83eb-e58c3a2ec0c0 |
| **H3** | **DOL-64** | [H3 - ส่งต่อคุณโบส] นำเข้าข้อมูลส่วนที่เหลือ (จาก ~80%) และส่งต่อให้คุณโบสทำส่วน Intelligent | Module H | cbd4b671-46b7-4191-a7ee-fc026f57d227 |
| **H4** | **DOL-65** | [H4 - ข้อมูลกลุ่ม 15] ตรวจสอบกลุ่ม 15 ให้เสร็จ นำเข้ากลุ่ม 7, 9, 11 และอัปเดตโครงสร้าง 15 กลุ่มให้ลูกค้า | Module H | 3f121f5a-3392-4904-8cc2-f3ec161135a5 |
| **H5** | **DOL-66** | [H5 - ชี้แจงลูกค้า] จัดทำสไลด์และตารางเปรียบเทียบโครงสร้างเดิม vs 15 กลุ่มใหม่ พร้อมสรุปยอดหน้ารวม | Module H | 13e72dea-9db0-4117-b738-2607c52d9f7a |
| **H6** | **DOL-67** | [H6 - ปรับปรุง Prototype] แก้ไขเอกสาร Prototype ตาม Feedback ผู้ใช้ 3-4 ข้อ | Module H | c7e0fc50-26eb-46df-8f7f-e9af025806df |
| **H7** | **DOL-68** | [H7 - นัดหารือสามารถ] ประชุมหารือ บมจ. สามารถ เรื่อง User Management และโครงสร้างสิทธิ์ราชการหลายระดับ | Module H | f6acf8c7-61e1-468c-a6b2-bd64c4d4565d |
| **H8** | **DOL-69** | [H8 - นำเสนอ MLOps] ดอมเตรียมเนื้อหาอธิบาย MLOps / ML Flow และการทดสอบความแม่นยำให้ลูกค้า | Module H | 754a0518-1872-4e1d-8aac-b20dca8e4fae |
| **H9** | **DOL-70** | [H9 - ติดตั้งเครื่อง On-prem] พี่เบิ้มติดตั้งซอฟต์แวร์ทั้งหมด (6-7 ตัว) บนเซิร์ฟเวอร์กรมที่ดิน | Module H | 69fdad05-70b5-4cd9-8728-9338163f6d64 |
| **H10** | **DOL-71** | [H10 - เอกสารอบรม] จัดทำเอกสารคู่มือ Training ทั้งส่วน AI และ Net Intelligence ให้พร้อมส่งมอบ | Module H | c0fc60cf-ab1e-4cec-836c-1ffaacf958e8 |
| **H11** | **DOL-72** | [H11 - ตรวจสอบข้อมูลก่อน Meta Data] พี่บิ๊งและคุณโบสทดสอบความถูกต้องข้อมูลต้นทาง-ปลายทาง และเตรียมทดสอบ 1-2 พ.ย. | Module H | f209c6e4-0749-4a41-96ee-22fe32835975 |
| **A1** | **DOL-6** | [A1] ทบทวนไฟล์ OCR + Metadata JSON เดิม / recheck จำนวนไฟล์ | Module A | 1a34c771-c6af-4450-aa46-d6afc1cf069e |
| **A2** | **DOL-7** | [A2] กำหนดเกณฑ์จัดกลุ่มเอกสาร (16→14 กลุ่ม) ร่วมกับกรมที่ดิน | Module A | 8a1ba369-312f-4ae0-8f81-e9174a90e46c |
| **A3** | **DOL-8** | [A3] รวบรวมไฟล์นอกชุด 48,000 ที่ตกหล่น | Module A | 8b9ac902-8349-4c1c-885a-6df4bd570f7b |
| **A4** | **DOL-9** | [A4] พัฒนา Classification (Rule/ML) ตามเกณฑ์ 14 ประเภท | Module A | 529acf27-ce83-4888-b385-dd2b1f5a279e |
| **A5** | **DOL-10** | [A5] รัน Classification + นำเข้าระบบ (48,000) | Module A | 21729ea6-d912-499c-9445-6c6e9402af91 |
| **A6** | **DOL-11** | [A6] QA / สุ่มตรวจผลการจัดกลุ่ม | Module A | 0bc14356-9f35-4677-95b5-e28ac3b6e268 |
| **A7** | **DOL-12** | [A7] สกัดวันมีผลบังคับใช้/วันยกเลิก (AI) + ให้ประธานอนุมัติ (ใช้กับชุด B ด้วย) | Module A | 7b72f9f9-e909-403a-9fd8-de71dc9fbf97 |
| **B1** | **DOL-13** | [B1] นำเข้าไฟล์ PDF ชุดใหม่ (3 งวดภายใน พ.ย.) | Module B | 8a430b72-19a3-4caf-a746-0fcfed547e08 |
| **B2** | **DOL-14** | [B2] พัฒนา ETL Pipeline (microservice/Docker/API) | Module B | 09b329fd-162e-4b44-95f2-751e2c7ce447 |
| **B3** | **DOL-15** | [B3] ตั้งค่า OCR Engine (ไทย/อังกฤษ/เลขไทย-อารบิก, สี/ขาวดำ) | Module B | e2ff4255-ae2f-43c8-8e94-5b171da36b0c |
| **B4** | **DOL-16** | [B4] รัน OCR เอกสารใหม่ทั้งหมด (50,000 หน้า) | Module B | 96bdf0da-eb7e-4a07-8b8c-ff277e6948dd |
| **B5** | **DOL-17** | [B5] ปรับปรุงคุณภาพข้อมูล (แก้คำผิด) ตาม 4.1.3 | Module B | 8d329e40-f38d-4248-8d0c-d179214cfccd |
| **B6** | **DOL-18** | [B6] จัดกลุ่มเอกสารตาม mapping ลูกค้า (14 กลุ่ม) | Module B | de6e033c-6962-46ae-bb44-9417cae8726b |
| **B7** | **DOL-19** | [B7] Export ข้อมูล JSON/CSV (ชุดข้อมูล) | Module B | 14d59fa6-69f6-448b-a98e-9d441c171864 |
| **B8** | **DOL-20** | [B8] QA / Validate ข้อมูล (รวม 48,000 + 50,000) | Module B | 0885d2f7-782d-4208-a180-407ee113497e |
| **B9** | **DOL-21** | [B9] PDPA/PII Screening (ซ่อน/แทนที่ข้อมูลส่วนบุคคล - หมวดคำพิพากษา) | Module B | ad861508-0ff5-45d1-a98c-a5de5f2335c5 |
| **C1** | **DOL-22** | [C1] พัฒนาฟังก์ชัน Export JSON/CSV (ระดับระบบ) | Module C | 4d37b061-9079-4baf-ac88-316cf45968f8 |
| **C2** | **DOL-23** | [C2] นำเข้าเอกสารประเภทเดียวกันหลายหน้าพร้อมกัน (Batch/Queue/Worker) | Module C | 38366d9f-0547-4a28-a566-544b45635b47 |
| **C3** | **DOL-24** | [C3] Integration Testing (ทุกโมดูล) | Module C | 5711c43f-9d25-48c0-bf11-21e006b944cd |
| **C4** | **DOL-25** | [C4] UAT ร่วมกับกรมที่ดิน (ระบบนำเข้า) | Module C | a0525504-684b-4420-a59f-bb23bfee6187 |
| **C5** | **DOL-26** | [C5] แก้ไข Bug ตามผล UAT | Module C | 9a2a19f9-2e4a-497f-a490-787f23045035 |
| **C6** | **DOL-27** | [C6] Go-live / ส่งมอบระบบและเอกสาร | Module C | de2178ac-f136-4751-aa83-84cc4c7c898a |
| **D1** | **DOL-28** | [D1] ออกแบบสถาปัตยกรรมเชื่อมข้อมูลเข้า GenAI (Knowledge Base) | Module D | 5d08cdc1-b522-429a-b4ae-63681498a576 |
| **D2** | **DOL-29** | [D2] Embedding / Knowledge Base (RAG) | Module D | 606d3f03-4c0a-48d3-9a28-86a87c3116a8 |
| **D3** | **DOL-30** | [D3] พัฒนา GenAI Agent (Prompt/Intent งานรังวัด, ภาษาไทย/อังกฤษ) | Module D | 32d0dc10-c521-413d-a460-b27c343331a2 |
| **D3.1** | **DOL-73** | [D3.1] ระบบแหล่งอ้างอิง (Citation): ส่งข้อมูลอ้างอิง + ลิงก์ PDF ต้นฉบับ | Module D | e2f63f8c-ec42-4e51-813e-91ff00d0d9e8 |
| **D4** | **DOL-31** | [D4] ทดสอบความแม่นยำ Agent (F1/Precision/Recall เทียบ Legal SME) | Module D | 214e02b8-9b6e-4d82-b091-1445cde7495e |
| **D5.1** | **DOL-32** | [D5.1] Softnix: ส่ง API Spec (Swagger) + Sandbox ให้สามารถ (ตอบ + citations[] + session) | Module D | fb746cf3-849c-4de3-8a06-9b37aee7052f |
| **D5.2** | **DOL-33** | [D5.2] Softnix: Agent API Production (auth, session, feedback, รองรับ concurrent) | Module D | f4ceec06-3ca1-448f-899e-ddb8fd8fa2aa |
| **D5.3** | **DOL-34** | [D5.3] สามารถ: เชื่อม Webchat เข้ากับ Agent API | Module D | a123de1c-972d-4ca7-94ed-4d3809d1e830 |
| **D5.4** | **DOL-35** | [D5.4] สามารถ: แสดงผลแหล่งอ้างอิงใน Webchat (citation + เปิดไฟล์ต้นฉบับ) | Module D | ca451d5a-477a-48bf-87c1-67de8325b845 |
| **D5.5** | **DOL-36** | [D5.5] Softnix: ส่งมอบ API Production + Swagger + Token ให้สามารถ (กำหนด 12 ก.พ. 2570) | Module D | f85bbb72-1568-4e20-9e80-a7ac07087425 |
| **D6** | **DOL-37** | [D6] Integration Testing บน Webchat จริง | Module D | c9d4c018-57ff-410d-bce3-b1063d7c54d0 |
| **D7** | **DOL-38** | [D7] UAT ผู้ใช้จริงผ่าน Webchat | Module D | 09599230-1db2-4571-af08-2e90ad094eb5 |
| **D7.1** | **DOL-76** | [D7.1] ตรวจสอบคุณสมบัติ Progressive Web Application (PWA) และช่องคำถาม >= 512 ตัวอักษร | Module D | e2c3a762-383f-4c90-9ec5-e5f6e9b3d7ce |
| **D8** | **DOL-39** | [D8] Go-live Agent บน Webchat + ส่งมอบ | Module D | 6bb0b811-9db0-45bb-af49-dea645593882 |
| **D9** | **DOL-40** | [D9] คู่มือ User/Admin Manual + Workflow Diagram + API Doc | Module D | ba1c1af9-1fec-4873-87cd-257380fd3615 |
| **E1** | **DOL-41** | [E1] ขอเปิด Internet + VPN/Remote Access (ผ่าน Security ลูกค้า) | Module E | 7f3a017e-de60-475f-bc0d-a10c2d3c7e63 |
| **E1.1** | **DOL-75** | [E1.1] ติดตั้งและกำหนดค่า Beszel (GPU & System Monitoring Hub/Agent) | Module E | f76fd6ed-1f64-4bb7-8ade-23128158224a |
| **E2** | **DOL-42** | [E2] ติดตั้ง OS + Microservices 6 ตัว บนเครื่อง Production (ปากเกร็ด) | Module E | 60dc699e-5ab3-4d4c-b217-272db47d8cb2 |
| **E3** | **DOL-43** | [E3] ย้ายข้อมูล 48,000 (Docker Volume dump) ขึ้นเครื่องลูกค้า | Module E | 94eefb83-bd19-49f8-9957-6a3b6e0e34c6 |
| **E4** | **DOL-44** | [E4] ทดสอบ Performance บนเครื่องจริง (OCR/LLM, Request deadline 1,800 วินาที) | Module E | 626017ea-b56f-4e00-9765-d81fc1bfc3e1 |
| **F1** | **DOL-45** | [F1] Gap Analysis TOR 4.2-4.5 เทียบ platform + ตกลงขอบเขต Softnix/สามารถ | Module F | fd1ad2c5-72e1-426b-8c5c-0281c8f775e5 |
| **F2** | **DOL-46** | [F2] Guardrail: บล็อกคำหยาบ/นอกขอบเขต + ข้อความปฏิเสธ | Module F | 7bf713a9-b33e-49da-b7ff-e53f54322247 |
| **F3** | **DOL-47** | [F3] บริบทการสนทนา (Session) + ประวัติสนทนา | Module F | ea543d48-d34e-4d7c-bfbd-c37b24323e97 |
| **F4** | **DOL-48** | [F4] Feedback/ความพึงพอใจ + Feedback loop (RLHF) | Module F | 07e2e831-dbae-49ee-b61f-74b1e0c0b2b4 |
| **F5** | **DOL-49** | [F5] รายงานสถิติการใช้งาน AI (ตอบถูก/ความพึงพอใจ/error) | Module F | e9f7b38b-b878-4084-bd06-c407ca5d63a2 |
| **F6** | **DOL-50** | [F6] ระบบบริหารจัดการผู้ใช้ (สิทธิ์, อนุมัติ, Dashboard) | Module F | 1d863ab1-6635-4b37-8824-9908e92c57bd |
| **F6.1** | **DOL-77** | [F6.1] พัฒนาระบบติดตามโควต้าการใช้งานตาม SOC 26.13 (Queries, Pages, Tokens) | Module F | f2193f5b-19bc-40d3-b71b-a26baf0205ab |
| **F7** | **DOL-51** | [F7] Log Management ตาม พ.ร.บ.คอมพิวเตอร์ 2550/2560 | Module F | 715faf1f-e5f0-4716-951d-01ddc8a394ed |
| **F8** | **DOL-52** | [F8] Load Test >= 100 การสนทนาพร้อมกัน | Module F | 370f9772-1a2a-422b-bcce-fa2d6288ff66 |
| **F9** | **DOL-53** | [F9] เชื่อมระบบสนับสนุนงานภาคสนาม/ระบบบริหารงานรังวัด (ขอบเขตต้องยืนยัน) | Module F | 039cc1ee-d14c-4464-85fa-9734b37c9524 |
| **G1** | **DOL-54** | [G1] ส่งมอบและติดตั้งระบบที่พัฒนาที่เหลือทั้งหมด | Module G | 7c09b820-e807-4014-a153-9ba92ed6ae9b |
| **G2** | **DOL-55** | [G2] จัดฝึกอบรมการใช้งานระบบ (สามารถนำ, Softnix สนับสนุน) | Module G | 42c072e7-b2dd-49c8-8a1d-b681905af6ca |
| **G2.1** | **DOL-78** | [G2.1] หลักสูตรอบรมผู้ดูแลระบบ (Admin Training - 0.5 วัน: สถาปัตยกรรม, Model Tuning, Beszel) | Module G | e727be77-99bb-4a40-8d5a-a5ca93421642 |
| **G2.2** | **DOL-79** | [G2.2] หลักสูตรอบรมผู้ใช้งานทั่วไป (User Training - 0.5 วัน: การถามตอบ, กฎหมายรังวัด, ตรวจสอบ Citation) | Module G | 173f8216-5272-4950-9ac9-82a329f94444 |
| **G3** | **DOL-56** | [G3] Penetration Testing ครั้งที่ 2 + รายงานผล | Module G | 114f1a1c-b982-439c-abda-feec07c50391 |
| **G3.1** | **DOL-74** | [G3.1] แก้ไขช่องโหว่ตามผล Pen Test (ส่วน Softnix) | Module G | 07f223fa-a2ad-4fdf-930a-56a1e2ed18a3 |
| **G4** | **DOL-57** | [G4] คู่มือปฏิบัติงานสำหรับผู้ใช้ระบบ | Module G | 25a7a2d8-aee6-4276-aaa4-c41c5b142cbb |
| **G5** | **DOL-58** | [G5] Source Listing + Library ของทุกโปรแกรมที่พัฒนา | Module G | e8c0aced-c4ef-4065-8968-290443ad8472 |
| **G6** | **DOL-59** | [G6] Architecture Diagram ของระบบที่พัฒนา | Module G | c9643f1c-436e-4b04-8907-785d238d74c5 |
| **G7** | **DOL-60** | [G7] คู่มือกำหนดค่า Configuration อุปกรณ์ + System Diagram | Module G | 6bc43d69-354b-4e99-9035-884ebc7b4497 |
| **G8** | **DOL-61** | [G8] ส่งมอบงวดที่ 5 (วันที่ 300) ให้ลูกค้า | Module G | 1b28c260-c97b-4b40-ab53-1af4e14114cb |
