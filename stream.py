import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set a wide layout for better visualization
st.set_page_config(layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('ShopSmart_BI_Dummy_5000.csv')
    df['Month'] = pd.to_datetime(df['Month'])
    return df

df = load_data()

# --- Dashboard Title and Description ---
st.title('ShopSmart Store Performance Dashboard 📊')
st.markdown("Explore key performance metrics and trends for our retail stores, with a focus on sales decline and its drivers.")

# --- Filters ---
st.sidebar.header('Store & Date Filters')

# Dropdown for selecting a store
all_stores = ['All Stores'] + sorted(df['Store_ID'].unique())
selected_store = st.sidebar.selectbox('Select Store ID:', all_stores)

# Slider for selecting a date range
min_date = df['Month'].min().date()
max_date = df['Month'].max().date()
date_range = st.sidebar.slider(
    'Select Date Range:',
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM"
)

# Filter the DataFrame based on user selections
filtered_df = df[(df['Month'].dt.date >= date_range[0]) & (df['Month'].dt.date <= date_range[1])]

if selected_store != 'All Stores':
    filtered_df = filtered_df[filtered_df['Store_ID'] == selected_store]

# Check if the filtered DataFrame is empty
if filtered_df.empty:
    st.warning("No data found for the selected filters. Please adjust your selections.")
    st.stop()

# --- KPI Section ---
st.header('Key Performance Indicators (KPIs)')
col1, col2, col3 = st.columns(3)

avg_sales_decline = filtered_df['Sales Decline'].mean()
avg_holding_costs = filtered_df['Inventory Holding Costs (₱)'].mean()
avg_market_share = filtered_df['Market Share in Region'].mean()

with col1:
    st.metric(label="Average Sales Decline", value=f"{avg_sales_decline:.2f}%")
with col2:
    st.metric(label="Average Inventory Holding Costs", value=f"₱{avg_holding_costs:,.0f}")
with col3:
    st.metric(label="Average Market Share", value=f"{avg_market_share:.2f}%")

st.markdown("---")

# --- 1. Overall Health Check ---
st.header('1. Overall Health Check')
st.markdown("Understanding the distribution and regional breakdown of sales decline.")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader('Distribution of Sales Decline')
    fig_hist = px.histogram(filtered_df, x='Sales Decline', color='Region', nbins=30, marginal="box",
                            hover_data=filtered_df.columns, title='Sales Decline Across All Observations')
    st.plotly_chart(fig_hist, use_container_width=True)

with col_b:
    st.subheader('Sales Decline by Region')
    fig_region_box = px.box(filtered_df, x='Region', y='Sales Decline',
                            color='Region', title='Sales Decline Distribution by Region')
    st.plotly_chart(fig_region_box, use_container_width=True)

st.markdown("---")

# --- 2. Inventory & Demand Alignment ---
st.header('2. Inventory & Demand Alignment')
st.markdown("Does inventory match local demand? What is the financial impact?")

# Using color to show hierarchy by Sales Decline value
fig_inv = px.bar(filtered_df.groupby('Inventory–Local Demand Match')['Sales Decline'].mean().reset_index(),
                 x='Inventory–Local Demand Match', y='Sales Decline',
                 color='Sales Decline',
                 category_orders={"Inventory–Local Demand Match": ["High", "Medium", "Low"]},
                 title='Average Sales Decline by Inventory–Demand Match')
st.plotly_chart(fig_inv, use_container_width=True)


st.markdown("---")

# --- 3. Customer Behavior ---
st.header('3. Customer Behavior')
st.markdown("Analyzing how basket size, trip frequency, and loyalty relate to sales decline.")

# Using color to show hierarchy by Sales Decline value
fig_loyalty = px.bar(filtered_df.groupby('Customer Loyalty & Engagement')['Sales Decline'].mean().reset_index(),
                     x='Customer Loyalty & Engagement', y='Sales Decline',
                     color='Sales Decline',
                     category_orders={"Customer Loyalty & Engagement": ["Strong", "Moderate", "Weak"]},
                     title='Average Sales Decline by Customer Loyalty & Engagement')
st.plotly_chart(fig_loyalty, use_container_width=True)


st.markdown("---")

# --- 4. Promotions & Pricing ---
st.header('4. Promotions & Pricing')
st.markdown("Examining the effectiveness of promotions and their link to costs.")

col_c, col_d = st.columns(2)

with col_c:
    fig_promo_sales = px.bar(filtered_df.groupby('Promotions & Pricing Effectiveness')['Sales Decline'].mean().reset_index(),
                             x='Promotions & Pricing Effectiveness', y='Sales Decline',
                             color='Promotions & Pricing Effectiveness',  # Use category for color
                             title='Sales Decline by Promotion Effectiveness')
    st.plotly_chart(fig_promo_sales, use_container_width=True)

with col_d:
    fig_promo_costs = px.bar(filtered_df.groupby('Promotions & Pricing Effectiveness')['Inventory Holding Costs (₱)'].mean().reset_index(),
                             x='Promotions & Pricing Effectiveness', y='Inventory Holding Costs (₱)',
                             color='Promotions & Pricing Effectiveness', # Use category for color
                             title='Avg Holding Costs by Promotion Effectiveness')
    st.plotly_chart(fig_promo_costs, use_container_width=True)

st.markdown("---")

# --- 5. Competition ---
st.header('5. Competition')
st.markdown("Understanding the impact of competitor actions on our sales and market share.")

col_e, col_f = st.columns(2)

with col_e:
    fig_comp_sales = px.scatter(filtered_df, x='Competitor New Stores', y='Sales Decline',
                                color='Region', trendline='ols', # Use Region for color
                                title='Sales Decline vs. Competitor New Stores')
    st.plotly_chart(fig_comp_sales, use_container_width=True)

with col_f:
    fig_comp_share = px.scatter(filtered_df, x='Competitor Ad Spend (₱)', y='Market Share in Region',
                                color='Region', trendline='ols', # Use Region for color
                                title='Market Share vs. Competitor Ad Spend')
    st.plotly_chart(fig_comp_share, use_container_width=True)

st.markdown("---")

# --- 6. Financial Impact ---
st.header('6. Financial Impact')
st.markdown("Visualizing the relationship between sales decline and key financial metrics.")

fig_cost_scatter = px.scatter(filtered_df, x='Sales Decline', y='Inventory Holding Costs (₱)',
                              color='Region', trendline='ols', # Use Region for color
                              title='Inventory Holding Costs vs. Sales Decline')
st.plotly_chart(fig_cost_scatter, use_container_width=True)

fig_share_scatter = px.scatter(filtered_df, x='Sales Decline', y='Market Share in Region',
                               color='Region', trendline='ols', # Use Region for color
                               title='Market Share vs. Sales Decline')
st.plotly_chart(fig_share_scatter, use_container_width=True)

st.markdown("---")

# --- 7. Time-Series Trends ---
st.header('7. Time-Series Trends')
st.markdown("Tracking sales decline over time to spot persistent issues.")

monthly_trends = filtered_df.groupby(['Month', 'Region'])['Sales Decline'].mean().reset_index()
fig_time = px.line(monthly_trends, x='Month', y='Sales Decline', color='Region',
                   markers=True, title='Average Monthly Sales Decline by Region')
st.plotly_chart(fig_time, use_container_width=True)

st.markdown("---")

# --- 8. Top/Bottom 10 Stores ---
st.header('8. Top/Bottom 10 Stores')
st.markdown("Identifying the highest and lowest performing stores at a glance.")

# Get top 10 best and worst performing stores
store_performance = filtered_df.groupby('Store_ID')['Sales Decline'].mean().sort_values(ascending=True)
top_10 = store_performance.head(10)
bottom_10 = store_performance.tail(10)

# Create a combined DataFrame for the bar chart
top_bottom_df = pd.concat([top_10, bottom_10]).reset_index()
top_bottom_df.columns = ['Store_ID', 'Average Sales Decline']
top_bottom_df['Performance'] = ['Best'] * 10 + ['Worst'] * 10

# Use a custom color map for the 'Performance' category
fig_top_bottom = px.bar(
    top_bottom_df,
    x='Average Sales Decline',
    y='Store_ID',
    color='Performance',
    orientation='h',
    color_discrete_map={'Best': 'green', 'Worst': 'red'},
    title='Top 10 Best and Worst Performing Stores by Sales Decline'
)
fig_top_bottom.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_top_bottom, use_container_width=True)
