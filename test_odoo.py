import logging
from services.odoo_client import OdooClient

logging.basicConfig(level=logging.INFO, format='%(message)s')

def test():
    client = OdooClient()
    
    print("--- Testing Authentication ---")
    auth_success = client.authenticate()
    print(f"Authenticated: {auth_success}")
    
    print("\n--- Testing Fetch Products ---")
    products = client.get_products()
    print(f"Products: {products}")
    
    print("\n--- Testing Fetch Vendors ---")
    vendors = client.get_vendors()
    print(f"Vendors: {vendors}")
    
    print("\n--- Testing Fetch Purchase Orders ---")
    pos = client.get_purchase_orders()
    print(f"Purchase Orders: {pos}")
    
    print("\n--- Testing Fetch RFQs ---")
    rfqs = client.get_rfq_data()
    print(f"RFQs: {rfqs}")

if __name__ == '__main__':
    test()
