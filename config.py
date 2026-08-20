import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ODOO_URL = os.getenv('ODOO_URL')
    ODOO_DB = os.getenv('ODOO_DB')
    ODOO_USERNAME = os.getenv('ODOO_USERNAME')
    ODOO_PASSWORD = os.getenv('ODOO_PASSWORD')
    
    AI_API_KEY = os.getenv('AI_API_KEY')
    AI_PROVIDER = os.getenv('AI_PROVIDER')
    AI_ENABLED = os.getenv('AI_ENABLED', 'false').lower() == 'true'
    
    DEMO_MODE = os.getenv('DEMO_MODE', 'true').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-secret')
