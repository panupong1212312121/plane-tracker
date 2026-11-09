import os
import requests
import json
import time

api_key = 'plane_api_753422726aad47afb951dc6cd3a7ceb4'
slug = 'panupong'
user_id = '6de5a3e3-a9ad-42a1-bdfa-21c193d628ef' # Panupong Jindarat (Owner)

os.environ['PLANE_API_KEY'] = api_key
os.environ['PLANE_WORKSPACE_SLUG'] = slug

from plane_mcp.client import get_plane_client_context
from plane.models.work_items import CreateWorkItem

client, workspace_slug = get_plane_client_context()

LAND_PID = '6dbd053c-9789-4056-8c18-f5f15616949c'
POST_PID = 'f0d660d0-9451-4b7a-8c00-5e9626f0712d'
PANUP_PID = '6c496f89-d85a-4744-a685-3bc17d4bc4b2'

headers = {'x-api-key': api_key}

# Get existing labels for LAND
r_land_labels = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{LAND_PID}/labels/', headers=headers)
land_labels = {l['name']: l['id'] for l in r_land_labels.json().get('results', [])}

# Get existing modules for LAND
r_land_modules = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{LAND_PID}/modules/', headers=headers)
land_modules = {m['name']: m['id'] for m in r_land_modules.json().get('results', [])}

# Get existing labels for POST
r_post_labels = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{POST_PID}/labels/', headers=headers)
post_labels = {l['name']: l['id'] for l in r_post_labels.json().get('results', [])}

# Get existing labels for PANUP
r_panup_labels = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{PANUP_PID}/labels/', headers=headers)
panup_labels = {l['name']: l['id'] for l in r_panup_labels.json().get('results', [])}

# States
land_states = {
    'backlog': '52e73278-6637-4947-9780-2c552bc2310e',
    'todo': '1fc908f2-a8dc-4a51-b31f-bf205f69e76f',
    'in_progress': 'f86e9bf4-3df1-40fd-a6b2-28c3500a5308',
    'done': '63ca1d81-6b0b-4ee7-aec1-ee2ba267dde5',
    'cancelled': 'bbef30d7-147a-4823-b434-b3fb34796151'
}

post_states = {
    'backlog': '408a6b99-caac-45ad-ad9a-d838b43630c7',
    'todo': 'de672684-ac83-483d-b0d2-d2175057b018',
    'in_progress': 'a4d65b60-bf70-4141-9c9c-2e6c5cc956fb',
    'done': 'bd3be960-e1f0-4a61-b943-aad7b73de777',
    'cancelled': '3ce988a7-cc9f-4c26-b18e-e7abb6b3f707'
}

panup_states = {
    'backlog': 'b6ebca61-4cb6-4662-83c3-7b58d6c4d045',
    'todo': '2688fd27-c35f-4888-bde9-22349161265d',
    'in_progress': '57afe74b-2912-4ba2-b7af-d4a2033ba005',
    'done': 'a4a8cfa7-7d15-499a-b773-7cc3d9b10f21',
    'cancelled': '63fffb94-d719-46f4-8be0-c34688ce02d6'
}

print("Labels and states mapped successfully.")

