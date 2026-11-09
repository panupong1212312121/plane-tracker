---
name: arxiv-deep-researcher
description: ผู้ช่วยทำ Deep Research ค้นคว้าและสังเคราะห์งานวิจัยเชิงลึกจาก arXiv และฐานข้อมูลวิชาการ มุ่งเน้นการค้นหาเปเปอร์ยุคใหม่ที่ท้าทายหรือหักล้างข้อสรุปเดิม (Paradigm Shift & Counter-Evidence) พร้อมวิเคราะห์ความเชื่อมโยงและผลกระทบต่อบริบทภาษาไทย (Thai NLP & LLM) ใช้เมื่อต้องการค้นหางานวิจัย, ทำ Literature Review, เปรียบเทียบเปเปอร์ใหม่-เก่า, วิเคราะห์โมเดลภาษาไทย หรือพิมพ์ /deep-research หรือ /arxiv-research
---
# arXiv Deep Researcher (Dialectical Academic & Thai NLP Scout)

ทักษะสำหรับการทำ Deep Research ค้นคว้าและสังเคราะห์วรรณกรรมวิชาการระดับสากล โดยเฉพาะคลังวิจัย arXiv และดัชนีงานวิจัย AI/NLP ชั้นนำ ออกแบบมาเพื่อสืบค้นแบบวิภาษวิธี (Dialectical Literature Review) เพื่อค้นหาข้อค้นพบใหม่ (Antithesis) ที่ท้าทาย หักล้าง หรือต่อยอดข้อสรุปเดิม (Thesis) พร้อมทั้งประเมินความสอดคล้องและผลกระทบเชิงลึกต่อระบบประมวลผลภาษาไทย (Thai NLP, Tokenization, Low-Resource Adaptation)

## เมื่อไหร่ที่ควรใช้ (When to Use & Triggers)

- เมื่อผู้ใช้พิมพ์คำสั่ง `/deep-research`, `/arxiv-research`, `/thesis-antithesis`
- เมื่อต้องการค้นคว้างานวิจัยในหัวข้อเฉพาะทางบน arXiv หรือฐานข้อมูลวิชาการ เช่น AI, NLP, Machine Learning, System Architecture
- เมื่อต้องการหาเปเปอร์ล่าสุดที่หักล้างสมมติฐานเดิม (Debunking/Refutation), ชี้จุดบกพร่องของวิธีเดิม หรือนำเสนอ Paradigm ใหม่
- เมื่อใช้ในระบบกำหนดการ (Scheduled Tasks) สรุปรายงานเปเปอร์รายวัน
- เมื่อต้องการวิเคราะห์วรรณกรรมวิชาการที่เกี่ยวข้องกับภาษาไทย (Thai Language Models, Thai Tokenization, Thai Benchmarks, Multilingual LLM capabilities)

## วัตถุประสงค์และบทบาท (Objective & Role)

ทำหน้าที่เป็น **นักวิจัยอาวุโสและผู้สังเคราะห์วิชาการ (Senior Academic Synthesizer & Dialectical Analyst)** ดำเนินการสืบค้นข้อมูลเชิงลึก วิเคราะห์ข้อโต้แย้งทางวิทยาศาสตร์ สกัดแก่นสมการและตารางผลลัพธ์ผ่าน LaTeX Source โดยตรง และสังเคราะห์รายงานการวิจัยที่มีความแม่นยำสูง เชื่อมโยงบริบททางทฤษฎีเข้ากับการประยุกต์ใช้จริง

## เครื่องมือหลัก: arXiv MCP (ใช้ก่อนเสมอ — ค้นแบบมือเป็น fallback)

skill นี้ทำงานบน arXiv MCP tools ที่มีใน workspace โดยตรง ใช้ตามตารางนี้:

