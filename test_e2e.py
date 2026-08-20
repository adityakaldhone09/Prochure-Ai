import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from data.seed_data import MOCK_PURCHASE_REQUESTS, MOCK_PURCHASE_ORDERS

def test_workflow():
    app.config['TESTING'] = True
    client = app.test_client()
    
    print("--- STARTING E2E TESTS ---")
    
    # 1. Invalid input rejected
    res = client.post('/purchase-request/create', data={
        'product': 'Laptop',
        'quantity': '-5',
        'budget': '60000',
        'delivery_date': '2026-09-01'
    }, follow_redirects=True)
    if b'Quantity and budget must be positive numbers' in res.data or b'alert-danger' in res.data:
        print("PASS: Invalid input rejected")
    else:
        print("FAIL: Invalid input not rejected!")
        
    # 2. Expected Workflow
    res = client.post('/purchase-request/create', data={
        'product': 'Test E2E Laptop',
        'category': 'IT Hardware',
        'quantity': '20',
        'budget': '60000',
        'delivery_date': '2026-09-01',
        'priority': 'High',
        'description': 'For new devs'
    }, follow_redirects=False)
    
    if res.status_code != 302:
        print(f"FAIL: Expected redirect after valid PR creation. Got {res.status_code}")
        return
        
    pr_id = res.headers['Location'].split('/')[-1]
    print(f"PASS: Created PR {pr_id}")
    
    # Check analyzing state
    res = client.get(f'/purchase-requests/{pr_id}')
    if b'ANALYZING' in res.data or b'Analyzing' in res.data or b'bg-status-analyzing' in res.data:
        print("PASS: Request is in ANALYZING state initially")
    else:
        print("FAIL: Not in ANALYZING state")
        
    # Check Vendor Comparison
    res = client.get(f'/vendors/compare/{pr_id}')
    if res.status_code == 200:
        print("PASS: Vendor comparison endpoint works")
        if b'TechWorld Solutions' in res.data:
            print("PASS: TechWorld found in comparison")
        if b'RISK' in res.data:
            print("PASS: Risk indicators are present")
    else:
        print("FAIL: Vendor comparison failed")
        
    # Check that after comparison, PR is PENDING_APPROVAL
    res = client.get(f'/purchase-requests/{pr_id}')
    if b'PENDING_APPROVAL' in res.data or b'bg-status-pending' in res.data or b'PENDING APPROVAL' in res.data:
        print("PASS: Status changed to PENDING_APPROVAL")
    else:
        print("FAIL: Status did NOT change to PENDING_APPROVAL")
        
    # Check rejection doesn't create PO
    res = client.post(f'/api/reject/{pr_id}', json={"reason": "Testing rejection"})
    if res.status_code == 200:
        print("PASS: Rejection API successful")
        pr_record = next(p for p in MOCK_PURCHASE_REQUESTS if p['id'] == pr_id)
        if pr_record['status'] == 'REJECTED':
            print("PASS: Request is marked REJECTED")
        if 'po_id' not in pr_record:
            print("PASS: No PO created on rejection")
            
    # Reset to Pending for approval test
    for pr in MOCK_PURCHASE_REQUESTS:
        if pr['id'] == pr_id:
            pr['status'] = 'PENDING_APPROVAL'
            
    # Approve and create PO
    res = client.post(f'/api/approve/{pr_id}')
    data = res.get_json()
    if data and data.get('success'):
        print(f"PASS: Approved and PO created: {data.get('po_id')}")
        pr_record = next(p for p in MOCK_PURCHASE_REQUESTS if p['id'] == pr_id)
        if pr_record['status'] == 'PO_CREATED':
            print("PASS: Request status is PO_CREATED")
    else:
        print(f"FAIL: Approval failed: {data}")
        
    print("--- E2E TESTS COMPLETE ---")

if __name__ == '__main__':
    test_workflow()