# LAND DATA DEFINITION
land_groups = [
    {
        "module_name": "01. ข้อซักถามและเกณฑ์ระบบ (Q&A)",
        "parent": {
            "name": "[Q&A] รวบรวมและตอบข้อซักถามการทำงานของระบบ (Knowledge Intelligence Questions)",
            "description_html": "<p>รวบรวมข้อซักถามจากผู้ใช้งานและทีมงานกรมที่ดินเกี่ยวกับกลไกการสกัดข้อมูล, การประมวลผลคำตอบ, ฟิลด์ข้อมูล และการอ้างอิง เพื่อชี้แจงและตรวจสอบความถูกต้องของระบบ</p>",
            "priority": "high",
            "state": land_states["in_progress"],
            "labels": [land_labels['คำถาม'], land_labels['สกัดข้อมูล/Prompt']]
        },
        "sub_items": [
            {
                "no": 1,
                "name": "[Q&A #1] ตรวจสอบ Output รูปแบบ set { ... }, list [ ... ] ที่คั่นด้วย comma",
                "description_html": "<p><b>คำถาม:</b> รูปแบบ Output ที่สกัดได้ รองรับรูปแบบ set { ... }, list [ ... ] ที่คั่นด้วย \",\" เช่น [\"ประมวลกฎหมายที่ดิน\", ...] หรือไม่</p><p><b>เป้าหมาย:</b> ตรวจสอบ Format Output ในระบบและทดสอบกรณีที่ต้องการได้ค่าแบบ Array / List คั่นด้วย Comma</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['คำถาม'], land_labels['สกัดข้อมูล/Prompt']]
            },
            {
                "no": 2,
                "name": "[Q&A #2] ประเภทฟิลด์ text vs textarea และแนวทางเลือกใช้",
                "description_html": "<p><b>คำถาม:</b> ประเภทฟิลด์ text vs textarea ต่างกันอย่างไร และควรเลือกใช้อย่างไร</p><p><b>วิธีแก้ไข / ชี้แจง (Solution):</b> ในโค้ดต่างกัน 2 เรื่อง ช่องกรอกของ textarea เป็นแบบหลายบรรทัด (3 แถว) และเก็บได้ยาวสูงสุด 50,000 ตัวอักษร ส่วน text เป็นบรรทัดเดียวและเก็บได้ 10,000 ตัวอักษร ส่วนการสกัดผิดนั้นเป็นที่ prompt คำสั่ง AI แก้ไขแล้ว ช่วยทดสอบใหม่</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['คำถาม'], land_labels['Schema/Field']]
            },
            {
                "no": 3,
                "name": "[Q&A #3] เกณฑ์การกรองฟิลด์ที่เข้ากลุ่ม \"รอตรวจ\"",
                "description_html": "<p><b>คำถาม:</b> เกณฑ์การกรองฟิลด์ที่เข้ากลุ่ม \"รอตรวจ\" ใช้เกณฑ์อะไรในการคัดกรอง เพราะบางฟิลด์มีข้อมูล บางฟิลด์ไม่มีข้อมูล</p><p><b>วิธีแก้ไข / ชี้แจง (Solution):</b> เมื่อ metadata บาง field ไม่ครบหรือครบแต่ไม่สมบูรณ์รอให้คนตรวจหรืออนุมัติ ผมเพิ่ม feature เอาเม้าไปวางบนข้อความสถานะจะมีคำอธิบายที่ละเอียดขึ้น</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['คำถาม'], land_labels['UI/UX']]
            },
            {
                "no": 4,
                "name": "[Q&A #4] สาเหตุที่คำตอบไม่ค่อยแสดงผลแม้จะเขียน prompt ละเอียด",
                "description_html": "<p><b>คำถาม:</b> ทำไมคำตอบไม่ค่อยแสดงผล แม้จะเขียน prompt อย่างละเอียดแล้ว</p><p><b>วิธีแก้ไข / ชี้แจง (Solution):</b> AI ส่งหลักฐานผิดรูปแบบ เช่น ใส่เครื่องหมายคำพูดครอบ เว้นวรรคต่างไป ตอบมาเป็นข้อความเปล่า ๆ หรือลืมแนบข้อความอ้างอิง ระบบจึงปฏิเสธ ทั้งที่เนื้อหาถูก แก้ไขแล้ว โดย ปรับคำสั่งที่ส่งให้ AI ให้แนบข้อความอ้างอิงเสมอ</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['คำถาม'], land_labels['สกัดข้อมูล/Prompt']]
            },
            {
                "no": 5,
                "name": "[Q&A #5] หลักการค้นหาคำตอบใน .md และการแนบลิงก์อ้างอิงจากหลายแหล่ง",
                "description_html": "<p><b>คำถาม:</b> หลักการค้นหาคำตอบใน md ข้อมูลไฟล์ที่เกี่ยวข้องจะแนบลิงก์มาใช่หรือไม่ และถ้าคำตอบจาก ai ที่ได้มีการดึงจากเอกสาร 2 แหล่งขึ้นไป จะแนบมา 2 ลิงก์ใช่หรือไม่</p><p><b>วิธีแก้ไข / ชี้แจง (Solution):</b> ใช่ ระบบจะแนบลิงก์ข้อมูลไฟล์ต้นทางตามจำนวนแหล่งที่ดึงข้อมูลมา</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['คำถาม'], land_labels['Verify/QA']]
            },
            {
                "no": 6,
                "name": "[Q&A #6] ความแตกต่างระหว่าง \"สกัดข้อมูลกฎหมาย\" กับ \"เติมข้อมูลที่ขาดอัตโนมัติ\"",
                "description_html": "<p><b>คำถาม:</b> ปุ่ม \"สกัดข้อมูลกฎหมาย\" กับ \"เติมข้อมูลที่ขาดอัตโนมัติ\" ต่างกันอย่างไร และเหตุใดกดแล้วบางฟิลด์ที่มีข้อมูลอยู่เดิมจึงหายไป</p><p><b>วิธีแก้ไข / ชี้แจง (Solution):</b> มี Bug สกัดไม่สมบูรณ์ถูกเขียนทับ แก้ไขแล้ว โดย สกัดข้อมูลกฎหมาย - gen metadata สำหรับเมนู \"กฎหมาย\"</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['คำถาม'], land_labels['สกัดข้อมูล/Prompt'], land_labels['Bug']]
            },
            {
                "no": 7,
                "name": "[Q&A #7] ตรวจสอบการจำกัดความยาว Character ของคำตอบและเหตุผลที่ตอบสั้น",
                "description_html": "<p><b>คำถาม:</b> จำนวนคำตอบมีการกำหนดความยาว character หรือไม่ เหตุใดฟิลด์ที่ควรยาวจึงตอบค่อนข้างสั้น ซึ่งเข้าใจว่าจะอ้างอิงจากในจำนวนเนื้อหาพบเจอ เช่น field เหตุผลในการประกาศใช้ จากระบบตอบว่า เพื่อปรับปรุงกฎหมายว่าด้วยระเบียบข้าราชการพลเรือน</p><p><b>เป้าหมาย:</b> ตรวจสอบ logic การจำกัดความยาว และปรับปรุง prompt คำสั่งสกัดให้แสดงเนื้อหาบริบทครบถ้วน</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['คำถาม'], land_labels['สกัดข้อมูล/Prompt']]
            },
            {
                "no": 8,
                "name": "[Q&A #8] กลไกการเลือกเนื้อหาหลังบ้านและการค้นหาข้อมูลที่อยู่หน้าสุดท้าย",
                "description_html": "<p><b>คำถาม:</b> หลักการเลือกเนื้อหาหลังบ้านเป็นแบบใด กำหนดจาก prompt หรือไม่ หากเนื้อหาจริงอยู่หน้าสุดท้าย</p><p><b>เป้าหมาย:</b> อธิบายกลไก Retrieval Chunking / RAG ของระบบ และการตั้งค่า prompt ให้ครอบคลุมเนื้อหาทั้งฉบับ</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['คำถาม'], land_labels['LightRAG/Engine']]
            },
            {
                "no": 9,
                "name": "[Q&A #9] ตรวจสอบ Checkbox \"ต้องมีข้อมูลหลังอ่านเอกสาร\" แต่คำตอบไม่ออก",
                "description_html": "<p><b>คำถาม:</b> ทำไมกดปุ่ม checkbox \"ต้องมีข้อมูลหลังอ่านเอกสาร\" แล้ว แต่บางฟิลด์คำตอบก็ยังไม่ออก</p><p><b>เป้าหมาย:</b> ตรวจสอบ condition validation หลังบ้าน และกรณีที่เอกสารไม่มีเนื้อหาสอดคล้องจริง</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['คำถาม'], land_labels['สกัดข้อมูล/Prompt']]
            },
            {
                "no": 14,
                "name": "[Q&A #14] ชี้แจงความแตกต่างของประเภทเอกสารมาตรฐาน (General, Legal, Regulation, Contract)",
                "description_html": "<p><b>คำถาม:</b> ประเภทเอกสารมาตรฐานแต่ละอันแตกต่างกันยังไง (General, Legal, Regulation, Contract)</p><p><b>เป้าหมาย:</b> จัดทำเอกสารคำอธิบายประเภทเอกสารมาตรฐาน พร้อมแนวทางการเลือกใช้สำหรับผู้ใช้งานกรมที่ดิน</p>",
                "priority": "medium",
                "state": land_states["todo"],
                "labels": [land_labels['คำถาม']]
            }
        ]
    },
    {
        "module_name": "02. ข้อผิดพลาดและ Engine (Bug Fixes)",
        "parent": {
            "name": "[Bug Fixes] แก้ไขและติดตามข้อผิดพลาดของระบบ & Engine (System & Engine Bugs)",
            "description_html": "<p>จัดการและติดตามการแก้ไขข้อผิดพลาดในการประมวลผล, LightRAG Engine, ข้อผิดพลาดตอนนำเข้าไฟล์ และปัญหาโควต้า API</p>",
            "priority": "urgent",
            "state": land_states["in_progress"],
            "labels": [land_labels['Bug'], land_labels['LightRAG/Engine']]
        },
        "sub_items": [
            {
                "no": 11,
                "name": "[Bug #11] เลือกประเภทฟิลด์หลายตัวเลือก (Array) แล้ว Error \"Request faild\"",
                "description_html": "<p><b>อาการ:</b> พอเลือกประเภทฟิลด์ = หลายตัวเลือก(Array) ได้ error \"Request faild\"</p><p><b>วิธีแก้ไข (Solution):</b> ไม่ได้ระบุค่าในช่องตัวเลือก ตอนนี้ทำ validate ค่าแล้ว พร้อมคำอธิบาย</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['Bug'], land_labels['Schema/Field']]
            },
            {
                "no": 12,
                "name": "[Bug #12] Error RETRIEVAL_ENGINE_UNAVAILABLE (LightRAG ล่ม)",
                "description_html": "<p><b>อาการ:</b> meta data, กฎหมาย ไม่ออก และมีขึ้น error \"RETRIEVAL_ENGINE_UNAVAILABLE\"</p><p><b>วิธีแก้ไข (Solution):</b> ปัญหา service LightRAG ล่ม มันจะ retry ใหม่เอง</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['Bug'], land_labels['LightRAG/Engine']]
            },
            {
                "no": 13,
                "name": "[Bug #13] Error RETRIEVAL_ENGINE_REJECTED (เอกสารซ้ำใน Queue)",
                "description_html": "<p><b>อาการ:</b> meta data, กฎหมาย ไม่ออก และมีขึ้น error \"RETRIEVAL_ENGINE_REJECTED\"</p><p><b>วิธีแก้ไข (Solution):</b> มีเอกสารซ้ำใน queue ของ LightRAG ผมทำการล้างและให้แสดง Error ให้ตรงกับปัญหา</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['Bug'], land_labels['LightRAG/Engine']]
            },
            {
                "no": 15,
                "name": "[Bug #15] กรณี Knowledge มี 1 ไฟล์ ไม่สามารถกดลบเอกสารได้",
                "description_html": "<p><b>อาการ:</b> กรณี knowledge มี 1 ไฟล์ ไม่สามารถกดลบเอกสารได้</p><p><b>วิธีแก้ไข (Solution):</b> ทดสอบลบสามารถลบได้ เลยไม่ได้แก้ใดๆ</p>",
                "priority": "medium",
                "state": land_states["done"],
                "labels": [land_labels['Bug']]
            },
            {
                "no": 16,
                "name": "[Bug #16] ปัญหาระบบ Error เมื่อนำเข้าไฟล์จำนวนมากพร้อมกัน (10+ ไฟล์)",
                "description_html": "<p><b>อาการ:</b> เกิดตอนนำเข้าไฟล์เยอะ ๆ เช่น ครั้งละ 10+ (พบวันที่ 08/10/2026)</p><p><b>เป้าหมาย:</b> ตรวจสอบ Batch Import Pipeline, Background Queue และเพิ่มการควบคุม Concurrency</p>",
                "priority": "medium",
                "state": land_states["todo"],
                "labels": [land_labels['Bug'], land_labels['Export/Data']]
            },
            {
                "no": 17,
                "name": "[Bug #17] นำเข้าไฟล์ .md ซ้ำแล้วติด error RETRIEVAL_ENGINE_BUSY",
                "description_html": "<p><b>อาการ:</b> เกิดตอนนำเข้าไฟล์ .md ผ่าน knowledge intelligence (ทั้งกรณีเยอะ, น้อย) เป็นบางไฟล์ ซึ่งมีบางไฟล์เกิดขึ้นซ้ำ ๆ คือ เอาไฟล์ชื่อ \"A\" เข้าไปครั้งที่ 1,2,3, ... เกิด error \"ดัชนีค้นหากำลังทำงานหนัก รอสักครู่แล้วกดประมวลผลอีกครั้ง The retrieval engine is busy. RETRIEVAL_ENGINE_BUSY\" นี้ทุกครั้ง (พบวันที่ 09/10/2026)</p><p><b>เป้าหมาย:</b> แก้ไขการ lock / unlock index ของ LightRAG เมื่อไฟล์ประมวลผลไม่สมบูรณ์</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['Bug'], land_labels['LightRAG/Engine']]
            },
            {
                "no": 18,
                "name": "[Bug #18] ข้อผิดพลาดเนื่องจากงบประมาณ/เครดิต API หมด (ตังค์หมด)",
                "description_html": "<p><b>อาการ:</b> ตังค์หมด ระบบหยุดทำงาน</p><p><b>วิธีแก้ไข (Solution):</b> เติมเครดิต และปรับปรุงการ Monitor การใช้งาน</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['Bug']]
            },
            {
                "no": 19,
                "name": "[Bug #19] ปัญหาตังค์หมดตอนนำเข้าไฟล์ตรงและ Sync ผ่าน Knowledge Center",
                "description_html": "<p><b>อาการ:</b> ตังค์หมด ทั้งตอน 1.เพิ่มเอกสาร นำเข้าตรง ๆ ใน knowledge intelligence 2.sync ผ่าน knowledge center เข้ามาที่ knowledge intelligence แล้วรอให้มันรัน สุดท้ายมันจะขึ้นตามรูป</p><p><b>วิธีแก้ไข (Solution):</b> จัดการเครดิตและตรวจสอบขั้นตอนการ Sync เรียบร้อย</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['Bug']]
            }
        ]
    },
    {
        "module_name": "03. การจัดการ Schema & ฟิลด์ (Schema Management)",
        "parent": {
            "name": "[Enhancement] ปรับปรุงการจัดการ Schema & Metadata Fields",
            "description_html": "<p>การเพิ่มขีดความสามารถในการจัดการ Schema, การแก้ไขย้อนหลัง, การคัดลอก (Copy) และการจัดลำดับฟิลด์</p>",
            "priority": "medium",
            "state": land_states["in_progress"],
            "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['Schema/Field']]
        },
        "sub_items": [
            {
                "no": 10,
                "name": "[Feature #10] ปุ่ม/ตัวเลือกให้แก้ไข Metadata Schema ย้อนหลังได้",
                "description_html": "<p><b>รายละเอียด:</b> กรณีต้องการเปลี่ยนแปลง meta data schema สามารถมีปุ่มหรือตัวเลือกให้ user สามารถกดเปลี่ยนแปลงได้ทีหลัง</p><p><b>เป้าหมาย:</b> รองรับ Schema Migration / Update Schema สำหรับชุดเอกสารที่มีอยู่เดิม</p>",
                "priority": "medium",
                "state": land_states["todo"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['Schema/Field']]
            },
            {
                "no": 21,
                "name": "[Feature #21] คัดลอก (Copy) รายละเอียดในฟิลด์ภายใน Knowledge Group เดียวกัน",
                "description_html": "<p><b>รายละเอียด:</b> รองรับการคัดลอก (Copy) รายละเอียดในฟิลด์ที่สร้างใน knowledge group เดียวกันลงมาข้างล่าง</p><p><b>วิธีแก้ไข (Solution):</b> พัฒนาระบบรองรับการคัดลอกรายละเอียดฟิลด์เรียบร้อยแล้ว</p>",
                "priority": "medium",
                "state": land_states["done"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['Schema/Field']]
            },
            {
                "no": 22,
                "name": "[Feature #22] เลื่อนหรือสลับตำแหน่งฟิลด์ไปมาเพื่อจัดเรียงลำดับ",
                "description_html": "<p><b>รายละเอียด:</b> สามารถเลื่อนหรือสลับตำแหน่งฟิลด์ไปมาระหว่างกันได้เพื่อจัดลำดับ (Reorder Fields via Drag/Buttons)</p>",
                "priority": "medium",
                "state": land_states["backlog"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['Schema/Field'], land_labels['UI/UX']]
            },
            {
                "no": 23,
                "name": "[Feature #23] สำเนา (Copy) Schema Metadata ข้าม Knowledge Group อื่น",
                "description_html": "<p><b>รายละเอียด:</b> สามารถทำสำเนา (Copy) schema metadata ข้าม knowledge group อื่นได้ เพื่อลดเวลาตั้งค่าใหม่</p>",
                "priority": "medium",
                "state": land_states["backlog"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['Schema/Field']]
            },
            {
                "no": 24,
                "name": "[Feature #24] ปุ่ม Multi-select เลือกได้หลายอันและลบทั้งหมดพร้อมกัน",
                "description_html": "<p><b>รายละเอียด:</b> ปุ่มเลือกได้หลายอัน แล้วลบที่เลือกทั้งหมดทุกส่วนที่จำเป็น (Batch Delete)</p>",
                "priority": "medium",
                "state": land_states["backlog"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['UI/UX']]
            }
        ]
    },
    {
        "module_name": "04. การนำเข้า/ส่งออกข้อมูล (Data Import & Export)",
        "parent": {
            "name": "[Enhancement] ปรับปรุงการ Import & Export ข้อมูล (Data Management)",
            "description_html": "<p>การนำเข้าไฟล์แบบลากวาง (Drag & Drop) และการส่งออกข้อมูล Metadata ในรูปแบบ JSON / CSV ที่เป็นมิตรและกำหนดเองได้</p>",
            "priority": "high",
            "state": land_states["in_progress"],
            "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['Export/Data']]
        },
        "sub_items": [
            {
                "no": 20,
                "name": "[Feature #20] รองรับการ Drag & Drop ไฟล์จากเครื่อง Local เพื่อเพิ่มเอกสาร",
                "description_html": "<p><b>รายละเอียด:</b> สามารถลากไฟล์จากเครื่อง local computer ไปวางในช่องเพิ่มเอกสารได้ (Drag & Drop File Upload)</p>",
                "priority": "medium",
                "state": land_states["backlog"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['UI/UX'], land_labels['Export/Data']]
            },
            {
                "no": 25,
                "name": "[Feature #25] Export ผลลัพธ์ Metadata ที่สกัดได้เป็นไฟล์ .json และ .csv",
                "description_html": "<p><b>รายละเอียด:</b> รองรับการ export ผลลัพท์ที่อยู่ในรูป meta ที่ได้จากการสกัดมาเป็น .json, .csv เพื่อนำไปใช้ต่อ</p><p><b>วิธีแก้ไข (Solution):</b> พัฒนาระบบส่งออก Metadata ในรูปแบบ JSON และ CSV เรียบร้อยแล้ว</p>",
                "priority": "high",
                "state": land_states["done"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['Export/Data']]
            },
            {
                "no": 26,
                "name": "[Feature #26] ปรับแต่งรูปแบบผลลัพธ์การ Export Metadata (JSON) ให้ Friendly",
                "description_html": "<p><b>รายละเอียด:</b> ผลลัพท์ที่ได้จากการกดปุ่ม \"ส่งออก Metadata (JSON)\" รูปแบบไม่ friendly อยากให้ปรับเป็นแบบ friendly ในรูป (Pretty formatted / Key-Value ชัดเจน)</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['Export/Data'], land_labels['UI/UX']]
            },
            {
                "no": 27,
                "name": "[Feature #27] เพิ่มการ Export ในส่วนของ Metadata (JSON) ที่ User ออกแบบเอง",
                "description_html": "<p><b>รายละเอียด:</b> อยากให้เพิ่มการ export ในส่วนของ Metadata (JSON) ของที่เราออกแบบเอง (Custom Schema JSON Export)</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['Export/Data']]
            }
        ]
    },
    {
        "module_name": "05. การแสดงผล UI & ประสบการณ์ใช้งาน (UI/UX)",
        "parent": {
            "name": "[Enhancement] ปรับปรุงการแสดงผล UI & ประสบการณ์ใช้งาน (UI/UX Polish)",
            "description_html": "<p>ปรับปรุงการตรึงส่วนหัวผลลัพธ์ (Freeze header), Floating action button และการเรียงลำดับเมนู</p>",
            "priority": "low",
            "state": land_states["backlog"],
            "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['UI/UX']]
        },
        "sub_items": [
            {
                "no": 28,
                "name": "[UI #28] เพิ่ม Floating button ทำหน้าที่ scroll-to-top / scroll-to-down",
                "description_html": "<p><b>รายละเอียด:</b> เพิ่ม floating button ที่ทำหน้าที่เป็น scroll-to-top, scroll-to-down ในแถบ \"จัดการประเภทเอกสาร\" เพื่ออำนวยความสะดวกเมื่อเอกสารยาว</p>",
                "priority": "low",
                "state": land_states["backlog"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['UI/UX']]
            },
            {
                "no": 29,
                "name": "[UI #29] ตรึงแถว/หน้า Modal ผลลัพธ์จากการวิเคราะห์ Metadata (Freeze Header)",
                "description_html": "<p><b>รายละเอียด:</b> หน้า modal ผลลัพท์ที่ได้จากการวิเคราะห์ Meta data -> เปลี่ยนให้ freeze ตรึงจนถึงเส้นสีแดงแทน เพื่อให้ดูข้อมูลเทียบกับหัวตารางได้ง่าย</p>",
                "priority": "low",
                "state": land_states["backlog"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['UI/UX']]
            },
            {
                "no": 30,
                "name": "[UI #30] จัดเรียงรายการเมนูตาม updated_at ขึ้นมาก่อน",
                "description_html": "<p><b>รายละเอียด:</b> เรียงเมนู ให้เรียงตาม updated_at ขึ้นมาก่อน เพื่อให้เห็นรายการที่มีการเปลี่ยนแปลงล่าสุด</p>",
                "priority": "low",
                "state": land_states["backlog"],
                "labels": [land_labels['สิ่งที่อยากให้ปรับปรุง'], land_labels['UI/UX']]
            }
        ]
    },
    {
        "module_name": "06. แผนงานและปฏิบัติการ กรมที่ดิน (Operations & Rollout)",
        "parent": {
            "name": "[Operations] แผนงานเตรียมการส่งมอบ อบรม และ Rollout กรมที่ดิน",
            "description_html": "<p>งานทดสอบสอบทานระบบ, ปรับจูน Prompt, ปรับปรุง Metadata ล่าสุด, งานหนังสือเวียน และการเตรียมการฝึกอบรม/สอนงาน</p>",
            "priority": "urgent",
            "state": land_states["in_progress"],
            "labels": [land_labels['งานปฏิบัติการ / แผนงาน'], land_labels['Verify/QA']]
        },
        "sub_items": [
            {
                "no": 101,
                "name": "[Ops] ทดสอบสอบทาน Item ที่ Done แล้วในระบบ (QA Verification)",
                "description_html": "<p><b>งานที่ต้องทำ:</b> ตรวจสอบและทดสอบรายการใน Excel ที่ระบุว่า Done แล้วทั้งหมดว่าบน Production ใช้งานได้สมบูรณ์จริงหรือไม่ หากผ่านให้ปิดเคสหรือย้ายไป complaint tracker</p>",
                "priority": "urgent",
                "state": land_states["in_progress"],
                "labels": [land_labels['งานปฏิบัติการ / แผนงาน'], land_labels['Verify/QA']]
            },
            {
                "no": 102,
                "name": "[Ops] ปรับแต่ง Prompt สกัดข้อมูล เน้นตอบคำถามให้ถูกต้องตรงประเด็น",
                "description_html": "<p><b>งานที่ต้องทำ:</b> ตรวจสอบและปรับปรุง Prompt คำสั่ง AI เพื่อให้ผลลัพธ์การสกัดและการตอบคำถามถูกต้องครบถ้วน แม่นยำตามเนื้อหาเอกสารกฎหมาย</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['งานปฏิบัติการ / แผนงาน'], land_labels['สกัดข้อมูล/Prompt']]
            },
            {
                "no": 103,
                "name": "[Ops] ปรับแก้ Metadata Schema ให้ตรงตาม Requirement ล่าสุดของกรมที่ดิน",
                "description_html": "<p><b>งานที่ต้องทำ:</b> ปรับ Metadata Schema และฟิลด์ต่างๆ ให้สอดคล้องกับข้อกำหนดล่าสุดของกรมที่ดิน</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['งานปฏิบัติการ / แผนงาน'], land_labels['Schema/Field']]
            },
            {
                "no": 104,
                "name": "[Ops] เสนอแนวทาง Archify กับพี่ท็อป",
                "description_html": "<p><b>งานที่ต้องทำ:</b> เตรียมข้อมูลและเข้าพบ/พูดคุยเสนอแนวทางการจัดเก็บและจัดการ Archify กับพี่ท็อป</p>",
                "priority": "medium",
                "state": land_states["todo"],
                "labels": [land_labels['งานปฏิบัติการ / แผนงาน']]
            },
            {
                "no": 105,
                "name": "[Ops] ดำเนินการจัดทำข้อมูลส่วน \"หนังสือเวียน\" ที่ยังค้างอยู่",
                "description_html": "<p><b>งานที่ต้องทำ:</b> รวบรวม ตรวจสอบ และนำเข้าสกัดข้อมูลในหมวด \"หนังสือเวียน\" ที่เหลือให้ครบถ้วนสมบูรณ์</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['งานปฏิบัติการ / แผนงาน']]
            },
            {
                "no": 106,
                "name": "[Ops] เตรียมความพร้อม Service และ Environment สำหรับการ Training",
                "description_html": "<p><b>งานที่ต้องทำ:</b> จัดเตรียม Service สำรอง, ตรวจสอบความเสถียร, API Quota และความพร้อมของระบบสำหรับ Session Training ของเจ้าหน้าที่กรมที่ดิน</p>",
                "priority": "high",
                "state": land_states["todo"],
                "labels": [land_labels['งานปฏิบัติการ / แผนงาน'], land_labels['Training/Onboarding']]
            },
            {
                "no": 107,
                "name": "[Ops] จัดเตรียมและอ่านเนื้อหาสำหรับสอนน้องธรรม (Intern)",
                "description_html": "<p><b>งานที่ต้องทำ:</b> สรุปหัวข้อ สถาปัตยกรรมระบบ Knowledge Intelligence และขั้นตอนการทำงาน เพื่อถ่ายทอดและสอนงานให้น้องธรรม (Intern)</p>",
                "priority": "medium",
                "state": land_states["todo"],
                "labels": [land_labels['งานปฏิบัติการ / แผนงาน'], land_labels['Training/Onboarding']]
            }
        ]
    }
]

