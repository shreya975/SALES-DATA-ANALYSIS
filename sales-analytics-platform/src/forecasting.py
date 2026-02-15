import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ----------------------------------------
# 1. PREPARE MONTHLY DATA
# ----------------------------------------

def prepare_monthly_data(df):

    monthly = df.groupby(["Year", "Month"])["Revenue"].sum().reset_index()
    monthly["Date"] = pd.to_datetime(
        monthly["Year"].astype(str) + "-" +
        monthly["Month"].astype(str) + "-01"
    )

    monthly = monthly.sort_values("Date")

    # Time Index
    monthly["Time_Index"] = np.arange(len(monthly))

    # Month as cyclical feature
    monthly["Month_Sin"] = np.sin(2 * np.pi * monthly["Month"] / 12)
    monthly["Month_Cos"] = np.cos(2 * np.pi * monthly["Month"] / 12)

    return monthly


# ----------------------------------------
# 2. TRAIN MODEL
# ----------------------------------------

def train_model(monthly):

    # Train: 2019-2022
    train = monthly[monthly["Year"] < 2023]
    test = monthly[monthly["Year"] == 2023]

    features = ["Time_Index", "Month_Sin", "Month_Cos"]

    X_train = train[features]
    y_train = train["Revenue"]

    X_test = test[features]
    y_test = test["Revenue"]

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    test_results = test.copy()
    test_results["Predicted_Revenue"] = y_pred

    metrics = {
        "RMSE": round(rmse, 2),
        "R2 Score": round(r2, 3)
    }

    return model, test_results, metrics


# ----------------------------------------
# 3. FORECAST NEXT 12 MONTHS
# ----------------------------------------

def forecast_future(model, monthly):

    last_index = monthly["Time_Index"].max()
    future_dates = pd.date_range(
        start=monthly["Date"].max() + pd.DateOffset(months=1),
        periods=12,
        freq="MS"
    )

    future_df = pd.DataFrame({
        "Date": future_dates
    })

    future_df["Year"] = future_df["Date"].dt.year
    future_df["Month"] = future_df["Date"].dt.month

    future_df["Time_Index"] = np.arange(
        last_index + 1,
        last_index + 13
    )

    future_df["Month_Sin"] = np.sin(2 * np.pi * future_df["Month"] / 12)
    future_df["Month_Cos"] = np.cos(2 * np.pi * future_df["Month"] / 12)

    features = ["Time_Index", "Month_Sin", "Month_Cos"]

    future_df["Forecasted_Revenue"] = model.predict(future_df[features])

    return future_df


# ----------------------------------------
# MAIN PIPELINE
# ----------------------------------------

def run_forecasting(df):

    monthly = prepare_monthly_data(df)
    model, test_results, metrics = train_model(monthly)
    future_forecast = forecast_future(model, monthly)

    return monthly, test_results, future_forecast, metrics
