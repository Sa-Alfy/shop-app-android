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
    """Export data to CSV files (in-memory, all columns)"""
    try:
        # Export stock data
        if st.session_state.stock_data:
            stock_df = pd.DataFrame(st.session_state.stock_data)
            stock_csv = stock_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Stock Data",
                data=stock_csv,
                file_name=f'stock_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv'
            )
        # Export sales data
        if st.session_state.sales_data:
            sales_df = pd.DataFrame(st.session_state.sales_data)
            sales_csv = sales_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Sales Data",
                data=sales_csv,
                file_name=f'sales_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv'
            )
    except Exception as e:
        st.error(f"Error exporting data: {str(e)}")

def import_data_from_csv():
    """Import data from CSV files (all columns)"""
    try:
        stock_file = st.file_uploader("Upload Stock Data CSV", type=['csv'], key="stock_upload")
        if stock_file:
            stock_df = pd.read_csv(stock_file)
            st.session_state.stock_data = stock_df.to_dict('records')
            st.success("Stock data imported successfully!")
            st.rerun()
        sales_file = st.file_uploader("Upload Sales Data CSV", type=['csv'], key="sales_upload")
        if sales_file:
            sales_df = pd.read_csv(sales_file)
            st.session_state.sales_data = sales_df.to_dict('records')
            st.success("Sales data imported successfully!")
            st.rerun()
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
    
    # Data Storage Options in main area
    st.subheader("Data Management")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Export your data as CSV files:**")
        export_data_to_csv()
    with col2:
        st.markdown("**Import your data from CSV files:**")
        import_data_from_csv()

    # Show quick summary
    if st.session_state.stock_data:
        st.subheader("Current Stock Summary")
        df = pd.DataFrame(st.session_state.stock_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No stock data available. Add some stock to get started!")

if __name__ == "__main__":
    main()