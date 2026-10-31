
from pathlib import Path
import pandas as pd

# Step 1: Define dataset paths
DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "retail_data.csv"
OUTPUT_FILE = DATA_DIR / "final_data_quality_report.csv"

# Step 2: Load dataset
df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully")
print("Dataset shape:", df.shape)

# Step 3: Generate column-level quality report
quality_report = pd.DataFrame({
    "column_name": df.columns,
    "data_type": df.dtypes.astype(str).values,
    "missing_values": df.isnull().sum().values,
    "missing_percentage": (
        df.isnull().mean().values * 100
    ).round(2),
    "unique_values": df.nunique().values
})

# Step 4: Dataset-level statistics
total_rows = len(df)
total_columns = len(df.columns)
total_missing = int(df.isnull().sum().sum())
duplicate_rows = int(df.duplicated().sum())

print("\n--- Final Data Quality Summary ---")
print("Total rows:", total_rows)
print("Total columns:", total_columns)
print("Total missing values:", total_missing)
print("Duplicate rows:", duplicate_rows)

# Step 5: Check numerical columns
print("\n--- Numerical Column Summary ---")
print(df.describe().T)

# Step 6: Check categorical columns
categorical_columns = df.select_dtypes(
    include=["object"]
).columns

print("\n--- Categorical Column Summary ---")

for col in categorical_columns:
    print(f"\n{col}")
    print(df[col].value_counts(dropna=False))

# Step 7: Save report
quality_report.to_csv(OUTPUT_FILE, index=False)

print("\nQuality report saved successfully:")
print(OUTPUT_FILE)

print("\nData quality reporting completed.")



