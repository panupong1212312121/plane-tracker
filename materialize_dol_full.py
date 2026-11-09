import os
import json
import time
import requests

api_key = os.getenv('PLANE_API_KEY')
slug = os.getenv('PLANE_WORKSPACE_SLUG', 'panupong')
project_id = os.getenv('PLANE_PROJECT_ID', 'd0795c71-dd1f-40c4-b204-14e14b33c880')
user_id = os.getenv('PLANE_USER_ID', '6de5a3e3-a9ad-42a1-bdfa-21c193d628ef')

if not api_key:
    raise ValueError("PLANE_API_KEY environment variable is required.")

from plane_mcp.client import get_plane_client_context
from plane.models.cycles import CreateCycle
from plane.models.modules import CreateModule
from plane.models.labels import CreateLabel
from plane.models.work_items import CreateWorkItem

client, workspace_slug = get_plane_client_context()
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}

def to_list(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get('results', [])
    return []

# ==========================================
# 1. STATES MAPPING
# ==========================================
print("\n--- 1. Mapping States ---")
r_states = requests.get(f"https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/states/", headers=headers)
state_list = to_list(r_states.json())
states = {s['name'].lower(): s['id'] for s in state_list}
states_by_group = {s['group']: s['id'] for s in state_list}
print("States mapped:", states)

STATE_BACKLOG = states.get('backlog', states_by_group.get('backlog'))
STATE_TODO = states.get('todo', states_by_group.get('unstarted'))
STATE_IN_PROGRESS = states.get('in progress', states_by_group.get('started'))
STATE_DONE = states.get('done', states_by_group.get('completed'))
STATE_CANCELLED = states.get('cancelled', states_by_group.get('cancelled'))

state_key_map = {
    'DONE': STATE_DONE,
    'IN_PROGRESS': STATE_IN_PROGRESS,
    'TODO': STATE_TODO,
    'BACKLOG': STATE_BACKLOG
}

# ==========================================
# 2. CREATE LABELS (19 LABELS)
# ==========================================
print("\n--- 2. Setting up 19 Labels ---")
r_lbl = requests.get(f"https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/labels/", headers=headers)
existing_labels = {l['name']: l['id'] for l in to_list(r_lbl.json())}
label_map = dict(existing_labels)

label_defs = [
    {"name": "Softnix", "color": "#0052CC", "description": "งานที่ทีม Softnix รับผิดชอบหลัก"},
    {"name": "สามารถ (Samart)", "color": "#FF8B00", "description": "งานที่ บมจ. สามารถ รับผิดชอบ"},
    {"name": "กรมที่ดิน (DOL)", "color": "#00875A", "description": "งานฝั่งกรมที่ดิน / ลูกค้า"},
    {"name": "Joint / ร่วมกัน", "color": "#6554C0", "description": "งานที่ต้องประสานงานร่วมกันหลายฝ่าย"},
    {"name": "Urgent / Blocker", "color": "#DE350B", "description": "งานเร่งด่วน หรือปัญหาที่เป็นคอขวด"},
    {"name": "Handoff / โบส", "color": "#57D9A3", "description": "งานส่งมอบให้คุณโบสรับช่วงต่อ"},
    {"name": "Data / ETL / OCR", "color": "#00B8D9", "description": "งานจัดการข้อมูล แปลงเอกสาร และจัดกลุ่ม"},
    {"name": "AI / RAG / Intelligent", "color": "#8777D9", "description": "งาน AI Model, Prompt, RAG และ Net Intelligence"},
    {"name": "API / Integration", "color": "#4C9AFF", "description": "งานพัฒนาและเชื่อมต่อ API กับ Webchat"},
    {"name": "Infra / On-prem", "color": "#FFAB00", "description": "งานเซิร์ฟเวอร์, OS, VPN และเครื่องลูกค้า"},
    {"name": "TOR Compliance", "color": "#FF5630", "description": "ข้อกำหนดตามขอบเขต TOR 4.1 - 4.5"},
    {"name": "Documentation / Training", "color": "#36B37E", "description": "คู่มือ, เอกสารระบบ, และการฝึกอบรม"},
    {"name": "งวด 1 (ตรวจรับแล้ว)", "color": "#10B981", "description": "งานในงวดที่ 1 ที่ผ่านการตรวจรับแล้ว"},
    {"name": "งวด 2 (24 พ.ย. 69)", "color": "#F59E0B", "description": "งานที่ผูกกับกำหนดส่งมอบงวด 2"},
    {"name": "งวด 5 (25 มี.ค. 70)", "color": "#8B5CF6", "description": "งานส่งมอบงวดสุดท้าย (300 วัน)"},
    {"name": "🚨 Delayed (ตกค้าง)", "color": "#EF4444", "description": "งานที่ล่าช้ากว่ากำหนด"},
    {"name": "⏳ Waiting Dependency", "color": "#EAB308", "description": "งานที่ต้องรองานอื่นหรือรอลูกค้า"},
    {"name": "🛡️ PDPA / PII", "color": "#3B82F6", "description": "งานคัดกรองและปกปิดข้อมูลส่วนบุคคล"},
    {"name": "🏢 รอสิทธิ์ลูกค้า (Customer Blocker)", "color": "#EC4899", "description": "ติดปัญหาการขอสิทธิ์/เปิดเน็ตจากลูกค้า"}
]

for l in label_defs:
    if l['name'] not in label_map:
        lbl = client.labels.create(workspace_slug=slug, project_id=project_id, data=CreateLabel(name=l['name'], color=l['color']))
        label_map[l['name']] = lbl.id
        print(f"Created label: {l['name']}")
    else:
        print(f"Label exists: {l['name']}")

# ==========================================
# 3. CREATE MODULES (8 MODULES)
# ==========================================
print("\n--- 3. Setting up 8 Modules ---")
r_mods = requests.get(f"https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/modules/", headers=headers)
existing_mods = {m['name']: m['id'] for m in to_list(r_mods.json())}
module_map = dict(existing_mods)

module_defs = [
    {
        "name": "Module H: Handoff & Immediate Action Items (งานติดตามเร่งด่วน พ.ย. 2569)",
        "description": "Action Items เร่งด่วนจากการประชุม 26 ต.ค. 2569 ในช่วงส่งมอบงานให้คุณโบสรับช่วงต่อ (แก้ API ล่ม, ตรวจสอบ 15 กลุ่ม, Prototype feedback)",
        "status": "in-progress"
    },
    {
        "name": "Module A: เอกสารเก่า 48,000 หน้า (Data Cleansing & 15 Categories)",
        "description": "ทบทวนไฟล์ OCR/Metadata เดิม, จับคู่ PDF/JSON, พัฒนาระบบ Classification และจัดกลุ่มเอกสาร 15 กลุ่มตามลำดับศักดิ์กฎหมาย",
        "status": "in-progress"
    },
    {
        "name": "Module B: เอกสารใหม่ 50,000 หน้า (Pipeline ETL, OCR & PDPA/PII)",
        "description": "Pipeline นำเข้า PDF, OCR ภาษาไทย/อังกฤษ/ตัวเลข, PDPA/PII Redaction, ปรับปรุงคำผิด และติดตามส่งมอบ 3 งวด",
        "status": "in-progress"
    },
    {
        "name": "Module C: System & Data Architecture / Integration",
        "description": "สถาปัตยกรรมระบบ, Data Model, Data Pipeline (11 ขั้นตอน), DB Schema, และการจัดเก็บ Vector/Metadata",
        "status": "in-progress"
    },
    {
        "name": "Module D: GenAI Agent, RAG & Webchat API Integration (Samart)",
        "description": "พัฒนาระบบตอบคำถามอัจฉริยะ (RAG), การให้เหตุผลตามลำดับศักดิ์กฎหมาย, Citation Links, และเชื่อมต่อ API กับ Webchat ของสามารถ",
        "status": "in-progress"
    },
    {
        "name": "Module E: ติดตั้งระบบ On-premise ณ เครื่องลูกค้า (กรมที่ดิน)",
        "description": "ติดตั้งซอฟต์แวร์ 6-7 ตัวบนเครื่องกรมที่ดิน, แก้ปัญหา Offline Environment, ขอ VPN / Remote Access และ Internet ชั่วคราว",
        "status": "in-progress"
    },
    {
        "name": "Module F: TOR Compliance & System Features (4.1 - 4.5)",
        "description": "การปฏิบัติตาม TOR: Audit Log, Knowledge Graph, การทดสอบความถูกต้อง, Model Re-training, และระบบประเมิน Feedback",
        "status": "planned"
    },
    {
        "name": "Module G: งวดงานและการส่งมอบ (งวดที่ 2, งวดที่ 5, คู่มือ, อบรม, Pen Test)",
        "description": "การส่งมอบงานตามสัญญา: งวดที่ 2 (Prototype), งวดที่ 5 (ระบบสมบูรณ์ 25 มี.ค. 2570), คู่มือผู้ใช้, Pen Test และจัดอบรม",
        "status": "planned"
    }
]

for m in module_defs:
    if m['name'] not in module_map:
        mod = client.modules.create(workspace_slug=slug, project_id=project_id, data=CreateModule(name=m['name'], description=m['description'], status=m['status']))
        module_map[m['name']] = mod.id
        print(f"Created module: {m['name']} -> {mod.id}")
    else:
        print(f"Module exists: {m['name']}")

# ==========================================
# 4. CREATE CYCLES (2 CYCLES)
# ==========================================
print("\n--- 4. Setting up 2 Cycles ---")
r_cyc = requests.get(f"https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/cycles/", headers=headers)
existing_cycles = {c['name']: c['id'] for c in to_list(r_cyc.json())}
cycle_map = dict(existing_cycles)

cycle_defs = [
    {
        "key": "NOV_2026",
        "name": "Cycle พ.ย. 2569: ติดตามงานส่งมอบเอกสาร 5 หมื่นหน้า & ทดสอบระบบ (โบส รับช่วงต่อ)",
        "description": "โฟกัสการรับมอบเอกสาร 50,000 หน้า 3 งวด (2, 16, 27 พ.ย.), การทดสอบระบบ 1-2 พ.ย., แก้ไข API Upload, อบรม 6 พ.ย., และเตรียมความพร้อมข้อมูล Intelligent",
        "start_date": "2026-11-01",
        "end_date": "2026-11-30"
    },
    {
        "key": "DEC26_MAR27",
        "name": "Cycle ธ.ค. 2569 - มี.ค. 2570: พัฒนาและเชื่อมต่อ API Production สู่การส่งมอบงวด 5",
        "description": "เชื่อมต่อ Webchat ร่วมกับ บมจ. สามารถ, ปรับจูน GenAI Agent, จัดทำคู่มือ, Pen Test และส่งมอบงวด 5 (25 มี.ค. 2570)",
        "start_date": "2026-12-01",
        "end_date": "2027-03-25"
    }
]

cycle_key_to_id = {}
for c in cycle_defs:
    if c['name'] not in cycle_map:
        cyc = client.cycles.create(
            workspace_slug=slug,
            project_id=project_id,
            data=CreateCycle(
                name=c['name'],
                description=c['description'],
                start_date=c['start_date'],
                end_date=c['end_date'],
                owned_by=user_id,
                project_id=project_id
            )
        )
        cycle_map[c['name']] = cyc.id
        cycle_key_to_id[c['key']] = cyc.id
        print(f"Created cycle: {c['name']} -> {cyc.id}")
    else:
        cycle_key_to_id[c['key']] = cycle_map[c['name']]
        print(f"Cycle exists: {c['name']}")

# ==========================================
# 5. CREATE VIEWS (4 VIEWS)
# ==========================================
print("\n--- 5. Setting up Views ---")
r_views = requests.get(f"https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/views/", headers=headers)
existing_views = {v['name']: v['id'] for v in to_list(r_views.json())}

view_defs = [
    {"name": "All Work (มุมมองงานทั้งหมด)", "description": "ตารางสรุปงานทั้งหมด 75 รายการ"},
    {"name": "By Module Board (มุมมองแยกตามหมวดงาน)", "description": "บอร์ดแสดงความคืบหน้าแยกตาม 8 Modules"},
    {"name": "Delayed & Urgent Focus (งานเร่งด่วนและตกค้าง)", "description": "มุมมองกรองเฉพาะงาน Urgent และ Delayed"},
    {"name": "Cycle พ.ย. 69 Board (โฟกัสสปริ้นท์ปัจจุบัน)", "description": "งานที่ต้องโฟกัสในเดือนพฤศจิกายน 2569"}
]

for v in view_defs:
    if v['name'] not in existing_views:
        r = requests.post(f"https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/views/", headers=headers, json={"name": v['name'], "description": v['description'], "query": {}})
        if r.status_code in (200, 201):
            print(f"Created View: {v['name']}")
        else:
            print(f"Error View {v['name']}: {r.status_code}")
    else:
        print(f"View exists: {v['name']}")

# ==========================================
# 6. LOAD AND COMPILE ALL 75 WORK ITEMS
# ==========================================
print("\n--- 6. Loading Task Data ---")
with open(r'C:\Users\Boat\.gemini\antigravity\brain\23a894ef-23ab-488f-bf02-43643b8012a4\scratch\all_tasks_compiled.json', 'r', encoding='utf-8') as f:
    compiled_tasks = json.load(f)

# Load supplementary subtasks
supplementary_subtasks = [
    {
        "code": "E1.1",
        "parent_code": "E1",
        "name": "[E1.1] ติดตั้งและกำหนดค่า Beszel (GPU & System Monitoring Hub/Agent)",
        "description_html": "<h3>📌 วัตถุประสงค์และขอบเขตงาน (อ้างอิง: คู่มือติดตั้ง Beszel)</h3><p>ติดตั้ง Beszel Hub และ Agent บนเซิร์ฟเวอร์ GPU กรมที่ดิน เพื่อเฝ้าระวังสถานะ CPU, Memory, GPU Utilization, VRAM, อุณหภูมิ, Power และ Container Health ตามมาตรฐานการส่งมอบ</p><p><strong>ผู้รับผิดชอบหลัก:</strong> พี่เบิ้ม (DevOps / Softnix)</p><p><strong>ผลลัพธ์ที่ส่งมอบ:</strong> Dashboard มอนิเตอร์เครื่องและระบบแจ้งเตือนข้อผิดพลาด</p>",
        "priority": "high",
        "state_key": "TODO",
        "module_name": "Module E: ติดตั้งระบบ On-premise ณ เครื่องลูกค้า (กรมที่ดิน)",
        "cycle_key": "NOV_2026",
        "labels": ["Softnix", "Infra / On-prem"]
    },
    {
        "code": "D7.1",
        "parent_code": "D7",
        "name": "[D7.1] ตรวจสอบคุณสมบัติ Progressive Web Application (PWA) และช่องคำถาม >= 512 ตัวอักษร",
        "description_html": "<h3>📌 วัตถุประสงค์และขอบเขตงาน (อ้างอิง: SOC ข้อ 26.8 & 26.11)</h3><p>ตรวจสอบและยืนยันว่าระบบสนทนาอัตโนมัติ (Webchat) ที่สามารถพัฒนา มีคุณสมบัติรองรับการแสดงผลบนทุกอุปกรณ์แบบ Progressive Web Application (PWA) และช่องรับคำถามรองรับความยาวได้ไม่น้อยกว่า 512 ตัวอักษรต่อคำถาม</p><p><strong>ผู้รับผิดชอบหลัก:</strong> ทีมพัฒนา Webchat (บมจ. สามารถ) / ตรวจสอบโดย Softnix (โบส)</p>",
        "priority": "medium",
        "state_key": "BACKLOG",
        "module_name": "Module D: GenAI Agent, RAG & Webchat API Integration (Samart)",
        "cycle_key": "DEC26_MAR27",
        "labels": ["สามารถ (Samart)", "TOR Compliance", "API / Integration"]
    },
    {
        "code": "F6.1",
        "parent_code": "F6",
        "name": "[F6.1] พัฒนาระบบติดตามโควต้าการใช้งานตาม SOC 26.13 (Queries, Pages, Tokens)",
        "description_html": "<h3>📌 วัตถุประสงค์และขอบเขตงาน (อ้างอิง: SOC ข้อ 26.13)</h3><p>พัฒนาระบบคำนวณและแสดงผลสถิติการใช้งานให้พิสูจน์ได้ว่ารองรับตามข้อกำหนดสัญญา:</p><ul><li>ไม่น้อยกว่า 6,000 Queries ต่อเดือน</li><li>ไม่น้อยกว่า 7,500 Pages ต่อเดือน</li><li>ไม่น้อยกว่า 1,000,000 Tokens ต่อเดือน</li></ul><p><strong>ผู้รับผิดชอบหลัก:</strong> Softnix (โบส / ผู้ดูแล API)</p>",
        "priority": "high",
        "state_key": "BACKLOG",
        "module_name": "Module F: TOR Compliance & System Features (4.1 - 4.5)",
        "cycle_key": "DEC26_MAR27",
        "labels": ["Softnix", "TOR Compliance"]
    },
    {
        "code": "G2.1",
        "parent_code": "G2",
        "name": "[G2.1] หลักสูตรอบรมผู้ดูแลระบบ (Admin Training - 0.5 วัน: สถาปัตยกรรม, Model Tuning, Beszel)",
        "description_html": "<h3>📌 วัตถุประสงค์และขอบเขตงาน (อ้างอิง: หัวข้ออบรม admin.docx)</h3><p>จัดอบรม 0.5 วัน สำหรับผู้ดูแลระบบกรมที่ดิน ครอบคลุม: สถาปัตยกรรม Softnix Gen AI / MAX Chatbot, การจัดการคลังความรู้ (Knowledge Base), การปรับแต่ง Model, และการดูแลรักษาระบบด้วย Beszel</p><p><strong>ผู้รับผิดชอบหลัก:</strong> สามารถ (ผู้จัด) / Softnix (คุณดอม, โบส, พี่เบิ้ม เป็นวิทยากรร่วม)</p>",
        "priority": "high",
        "state_key": "BACKLOG",
        "module_name": "Module G: งวดงานและการส่งมอบ (งวดที่ 2, งวดที่ 5, คู่มือ, อบรม, Pen Test)",
        "cycle_key": "DEC26_MAR27",
        "labels": ["Joint / ร่วมกัน", "Documentation / Training"]
    },
    {
        "code": "G2.2",
        "parent_code": "G2",
        "name": "[G2.2] หลักสูตรอบรมผู้ใช้งานทั่วไป (User Training - 0.5 วัน: การถามตอบ, กฎหมายรังวัด, ตรวจสอบ Citation)",
        "description_html": "<h3>📌 วัตถุประสงค์และขอบเขตงาน (อ้างอิง: หัวข้ออบรม user.docx)</h3><p>จัดอบรม 0.5 วัน สำหรับช่างรังวัดและเจ้าหน้าที่กรมที่ดิน ครอบคลุม: วิธีการใช้งาน Chatbot, การสืบค้นระเบียบ/ข้อกฎหมายรังวัด, และการตรวจสอบความถูกต้องของแหล่งอ้างอิง (Citation)</p><p><strong>ผู้รับผิดชอบหลัก:</strong> สามารถ (ผู้จัด) / Softnix (ทีมอบรม สนับสนุน)</p>",
        "priority": "high",
        "state_key": "BACKLOG",
        "module_name": "Module G: งวดงานและการส่งมอบ (งวดที่ 2, งวดที่ 5, คู่มือ, อบรม, Pen Test)",
        "cycle_key": "DEC26_MAR27",
        "labels": ["Joint / ร่วมกัน", "Documentation / Training"]
    }
]

# Build unified task list
all_tasks = []
for t in compiled_tasks:
    # Build rich HTML description
    desc = f"<p><b>งาน:</b> {t.get('raw_task', '')}</p>"
    if t.get('status_text'):
        desc += f"<p><b>สถานะปัจจุบัน:</b> {t.get('status_text')}</p>"
    if t.get('meeting_evidence'):
        desc += f"<p><b>บันทึกการประชุม/ความคืบหน้า:</b> {t.get('meeting_evidence')}</p>"
    if t.get('remaining_work'):
        desc += f"<p><b>งานที่ต้องดำเนินการต่อ:</b> {t.get('remaining_work')}</p>"
    desc += f"<p><b>ผู้รับผิดชอบ:</b> {t.get('assignee', 'Softnix')}</p>"
    
    # Determine labels
    t_labels = []
    assignee = t.get('assignee', '')
    if 'Softnix' in assignee or 'พี่' in assignee or 'โบส' in assignee or 'อาร์ม' in assignee or 'เบล' in assignee or 'ดอม' in assignee or 'บิ๊ง' in assignee:
        t_labels.append('Softnix')
    if 'สามารถ' in assignee:
        t_labels.append('สามารถ (Samart)')
    if 'Joint' in assignee or 'ร่วมกัน' in assignee:
        t_labels.append('Joint / ร่วมกัน')
    if 'กรม' in assignee or 'ลูกค้า' in assignee:
        t_labels.append('กรมที่ดิน (DOL)')
    if t.get('priority') == 'urgent':
        t_labels.append('Urgent / Blocker')
    if 'โบส' in t.get('name', '') or 'โบส' in assignee or t.get('code', '').startswith('H'):
        t_labels.append('Handoff / โบส')
    
    # Milestone/Phase tag
    if t.get('code') in ('A1', 'A2', 'A3', 'G1'):
        t_labels.append('งวด 1 (ตรวจรับแล้ว)')
    elif t.get('target_date', '') <= '2026-11-24' and t.get('code') not in ('A1', 'A2', 'A3', 'G1'):
        t_labels.append('งวด 2 (24 พ.ย. 69)')
    else:
        t_labels.append('งวด 5 (25 มี.ค. 70)')
        
    if t.get('code') in ('A4', 'B1'):
        t_labels.append('🚨 Delayed (ตกค้าง)')
        
    all_tasks.append({
        "code": t['code'],
        "name": t['name'],
        "parent_code": 'D3' if t['code'] == 'D3.1' else ('G3' if t['code'] == 'G3.1' else None),
        "description_html": desc,
        "priority": t.get('priority', 'medium'),
        "state_key": t.get('state_key', 'TODO'),
        "module_name": t.get('module_name'),
        "cycle_key": t.get('cycle_key', 'NOV_2026'),
        "start_date": t.get('start_date'),
        "target_date": t.get('target_date'),
        "labels": t_labels
    })

# Append supplementary subtasks
for st in supplementary_subtasks:
    all_tasks.append({
        "code": st['code'],
        "name": st['name'],
        "parent_code": st['parent_code'],
        "description_html": st['description_html'],
        "priority": st['priority'],
        "state_key": st['state_key'],
        "module_name": st['module_name'],
        "cycle_key": st['cycle_key'],
        "start_date": None,
        "target_date": None,
        "labels": st['labels']
    })

print(f"Total unified work items to create: {len(all_tasks)}")

# ==========================================
# 7. CREATE WORK ITEMS (PARENTS FIRST, THEN CHILDREN)
# ==========================================
print("\n--- 7. Creating Work Items in Plane ---")

# Separate parents (parent_code is None) vs children
parents = [t for t in all_tasks if not t.get('parent_code')]
children = [t for t in all_tasks if t.get('parent_code')]

code_to_id = {}
code_to_seq = {}
module_issue_bundles = {m_id: [] for m_id in module_map.values()}
cycle_issue_bundles = {c_id: [] for c_id in cycle_map.values()}

def create_task_item(item, parent_id=None):
    c_key = item.get('cycle_key', 'NOV_2026')
    cyc_id = cycle_key_to_id.get(c_key)
    mod_id = module_map.get(item.get('module_name'))
    st_id = state_key_map.get(item.get('state_key'), STATE_TODO)
    
    # Resolve label UUIDs
    l_ids = [label_map[l] for l in item.get('labels', []) if l in label_map]
    
    payload = {
        "name": item['name'],
        "description_html": item['description_html'],
        "priority": item.get('priority', 'medium'),
        "state": st_id,
        "labels": l_ids,
        "assignees": [user_id]
    }
    if item.get('start_date'):
        payload['start_date'] = item['start_date']
    if item.get('target_date'):
        payload['target_date'] = item['target_date']
    if parent_id:
        payload['parent'] = parent_id
        
    r = requests.post(f"https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/issues/", headers=headers, json=payload)
    if r.status_code in (200, 201):
        res = r.json()
        iid = res['id']
        seq = res.get('sequence_id')
        code_to_id[item['code']] = iid
        code_to_seq[item['code']] = f"DOL-{seq}"
        print(f"Created [{item['code']}] -> {code_to_seq[item['code']]} (UUID: {iid})")
        
        if mod_id:
            module_issue_bundles[mod_id].append(iid)
        if cyc_id:
            cycle_issue_bundles[cyc_id].append(iid)
        return iid
    else:
        print(f"Error creating [{item['code']}]: {r.status_code} {r.text[:150]}")
        return None

# 7.1 Create Parents
print("\nCreating Parent items...")
for p in parents:
    create_task_item(p)
    time.sleep(0.15)

# 7.2 Create Children
print("\nCreating Child items...")
for c in children:
    p_id = code_to_id.get(c['parent_code'])
    create_task_item(c, parent_id=p_id)
    time.sleep(0.15)

# ==========================================
# 8. ATTACH WORK ITEMS TO MODULES AND CYCLES
# ==========================================
print("\n--- 8. Attaching Work Items to Modules & Cycles ---")
for m_id, iids in module_issue_bundles.items():
    if iids:
        r = requests.post(f"https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/modules/{m_id}/module-issues/", headers=headers, json={"issues": iids})
        print(f"Attached {len(iids)} issues to Module {m_id}: {r.status_code}")

for c_id, iids in cycle_issue_bundles.items():
    if iids:
        r = requests.post(f"https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/cycles/{c_id}/cycle-issues/", headers=headers, json={"issues": iids})
        print(f"Attached {len(iids)} issues to Cycle {c_id}: {r.status_code}")

# ==========================================
# 9. WIRE BLOCKING RELATIONS
# ==========================================
print("\n--- 9. Setting up Blocking Dependencies ---")
edges = [
    # Workstream A
    ('A2', 'A4'), ('A1', 'A4'), ('A4', 'A5'), ('H2', 'A5'), ('H11', 'A5'), ('A5', 'A6'), ('A6', 'A7'),
    # Workstream B & C
    ('B2', 'B3'), ('B3', 'B4'), ('B8', 'B4'), ('H1', 'B8'), ('H1', 'B1'),
    ('B4', 'B5'), ('B4', 'B9'), ('B5', 'B6'), ('B6', 'C3'), ('C3', 'C4'),
    ('C4', 'C5'), ('H3', 'C5'), ('C5', 'D1'), ('C5', 'C6'), ('B7', 'C1'),
    # Workstream D
    ('D1', 'D2'), ('D2', 'D3'), ('D3', 'D3.1'), ('D3', 'D4'),
    ('D4', 'D5.1'), ('D4', 'D5.2'), ('D4', 'D7'), ('D7', 'D7.1'),
    ('D5.1', 'D5.4'), ('D5.2', 'D5.5'),
    ('D6', 'D9'), ('D7', 'D8'),
    # Workstream E
    ('H9', 'E1'), ('E1', 'E1.1'), ('E1', 'E3'), ('E2', 'E3'), ('E3', 'E4'), ('E4', 'G4'),
    # Workstream F & G
    ('A7', 'G4'), ('F6', 'F6.1'), ('G2', 'G2.1'), ('G2', 'G2.2'), ('G3', 'G3.1'),
    # Workstream H
    ('H4', 'H5'),
]

rel_count = 0
for up_code, down_code in edges:
    up_id = code_to_id.get(up_code)
    down_id = code_to_id.get(down_code)
    if up_id and down_id:
        url = f"https://api.plane.so/api/v1/workspaces/{slug}/projects/{project_id}/work-items/{down_id}/relations/"
        r = requests.post(url, headers=headers, json={'relation_type': 'blocked_by', 'issues': [up_id]})
        if r.status_code in (200, 201):
            print(f"Linked relation: [{down_code}] blocked_by [{up_code}]")
            rel_count += 1
        elif r.status_code == 400 and 'already' in r.text.lower():
            rel_count += 1
        else:
            print(f"Relation notice [{down_code}] <- [{up_code}]: {r.status_code}")
        time.sleep(0.1)

print(f"\nAll relations processed! Successfully wired {rel_count} dependencies.")

# Save mapping to file
with open('dol_materialized_mapping.json', 'w', encoding='utf-8') as f:
    json.dump({
        'project_id': project_id,
        'code_to_id': code_to_id,
        'code_to_seq': code_to_seq,
        'module_map': module_map,
        'cycle_map': cycle_map,
        'label_map': label_map
    }, f, ensure_ascii=False, indent=2)

print("\n==========================================")
print("PROJECT 'กรมที่ดิน' (DOL) MATERIALIZED SUCCESSFULLY!")
print(f"Total Work Items Created: {len(code_to_id)}")
print(f"Total Modules: {len(module_map)}")
print(f"Total Cycles: {len(cycle_map)}")
print(f"Total Labels: {len(label_map)}")
print(f"Total Relations: {rel_count}")
print("==========================================")
