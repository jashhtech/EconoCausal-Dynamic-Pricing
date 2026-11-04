import pandas as pd
from pathlib import Path

# File paths
DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "retail_data.csv"
OUTPUT_FILE = DATA_DIR / "week4_day4_variable_summary.csv"

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

# Candidate variables for DML
variables = {
    "campaign_exposure": {
        "role": "Candidate Treatment",
        "description": "Indicates acceptance of at least one of five campaigns."
    },
    "campaign_response": {
        "role": "Candidate Outcome",
        "description": "Customer response copied from the original Response column."
    },
    "Income": {
        "role": "Candidate Confounder",
        "description": "Customer income."
    },
    "age": {
        "role": "Candidate Confounder",
        "description": "Customer age."
    },
    "Kidhome": {
        "role": "Candidate Confounder",
        "description": "Number of children at home."
    },
    "Teenhome": {
        "role": "Candidate Confounder",
        "description": "Number of teenagers at home."
    },
    "Recency": {
        "role": "Candidate Confounder",
        "description": "Days since the customer's last purchase."
    },
    "NumWebVisitsMonth": {
        "role": "Candidate Confounder",
        "description": "Number of website visits per month."
    }
}

results = []

for column, information in variables.items():
    exists = column in df.columns

    if exists:
        results.append({
            "variable": column,
            "proposed_role": information["role"],
            "description": information["description"],
            "available_in_dataset": "Yes",
            "missing_values": int(df[column].isna().sum()),
            "unique_values": int(df[column].nunique())
        })
    else:
        results.append({
            "variable": column,
            "proposed_role": information["role"],
            "description": information["description"],
            "available_in_dataset": "No",
            "missing_values": None,
            "unique_values": None
        })

report = pd.DataFrame(results)
report.to_csv(OUTPUT_FILE, index=False)

print("WEEK 4 - DAY 4 VARIABLE DOCUMENTATION")
print("-" * 50)
print(report.to_string(index=False))

print("\nTotal candidate variables:", len(report))
print("Available variables:", (report["available_in_dataset"] == "Yes").sum())
print("Missing variables:", (report["available_in_dataset"] == "No").sum())

print("\nSummary saved to:", OUTPUT_FILE)
