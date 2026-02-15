import os

# Base directory
base_dir = "sales-analytics-platform"

# Folder structure
folders = [
    "data/raw",
    "data/processed",
    "data/external",
    "notebooks",
    "src",
    "streamlit_app",
    "powerbi",
    "visuals"
]

# Files to create
files = [
    "data/raw/sales_raw.csv",
    "data/processed/sales_cleaned.csv",

    "notebooks/01_eda.ipynb",
    "notebooks/02_feature_engineering.ipynb",
    "notebooks/03_modeling.ipynb",

    "src/data_generator.py",
    "src/data_loader.py",
    "src/preprocessing.py",
    "src/kpi.py",
    "src/forecasting.py",
    "src/segmentation.py",
    "src/utils.py",

    "streamlit_app/app.py",
    "powerbi/dashboard.pbix",

    "requirements.txt",
    "README.md"
]

# Create folders
for folder in folders:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

# Create empty files
for file in files:
    file_path = os.path.join(base_dir, file)
    with open(file_path, "w") as f:
        pass  # Creates an empty file

print("Project structure created successfully!")
