
from pathlib import Path
import pandas as pd

# Step 1: Define paths
DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "retail_data.csv"
OUTPUT_FILE = DATA_DIR / "week4_day1_audit_report.csv"

# Step 2: Check dataset availability
if not INPUT_FILE.exists():
    raise FileNotFoundError("retail_data.csv not found")

# Step 3: Load dataset
df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully")

# Step 4: Dataset overview
print("\n--- DATASET OVERVIEW ---")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("Missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())

# Step 5: Column validation
print("\n--- COLUMN NAMES ---")
for column in df.columns:
    print(column)

# Step 6: Data type validation
print("\n--- DATA TYPES ---")
print(df.dtypes)

# Step 7: Validate important features
required_features = [
    "age",
    "total_purchase_amount",
    "total_purchases",
    "deal_purchase_indicator",
    "campaign_exposure",
    "campaign_response"
]

print("\n--- FEATURE VALIDATION ---")

for feature in required_features:
    if feature in df.columns:
        print(f"PASS: {feature}")
    else:
        print(f"FAIL: {feature}")

missing_features = [
    feature for feature in required_features
    if feature not in df.columns
]

# Step 8: Generate column-level report
report = pd.DataFrame({
    "column_name": df.columns,
    "data_type": df.dtypes.astype(str).values,
    "missing_values": df.isnull().sum().values,
    "unique_values": df.nunique().values
})

report.to_csv(OUTPUT_FILE, index=False)

# Step 9: Final audit result
print("\n--- FINAL AUDIT ---")

if (
    df.isnull().sum().sum() == 0
    and df.duplicated().sum() == 0
    and not missing_features
):
    print("PASS: Dataset structural audit completed.")
else:
    print("WARNING: Dataset requires further review.")

print("\nAudit report saved:", OUTPUT_FILE)

