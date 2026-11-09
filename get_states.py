import requests

api_key = 'plane_api_753422726aad47afb951dc6cd3a7ceb4'
headers = {'x-api-key': api_key}
slug = 'panupong'

for pid, name in [('6dbd053c-9789-4056-8c18-f5f15616949c', 'LAND'), ('f0d660d0-9451-4b7a-8c00-5e9626f0712d', 'POST')]:
    r = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{pid}/states/', headers=headers)
    print(f'States for {name}:')
    for s in r.json().get('results', []):
        print(f"  {s.get('name')} ({s.get('group')}): {s.get('id')}")
