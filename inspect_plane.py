import os
import requests
import json

api_key = 'plane_api_753422726aad47afb951dc6cd3a7ceb4'
headers = {'x-api-key': api_key}
slug = 'panupong'

r = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/', headers=headers)
print('Projects status:', r.status_code)
projects_data = r.json()
results = projects_data.get('results', projects_data if isinstance(projects_data, list) else [])
for p in results:
    p_id = p.get('id')
    p_name = p.get('name')
    p_ident = p.get('identifier')
    print(f"Project: {p_name} ({p_ident}) -> ID: {p_id}")
    
    # get states
    r_states = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{p_id}/states/', headers=headers)
    states = r_states.json().get('results', [])
    print("  States:", [(s.get('name'), s.get('group'), s.get('id')) for s in states])
    
    # get labels
    r_labels = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{p_id}/labels/', headers=headers)
    labels = r_labels.json().get('results', [])
    print("  Labels:", [(l.get('name'), l.get('id')) for l in labels])
    
    # get issues count
    r_issues = requests.get(f'https://api.plane.so/api/v1/workspaces/{slug}/projects/{p_id}/issues/', headers=headers)
    issues = r_issues.json().get('results', [])
    print(f"  Issues count: {len(issues)}")
