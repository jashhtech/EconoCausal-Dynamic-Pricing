import pandas as pd
from pathlib import Path

# Project paths
DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "retail_data.csv"
OUTPUT_FILE = DATA_DIR / "week4_day2_quality_checks.csv"

# Load dataset
if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

print("WEEK 4 - DAY 2 DATA QUALITY CHECKS")
print("-" * 45)

checks = []

def add_check(name, condition, details):
    checks.append({
        "check_name": name,
        "status": "PASS" if condition else "FAIL",
        "details": details
    })

# 1. Dataset dimensions
print("Dataset shape:", df.shape)
add_check(
    "Dataset is not empty",
    len(df) > 0 and len(df.columns) > 0,
    f"Rows: {len(df)}, Columns: {len(df.columns)}"
)

# 2. Missing values
missing_count = int(df.isnull().sum().sum())
print("Missing values:", missing_count)
add_check(
    "Missing values",
    missing_count == 0,
    f"Total missing values: {missing_count}"
)

# 3. Duplicate rows
duplicate_count = int(df.duplicated().sum())
print("Duplicate rows:", duplicate_count)
add_check(
    "Duplicate rows",
    duplicate_count == 0,
    f"Total duplicate rows: {duplicate_count}"
)

# 4. Required engineered features
required_features = [
    "age",
    "total_purchase_amount",
    "total_purchases",
    "deal_purchase_indicator",
    "campaign_exposure",
    "campaign_response"
]

for column in required_features:
    exists = column in df.columns
    add_check(
        f"Required feature: {column}",
        exists,
        "Column exists" if exists else "Column is missing"
    )

# 5. Binary campaign columns
binary_columns = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Response",
    "deal_purchase_indicator",
    "campaign_exposure",
    "campaign_response"
]

for column in binary_columns:
    if column in df.columns:
        values = set(df[column].dropna().unique())
        valid = values.issubset({0, 1})
        add_check(
            f"Binary values: {column}",
            valid,
            f"Found values: {sorted(values)}"
        )

# 6. Non-negative numeric columns
non_negative_columns = [
    "Income",
    "NumDealsPurchases",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
    "total_purchase_amount",
    "total_purchases"
]

for column in non_negative_columns:
    if column in df.columns:
        numeric_values = pd.to_numeric(df[column], errors="coerce")
        valid = numeric_values.notna().all() and (numeric_values >= 0).all()

        add_check(
            f"Non-negative values: {column}",
            valid,
            "All values are numeric and non-negative"
            if valid else "Invalid, non-numeric, or negative values found"
        )

# 7. Age consistency
if "Year_Birth" in df.columns and "age" in df.columns:
    expected_age = 2025 - df["Year_Birth"]
    valid_age = (expected_age == df["age"]).all()

    add_check(
        "Age calculation",
        valid_age,
        "age should equal 2025 - Year_Birth"
    )

# 8. Save report
report = pd.DataFrame(checks)
report.to_csv(OUTPUT_FILE, index=False)

print("\nQUALITY CHECK SUMMARY")
print(report.to_string(index=False))

passed = (report["status"] == "PASS").sum()
failed = (report["status"] == "FAIL").sum()

print("\nPassed checks:", passed)
print("Failed checks:", failed)
print("Report saved to:", OUTPUT_FILE)

if failed == 0:
    print("\nOverall result: ALL CHECKS PASSED")
else:
    print("\nOverall result: SOME CHECKS FAILED")
    print("Review the report before proceeding.")
    