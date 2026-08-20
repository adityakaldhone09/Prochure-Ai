# MOCK/DEMO DATA for ProcureAI

MOCK_VENDORS = [
    {
        "id": 1, 
        "name": "TechWorld Solutions", 
        "category": "IT Hardware", 
        "rating": 92, 
        "reliability": 94, 
        "delivery": 92, 
        "accuracy": 98, 
        "price_competitiveness": 85,
        "email": "sales@techworld.in", "phone": "555-0001"
    },
    {
        "id": 2, 
        "name": "GlobalTech Suppliers", 
        "category": "Electronics", 
        "rating": 84, 
        "reliability": 82, 
        "delivery": 75, 
        "accuracy": 91, 
        "price_competitiveness": 95,
        "email": "contact@globaltech.com", "phone": "555-0002"
    },
    {
        "id": 3, 
        "name": "DigitalMart", 
        "category": "Retail", 
        "rating": 88, 
        "reliability": 88, 
        "delivery": 90, 
        "accuracy": 94, 
        "price_competitiveness": 88,
        "email": "b2b@digitalmart.com", "phone": "555-0003"
    },
    {
        "id": 4, 
        "name": "CompIndia Systems", 
        "category": "Enterprise IT", 
        "rating": 95, 
        "reliability": 96, 
        "delivery": 95, 
        "accuracy": 99, 
        "price_competitiveness": 80,
        "email": "enterprise@compindia.in", "phone": "555-0004"
    },
    {
        "id": 5, 
        "name": "PrimeSystems", 
        "category": "Hardware & Networking", 
        "rating": 89, 
        "reliability": 90, 
        "delivery": 88, 
        "accuracy": 93, 
        "price_competitiveness": 90,
        "email": "info@primesystems.com", "phone": "555-0005"
    }
]

MOCK_PRODUCTS = [
    {"id": 101, "name": "Laptop", "list_price": 55000.00},
    {"id": 102, "name": "Monitor", "list_price": 12000.00},
    {"id": 103, "name": "Keyboard", "list_price": 1500.00},
    {"id": 104, "name": "Mouse", "list_price": 800.00},
    {"id": 105, "name": "Printer", "list_price": 15000.00},
    {"id": 106, "name": "Router", "list_price": 3500.00},
    {"id": 107, "name": "Server", "list_price": 250000.00},
]

MOCK_QUOTATIONS = [
    {
        "id": 5001,
        "rfq_id": "RFQ-2026-001",
        "requirement": "20 Laptops",
        "budget_per_unit": 60000,
        "required_delivery_days": 7,
        "bids": [
            {"vendor_id": 1, "vendor_name": "TechWorld Solutions", "price_per_unit": 58000, "delivery_days": 5, "total_price": 1160000},
            {"vendor_id": 2, "vendor_name": "GlobalTech Suppliers", "price_per_unit": 52000, "delivery_days": 10, "total_price": 1040000},
            {"vendor_id": 3, "vendor_name": "DigitalMart", "price_per_unit": 59500, "delivery_days": 6, "total_price": 1190000},
            {"vendor_id": 4, "vendor_name": "CompIndia Systems", "price_per_unit": 62000, "delivery_days": 4, "total_price": 1240000},
            {"vendor_id": 5, "vendor_name": "PrimeSystems", "price_per_unit": 57500, "delivery_days": 8, "total_price": 1150000}
        ]
    }
]

MOCK_PURCHASE_ORDERS = [
    {"id": 1001, "name": "PO0001", "partner_id": [1, "TechWorld Solutions"], "state": "purchase", "amount_total": 1160000},
]

MOCK_PURCHASE_REQUESTS = []
