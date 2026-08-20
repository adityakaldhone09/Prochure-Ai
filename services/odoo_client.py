import xmlrpc.client
import logging
from config import Config
from data.seed_data import MOCK_VENDORS, MOCK_PRODUCTS, MOCK_PURCHASE_ORDERS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OdooClient:
    def __init__(self):
        self.url = Config.ODOO_URL
        self.db = Config.ODOO_DB
        self.username = Config.ODOO_USERNAME
        self.password = Config.ODOO_PASSWORD
        self.demo_mode = Config.DEMO_MODE
        self.uid = None
        self.models = None
        self.common = None

    def authenticate(self):
        if self.demo_mode:
            logger.info("DEMO_MODE is ON. Bypassing real Odoo authentication.")
            return True

        if not all([self.url, self.db, self.username, self.password]):
            logger.error("Odoo credentials missing in environment variables.")
            return False

        try:
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            if self.uid:
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                logger.info(f"Successfully authenticated to Odoo. UID: {self.uid}")
                return True
            else:
                logger.error("Odoo authentication failed: Invalid credentials.")
                return False
        except Exception as e:
            logger.error(f"Connection error to Odoo: {e}")
            return False

    def get_products(self, limit=10):
        if self.demo_mode:
            logger.info("DEMO_MODE: Returning mock products.")
            return MOCK_PRODUCTS

        if not self.uid and not self.authenticate(): 
            return []

        try:
            products = self.models.execute_kw(self.db, self.uid, self.password,
                'product.product', 'search_read',
                [[['sale_ok', '=', True]]],
                {'fields': ['id', 'name', 'list_price'], 'limit': limit})
            logger.info(f"Fetched {len(products)} products from Odoo.")
            return products
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return []

    def get_vendors(self, limit=10):
        if self.demo_mode:
            logger.info("DEMO_MODE: Returning mock vendors.")
            return MOCK_VENDORS

        if not self.uid and not self.authenticate(): 
            return []

        try:
            # We filter vendors that are flagged as suppliers, or generally companies
            vendors = self.models.execute_kw(self.db, self.uid, self.password,
                'res.partner', 'search_read',
                [[['supplier_rank', '>', 0]]],
                {'fields': ['id', 'name', 'email', 'phone'], 'limit': limit})
            logger.info(f"Fetched {len(vendors)} vendors from Odoo.")
            return vendors
        except Exception as e:
            logger.error(f"Error fetching vendors: {e}")
            return []

    def get_vendor(self, vendor_id):
        if self.demo_mode:
            logger.info(f"DEMO_MODE: Returning mock vendor {vendor_id}.")
            return next((v for v in MOCK_VENDORS if v['id'] == vendor_id), None)

        if not self.uid and not self.authenticate(): 
            return None

        try:
            vendor = self.models.execute_kw(self.db, self.uid, self.password,
                'res.partner', 'read',
                [vendor_id],
                {'fields': ['id', 'name', 'email', 'phone']})
            return vendor[0] if vendor else None
        except Exception as e:
            logger.error(f"Error fetching vendor {vendor_id}: {e}")
            return None

    def get_purchase_orders(self, limit=10):
        if self.demo_mode:
            logger.info("DEMO_MODE: Returning mock purchase orders.")
            return MOCK_PURCHASE_ORDERS

        if not self.uid and not self.authenticate(): 
            return []

        try:
            pos = self.models.execute_kw(self.db, self.uid, self.password,
                'purchase.order', 'search_read',
                [[]],
                {'fields': ['id', 'name', 'partner_id', 'state', 'amount_total', 'date_order'], 'limit': limit})
            logger.info(f"Fetched {len(pos)} purchase orders from Odoo.")
            return pos
        except Exception as e:
            logger.error(f"Error fetching purchase orders: {e}")
            return []

    def get_rfq_data(self, limit=10):
        if self.demo_mode:
            logger.info("DEMO_MODE: Returning mock RFQs.")
            return [po for po in MOCK_PURCHASE_ORDERS if po['state'] == 'draft']

        if not self.uid and not self.authenticate(): 
            return []
            
        try:
            rfqs = self.models.execute_kw(self.db, self.uid, self.password,
                'purchase.order', 'search_read',
                [[['state', 'in', ['draft', 'sent']]]],
                {'fields': ['id', 'name', 'partner_id', 'state', 'amount_total'], 'limit': limit})
            logger.info(f"Fetched {len(rfqs)} RFQs from Odoo.")
            return rfqs
        except Exception as e:
            logger.error(f"Error fetching RFQs: {e}")
            return []

    def create_purchase_order(self, vendor_id, product_lines, reference=None):
        """
        Creates a new purchase order.
        product_lines format: [{'product_id': 1, 'product_qty': 5, 'price_unit': 100.0}]
        """
        if self.demo_mode:
            logger.info("DEMO_MODE: Mock PO creation.")
            new_id = f"PO-2026-{len(MOCK_PURCHASE_ORDERS) + 1024}"
            total = sum([p.get('product_qty', 1) * p.get('price_unit', 0) for p in product_lines])
            vendor = self.get_vendor(vendor_id)
            new_po = {
                "id": new_id,
                "name": new_id,
                "partner_id": [vendor_id, vendor['name'] if vendor else 'Unknown'],
                "state": "draft",
                "amount_total": total,
                "origin": reference
            }
            MOCK_PURCHASE_ORDERS.append(new_po)
            logger.info(f"Mock PO created successfully: {new_id}")
            return new_id

        if not self.uid and not self.authenticate(): 
            raise Exception("Failed to authenticate with Odoo. Check credentials and server availability.")

        try:
            order_lines = []
            for line in product_lines:
                order_lines.append((0, 0, {
                    'product_id': line['product_id'],
                    'product_qty': line['product_qty'],
                    'price_unit': line['price_unit']
                }))
            
            payload = {
                'partner_id': vendor_id,
                'order_line': order_lines
            }
            if reference:
                payload['origin'] = reference
                
            po_id = self.models.execute_kw(self.db, self.uid, self.password, 'purchase.order', 'create', [payload])
            
            po_data = self.models.execute_kw(self.db, self.uid, self.password, 'purchase.order', 'read', [[po_id]], {'fields': ['name']})
            po_name = po_data[0]['name'] if po_data else f"PO-{po_id}"
            
            logger.info(f"Successfully created Purchase Order: {po_name}")
            return po_name
        except Exception as e:
            logger.error(f"Error creating purchase order: {e}")
            raise Exception(f"Odoo API Error: {str(e)}")
