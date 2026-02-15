import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ----------------------------------------
# 1. CREATE RFM TABLE
# ----------------------------------------

def create_rfm(df):

    snapshot_date = df["Order_Date"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("Customer_ID").agg({
        "Order_Date": lambda x: (snapshot_date - x.max()).days,
        "Order_ID": "count",
        "Revenue": "sum"
    }).reset_index()

    rfm.columns = ["Customer_ID", "Recency", "Frequency", "Monetary"]

    return rfm


# ----------------------------------------
# 2. RFM SCORING (Quantile-based)
# ----------------------------------------

def rfm_scoring(rfm):

    rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4])

    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str) +
        rfm["F_Score"].astype(str) +
        rfm["M_Score"].astype(str)
    )

    return rfm


# ----------------------------------------
# 3. KMEANS CLUSTERING
# ----------------------------------------

def apply_kmeans(rfm, n_clusters=4):

    features = rfm[["Recency", "Frequency", "Monetary"]]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    rfm["Cluster"] = kmeans.fit_predict(scaled_features)

    return rfm


# ----------------------------------------
# 4. ASSIGN SEGMENT LABELS
# ----------------------------------------

def label_segments(rfm):

    cluster_summary = rfm.groupby("Cluster")[["Recency","Frequency","Monetary"]].mean()

    cluster_order = cluster_summary.sort_values(
        ["Monetary","Frequency"], ascending=False
    ).index.tolist()

    segment_labels = {
        cluster_order[0]: "Champions",
        cluster_order[1]: "Loyal Customers",
        cluster_order[2]: "Potential Loyalists",
        cluster_order[3]: "At Risk"
    }

    rfm["Segment"] = rfm["Cluster"].map(segment_labels)

    return rfm


# ----------------------------------------
# MAIN FUNCTION
# ----------------------------------------

def run_segmentation(df):

    rfm = create_rfm(df)
    rfm = rfm_scoring(rfm)
    rfm = apply_kmeans(rfm)
    rfm = label_segments(rfm)

    return rfm
