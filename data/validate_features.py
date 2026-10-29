
from pathlib import Path
import pandas as pd

# Step 1: Define dataset paths
DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "retail_data.csv"

# Step 2: Load the cleaned dataset
df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully")
print("Dataset shape:", df.shape)

# Step 3: Validate required columns
required_columns = [
    "Year_Birth",
    "age",
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumDealsPurchases",
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Response",
    "total_purchase_amount",
    "total_purchases",
    "deal_purchase_indicator",
    "campaign_exposure",
    "campaign_response"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Step 4: Validate age
expected_age = 2025 - df["Year_Birth"]
age_valid = df["age"].equals(expected_age)

print("\nAge calculation valid:", age_valid)

# Step 5: Validate total purchase amount
purchase_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

expected_amount = df[purchase_columns].sum(axis=1)
amount_valid = (
    df["total_purchase_amount"].equals(expected_amount)
)

print("Total purchase amount valid:", amount_valid)

# Step 6: Validate total purchases
purchase_count_columns = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

expected_purchases = df[purchase_count_columns].sum(axis=1)
purchases_valid = df["total_purchases"].equals(
    expected_purchases
)

print("Total purchases valid:", purchases_valid)

# Step 7: Validate deal purchase indicator
expected_deal = (df["NumDealsPurchases"] > 0).astype(int)
deal_valid = df["deal_purchase_indicator"].equals(expected_deal)

print("Deal purchase indicator valid:", deal_valid)

# Step 8: Validate campaign exposure
campaign_columns = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5"
]

expected_exposure = (
    df[campaign_columns].sum(axis=1) > 0
).astype(int)

exposure_valid = df["campaign_exposure"].equals(
    expected_exposure
)

print("Campaign exposure calculation valid:", exposure_valid)

# Step 9: Validate campaign response
response_valid = df["campaign_response"].equals(df["Response"])

print("Campaign response valid:", response_valid)

# Step 10: Final validation summary
checks = {
    "Age": age_valid,
    "Total purchase amount": amount_valid,
    "Total purchases": purchases_valid,
    "Deal purchase indicator": deal_valid,
    "Campaign exposure": exposure_valid,
    "Campaign response": response_valid
}

print("\n--- Validation Summary ---")

for feature, passed in checks.items():
    print(f"{feature}: {'PASS' if passed else 'FAIL'}")

if not all(checks.values()):
    raise ValueError("One or more feature validation checks failed.")

print("\nAll derived feature checks passed.")

