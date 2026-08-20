import requests

BASE_URL = "http://127.0.0.1:5000"

def test_compare():
    # 1. Create a PR
    data = {
        'product': 'Test Laptop',
        'category': 'IT Hardware',
        'quantity': '20',
        'budget': '60000',
        'delivery_date': '2026-09-10',
        'priority': 'High',
        'description': 'For new developers'
    }
    r = requests.post(f"{BASE_URL}/purchase-request/create", data=data, allow_redirects=False)
    
    if r.status_code != 302:
        print("Failed to create PR")
        return
        
    location = r.headers['Location'] # e.g. /purchase-requests/PR-1001
    pr_id = location.split('/')[-1]
    
    # 2. Fetch compare page
    r_compare = requests.get(f"{BASE_URL}/vendors/compare/{pr_id}")
    
    if r_compare.status_code == 200:
        if b"RECOMMENDED VENDOR" in r_compare.content and b"Final Score" in r_compare.content:
            print("PASS: Compare page loaded successfully with recommended vendor.")
        else:
            print("FAIL: Page loaded but missing expected content.")
    else:
        print(f"FAIL: Compare page returned status {r_compare.status_code}")

if __name__ == '__main__':
    test_compare()
