# ==========================================================
# 📊 ENTERPRISE SALES ANALYTICS DASHBOARD
# ==========================================================

import sys
import os

# ----------------------------------------------------------
# FIX: Add project root to Python path
# ----------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.kpi import executive_summary
from src.segmentation import run_segmentation
from src.forecasting import run_forecasting

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------

st.set_page_config(
    page_title="Enterprise Sales Analytics",
    layout="wide"
)

# ----------------------------------------------------------
# CUSTOM CSS (Corporate Look)
# ----------------------------------------------------------

st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Enterprise Sales Analytics Platform")
st.markdown("---")

# ----------------------------------------------------------
# LOAD DATA (Using absolute path)
# ----------------------------------------------------------

@st.cache_data
def load_data():
    data_path = os.path.join(PROJECT_ROOT, "data", "processed", "sales_cleaned.csv")
    df = pd.read_csv(data_path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

# ----------------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------------

st.sidebar.header("🔎 Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Order_Date"].min(), df["Order_Date"].max()]
)

# Apply Filters
filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category)) &
    (df["Order_Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order_Date"] <= pd.to_datetime(date_range[1]))
]

# ----------------------------------------------------------
# PAGE NAVIGATION
# ----------------------------------------------------------

page = st.sidebar.radio("Navigate", [
    "Executive Overview",
    "Product Analysis",
    "Regional Insights",
    "Customer Intelligence",
    "Forecasting"
])

# ==========================================================
# 🏠 EXECUTIVE OVERVIEW
# ==========================================================

if page == "Executive Overview":

    st.markdown("## 🏠 Executive Overview")

    kpis = executive_summary(filtered_df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"₹{kpis['Total Revenue']:,.0f}")
    col2.metric("Total Profit", f"₹{kpis['Total Profit']:,.0f}")
    col3.metric("Profit Margin %", f"{kpis['Profit Margin %']}%")
    col4.metric("Avg Order Value", f"₹{kpis['Average Order Value']:,.0f}")

    st.markdown("---")
    st.subheader("📈 Monthly Revenue Trend")

    monthly = filtered_df.groupby(["Year", "Month"])["Revenue"].sum().reset_index()
    monthly["Date"] = pd.to_datetime(
        monthly["Year"].astype(str) + "-" +
        monthly["Month"].astype(str) + "-01"
    )
    monthly = monthly.sort_values("Date")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(monthly["Date"], monthly["Revenue"], marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    ax.set_title("Monthly Revenue Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.download_button(
        label="📥 Download Filtered Data",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_sales.csv",
        mime="text/csv"
    )

# ==========================================================
# 📦 PRODUCT ANALYSIS
# ==========================================================

elif page == "Product Analysis":

    st.markdown("## 📦 Product Performance")

    product_rev = filtered_df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    product_rev.head(10).plot(kind="bar", ax=ax)
    ax.set_title("Top 10 Products by Revenue")
    ax.set_ylabel("Revenue")
    st.pyplot(fig)

# ==========================================================
# 🌍 REGIONAL INSIGHTS
# ==========================================================

elif page == "Regional Insights":

    st.markdown("## 🌍 Regional Performance")

    region_rev = filtered_df.groupby("Region")["Revenue"].sum().sort_values()

    fig, ax = plt.subplots(figsize=(8, 5))
    region_rev.plot(kind="barh", ax=ax)
    ax.set_title("Revenue by Region")
    ax.set_xlabel("Revenue")
    st.pyplot(fig)

# ==========================================================
# 👤 CUSTOMER INTELLIGENCE
# ==========================================================

elif page == "Customer Intelligence":

    st.markdown("## 👤 Customer Segmentation (RFM + KMeans)")

    rfm = run_segmentation(filtered_df)

    segment_counts = rfm["Segment"].value_counts()

    fig, ax = plt.subplots()
    segment_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    ax.set_title("Customer Segment Distribution")
    st.pyplot(fig)

# ==========================================================
# 🔮 FORECASTING
# ==========================================================

elif page == "Forecasting":

    st.markdown("## 🔮 Revenue Forecasting")

    monthly, test_results, future_forecast, metrics = run_forecasting(filtered_df)

    st.subheader("Model Performance")
    st.write(metrics)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(monthly["Date"], monthly["Revenue"], label="Actual")
    ax.plot(test_results["Date"], test_results["Predicted_Revenue"], label="Predicted 2023")
    ax.plot(future_forecast["Date"], future_forecast["Forecasted_Revenue"], label="Forecast 2024")
    ax.legend()

    ax.set_title("Revenue Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")

    st.pyplot(fig)

# ----------------------------------------------------------
# FOOTER
# ----------------------------------------------------------

st.markdown("---")
st.markdown("Developed by Shreya | Enterprise Sales Analytics Platform 🚀")