print("Starting to create LAND items...")
created_land_summary = []

for group in land_groups:
    mod_name = group["module_name"]
    mod_id = land_modules[mod_name]
    p_info = group["parent"]
    
    print(f"\nCreating Parent: {p_info['name']}")
    parent_item = client.work_items.create(
        workspace_slug=workspace_slug,
        project_id=LAND_PID,
        data=CreateWorkItem(
            name=p_info["name"],
            description_html=p_info["description_html"],
            priority=p_info["priority"],
            state=p_info["state"],
            labels=p_info["labels"],
            assignees=[user_id]
        )
    )
    print(f"  Parent created: {parent_item.id} (Identifier: {parent_item.sequence_id})")
    
    # Link parent to module
    client.modules.add_work_items(
        workspace_slug=workspace_slug,
        project_id=LAND_PID,
        module_id=mod_id,
        issue_ids=[parent_item.id]
    )
    
    sub_ids = []
    for sub in group["sub_items"]:
        sub_item = client.work_items.create(
            workspace_slug=workspace_slug,
            project_id=LAND_PID,
            data=CreateWorkItem(
                name=sub["name"],
                description_html=sub["description_html"],
                priority=sub["priority"],
                state=sub["state"],
                labels=sub["labels"],
                parent=parent_item.id,
                assignees=[user_id]
            )
        )
        sub_ids.append(sub_item.id)
        print(f"    Sub-item created: #{sub['no']} -> {sub_item.id} (Identifier: {sub_item.sequence_id})")
        time.sleep(0.1) # smooth API calls
    
    # Link sub-items to module as well
    if sub_ids:
        client.modules.add_work_items(
            workspace_slug=workspace_slug,
            project_id=LAND_PID,
            module_id=mod_id,
            issue_ids=sub_ids
        )
    
    created_land_summary.append({
        "parent": parent_item.name,
        "parent_id": parent_item.id,
        "sub_count": len(sub_ids)
    })

