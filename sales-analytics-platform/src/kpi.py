import pandas as pd

# -----------------------------------------
# 1. EXECUTIVE SUMMARY KPIs
# -----------------------------------------

def executive_summary(df):

    total_revenue = df["Revenue"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()
    total_customers = df["Customer_ID"].nunique()

    avg_order_value = total_revenue / total_orders
    profit_margin = (total_profit / total_revenue) * 100

    repeat_customers = df["Customer_ID"].value_counts()
    repeat_rate = (repeat_customers[repeat_customers > 1].count() 
                   / total_customers) * 100

    return {
        "Total Revenue": round(total_revenue, 2),
        "Total Profit": round(total_profit, 2),
        "Profit Margin %": round(profit_margin, 2),
        "Total Orders": total_orders,
        "Total Customers": total_customers,
        "Average Order Value": round(avg_order_value, 2),
        "Repeat Purchase Rate %": round(repeat_rate, 2)
    }


# -----------------------------------------
# 2. GROWTH METRICS
# -----------------------------------------

def growth_metrics(df):

    monthly = df.groupby(["Year", "Month"])["Revenue"].sum().reset_index()
    monthly["Date"] = pd.to_datetime(
        monthly["Year"].astype(str) + "-" +
        monthly["Month"].astype(str) + "-01"
    )
    monthly = monthly.sort_values("Date")

    monthly["MoM_Growth_%"] = monthly["Revenue"].pct_change() * 100
    monthly["YoY_Growth_%"] = monthly["Revenue"].pct_change(12) * 100

    latest = monthly.iloc[-1]

    return {
        "Latest MoM Growth %": round(latest["MoM_Growth_%"], 2),
        "Latest YoY Growth %": round(latest["YoY_Growth_%"], 2)
    }


# -----------------------------------------
# 3. PRODUCT PERFORMANCE
# -----------------------------------------

def product_performance(df):

    product_rev = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)

    top_5 = product_rev.head(5)
    bottom_5 = product_rev.tail(5)

    category_rev = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)

    return top_5, bottom_5, category_rev


# -----------------------------------------
# 4. REGIONAL PERFORMANCE
# -----------------------------------------

def regional_performance(df):

    region_rev = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
    region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)

    return region_rev, region_profit


# -----------------------------------------
# 5. CUSTOMER INSIGHTS
# -----------------------------------------

def customer_insights(df):

    clv = df.groupby("Customer_ID")["Revenue"].sum().sort_values(ascending=False)

    high_value = clv.head(10)

    age_group = pd.cut(
        df["Age"],
        bins=[18,25,35,50,70],
        labels=["18-25","26-35","36-50","50+"]
    )

    age_revenue = df.groupby(age_group)["Revenue"].sum()

    return high_value, age_revenue
