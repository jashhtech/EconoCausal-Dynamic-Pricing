from pathlib import Path
import pandas as pd

# Step 1: Define project paths
DATA_DIR = Path(__file__).resolve().parent

DATASET = DATA_DIR / "retail_data.csv"
DICTIONARY = DATA_DIR / "data_dictionary.csv"
QUALITY_REPORT = DATA_DIR / "final_data_quality_report.csv"

# Step 2: Check required files
required_files = [
    DATASET,
    DICTIONARY,
    QUALITY_REPORT
]

print("---- FILE VERIFICATION ----")

for file in required_files:
    if file.exists():
        print(f"FOUND: {file.name}")
    else:
        print(f"MISSING: {file.name}")

missing_files = [
    file.name for file in required_files
    if not file.exists()
]

if missing_files:
    raise FileNotFoundError(
        f"Required files missing: {missing_files}"
    )

# Step 3: Load final dataset
df = pd.read_csv(DATASET)

print("\n---- DATASET SUMMARY ----")
print("Dataset shape:", df.shape)
print("Total rows:", len(df))
print("Total columns:", len(df.columns))
print("Missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())

# Step 4: Display dataset columns
print("\n---- DATASET COLUMNS ----")

for column in df.columns:
    print(column)

# Step 5: Verify important engineered features
important_features = [
    "age",
    "total_purchase_amount",
    "total_purchases",
    "deal_purchase_indicator",
    "campaign_exposure",
    "campaign_response"
]

print("\n---- FEATURE VERIFICATION ----")

for feature in important_features:
    if feature in df.columns:
        print(f"PASS: {feature}")
    else:
        print(f"FAIL: {feature}")

missing_features = [
    feature for feature in important_features
    if feature not in df.columns
]

if missing_features:
    raise ValueError(
        f"Missing engineered features: {missing_features}"
    )

# Step 6: Final validation
print("\n---- FINAL VALIDATION ----")

assert df.isnull().sum().sum() == 0, "Missing values found"
assert df.duplicated().sum() == 0, "Duplicate rows found"

print("Dataset validation successful.")
print("Final data handoff verification completed.")
