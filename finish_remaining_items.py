import os
import requests
import json
import time

api_key = 'plane_api_753422726aad47afb951dc6cd3a7ceb4'
slug = 'panupong'
user_id = '6de5a3e3-a9ad-42a1-bdfa-21c193d628ef'

os.environ['PLANE_API_KEY'] = api_key
os.environ['PLANE_WORKSPACE_SLUG'] = slug

from plane_mcp.client import get_plane_client_context
from plane.models.work_items import CreateWorkItem

client, workspace_slug = get_plane_client_context()

POST_PID = 'f0d660d0-9451-4b7a-8c00-5e9626f0712d'
PANUP_PID = '6c496f89-d85a-4744-a685-3bc17d4bc4b2'

headers = {'x-api-key': api_key}

# Get labels
r_post_labels = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{POST_PID}/labels/', headers=headers)
post_labels = {l['name']: l['id'] for l in r_post_labels.json().get('results', [])}

r_panup_labels = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{PANUP_PID}/labels/', headers=headers)
panup_labels = {l['name']: l['id'] for l in r_panup_labels.json().get('results', [])}

# States
post_states = {
    'todo': 'de672684-ac83-483d-b0d2-d2175057b018'
}
panup_states = {
    'todo': '2688fd27-c35f-4888-bde9-22349161265d'
}

post_parent_id = 'd079a2ba-89b5-4b14-a4da-e92a759e5091'

def create_with_retry(pid, data):
    for attempt in range(5):
        try:
            res = client.work_items.create(
                workspace_slug=workspace_slug,
                project_id=pid,
                data=data
            )
            return res
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Failed after retries")

print("Waiting 10 seconds to clear rate limit...")
time.sleep(10)

print("Creating POST Sub-item 1...")
post_sub1 = create_with_retry(
    POST_PID,
    CreateWorkItem(
        name="[UI] ลบชื่อที่แสดงเป็นตัวหนังสือสีดำเบียด ๆ กันบนหน้าจอออก (แต่คงไว้ตอน Export)",
        description_html="<p><b>Solution จากการคุยกับทาง Dev:</b> จะลบชื่อที่แสดงเป็นตัวหนังสือสีดำเบียด ๆ กันออกครับ (แต่ตอน export ยังให้แสดงอยู่)</p>",
        priority="high",
        state=post_states["todo"],
        labels=[post_labels['UI/Display']],
        parent=post_parent_id,
        assignees=[user_id]
    )
)
print("  Created:", post_sub1.id)
time.sleep(2)

print("Creating POST Sub-item 2...")
post_sub2 = create_with_retry(
    POST_PID,
    CreateWorkItem(
        name="[Export] เพิ่ม Column Name \"department\" ในไฟล์ CSV ที่ Export",
        description_html="<p><b>Solution จากการคุยกับทาง Dev:</b> เพิ่ม column name csv ที่ export มี column name \"department\" มาเพิ่ม</p>",
        priority="high",
        state=post_states["todo"],
        labels=[post_labels['Export/CSV']],
        parent=post_parent_id,
        assignees=[user_id]
    )
)
print("  Created:", post_sub2.id)
time.sleep(2)

print("Creating PANUP Parent...")
panup_parent = create_with_retry(
    PANUP_PID,
    CreateWorkItem(
        name="[Internal/Ops] การประสานงานและระบบโครงสร้างพื้นฐาน",
        description_html="<p>งานประสานงานทั่วไป งานสิทธิ์การเข้าถึง และโครงสร้างพื้นฐาน</p>",
        priority="medium",
        state=panup_states["todo"],
        labels=[panup_labels.get('admin', '')] if 'admin' in panup_labels else [],
        assignees=[user_id]
    )
)
print("  Created:", panup_parent.id)
time.sleep(2)

print("Creating PANUP Sub-item 1...")
panup_sub1 = create_with_retry(
    PANUP_PID,
    CreateWorkItem(
        name="[Infra] ประสานงานและคุยเรื่องสิทธิ์/การเชื่อมต่อ VPN กับพี่เบิร์ด",
        description_html="<p><b>งานที่ต้องทำ:</b> คุยเรื่อง vpn กับพี่เบิร์ด สำหรับสิทธิ์และการเชื่อมต่อเข้าระบบภายใน</p>",
        priority="medium",
        state=panup_states["todo"],
        labels=[panup_labels.get('admin', '')] if 'admin' in panup_labels else [],
        parent=panup_parent.id,
        assignees=[user_id]
    )
)
print("  Created:", panup_sub1.id)
print("\nALL REMAINING ITEMS CREATED SUCCESSFULLY!")