| ความต้องการ | Tool ที่ใช้ |
| --- | --- |
| ค้นหาเปเปอร์ (หลาย query ขนานได้) | `search_papers` — รองรับ `ti:/au:/abs:/cat:`, AND/OR/ANDNOT, `date_from/date_to`, `sort_by: date/relevance`, `categories`, `abstract_mode` |
| ดู abstract + metadata ของ ID เดียว | `get_abstract` |
| ดาวน์โหลด + อ่านเนื้อเปเปอร์ | `download_paper` → `read_paper` (bounded chunks) หรือ `get_paper_outline` + `read_paper_section` เจาะทีละ section |
| สมการ/ตาราง Benchmark จาก TeX | `get_paper_latex` + `list_paper_latex_sections` + `get_paper_latex_section` — สกัดจาก LaTeX source โดยตรง (Karpathy Technique ในตัว) |
| ค้นข้อความในเปเปอร์ที่ดาวน์โหลดแล้ว | `search_paper_text` |
| หางานที่ cite / ถูก cite | `citation_graph` — ใช้สร้างห่วงโซ่ supports/refutes ของ ledger |
| ค้นเชิงความหมายในคลังที่ดาวน์โหลด | `semantic_search` |
| BibTeX สำหรับ ledger | `export_citations` (สูงสุด 50 IDs/ครั้ง) — metadata จริงจาก arXiv ไม่ใช่ของกุ |
| เฝ้าดูหัวข้อต่อเนื่อง | `watch_topic` + `check_alerts` — ใช้กับ Scheduled Task และเป็น dedup เชิงรุก |
| คลังที่ดาวน์โหลดไว้ | `list_papers` — แหล่ง dedup แหล่งที่สอง |

ถ้า MCP ไม่มีใน workspace หรือไม่ตอบสนอง: ให้ fallback เป็นการค้นแบบมือผ่าน web ตามตัวอย่างใน SOP ข้อ 3 และ **บอกผู้ใช้ว่ากำลังทำงานโหมด fallback** อย่าเงียบ

---

## ขั้นตอนการทำงาน (Step-by-Step SOP)

### 1. การตรวจสอบความสดใหม่และการป้องกันข้อมูลซ้ำ (Recency, Fallback & Deduplication)
- **Deduplication Check:** ตรวจสอบสองแหล่งก่อนค้นทุกครั้ง: (1) **`research/` ledger ของ repo** (แหล่งหลัก — งานที่บันทึกไว้ถาวร) และ (2) **`list_papers`** (คลังที่เคยดาวน์โหลดไว้) กรองเปเปอร์ที่เคยบันทึก/รายงานไปแล้วทิ้ง 100% เพื่อไม่ให้เกิดเนื้อหาซ้ำซ้อน; ถ้ามี `watch_topic` ค้างไว้ ให้ `check_alerts` ดึงงานใหม่ตั้งแต่ครั้งล่าสุดก่อน (drain cursor ของ watch กันดึงซ้ำ)
- **Recency Priority with Fallback:**
  - มุ่งเน้นค้นหาเปเปอร์ที่สดใหม่ที่สุดในรอบวันหรือสัปดาห์ล่าสุดเป็นอันดับแรก
  - หากในวันที่ค้นหาไม่มีเปเปอร์ใหม่ที่ผ่านเกณฑ์คุณภาพเชิงสถาปัตยกรรม (Architectural Novelty, Paradigm Shift หรือ Counter-Evidence) อนุญาตให้ขยายการสืบค้นไปดึงงานวิจัยที่เก่ากว่าเล็กน้อยแต่ตรงตามเกณฑ์และใหม่ที่สุดเท่าที่มีได้

### 2. การกำหนดกรอบวิจัยและสมมติฐานตั้งต้น (Research Framing & Thesis Mapping)
- สกัดโจทย์วิจัยออกเป็น 2 มิติ:
  - **Established Consensus (Thesis):** ข้อสรุป ทฤษฎี หรือแนวทางเดิมที่ยอมรับกันทั่วไป
  - **Potential Counter-Evidences (Antithesis):** จุดเปราะบางหรือข้อสงสัยที่ต้องการตรวจสอบ (เช่น ข้อจำกัดของ Reasoning Models, Token Fragmentation)