print("\n--- Creating POST Project Items ---")
post_parent = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=POST_PID,
    data=CreateWorkItem(
        name="[Thailand Post] แก้ไขการแสดงผล UI และเพิ่มคอลัมน์ Export CSV (ให้คุณขวัญ)",
        description_html="<p>ปรับปรุงตามที่สรุป Solution กับทีม Dev: ซ่อนตัวหนังสือชื่อที่เบียดกันในหน้าจอ และเพิ่มฟิลด์ department ในการส่งออก CSV</p>",
        priority="high",
        state=post_states["todo"],
        labels=[post_labels['Bug/Fix'], post_labels['Export/CSV'], post_labels['UI/Display']],
        assignees=[user_id]
    )
)
print(f"POST Parent created: {post_parent.id}")

post_sub1 = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=POST_PID,
    data=CreateWorkItem(
        name="[UI] ลบชื่อที่แสดงเป็นตัวหนังสือสีดำเบียด ๆ กันบนหน้าจอออก (แต่คงไว้ตอน Export)",
        description_html="<p><b>Solution จากการคุยกับทาง Dev:</b> จะลบชื่อที่แสดงเป็นตัวหนังสือสีดำเบียด ๆ กันออกครับ (แต่ตอน export ยังให้แสดงอยู่)</p>",
        priority="high",
        state=post_states["todo"],
        labels=[post_labels['UI/Display']],
        parent=post_parent.id,
        assignees=[user_id]
    )
)
print(f"  POST Sub-item 1 created: {post_sub1.id}")

