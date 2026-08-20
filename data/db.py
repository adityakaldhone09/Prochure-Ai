import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'purchase_requests.json')

def load_prs():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_prs(prs):
    with open(DB_FILE, 'w') as f:
        json.dump(prs, f, indent=4)
