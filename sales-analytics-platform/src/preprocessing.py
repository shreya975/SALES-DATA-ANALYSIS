import pandas as pd
import numpy as np

RAW_PATH = "data/raw/sales_raw.csv"
PROCESSED_PATH = "data/processed/sales_cleaned.csv"


# ----------------------------------------
# 1. Load Data
# ----------------------------------------

def load_data(path=RAW_PATH):
    df = pd.read_csv(path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df


# ----------------------------------------
# 2. Data Validation & Cleaning
# ----------------------------------------

def clean_data(df):

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove negative values
    df = df[df["Quantity"] > 0]
    df = df[df["Unit_Price"] > 0]

    # Handle missing values
    df = df.fillna({
        "Discount_%": 0,
        "Profit_Margin": 0
    })

    return df


# ----------------------------------------
# 3. Feature Engineering
# ----------------------------------------

def engineer_features(df):

    # Time Features
    df["Month_Name"] = df["Order_Date"].dt.month_name()
    df["Day"] = df["Order_Date"].dt.day
    df["Weekday"] = df["Order_Date"].dt.day_name()

    # Order Value
    df["Order_Value"] = df["Revenue"]

    # Profit Margin %
    df["Profit_Margin_%"] = (df["Profit"] / df["Revenue"]) * 100

    # Customer Lifetime Value (Basic)
    clv = df.groupby("Customer_ID")["Revenue"].sum().reset_index()
    clv.columns = ["Customer_ID", "Customer_Lifetime_Value"]
    df = df.merge(clv, on="Customer_ID", how="left")

    return df


# ----------------------------------------
# 4. Monthly Aggregation for Growth
# ----------------------------------------

def calculate_growth_metrics(df):

    monthly = df.groupby(["Year", "Month"])["Revenue"].sum().reset_index()
    monthly["Date"] = pd.to_datetime(
        monthly["Year"].astype(str) + "-" +
        monthly["Month"].astype(str) + "-01"
    )

    monthly = monthly.sort_values("Date")

    # MoM Growth
    monthly["MoM_Growth_%"] = monthly["Revenue"].pct_change() * 100

    # YoY Growth
    monthly["YoY_Growth_%"] = monthly["Revenue"].pct_change(12) * 100

    return monthly


# ----------------------------------------
# 5. Save Processed Data
# ----------------------------------------

def save_processed_data(df, path=PROCESSED_PATH):
    df.to_csv(path, index=False)


# ----------------------------------------
# MAIN EXECUTION
# ----------------------------------------

if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)
    df = engineer_features(df)
    save_processed_data(df)

    print("✅ Data cleaning and feature engineering completed.")
