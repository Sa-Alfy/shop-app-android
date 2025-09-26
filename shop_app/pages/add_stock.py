import streamlit as st
import uuid
from datetime import datetime
import pandas as pd

# Set page title and favicon
st.set_page_config(
    page_title="Shop App - Home",
    page_icon=":shopping_cart:"
)

def render():
    st.header("Add New Stock")
    
    # Initialize session state if needed
    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = []
    
    with st.form("add_stock_form", clear_on_submit=True):
        product_name = st.text_input("Product Name")
        col1, col2 = st.columns(2)
        
        with col1:
            purchase_price = st.number_input("Purchase Price", min_value=0.0, step=0.01)
            supplier = st.text_input("Supplier")
            
        with col2:
            selling_price = st.number_input("Selling Price", min_value=0.0, step=0.01)
            quantity = st.number_input("Quantity", min_value=1, step=1)
            
        if st.form_submit_button("Add Stock"):
            if not product_name or not supplier:
                st.error("Please fill in all required fields!")
                return
                
            try:
                product_data = {
                    "product_id": str(uuid.uuid4()),
                    "product_name": product_name,
                    "purchase_price": purchase_price,
                    "selling_price": selling_price,
                    "supplier": supplier,
                    "quantity": quantity,
                    "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.session_state.stock_data.append(product_data)
                st.success("Stock added successfully!")
                st.balloons()
                
            except Exception as e:
                st.error(f"Error adding stock: {str(e)}")
                
    # Show current stock
    st.subheader("Current Stock")
    if st.session_state.stock_data:
        stock_df = pd.DataFrame(st.session_state.stock_data)
        
        # Format currency columns
        stock_df['purchase_price'] = stock_df['purchase_price'].apply(lambda x: f"${x:.2f}")
        stock_df['selling_price'] = stock_df['selling_price'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(
            stock_df,
            use_container_width=True,
            hide_index=True,
            column_order=[
                'product_name', 'quantity', 'selling_price', 
                'purchase_price', 'supplier', 'date_added', 'product_id'
            ]
        )
    else:
        st.info("No stock items found")


if __name__ == "__main__":
    render()