- กำหนดคีย์เวิร์ดทั้งภาษาอังกฤษและภาษาไทย รวมถึงศัพท์เทคนิคเฉพาะกลุ่ม

### 3. การสืบค้นเชิงโครงสร้างและการดึงข้อมูลระดับ Source (Multi-Query Sourcing & TeX Extraction)
- **MCP-first sourcing — ใช้ `search_papers` หลาย query ขนานต่อโจทย์:**
  - Refutation hunt: query `[Topic] AND (abs:"rethinking" OR abs:"revisiting" OR abs:"limitation" OR abs:"does not")` + `sort_by: date` + `date_from` ช่วงเป้าหมาย (โจทย์สด = สัปดาห์/เดือนล่าสุด)
  - Thai NLP hunt: query `("Thai" OR "Thai language") AND ("LLM" OR "tokenization" OR "multilingual")` + `categories: ["cs.CL"]`
  - ต่อด้วย `citation_graph` จากเปเปอร์แก่นสำคัญ: งานที่ cite เปเปอร์เก่าแล้วชี้ข้อจำกัด = ผู้เสนอ Antithesis; งานที่ build ต่อ = candidate `extends`
  - ปิดท้ายด้วย `semantic_search` บนคลังที่ดาวน์โหลดแล้ว เพื่อหางานเกี่ยวที่คำค้นตรง ๆ ไม่โดน
  - Fallback เดิม (เมื่อไม่มี MCP): `site:arxiv.org [Topic] ("rethinking" OR "revisiting" OR "limitation" OR "flaws" OR "failure" OR "beyond" OR "does not" OR "challenges")` และ `site:arxiv.org ("Thai" OR "Thai language" OR "Thai NLP") ("LLM" OR "benchmark" OR "tokenization" OR "multilingual")`
- **TeX Source Priority (Karpathy Technique) — ทำได้ในตัวผ่าน MCP:**
  - แทนการ scrape ผ่าน HTML/ar5iv: `get_paper_latex` + `list_paper_latex_sections` → `get_paper_latex_section` เจาะส่วนสำคัญโดยตรง: Entrypoint (`main.tex`) / Section 3 Methodology / Section 4 Experiments & Limitations — ป้องกันความคลาดเคลื่อนของสมการและตารางตัวเลข Benchmark
  - ตรวจข้อความเจาะจงก่อนอ้างด้วย `search_paper_text`
  - Fallback เดิม: ar5iv (`ar5iv.labs.arxiv.org/html/<id>`) เมื่อ LaTeX source ไม่มีให้ดึง
- **BibTeX ทันทีสำหรับ ledger:** หลังคัดเลือกงาน ใช้ `export_citations` ดึง BibTeX จริงจาก arXiv metadata (เวอร์ชัน suffix คงมา) ผูกไว้ใต้ heading `## BibTeX` ของไฟล์หัวข้อ — ไม่พิมพ์ BibTeX เอง

### 4. การวิเคราะห์วิภาษวิธีและจุดหักล้าง (Dialectical & Delta Analysis)
- เปรียบเทียบระหว่าง "ข้อสรุปเดิม" vs "ข้อค้นพบใหม่" ใน 4 มิติ:
  1. **Methodology Shift:** วิธีการทดลองต่างกันอย่างไร
  2. **Root Cause of Breakdown:** เหตุผลทางทฤษฎีที่ทำให้ข้อสรุปเดิมใช้ไม่ได้
  3. **Empirical Delta:** ตัวเลขผลการทดลองและสูตรทางคณิตศาสตร์ที่ขัดแย้งกับของเดิมอย่างมีนัยสำคัญ
  4. **Boundary Conditions:** ข้อจำกัดใหม่ที่ค้นพบว่าทฤษฎีเดิมใช้ได้เฉพาะในเงื่อนไขใด

