# ==========================================================
# 🪵 SALES DATA ANALYSIS PLATFORM
# ==========================================================

import sys
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.kpi import executive_summary
from src.segmentation import run_segmentation
from src.forecasting import run_forecasting

st.set_page_config(page_title="SALES DATA ANALYSIS PLATFORM", layout="wide")

# ================= DESIGN SYSTEM =================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600&display=swap');

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #2E1F1B, #5E4B43);
    color: #F3EDE7;
    font-family: 'Inter', sans-serif;
}

.header-panel {
    background: rgba(255,255,255,0.06);
    padding: 60px;
    border-radius: 50px;
    box-shadow: 0px 30px 70px rgba(0,0,0,0.6);
    margin-bottom: 50px;
}

.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 48px;
}

.header-subtitle {
    font-size: 20px;
    opacity: 0.85;
    margin-top: 15px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 34px;
    margin-bottom: 35px;
}

.scorecard {
    background: rgba(255,255,255,0.07);
    padding: 25px;
    border-radius: 35px;
    text-align: center;
    font-size: 20px;
}

.insight-box {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 40px;
    font-size: 18px;
    line-height: 1.6;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================

st.markdown("""
<div class="header-panel">
    <div class="header-title">SALES DATA ANALYSIS PLATFORM</div>
    <div class="header-subtitle">
        Executive Strategy • Revenue Optimization • Predictive Intelligence
    </div>
</div>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================

@st.cache_data
def load_data():
    path = os.path.join(PROJECT_ROOT, "data", "processed", "sales_cleaned.csv")
    df = pd.read_csv(path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

# ================= STRATEGIC SCORING =================

def calculate_business_scores(df):
    monthly = df.groupby(["Year","Month"])["Revenue"].sum().reset_index()
    monthly["Date"] = pd.to_datetime(
        monthly["Year"].astype(str)+"-"+monthly["Month"].astype(str)+"-01"
    )

    growth = monthly["Revenue"].pct_change().mean()
    momentum = min(max((growth*100)+50,0),100)

    volatility = monthly["Revenue"].std()/monthly["Revenue"].mean()
    stability = min(max(100-(volatility*100),0),100)

    product_share = df.groupby("Product")["Revenue"].sum()
    top_share = product_share.max()/product_share.sum()
    diversification = min(max((1-top_share)*100,0),100)

    margin = df["Profit"].sum()/df["Revenue"].sum()
    profitability = min(max(margin*200,0),100)

    overall = np.mean([momentum,stability,diversification,profitability])

    return {
        "Momentum": round(momentum,1),
        "Stability": round(stability,1),
        "Diversification": round(diversification,1),
        "Profitability": round(profitability,1),
        "Business Health": round(overall,1)
    }

# ================= NAVIGATION =================

modules = [
    "Executive Overview",
    "Product Intelligence",
    "Regional Matrix",
    "Customer Segmentation",
    "Forecast Strategy"
]

selected = st.selectbox("Select Module", modules)

# ================= EXECUTIVE OVERVIEW =================

if selected == "Executive Overview":

    st.markdown("<div class='section-title'>Executive Overview</div>", unsafe_allow_html=True)

    kpis = executive_summary(df)
    scores = calculate_business_scores(df)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Revenue", f"₹{kpis['Total Revenue']:,.0f}")
    c2.metric("Total Profit", f"₹{kpis['Total Profit']:,.0f}")
    c3.metric("Profit Margin", f"{kpis['Profit Margin %']}%")
    c4.metric("Avg Order Value", f"₹{kpis['Average Order Value']:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    s1,s2,s3,s4,s5 = st.columns(5)
    s1.markdown(f"<div class='scorecard'>Momentum<br><b>{scores['Momentum']}</b></div>", unsafe_allow_html=True)
    s2.markdown(f"<div class='scorecard'>Stability<br><b>{scores['Stability']}</b></div>", unsafe_allow_html=True)
    s3.markdown(f"<div class='scorecard'>Diversification<br><b>{scores['Diversification']}</b></div>", unsafe_allow_html=True)
    s4.markdown(f"<div class='scorecard'>Profitability<br><b>{scores['Profitability']}</b></div>", unsafe_allow_html=True)
    s5.markdown(f"<div class='scorecard'>Business Health<br><b>{scores['Business Health']}</b></div>", unsafe_allow_html=True)

    monthly = df.groupby(["Year","Month"])["Revenue"].sum().reset_index()
    monthly["Date"] = pd.to_datetime(monthly["Year"].astype(str)+"-"+monthly["Month"].astype(str)+"-01")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Date"],
        y=monthly["Revenue"],
        line=dict(color="#F3EDE7", width=5),
        fill="tozeroy",
        fillcolor="rgba(243,237,231,0.1)"
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=16,color="#F3EDE7")
    )

    st.plotly_chart(fig, use_container_width=True)

# ================= PRODUCT INTELLIGENCE =================

elif selected == "Product Intelligence":

    st.markdown("<div class='section-title'>Product Intelligence</div>", unsafe_allow_html=True)

    product = df.groupby("Product")["Revenue"].sum().sort_values().tail(10).reset_index()

    fig = px.bar(product, x="Revenue", y="Product", orientation="h",
                 color="Revenue", color_continuous_scale=["#3A2A25","#E8DFD8"])

    fig.update_layout(font=dict(size=16,color="#F3EDE7"))
    st.plotly_chart(fig, use_container_width=True)

# ================= REGIONAL MATRIX =================

elif selected == "Regional Matrix":

    st.markdown("<div class='section-title'>Regional Matrix</div>", unsafe_allow_html=True)

    region = df.groupby("Region")["Revenue"].sum().reset_index()

    fig = px.bar(region, x="Revenue", y="Region", orientation="h",
                 color="Revenue", color_continuous_scale=["#5E4B43","#E8DFD8"])

    fig.update_layout(font=dict(size=16,color="#F3EDE7"))
    st.plotly_chart(fig, use_container_width=True)

# ================= CUSTOMER SEGMENTATION =================

elif selected == "Customer Segmentation":

    st.markdown("<div class='section-title'>Customer Segmentation</div>", unsafe_allow_html=True)

    rfm = run_segmentation(df)
    seg = rfm["Segment"].value_counts().reset_index()
    seg.columns = ["Segment","Count"]

    fig = px.pie(seg, names="Segment", values="Count", hole=0.6,
                 color_discrete_sequence=["#E8DFD8","#C7B5AC","#A68A7B","#8C6F63"])

    fig.update_layout(font=dict(size=16,color="#F3EDE7"))
    st.plotly_chart(fig, use_container_width=True)

# ================= FORECAST STRATEGY =================

elif selected == "Forecast Strategy":

    st.markdown("<div class='section-title'>Forecast Strategy</div>", unsafe_allow_html=True)

    monthly, test_results, future_forecast, metrics = run_forecasting(df)

    st.metric("Model R² Score", f"{metrics['R2 Score']:.3f}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Date"],
        y=monthly["Revenue"],
        name="Actual",
        line=dict(color="#F3EDE7", width=5)
    ))
    fig.add_trace(go.Scatter(
        x=future_forecast["Date"],
        y=future_forecast["Forecasted_Revenue"],
        name="Forecast",
        line=dict(color="#C7B5AC", width=5, dash="dot")
    ))

    fig.update_layout(font=dict(size=16,color="#F3EDE7"))
    st.plotly_chart(fig, use_container_width=True)
