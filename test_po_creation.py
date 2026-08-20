import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_po_creation():
    # 1. Create a PR
    data = {
        'product': 'Test PO Laptop',
        'category': 'IT Hardware',
        'quantity': '10',
        'budget': '50000',
        'delivery_date': '2026-09-10',
        'priority': 'High',
        'description': 'For new developers'
    }
    r = requests.post(f"{BASE_URL}/purchase-request/create", data=data, allow_redirects=False)
    if r.status_code != 302:
        print("Failed to create PR")
        return
        
    pr_id = r.headers['Location'].split('/')[-1]
    
    # 2. Approve PR (this should create the PO)
    r_app = requests.post(f"{BASE_URL}/api/approve/{pr_id}")
    
    if r_app.status_code == 200:
        resp = r_app.json()
        if resp.get('success'):
            print("PASS: Successfully approved PR and created PO!")
            print(f"PO ID: {resp.get('po_id')}")
            print(f"Vendor: {resp.get('vendor')}")
            print(f"Total Amount: ₹{resp.get('amount')}")
        else:
            print("FAIL: API returned success=False")
            print(resp.get('error'))
    elif r_app.status_code == 500:
        resp = r_app.json()
        print("FAIL (Expected if real Odoo is down and DEMO_MODE=false):")
        print(resp.get('error'))
    else:
        print(f"FAIL: Status code {r_app.status_code}")

if __name__ == '__main__':
    test_po_creation()
