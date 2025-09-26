import pandas as pd
from datetime import datetime
import os
from sheets_utils import read_stock_sheet, read_sales_sheet

def export_stock_data(output_dir="."):
    """Export stock data to Excel"""
    stock_df = read_stock_sheet()
    
    if stock_df.empty:
        return None
        
    # Format the display columns
    display_df = stock_df[[
        'Product Name', 'Date Added', 'Purchase Price', 
        'Selling Price', 'Supplier', 'Quantity', 'Product ID'
    ]].copy()
    
    # Convert numeric columns
    display_df['Purchase Price'] = pd.to_numeric(display_df['Purchase Price'])
    display_df['Selling Price'] = pd.to_numeric(display_df['Selling Price'])
    display_df['Quantity'] = pd.to_numeric(display_df['Quantity'])
    
    # Format currency columns
    display_df['Purchase Price'] = display_df['Purchase Price'].apply(lambda x: f"${x:.2f}")
    display_df['Selling Price'] = display_df['Selling Price'].apply(lambda x: f"${x:.2f}")
    
    filename = os.path.join(output_dir, f'stock_data_{datetime.now().strftime("%Y%m%d")}.xlsx')
    display_df.to_excel(filename, sheet_name='Stock', index=False)
    
    return filename

def export_sales_data(output_dir=".", start_date=None, end_date=None):
    """Export sales data to Excel with optional date filtering"""
    sales_df = read_sales_sheet()
    stock_df = read_stock_sheet()
    
    if sales_df.empty:
        return None
        
    # Convert date column to datetime
    sales_df['Date of Sale'] = pd.to_datetime(sales_df['Date of Sale'])
    
    # Apply date filtering if specified
    if start_date and end_date:
        sales_df = sales_df[
            (sales_df['Date of Sale'] >= start_date) & 
            (sales_df['Date of Sale'] <= end_date)
        ]
    
    # Merge with stock data to get product names
    merged_df = sales_df.merge(
        stock_df[['Product ID', 'Product Name']],
        on='Product ID',
        how='left'
    )
    
    # Format the display columns
    display_df = merged_df[[
        'Date of Sale', 'Product Name', 'Product ID',
        'Quantity Sold', 'Total Price'
    ]].copy()
    
    # Convert numeric columns
    display_df['Total Price'] = pd.to_numeric(display_df['Total Price'])
    display_df['Quantity Sold'] = pd.to_numeric(display_df['Quantity Sold'])
    
    # Format date and currency
    display_df['Date of Sale'] = display_df['Date of Sale'].dt.strftime('%Y-%m-%d %H:%M')
    display_df['Total Price'] = display_df['Total Price'].apply(lambda x: f"${x:.2f}")
    
    filename = os.path.join(output_dir, f'sales_data_{datetime.now().strftime("%Y%m%d")}.xlsx')
    display_df.to_excel(filename, sheet_name='Sales', index=False)
    
    return filename

def export_combined_data(output_dir="."):
    """Export both stock and sales data to a single Excel file with multiple sheets"""
    filename = os.path.join(output_dir, f'shop_data_{datetime.now().strftime("%Y%m%d")}.xlsx')
    
    # Create Excel writer object
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Export stock data
        stock_df = read_stock_sheet()
        if not stock_df.empty:
            # Format stock data
            stock_df['Purchase Price'] = pd.to_numeric(stock_df['Purchase Price'])
            stock_df['Selling Price'] = pd.to_numeric(stock_df['Selling Price'])
            stock_df['Quantity'] = pd.to_numeric(stock_df['Quantity'])
            
            stock_df['Purchase Price'] = stock_df['Purchase Price'].apply(lambda x: f"${x:.2f}")
            stock_df['Selling Price'] = stock_df['Selling Price'].apply(lambda x: f"${x:.2f}")
            
            stock_df.to_excel(writer, sheet_name='Stock', index=False)
        
        # Export sales data
        sales_df = read_sales_sheet()
        if not sales_df.empty:
            # Merge with stock data
            merged_df = sales_df.merge(
                stock_df[['Product ID', 'Product Name']],
                on='Product ID',
                how='left'
            )
            
            # Format sales data
            merged_df['Date of Sale'] = pd.to_datetime(merged_df['Date of Sale'])
            merged_df['Total Price'] = pd.to_numeric(merged_df['Total Price'])
            
            merged_df['Date of Sale'] = merged_df['Date of Sale'].dt.strftime('%Y-%m-%d %H:%M')
            merged_df['Total Price'] = merged_df['Total Price'].apply(lambda x: f"${x:.2f}")
            
            merged_df.to_excel(writer, sheet_name='Sales', index=False)
    
    return filename