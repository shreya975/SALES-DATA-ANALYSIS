# ==========================================================
# 💎 PREMIUM ENTERPRISE SALES ANALYTICS DASHBOARD
# ==========================================================

import sys
import os

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
    page_title="Enterprise Sales Intelligence",
    layout="wide"
)

# ----------------------------------------------------------
# PREMIUM CSS
# ----------------------------------------------------------

st.markdown("""
<style>
.metric-card {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}
.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #1f4e79;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='section-title'>📊 Enterprise Sales Intelligence Platform</div>", unsafe_allow_html=True)
st.markdown("---")

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

@st.cache_data
def load_data():
    path = os.path.join(PROJECT_ROOT, "data", "processed", "sales_cleaned.csv")
    df = pd.read_csv(path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------

st.sidebar.header("🔎 Filters")

selected_region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Order_Date"].min(), df["Order_Date"].max()]
)

filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category)) &
    (df["Order_Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order_Date"] <= pd.to_datetime(date_range[1]))
]

page = st.sidebar.radio("Navigate", [
    "Executive Overview",
    "Product Performance",
    "Regional Insights",
    "Customer Intelligence",
    "Forecasting"
])

# ==========================================================
# 🏠 EXECUTIVE OVERVIEW
# ==========================================================

if page == "Executive Overview":

    st.markdown("<div class='section-title'>Executive Overview</div>", unsafe_allow_html=True)

    kpis = executive_summary(filtered_df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"₹{kpis['Total Revenue']:,.0f}")
    col2.metric("Total Profit", f"₹{kpis['Total Profit']:,.0f}")
    col3.metric("Profit Margin", f"{kpis['Profit Margin %']}%")
    col4.metric("Avg Order Value", f"₹{kpis['Average Order Value']:,.0f}")

    st.markdown("---")

    colA, colB = st.columns(2)

    # Revenue Trend
    monthly = filtered_df.groupby(["Year","Month"])["Revenue"].sum().reset_index()
    monthly["Date"] = pd.to_datetime(
        monthly["Year"].astype(str) + "-" +
        monthly["Month"].astype(str) + "-01"
    )
    monthly = monthly.sort_values("Date")

    with colA:
        st.subheader("📈 Revenue Trend")
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(monthly["Date"], monthly["Revenue"], marker="o", color="#1f4e79")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with colB:
        st.subheader("💰 Profit Trend")
        profit_monthly = filtered_df.groupby(["Year","Month"])["Profit"].sum().reset_index()
        profit_monthly["Date"] = pd.to_datetime(
            profit_monthly["Year"].astype(str) + "-" +
            profit_monthly["Month"].astype(str) + "-01"
        )
        profit_monthly = profit_monthly.sort_values("Date")

        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.plot(profit_monthly["Date"], profit_monthly["Profit"], marker="o", color="green")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    st.markdown("### 📌 Key Insight")
    st.info("Revenue shows strong seasonal spikes during festive months with steady post-COVID recovery trend.")

# ==========================================================
# 📦 PRODUCT PERFORMANCE
# ==========================================================

elif page == "Product Performance":

    st.markdown("<div class='section-title'>Product Performance</div>", unsafe_allow_html=True)

    product_rev = filtered_df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10,5))
    product_rev.head(10).plot(kind="bar", ax=ax, color="#1f4e79")
    st.pyplot(fig)

    st.info("Top 10 products contribute majority of revenue — inventory optimization recommended.")

# ==========================================================
# 🌍 REGIONAL INSIGHTS
# ==========================================================

elif page == "Regional Insights":

    st.markdown("<div class='section-title'>Regional Insights</div>", unsafe_allow_html=True)

    region_rev = filtered_df.groupby("Region")["Revenue"].sum().sort_values()

    fig, ax = plt.subplots(figsize=(8,4))
    region_rev.plot(kind="barh", ax=ax, color="#1f4e79")
    st.pyplot(fig)

# ==========================================================
# 👤 CUSTOMER INTELLIGENCE
# ==========================================================

elif page == "Customer Intelligence":

    st.markdown("<div class='section-title'>Customer Intelligence</div>", unsafe_allow_html=True)

    rfm = run_segmentation(filtered_df)

    segment_counts = rfm["Segment"].value_counts()

    fig, ax = plt.subplots()
    segment_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

# ==========================================================
# 🔮 FORECASTING
# ==========================================================

elif page == "Forecasting":

    st.markdown("<div class='section-title'>Revenue Forecasting</div>", unsafe_allow_html=True)

    monthly, test_results, future_forecast, metrics = run_forecasting(filtered_df)

    st.metric("Model R² Score", metrics["R2 Score"])

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(monthly["Date"], monthly["Revenue"], label="Actual", color="#1f4e79")
    ax.plot(test_results["Date"], test_results["Predicted_Revenue"], label="Predicted", color="orange")
    ax.plot(future_forecast["Date"], future_forecast["Forecasted_Revenue"], label="Forecast", color="green")
    ax.legend()
    st.pyplot(fig)

# ----------------------------------------------------------
# FOOTER
# ----------------------------------------------------------

st.markdown("---")
st.markdown("Developed by Shreya | Premium Enterprise Analytics Platform 🚀")
