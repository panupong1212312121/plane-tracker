import os
import requests
import json
import time

api_key = 'plane_api_753422726aad47afb951dc6cd3a7ceb4'
slug = 'panupong'
p_id = '6c496f89-d85a-4744-a685-3bc17d4bc4b2'

os.environ['PLANE_API_KEY'] = api_key
os.environ['PLANE_WORKSPACE_SLUG'] = slug

from plane_mcp.client import get_plane_client_context
client, workspace_slug = get_plane_client_context()

headers = {'x-api-key': api_key}
r = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{p_id}/issues/', headers=headers)
items = r.json().get('results', [])

tutorial_keywords = [
    'Welcome to Plane',
    '1. Create Projects',
    '2. Invite your team',
    '3. Create and assign Work Items',
    '4. Visualize your work',
    '5. Use Cycles to time box tasks',
    '6. Customize your settings'
]

print("Found total items in Panupong:", len(items))
deleted_count = 0

for item in items:
    item_id = item['id']
    item_name = item['name']
    is_tutorial = any(k.lower() in item_name.lower() for k in tutorial_keywords)
    
    if is_tutorial:
        print(f"Deleting tutorial item: [{item_name}] (ID: {item_id})...")
        try:
            client.work_items.delete(
                workspace_slug=workspace_slug,
                project_id=p_id,
                work_item_id=item_id
            )
            print(f"  -> Deleted successfully!")
            deleted_count += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  -> Error deleting: {e}")
    else:
        print(f"Preserving non-tutorial item: [{item_name}] (ID: {item_id})")

print(f"\nDone! Deleted {deleted_count} tutorial work items.")
