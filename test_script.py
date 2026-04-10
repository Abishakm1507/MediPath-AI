import requests
import json

API_URL = "http://localhost:8000/analyze"

data = {"symptoms": "Chest pain and fever"}

try:
    print("Testing endpoint...")
    res = requests.post(API_URL, json=data, timeout=120)
    print(f"Status: {res.status_code}")
    print(json.dumps(res.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