post_sub2 = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=POST_PID,
    data=CreateWorkItem(
        name="[Export] เพิ่ม Column Name \"department\" ในไฟล์ CSV ที่ Export",
        description_html="<p><b>Solution จากการคุยกับทาง Dev:</b> เพิ่ม column name csv ที่ export มี column name \"department\" มาเพิ่ม</p>",
        priority="high",
        state=post_states["todo"],
        labels=[post_labels['Export/CSV']],
        parent=post_parent.id,
        assignees=[user_id]
    )
)
print(f"  POST Sub-item 2 created: {post_sub2.id}")

print("\n--- Creating PANUP Project Items (Internal & Infra) ---")
panup_parent = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=PANUP_PID,
    data=CreateWorkItem(
        name="[Internal/Ops] การประสานงานและระบบโครงสร้างพื้นฐาน",
        description_html="<p>งานประสานงานทั่วไป งานสิทธิ์การเข้าถึง และโครงสร้างพื้นฐาน</p>",
        priority="medium",
        state=panup_states["todo"],
        labels=[panup_labels.get('admin', '')] if 'admin' in panup_labels else [],
        assignees=[user_id]
    )
)
print(f"PANUP Parent created: {panup_parent.id}")

panup_sub1 = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=PANUP_PID,
    data=CreateWorkItem(
        name="[Infra] ประสานงานและคุยเรื่องสิทธิ์/การเชื่อมต่อ VPN กับพี่เบิร์ด",
        description_html="<p><b>งานที่ต้องทำ:</b> คุยเรื่อง vpn กับพี่เบิร์ด สำหรับสิทธิ์และการเชื่อมต่อเข้าระบบภายใน</p>",
        priority="medium",
        state=panup_states["todo"],
        labels=[panup_labels.get('admin', '')] if 'admin' in panup_labels else [],
        parent=panup_parent.id,
        assignees=[user_id]
    )
)
print(f"  PANUP Sub-item 1 created: {panup_sub1.id}")

print("\n==========================================")
print("ALL WORK ITEMS AND SUB-ITEMS CREATED SUCCESSFULLY!")
print(f"LAND: 6 Parents, 37 Sub-items")
print(f"POST: 1 Parent, 2 Sub-items")
print(f"PANUP: 1 Parent, 1 Sub-item")
print("==========================================")