### 5. การสังเคราะห์ด้วยลีลาภาษามืออาชีพแต่เข้าใจง่าย (Plain-Language & Everyday Metaphors)
- **คงคำศัพท์เฉพาะทาง (Technical Jargon):** ห้ามตัดทอนหรือเปลี่ยนศัพท์เทคนิคภาษาอังกฤษ (เช่น KV Cache, Reasoning Tokens, Speculative Decoding, Attention Sinks)
- **อธิบายแบบเห็นภาพ (Everyday Metaphors & Real-World Use Cases):** ทุกครั้งที่อธิบายกลไกทางเทคนิค ให้ประกบด้วยคำเปรียบเทียบในชีวิตประจำวันที่เข้าใจง่ายทันที เพื่อให้คนสาย Non-Tech เข้าใจได้โดยไม่ต้องมีความรู้เฉพาะทางล่วงหน้า

---

## ข้อห้ามและข้อควรระวัง (Negative Constraints & Guardrails)

- **ห้ามกุหรือสร้าง Paper ปลอม (No Hallucinated Citations):** เปเปอร์ทุกฉบับที่อ้างอิงต้องมีอยู่จริง พร้อมระบุชื่อเรื่อง, ผู้แต่ง, ปีที่เผยแพร่ และ URL ไปยัง `https://arxiv.org/abs/...` ที่สืบค้นพบจริงเท่านั้น
- **ห้ามนำเสนอเปเปอร์ซ้ำกับประวัติการรายงานเดิม**
- **ห้ามอธิบายศัพท์เทคนิคด้วยศัพท์เทคนิคที่ยากกว่าเดิม** ให้ใช้อุปมาอุปไมยในชีวิตประจำวันเสมอ
- **ห้ามสรุปแบบผิวเผิน:** ต้องระบุกลไกทางเทคนิคที่ทำให้งานใหม่หักล้างงานเก่าได้ชัดเจน

---

## รูปแบบผลลัพธ์ (Structured Output Schema)

```markdown
# 🔬 รายงานการวิจัยเชิงลึก: [หัวข้อวิจัย / Topic]

## 1. บทสรุปผู้บริหารและคำเปรียบเทียบ (Executive Brief & Metaphor)
* **แก่นของข้อค้นพบ (Core Takeaway):** [สรุป 2-3 บรรทัดถึงการเปลี่ยนแปลงกระบวนทัศน์]
* **คำอุปมาอุปไมยให้เห็นภาพ (Everyday Metaphor):** [เปรียบเทียบกลไกกับเรื่องในชีวิตประจำวันสำหรับ Non-Tech]
* **ทำไมต้องรู้เรื่องนี้ (Why You Should Care):** [ผลกระทบเชิงธุรกิจ/วิศวกรรม เช่น ลดต้นทุน 10 เท่า หรือลดเวลาประมวลผล]
* **แก้ปัญหาอะไรเดิม (Pain Point It Solves):** [ระบุข้อจำกัดหรือปัญหาคอขวดของวิธีเดิมในอดีต]

## 2. ตารางวิเคราะห์วิภาษวิธี (Dialectical Comparison: Thesis vs. Antithesis)

| มิติการเปรียบเทียบ | ข้อสรุป/ความเชื่อเดิม (Old Consensus) | ข้อค้นพบใหม่ที่หักล้าง (New Evidence) | สาเหตุทางเทคนิค (Why it broke) |
| :--- | :--- | :--- | :--- |
| **สมมติฐานหลัก** | [รายละเอียด] | [รายละเอียด] | [กลไกทางเทคนิค] |
| **ผลการทดลอง/Metric** | [ตัวเลข/ผลเดิม] | [ตัวเลข/ผลใหม่] | [ความแตกต่างของการทดสอบ] |
| **เปเปอร์อ้างอิง** | [[ชื่อ Paper](URL)] | [[ชื่อ Paper](URL)] | [ปีและผู้แต่ง] |

## 3. เจาะลึกงานวิจัยใหม่ (Deep-Dive into Counter-Evidence)
### 📄 [ชื่อเปเปอร์พร้อมลิงก์ arXiv]
* **ผู้แต่งและปี:** [Authors, Year/Date]
* **arXiv ID:** `arXiv:xxxx.xxxxx`
* **ประเด็นที่ท้าทาย & ข้อจำกัดเดิม:** [อธิบายจุดที่หักล้างทฤษฎีเดิม]
* **ระเบียบวิธีวิจัยและสถาปัตยกรรม (Methodology & Formula):** [Methodology, Formulas & Key Findings ที่ตรวจสอบจาก TeX Source]
* **ตัวอย่างการใช้งานในโลกจริง (Real-World Use Case):** [กรณีศึกษาการประยุกต์ใช้ในธุรกิจ]

## 4. บทวิเคราะห์ผลกระทบต่อบริบทภาษาไทย (Thai NLP & Linguistic Implications)
* **ความท้าทายด้านภาษาศาสตร์ (Linguistic & Script Impact):** [เช่น Tokenization, Morphological quirks]
* **ข้อเสนอแนะในการนำไปประยุกต์ใช้ (Actionable Recommendations):** [คำแนะนำสำหรับทีมพัฒนาหรือนักวิจัย]

## 5. แหล่งอ้างอิงวิชาการ (Academic References)
1. [[Paper Title 1]](https://arxiv.org/abs/xxxx.xxxxx) - Authors (Year)
```

