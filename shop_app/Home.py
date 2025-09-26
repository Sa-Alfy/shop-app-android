import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import json
import os
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

def export_data_to_csv():
    """Export data to CSV files"""
    try:
        # Export stock data
        if st.session_state.stock_data:
            stock_df = pd.DataFrame(st.session_state.stock_data)
            stock_file = f'stock_data_{datetime.now().strftime("%Y%m%d")}.csv'
            stock_df.to_csv(stock_file, index=False)
            
            with open(stock_file, 'rb') as f:
                st.download_button(
                    label="Download Stock Data",
                    data=f,
                    file_name=stock_file,
                    mime='text/csv'
                )
        
        # Export sales data
        if st.session_state.sales_data:
            sales_df = pd.DataFrame(st.session_state.sales_data)
            sales_file = f'sales_data_{datetime.now().strftime("%Y%m%d")}.csv'
            sales_df.to_csv(sales_file, index=False)
            
            with open(sales_file, 'rb') as f:
                st.download_button(
                    label="Download Sales Data",
                    data=f,
                    file_name=sales_file,
                    mime='text/csv'
                )
    except Exception as e:
        st.error(f"Error exporting data: {str(e)}")

def import_data_from_csv():
    """Import data from CSV files"""
    try:
        stock_file = st.file_uploader("Upload Stock Data CSV", type=['csv'])
        sales_file = st.file_uploader("Upload Sales Data CSV", type=['csv'])
        
        if stock_file:
            stock_df = pd.read_csv(stock_file)
            st.session_state.stock_data = stock_df.to_dict('records')
            st.success("Stock data imported successfully!")
            
        if sales_file:
            sales_df = pd.read_csv(sales_file)
            st.session_state.sales_data = sales_df.to_dict('records')
            st.success("Sales data imported successfully!")
    except Exception as e:
        st.error(f"Error importing data: {str(e)}")

st.set_page_config(
    page_title="Shop Management System",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    st.title("Shop Management System 🏪")
    
    # Initialize session state for data storage
    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = []
    if 'sales_data' not in st.session_state:
        st.session_state.sales_data = []
    
    st.header("Welcome to Shop Management System")
    
    # Data Storage Options in sidebar
    st.sidebar.title("Data Management")
    
    # Use columns to place buttons side-by-side
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Export to CSV", use_container_width=True):
            export_data_to_csv()
    with col2:
        if st.button("Import from CSV", use_container_width=True):
            import_data_from_csv()
            
    # Show quick summary
    if st.session_state.stock_data:
        st.subheader("Current Stock Summary")
        df = pd.DataFrame(st.session_state.stock_data)
        st.dataframe(df[['product_name', 'quantity', 'selling_price']], use_container_width=True)
    else:
        st.info("No stock data available. Add some stock to get started!")

if __name__ == "__main__":
    main()