from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
import config

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

from .exceptions import SheetOperationError
import os

def get_google_sheets_service():
    """Initialize and return Google Sheets service"""
    try:
        # Validate configuration first
        is_valid, message = config.validate_config()
        if not is_valid:
            raise SheetOperationError(message)
            
        creds = service_account.Credentials.from_service_account_file(
            config.GOOGLE_SHEETS_CREDENTIALS_FILE,
            scopes=SCOPES
        )
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        if isinstance(e, SheetOperationError):
            raise e
        raise SheetOperationError(f"Failed to initialize Google Sheets service: {str(e)}")

def read_stock_sheet():
    """Read data from the Stock sheet"""
    try:
        if not config.SPREADSHEET_ID:
            raise SheetOperationError("Spreadsheet ID not configured")
            
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        
        result = sheet.values().get(
            spreadsheetId=config.SPREADSHEET_ID,
            range='Stock!A2:G'  # Assuming headers are in row 1
        ).execute()
            
        values = result.get('values', [])
    except Exception as e:
        if isinstance(e, SheetOperationError):
            raise e
        raise SheetOperationError(f"Failed to read Stock sheet: {str(e)}")
    
    if not values:
        return pd.DataFrame(columns=[
            'Product Name', 'Date Added', 'Purchase Price', 
            'Selling Price', 'Supplier', 'Quantity', 'Product ID'
        ])
    
    return pd.DataFrame(values, columns=[
        'Product Name', 'Date Added', 'Purchase Price', 
        'Selling Price', 'Supplier', 'Quantity', 'Product ID'
    ])

def read_sales_sheet():
    """Read data from the Sales sheet"""
    try:
        if not config.SPREADSHEET_ID:
            raise SheetOperationError("Spreadsheet ID not configured")
            
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        
        result = sheet.values().get(
            spreadsheetId=config.SPREADSHEET_ID,
            range='Sales!A2:D'  # Assuming headers are in row 1
        ).execute()
            
        values = result.get('values', [])
    except Exception as e:
        if isinstance(e, SheetOperationError):
            raise e
        raise SheetOperationError(f"Failed to read Sales sheet: {str(e)}")
    
    if not values:
        return pd.DataFrame(columns=[
            'Product ID', 'Date of Sale', 'Quantity Sold', 'Total Price'
        ])
    
    return pd.DataFrame(values, columns=[
        'Product ID', 'Date of Sale', 'Quantity Sold', 'Total Price'
    ])

def append_stock(product_data):
    """Add new stock entry to the Stock sheet"""
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    
    # Generate unique Product ID (timestamp-based)
    product_id = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    values = [[
        product_data['Product Name'],
        datetime.now().strftime('%Y-%m-%d'),
        product_data['Purchase Price'],
        product_data['Selling Price'],
        product_data['Supplier'],
        product_data['Quantity'],
        product_id
    ]]
    
    body = {
        'values': values
    }
    
    result = sheet.values().append(
        spreadsheetId=config.SPREADSHEET_ID,
        range='Stock!A2:G',
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    return product_id

def update_stock_quantity(product_id, new_quantity):
    """Update stock quantity for a specific product"""
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    
    # First, find the row with the product ID
    result = sheet.values().get(
        spreadsheetId=config.SPREADSHEET_ID,
        range='Stock!A2:G'
    ).execute()
    values = result.get('values', [])
    
    row_idx = None
    for idx, row in enumerate(values):
        if row[6] == product_id:  # Product ID is in column G (index 6)
            row_idx = idx + 2  # Add 2 because we start from A2
            break
    
    if row_idx is None:
        raise ValueError(f"Product ID {product_id} not found")
    
    # Update the quantity in column F
    range_name = f'Stock!F{row_idx}'
    body = {
        'values': [[str(new_quantity)]]
    }
    
    result = sheet.values().update(
        spreadsheetId=config.SPREADSHEET_ID,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    return result

def record_sale(product_id, quantity_sold, total_price):
    """Record a new sale in the Sales sheet"""
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    
    values = [[
        product_id,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        str(quantity_sold),
        str(total_price)
    ]]
    
    body = {
        'values': values
    }
    
    result = sheet.values().append(
        spreadsheetId=config.SPREADSHEET_ID,
        range='Sales!A2:D',
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    return result