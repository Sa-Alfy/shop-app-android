import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

# Sheet Names
STOCK_SHEET = 'Stock'
SALES_SHEET = 'Sales'

# API Configuration
API_HOST = os.getenv('API_HOST', 'localhost')
API_PORT = int(os.getenv('API_PORT', 8000))

# Frontend Configuration
FRONTEND_HOST = os.getenv('FRONTEND_HOST', 'localhost')

def validate_config():
    """Validate that all required configuration is present and valid."""
    missing = []
    
    if not GOOGLE_SHEETS_CREDENTIALS_FILE:
        missing.append("GOOGLE_SHEETS_CREDENTIALS_FILE")
        return False, "Google Sheets credentials file path not configured"
        
    if not SPREADSHEET_ID:
        missing.append("SPREADSHEET_ID")
        return False, "Spreadsheet ID not configured"
        
    if missing:
        return False, f"Missing required configuration: {', '.join(missing)}"
        
    # Check if credentials file exists
    if GOOGLE_SHEETS_CREDENTIALS_FILE and not os.path.exists(GOOGLE_SHEETS_CREDENTIALS_FILE):
        return False, f"Google Sheets credentials file not found at: {GOOGLE_SHEETS_CREDENTIALS_FILE}"
        
    return True, "Configuration is valid"
FRONTEND_PORT = int(os.getenv('FRONTEND_PORT', 8501))