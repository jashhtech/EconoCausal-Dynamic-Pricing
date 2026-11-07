import pandas as pd
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DOCS_DIR = PROJECT_DIR / "docs"

DATASET_FILE = DATA_DIR / "retail_data.csv"
OUTPUT_FILE = DATA_DIR / "week4_day7_handoff_report.csv"

# Files expected in the project
required_files = [
    "data/marketing_campaign.csv",
    "data/retail_data.csv",
    "data/prepare_dataset.py",
    "data/data_dictionary.csv",
    "data/data_quality_report.csv",
    "data/week4_day1_audit_report.csv",
    "data/week4_day2_quality_checks.csv",
    "data/week4_day3_feature_verification.csv",
    "data/week4_day4_variable_summary.csv",
    "data/week4_day5_reproducibility_report.csv",
    "src/dml_estimation.py",
    "docs/dml_results.md",
    "README.md"
]

print("=" * 55)
print("WEEK 4 - DAY 7 FINAL DATASET HANDOFF")
print("=" * 55)

# 1. Check required files
file_results = []

for relative_path in required_files:
    file_path = PROJECT_DIR / relative_path

    file_results.append({
        "file": relative_path,
        "status": "AVAILABLE" if file_path.exists() else "MISSING"
    })

file_report = pd.DataFrame(file_results)

print("\n1. PROJECT FILE CHECK")
print(file_report.to_string(index=False))

# 2. Validate cleaned dataset
dataset_results = []

if DATASET_FILE.exists():

    df = pd.read_csv(DATASET_FILE)

    print("\n2. DATASET SUMMARY")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Missing values:", df.isnull().sum().sum())
    print("Duplicate rows:", df.duplicated().sum())

    dataset_results.extend([
        {
            "check": "Dataset is not empty",
            "status": "PASS" if len(df) > 0 else "FAIL"
        },
        {
            "check": "No missing values",
            "status": "PASS" if df.isnull().sum().sum() == 0 else "FAIL"
        },
        {
            "check": "No duplicate rows",
            "status": "PASS" if df.duplicated().sum() == 0 else "FAIL"
        }
    ])

    required_features = [
        "age",
        "total_purchase_amount",
        "total_purchases",
        "deal_purchase_indicator",
        "campaign_exposure",
        "campaign_response"
    ]

    for feature in required_features:
        exists = feature in df.columns

        dataset_results.append({
            "check": f"Feature available: {feature}",
            "status": "PASS" if exists else "FAIL"
        })

else:
    print("\nCleaned dataset is missing.")

    dataset_results.append({
        "check": "Cleaned dataset exists",
        "status": "FAIL"
    })

# 3. Combine results
dataset_report = pd.DataFrame(dataset_results)

print("\n3. DATASET VALIDATION")
print(dataset_report.to_string(index=False))

# 4. Save handoff report
file_report["category"] = "Project file"
dataset_report["category"] = "Dataset validation"

file_report = file_report.rename(columns={
    "file": "item"
})

dataset_report = dataset_report.rename(columns={
    "check": "item"
})

final_report = pd.concat(
    [
        file_report[["category", "item", "status"]],
        dataset_report[["category", "item", "status"]]
    ],
    ignore_index=True
)

final_report.to_csv(OUTPUT_FILE, index=False)

print("\n4. FINAL HANDOFF SUMMARY")

available = (file_report["status"] == "AVAILABLE").sum()
missing = (file_report["status"] == "MISSING").sum()

print("Available project files:", available)
print("Missing project files:", missing)

passed = (dataset_report["status"] == "PASS").sum()
failed = (dataset_report["status"] == "FAIL").sum()

print("Dataset checks passed:", passed)
print("Dataset checks failed:", failed)

print("\nReport saved to:", OUTPUT_FILE)

if missing == 0 and failed == 0:
    print("\nHANDOFF STATUS: ALL CHECKS PASSED")
else:
    print("\nHANDOFF STATUS: REVIEW REQUIRED")
    print("Check missing files and failed validations.")
    