import requests

api_key = 'plane_api_753422726aad47afb951dc6cd3a7ceb4'
headers = {'x-api-key': api_key}
slug = 'panupong'

projects = [
    ('6dbd053c-9789-4056-8c18-f5f15616949c', 'LAND', 'Knowledge Intelligence (กรมที่ดิน)'),
    ('f0d660d0-9451-4b7a-8c00-5e9626f0712d', 'POST', 'ไปรษณีย์ไทย (Thailand Post)'),
    ('6c496f89-d85a-4744-a685-3bc17d4bc4b2', 'PANUP', 'Panupong (Internal & Personal)')
]

for pid, code, name in projects:
    r = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{pid}/issues/', headers=headers)
    items = r.json().get('results', [])
    parents = [i for i in items if not i.get('parent')]
    children = [i for i in items if i.get('parent')]
    print(f"\n=== Project: {name} ({code}) ===")
    print(f"Total issues: {len(items)} | Parents: {len(parents)} | Sub-items: {len(children)}")
    for p in parents:
        subs = [c for c in children if c.get('parent') == p.get('id')]
        print(f"  Parent: [{p.get('name')}] -> {len(subs)} sub-items")