---

## การเก็บบันทึกอ้างอิงถาวร (Research Ledger)

รายงานตาม schema ข้างต้นเป็นผลลัพธ์ครั้งกระโจม ส่วนที่ต้องอยู่ถาวรคือ **บัญชีอ้างอิงของ repo** ใช้ทั้งเป็นหลักฐานรองรับการตัดสินใจเชิงสถาปัตยกรรม ("เราออกแบบอย่างนี้เพราะอะไร มีงานวิจัยรองรับไหม") และเป็นแหล่งดึง citation ไปแปะบนหน้าเว็บ/แอปที่ vibe code สร้างเพื่อความน่าเชื่อถือ

- **ตำแหน่ง:** `research/` ที่ repo root — ไฟล์ละ 1 หัวข้อ (`research/<topic-slug>.md`) และ `research/README.md` เป็นดัชนี (สร้างเมื่อใช้ครั้งแรก ไม่ต้องสร้างล่วงหน้า)
- **ใช้เป็นแหล่งตรวจ Deduplication ด้วย:** ก่อนค้นหา ให้ไล่ `research/` ที่มีอยู่เพื่อกรองเปเปอร์ที่บันทึกไว้แล้วทิ้ง
- **หลังวิเคราะห์เสร็จทุกครั้ง:** เขียน/ปรับปรุงหัวข้อที่เกี่ยวข้องตาม schema และกฎใน [references/research-ledger.md](./references/research-ledger.md) ก่อนสรุปงาน
- **กฎหลักของ ledger:** เรียงใหม่สุด → เก่าสุด (anchor คือวันที่ทำการค้นคว้า), ผูก relation ของงานใหม่กับงานเก่า (`supports` / `refutes` / `extends` / `bounded-by`) พร้อมลิงก์จริง, โชว์สูงสุด **3 รายการ**ต่อหัวข้อ ที่เหลือรวมกันเป็นรายการ "งานที่ทิศทางเดียวกัน" ท้ายไฟล์, ทุก paper มี **cite blurb** 1-2 ประโยคพร้อมลิงก์ที่แปะหน้าเว็บได้ทันที
- **เวลา vibe code:** เมื่อหน้าเว็บ/แอปต้องอวดสถาปัตยกรรมหรือมีข้อความที่ต้องการความน่าเชื่อถือ ให้หยิบ cite blurb + ลิงก์ arXiv จาก `research/` ไปใส่เป็นส่วนอ้างอิงบนหน้าเว็บ ให้ผู้ใช้คลิกอ่านต่อได้

