import streamlit as st
from datetime import datetime
import pandas as pd

st.header("Record Sale")

# Initialize session state if needed
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = []
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []

if not st.session_state.stock_data:
    st.error("No products in stock. Please add stock first!")
    st.stop()

# Convert stock data to DataFrame
stock_df = pd.DataFrame(st.session_state.stock_data)

# Only show products with quantity > 0
available_stock = stock_df[stock_df['quantity'] > 0].copy()

if available_stock.empty:
    st.error("No products available in stock!")
    st.stop()

with st.form("record_sale_form", clear_on_submit=True):
    # Create product selection dropdown
    product_options = available_stock['product_name'].tolist()
    
    selected_product_name = st.selectbox(
        "Select Product",
        options=[f"{name} (Qty: {available_stock[available_stock['product_name'] == name]['quantity'].iloc[0]})" 
                for name in product_options]
    )
    
    if selected_product_name:
        selected_product_name = selected_product_name.split(" (Qty:")[0]  # Extract just the product name
    
        # Get the selected product's data
        product_data = available_stock[available_stock['product_name'] == selected_product_name].iloc[0]
        
        # Show product details
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Selling Price: ${float(product_data['selling_price']):.2f}")
        with col2:
            st.info(f"Available Quantity: {int(product_data['quantity'])}")
        
        # Quantity input
        quantity = st.number_input(
            "Quantity to Sell",
            min_value=1,
            max_value=int(product_data['quantity']),
            step=1
        )
        
        # Calculate total price
        total_price = quantity * float(product_data['selling_price'])
        st.write(f"Total Price: ${total_price:.2f}")
        
        if st.form_submit_button("Record Sale"):
            try:
                # Create sale record
                sale_record = {
                    "product_id": product_data['product_id'],
                    "date_of_sale": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "quantity_sold": quantity,
                    "total_price": total_price
                }
                
                # Update stock quantity
                # Find the index in the original list, not the filtered one
                product_idx_list = [i for i, d in enumerate(st.session_state.stock_data) if d['product_id'] == product_data['product_id']]
                if product_idx_list:
                    product_idx = product_idx_list[0]
                    st.session_state.stock_data[product_idx]['quantity'] -= quantity
                
                # Add sale record
                st.session_state.sales_data.append(sale_record)
                
                st.success("Sale recorded successfully!")
                st.balloons()
                st.rerun()
                
            except Exception as e:
                st.error(f"Error recording sale: {str(e)}")

# Show recent sales
st.subheader("Recent Sales")
if st.session_state.sales_data:
    sales_df = pd.DataFrame(st.session_state.sales_data)
    sales_df['date_of_sale'] = pd.to_datetime(sales_df['date_of_sale'])
    
    # Get last 5 sales
    recent_sales = sales_df.sort_values('date_of_sale', ascending=False).head(5)
    
    # Add product names
    if st.session_state.stock_data:
        stock_df_for_merge = pd.DataFrame(st.session_state.stock_data)
        recent_sales = recent_sales.merge(
            stock_df_for_merge[['product_id', 'product_name']],
            on='product_id',
            how='left'
        )
    
    # Format display
    recent_sales['date_of_sale'] = recent_sales['date_of_sale'].dt.strftime('%Y-%m-%d %H:%M')
    recent_sales['total_price'] = recent_sales['total_price'].apply(lambda x: f"${x:.2f}")
    
    st.dataframe(
        recent_sales[[
            'date_of_sale', 'product_name', 'quantity_sold', 'total_price'
        ]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No sales recorded yet")