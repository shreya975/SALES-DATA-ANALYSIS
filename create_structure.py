import os

structure = {
    "sales-analytics-platform": {
        "data": {
            "raw": {
                "sales_raw.csv": ""
            },
            "processed": {
                "sales_cleaned.csv": ""
            },
            "external": {}
        },
        "notebooks": {
            "01_data_exploration.ipynb": "",
            "02_feature_engineering.ipynb": "",
            "03_modeling.ipynb": ""
        },
        "src": {
            "data_loader.py": "",
            "preprocessing.py": "",
            "kpi.py": "",
            "visualization.py": "",
            "forecasting.py": "",
            "segmentation.py": "",
            "utils.py": ""
        },
        "streamlit_app": {
            "app.py": ""
        },
        "powerbi": {
            "dashboard.pbix": ""
        },
        "requirements.txt": "",
        "README.md": ""
    }
}

def create_structure(base_path, tree):
    for name, content in tree.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

# Run the generator
create_structure(".", structure)

print("Sales Analytics Platform structure created successfully!")
