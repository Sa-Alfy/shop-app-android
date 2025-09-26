import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import altair as alt

st.header("Sales History")

# Initialize session state if needed
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = []
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []

if not st.session_state.sales_data:
    st.info("No sales records found.")
    st.markdown("""
        ℹ️ To get started:
        1. Add some stock items first
        2. Record some sales
        3. Come back to view your sales history
    """)
    st.stop()
    
# Convert data to DataFrames
sales_df = pd.DataFrame(st.session_state.sales_data)
stock_df = pd.DataFrame(st.session_state.stock_data)

# Convert date column to datetime
sales_df['date_of_sale'] = pd.to_datetime(sales_df['date_of_sale'])

# Filter controls
filter_type = st.radio(
    "Filter Period",
    options=["1 Day", "1 Week", "All Time"],
    horizontal=True
)

# Calculate date range based on filter
end_date = datetime.now()
if filter_type == "1 Day":
    start_date = end_date - timedelta(days=1)
elif filter_type == "1 Week":
    start_date = end_date - timedelta(weeks=1)
else:  # All Time
    start_date = sales_df['date_of_sale'].min()

# Filter the data
filtered_sales = sales_df[
    (sales_df['date_of_sale'] >= start_date) & 
    (sales_df['date_of_sale'] <= end_date)
]

if filtered_sales.empty:
    st.info(f"No sales found for the selected period ({filter_type})")
    st.stop()
    

# Merge with stock to get product names and purchase price
if not stock_df.empty:
    merged_df = filtered_sales.merge(
        stock_df[['product_id', 'product_name', 'selling_price', 'purchase_price']],
        on='product_id',
        how='left'
    )
else:
    merged_df = filtered_sales.copy()
    merged_df['product_name'] = 'N/A'
    merged_df['selling_price'] = 0
    merged_df['purchase_price'] = 0

# Calculate profit per sale
merged_df['profit'] = (pd.to_numeric(merged_df['selling_price'], errors='coerce').fillna(0) - pd.to_numeric(merged_df['purchase_price'], errors='coerce').fillna(0)) * pd.to_numeric(merged_df['quantity_sold'], errors='coerce').fillna(0)

total_sales = merged_df['total_price'].sum()

# Display summary metrics
st.subheader("Sales Summary")
col1, col2, col3, col4 = st.columns(4)

total_sales = merged_df['total_price'].sum()
total_profit = merged_df['profit'].sum()
col1.metric("Total Sales", f"${total_sales:.2f}")
col2.metric("Total Profit", f"${total_profit:.2f}")
col3.metric("Number of Sales", len(merged_df))
col4.metric("Unique Products Sold", merged_df['product_id'].nunique())



# Display sales trend as interactive bar chart
st.subheader("Sales Trend (Daily Sales)")
daily_sales = merged_df.copy()
daily_sales['date'] = daily_sales['date_of_sale'].dt.date
daily_sales = daily_sales.groupby('date').agg({'total_price': 'sum', 'profit': 'sum'}).reset_index()

bar_chart = alt.Chart(daily_sales).mark_bar(size=30, color='#4F8DFD').encode(
    x=alt.X('date:T', title='Date'),
    y=alt.Y('total_price:Q', title='Total Sales'),
    tooltip=[alt.Tooltip('date:T', title='Date'), alt.Tooltip('total_price:Q', title='Total Sales ($)', format=',.2f'), alt.Tooltip('profit:Q', title='Profit ($)', format=',.2f')]
).properties(
    title='Total Sales Per Day',
    height=350
)
st.altair_chart(bar_chart.interactive(), use_container_width=True)

# Top selling products chart
st.subheader("Top Selling Products")
top_products = merged_df.groupby('product_name').agg({'total_price': 'sum', 'profit': 'sum'}).reset_index()
top_products = top_products.sort_values('total_price', ascending=False).head(10)

product_chart = alt.Chart(top_products).mark_bar(size=20, color='#00C49A').encode(
    x=alt.X('total_price:Q', title='Total Sales ($)', axis=alt.Axis(format=',.2f')),
    y=alt.Y('product_name:N', sort='-x', title='Product'),
    tooltip=[alt.Tooltip('product_name:N', title='Product'), alt.Tooltip('total_price:Q', title='Total Sales ($)', format=',.2f'), alt.Tooltip('profit:Q', title='Profit ($)', format=',.2f')]
).properties(
    title='Top 10 Products by Sales',
    height=350
)
st.altair_chart(product_chart.interactive(), use_container_width=True)

# Top products by profit chart
st.subheader("Top Profitable Products")
top_profit_products = top_products.sort_values('profit', ascending=False).head(10)
profit_chart = alt.Chart(top_profit_products).mark_bar(size=20, color='#FFB300').encode(
    x=alt.X('profit:Q', title='Total Profit ($)', axis=alt.Axis(format=',.2f')),
    y=alt.Y('product_name:N', sort='-x', title='Product'),
    tooltip=[alt.Tooltip('product_name:N', title='Product'), alt.Tooltip('profit:Q', title='Profit ($)', format=',.2f'), alt.Tooltip('total_price:Q', title='Total Sales ($)', format=',.2f')]
).properties(
    title='Top 10 Products by Profit',
    height=350
)
st.altair_chart(profit_chart.interactive(), use_container_width=True)

# Display detailed sales data
st.subheader("Sales Details")

# Prepare display dataframe
display_df = merged_df.copy()
display_df['date_of_sale'] = display_df['date_of_sale'].dt.strftime('%Y-%m-%d %H:%M')

# Safely apply currency formatting
for col in ['selling_price', 'purchase_price', 'total_price', 'profit']:
    if col in display_df.columns:
        display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0).apply(lambda x: f"${x:.2f}")

# Define columns to display
columns_to_display = ['date_of_sale', 'product_name', 'quantity_sold', 'selling_price', 'purchase_price', 'total_price', 'profit']
st.dataframe(
    display_df[columns_to_display],
    use_container_width=True,
    hide_index=True
)