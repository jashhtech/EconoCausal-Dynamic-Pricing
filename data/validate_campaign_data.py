
from pathlib import Path
import pandas as pd

# Step 1: Load cleaned dataset
DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "retail_data.csv"

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully")
print("Dataset shape:", df.shape)

# Step 2: Validate required columns
required_columns = [
    "campaign_exposure",
    "campaign_response",
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Response"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

# Step 3: Check missing values
print("\nMissing values:")
print(df[required_columns].isnull().sum())

# Step 4: Check campaign exposure distribution
print("\nCampaign Exposure Distribution:")
print(df["campaign_exposure"].value_counts(dropna=False))

print("\nCampaign Exposure Percentages:")
print(
    df["campaign_exposure"]
    .value_counts(normalize=True, dropna=False) * 100
)

# Step 5: Check campaign response distribution
print("\nCampaign Response Distribution:")
print(df["campaign_response"].value_counts(dropna=False))

print("\nCampaign Response Percentages:")
print(
    df["campaign_response"]
    .value_counts(normalize=True, dropna=False) * 100
)

# Step 6: Validate binary values
for col in ["campaign_exposure", "campaign_response"]:
    print(
        f"\n{col} contains only binary values:",
        set(df[col].dropna().unique()).issubset({0, 1})
    )

# Step 7: Check individual campaign acceptance
campaign_columns = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5"
]

print("\nIndividual Campaign Acceptance:")
for col in campaign_columns:
    print(f"{col}:")
    print(df[col].value_counts(dropna=False))

# Step 8: Cross-tabulation
print("\nCampaign Exposure vs Campaign Response:")
print(
    pd.crosstab(
        df["campaign_exposure"],
        df["campaign_response"],
        margins=True
    )
)

# Step 9: Validate campaign response consistency
response_valid = df["campaign_response"].equals(df["Response"])

print("\nCampaign response matches original Response:", response_valid)

# Step 10: Final summary
print("\n--- Validation Summary ---")
print("Total observations:", len(df))
print("Missing campaign exposure:", df["campaign_exposure"].isnull().sum())
print("Missing campaign response:", df["campaign_response"].isnull().sum())

print("\nCampaign data validation completed.")


