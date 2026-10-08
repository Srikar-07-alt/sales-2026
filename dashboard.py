# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd

# Set page config for a wider layout and modern title
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

# App Title
st.title("📊 Advanced Sales Data Analyzer Dashboard")
st.markdown("Welcome to the interactive sales dashboard. Filter and analyze your data below to uncover key insights.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('sales_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Revenue'] = df['Quantity'] * df['Price']
    return df

data = load_data()

# Sidebar for Filters
st.sidebar.header("Filters 🔍")
selected_region = st.sidebar.multiselect(
    "Select Region:",
    options=data['Region'].unique(),
    default=data['Region'].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category:",
    options=data['Category'].unique(),
    default=data['Category'].unique()
)

# Filter the data based on selection
filtered_data = data[
    (data['Region'].isin(selected_region)) & 
    (data['Category'].isin(selected_category))
]

if filtered_data.empty:
    st.warning("No data available for the selected filters. Please adjust your selection in the sidebar.")
else:
    # --- Top Level Metrics ---
    st.markdown("### 🏆 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = filtered_data['Revenue'].sum()
    total_quantity = filtered_data['Quantity'].sum()
    avg_price = filtered_data['Price'].mean()
    top_product = filtered_data.groupby('Product')['Revenue'].sum().idxmax()
    
    col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    col2.metric("Total Items Sold", f"{total_quantity:,}")
    col3.metric("Average Item Price", f"₹{avg_price:,.2f}")
    col4.metric("Top Revenue Product", top_product)

    st.divider()

    # --- Charts ---
    st.markdown("### 📈 Revenue Trends & Breakdowns")
    
    # Row 1 of charts
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.subheader("Monthly Revenue Trend")
        # Resample by month end (ME)
        monthly_trend = filtered_data.set_index('Date').resample('ME')['Revenue'].sum()
        if not monthly_trend.empty:
            st.line_chart(monthly_trend)
        else:
            st.info("Not enough data points for a trend line.")
        
    with row1_col2:
        st.subheader("Revenue by Region")
        region_rev = filtered_data.groupby('Region')['Revenue'].sum()
        st.bar_chart(region_rev)
        
    # Row 2 of charts
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.subheader("Revenue by Category")
        category_rev = filtered_data.groupby('Category')['Revenue'].sum()
        st.bar_chart(category_rev)
        
    with row2_col2:
        st.subheader("Revenue by Product")
        product_rev = filtered_data.groupby('Product')['Revenue'].sum()
        st.bar_chart(product_rev)
        
    st.divider()
    
    # --- Raw Data Table ---
    st.markdown("### 📋 Raw Sales Data")
    # Display the dataframe beautifully
    st.dataframe(
        filtered_data.sort_values(by="Date", ascending=False),
        use_container_width=True,
        hide_index=True
    )
