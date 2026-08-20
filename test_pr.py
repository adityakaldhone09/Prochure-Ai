import requests

BASE_URL = "http://127.0.0.1:5000"

def test_pr():
    print("Testing missing product...")
    data = {'product': '', 'quantity': '1', 'budget': '10', 'delivery_date': '2026-09-01'}
    r = requests.post(f"{BASE_URL}/purchase-request/create", data=data)
    if b"Product is required" not in r.content:
        print("FAIL: missing product validation")
    else:
        print("PASS")

    print("Testing missing date...")
    data = {'product': 'Laptop', 'quantity': '1', 'budget': '10', 'delivery_date': ''}
    r = requests.post(f"{BASE_URL}/purchase-request/create", data=data)
    if b"Required delivery date is required" not in r.content:
        print("FAIL: missing date validation")
    else:
        print("PASS")

    print("Testing invalid quantity...")
    data = {'product': 'Laptop', 'quantity': '-5', 'budget': '10', 'delivery_date': '2026-09-01'}
    r = requests.post(f"{BASE_URL}/purchase-request/create", data=data)
    if b"Quantity must be a positive integer" not in r.content and b"Invalid quantity" not in r.content:
        print("FAIL: invalid quantity validation")
    else:
        print("PASS")

    print("Testing invalid budget...")
    data = {'product': 'Laptop', 'quantity': '5', 'budget': 'abc', 'delivery_date': '2026-09-01'}
    r = requests.post(f"{BASE_URL}/purchase-request/create", data=data)
    if b"Invalid budget" not in r.content:
        print("FAIL: invalid budget validation")
    else:
        print("PASS")

    print("Testing valid request...")
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
    if r.status_code == 302:
        print(f"PASS: Redirected to {r.headers['Location']}")
    else:
        print("FAIL: valid request did not redirect")
    
    print("Testing view list...")
    r = requests.get(f"{BASE_URL}/purchase-requests")
    if b"Test Laptop" in r.content:
        print("PASS")
    else:
        print("FAIL: created item not in list")
        
    print("Finished.")

if __name__ == '__main__':
    test_pr()
