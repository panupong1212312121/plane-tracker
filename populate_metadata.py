import os
import requests
import json

api_key = 'plane_api_753422726aad47afb951dc6cd3a7ceb4'
slug = 'panupong'
os.environ['PLANE_API_KEY'] = api_key
os.environ['PLANE_WORKSPACE_SLUG'] = slug

from plane_mcp.client import get_plane_client_context
from plane.models.modules import CreateModule
from plane.models.labels import CreateLabel

client, workspace_slug = get_plane_client_context()

LAND_PID = '6dbd053c-9789-4056-8c18-f5f15616949c'
POST_PID = 'f0d660d0-9451-4b7a-8c00-5e9626f0712d'

# Check existing labels for LAND
headers = {'x-api-key': api_key}
r = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{LAND_PID}/labels/', headers=headers)
existing_land_labels = {l['name']: l['id'] for l in r.json().get('results', [])}
print('Existing LAND labels:', list(existing_land_labels.keys()))

land_label_defs = [
    ('คำถาม', '#2563EB'),
    ('Bug', '#DC2626'),
    ('สิ่งที่อยากให้ปรับปรุง', '#16A34A'),
    ('งานปฏิบัติการ / แผนงาน', '#7C3AED'),
    ('สกัดข้อมูล/Prompt', '#D97706'),
    ('LightRAG/Engine', '#DB2777'),
    ('Schema/Field', '#4F46E5'),
    ('Export/Data', '#0D9488'),
    ('UI/UX', '#0891B2'),
    ('Training/Onboarding', '#EA580C'),
    ('Verify/QA', '#65A30D')
]
for name, color in land_label_defs:
    if name not in existing_land_labels:
        lbl = client.labels.create(workspace_slug=workspace_slug, project_id=LAND_PID, data=CreateLabel(name=name, color=color))
        existing_land_labels[name] = lbl.id
        print(f"Created label: {name}")

# Check existing labels for POST
r_post = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{POST_PID}/labels/', headers=headers)
existing_post_labels = {l['name']: l['id'] for l in r_post.json().get('results', [])}
print('Existing POST labels:', list(existing_post_labels.keys()))

post_label_defs = [
    ('Bug/Fix', '#DC2626'),
    ('Export/CSV', '#0D9488'),
    ('UI/Display', '#2563EB')
]
for name, color in post_label_defs:
    if name not in existing_post_labels:
        lbl = client.labels.create(workspace_slug=workspace_slug, project_id=POST_PID, data=CreateLabel(name=name, color=color))
        existing_post_labels[name] = lbl.id
        print(f"Created label: {name}")

# Modules for LAND
r_mod = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{LAND_PID}/modules/', headers=headers)
existing_land_modules = {m['name']: m['id'] for m in r_mod.json().get('results', [])}

land_module_defs = [
    ('01. ข้อซักถามและเกณฑ์ระบบ (Q&A)', 'รวบรวมข้อซักถาม ชี้แจงพฤติกรรมการทำงานของ AI และเกณฑ์การประมวลผล'),
    ('02. ข้อผิดพลาดและ Engine (Bug Fixes)', 'ติดตามและแก้ไขปัญหาการประมวลผล, LightRAG Engine, นำเข้าไฟล์ และโควต้า'),
    ('03. การจัดการ Schema & ฟิลด์ (Schema Management)', 'ปรับปรุงระบบจัดการ Schema, ฟิลด์, การแก้ไขย้อนหลัง และการจัดเรียง'),
    ('04. การนำเข้า/ส่งออกข้อมูล (Data Import & Export)', 'ระบบ Drag & Drop อัปโหลด และการ Export ผลลัพธ์ Metadata (JSON/CSV)'),
    ('05. การแสดงผล UI & ประสบการณ์ใช้งาน (UI/UX)', 'ปรับปรุงการ Freeze ส่วนหัว, Floating buttons และการจัดเรียงเมนู'),
    ('06. แผนงานและปฏิบัติการ กรมที่ดิน (Operations & Rollout)', 'งานทดสอบระบบ, ปรับจูน Prompt, อัปเดต Schema, หนังสือเวียน และการจัดอบรม')
]

for name, desc in land_module_defs:
    if name not in existing_land_modules:
        m = client.modules.create(workspace_slug=workspace_slug, project_id=LAND_PID, data=CreateModule(name=name, description=desc))
        existing_land_modules[name] = m.id
        print(f"Created module: {name} -> {m.id}")

print("Modules and labels ready!")
