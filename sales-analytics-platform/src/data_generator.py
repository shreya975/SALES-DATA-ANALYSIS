import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# -----------------------------------
# CONFIGURATION
# -----------------------------------

START_DATE = "2019-01-01"
END_DATE = "2023-12-31"
TOTAL_ROWS = 7500

# Yearly Growth Factors
YEAR_GROWTH = {
    2019: 1.0,
    2020: 0.85,
    2021: 1.10,
    2022: 1.25,
    2023: 1.40
}

# Seasonal Multipliers
MONTH_MULTIPLIER = {
    1: 1.10,
    2: 0.90,
    3: 1.00,
    4: 1.00,
    5: 1.05,
    6: 1.15,
    7: 0.95,
    8: 1.00,
    9: 1.05,
    10: 1.30,
    11: 1.25,
    12: 1.20
}

# Cities & Regions
CITY_REGION = {
    "Mumbai": "West",
    "Delhi": "North",
    "Bangalore": "South",
    "Hyderabad": "South",
    "Chennai": "South",
    "Pune": "West",
    "Kolkata": "East",
    "Ahmedabad": "West"
}

CATEGORIES = {
    "Electronics": ["Laptop", "Smartphone", "Headphones", "Smartwatch"],
    "Fashion": ["T-shirt", "Jeans", "Shoes", "Jacket"],
    "Home & Kitchen": ["Mixer", "Microwave", "Cookware Set", "Sofa"],
    "Grocery": ["Rice", "Cooking Oil", "Snacks"],
    "Accessories": ["Backpack", "Sunglasses", "Wallet"]
}

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "COD"]

# -----------------------------------
# PRICE GENERATOR
# -----------------------------------

def generate_price(category):
    price_ranges = {
        "Electronics": (5000, 80000),
        "Fashion": (500, 5000),
        "Home & Kitchen": (1000, 25000),
        "Grocery": (100, 2000),
        "Accessories": (300, 4000)
    }
    return round(np.random.uniform(*price_ranges[category]), 2)

# -----------------------------------
# CUSTOMER GENERATION
# -----------------------------------

CUSTOMER_IDS = [f"CUST_{i}" for i in range(1, 1201)]

def generate_customer():
    customer_id = random.choice(CUSTOMER_IDS)
    age = np.random.choice(
        [np.random.randint(18,25),
         np.random.randint(26,35),
         np.random.randint(36,50),
         np.random.randint(50,65)],
        p=[0.2, 0.35, 0.3, 0.15]
    )
    gender = np.random.choice(["Male", "Female"], p=[0.55, 0.45])
    city = random.choice(list(CITY_REGION.keys()))
    region = CITY_REGION[city]
    return customer_id, age, gender, city, region

# -----------------------------------
# MAIN DATA GENERATION
# -----------------------------------

def generate_sales_data():
    data = []
    date_range = pd.date_range(start=START_DATE, end=END_DATE)

    for i in range(TOTAL_ROWS):
        order_date = random.choice(date_range)
        year = order_date.year
        month = order_date.month
        quarter = (month - 1) // 3 + 1

        growth_factor = YEAR_GROWTH[year]
        seasonal_factor = MONTH_MULTIPLIER[month]

        # COVID dip logic
        if year == 2020 and month in [4,5,6,7,8]:
            seasonal_factor *= 0.75

        category = random.choice(list(CATEGORIES.keys()))
        product = random.choice(CATEGORIES[category])

        unit_price = generate_price(category)
        quantity = np.random.randint(1, 5)

        discount = round(np.random.uniform(0, 0.1), 2)
        if month in [10, 11]:
            discount = round(np.random.uniform(0.1, 0.3), 2)

        cost_price = round(unit_price * np.random.uniform(0.6, 0.75), 2)

        revenue = unit_price * quantity * (1 - discount)
        revenue *= growth_factor * seasonal_factor

        profit = revenue - (cost_price * quantity)
        profit_margin = profit / revenue if revenue > 0 else 0

        payment_method = np.random.choice(
            PAYMENT_METHODS,
            p=[0.4, 0.3, 0.2, 0.1]
        )

        customer_id, age, gender, city, region = generate_customer()

        data.append([
            f"ORD_{i+1}",
            order_date,
            year,
            month,
            quarter,
            customer_id,
            age,
            gender,
            city,
            region,
            product,
            category,
            quantity,
            unit_price,
            discount,
            cost_price,
            payment_method,
            round(revenue,2),
            round(profit,2),
            round(profit_margin,2)
        ])

    columns = [
        "Order_ID","Order_Date","Year","Month","Quarter",
        "Customer_ID","Age","Gender","City","Region",
        "Product","Category","Quantity","Unit_Price",
        "Discount_%","Cost_Price","Payment_Method",
        "Revenue","Profit","Profit_Margin"
    ]

    df = pd.DataFrame(data, columns=columns)
    return df


if __name__ == "__main__":
    df = generate_sales_data()
    df.to_csv("data/raw/sales_raw.csv", index=False)
    print("✅ Enterprise sales dataset generated successfully!")

