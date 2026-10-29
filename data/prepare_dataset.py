from pathlib import Path
import pandas as pd

# Define file paths relative to this script
DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "marketing_campaign.csv"
OUTPUT_FILE = DATA_DIR / "retail_data.csv"

# Step 1: Load dataset
df = pd.read_csv(INPUT_FILE, sep="\t")

print("Original shape:", df.shape)

# Step 2: Remove duplicates
df = df.drop_duplicates()

# Step 3: Fill missing Income values
df["Income"] = df["Income"].fillna(df["Income"].median())

# Step 4: Remove unrealistic birth years
df = df[df["Year_Birth"] >= 1940].copy()

# Step 5: Create age
df["age"] = 2025 - df["Year_Birth"]

# Step 6: Clean Marital_Status
df["Marital_Status"] = df["Marital_Status"].replace({
    "Alone": "Single",
    "Absurd": "Unknown",
    "YOLO": "Unknown"
})

# Step 7: Create total purchase amount
purchase_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

df["total_purchase_amount"] = df[purchase_columns].sum(axis=1)

# Step 8: Create total number of purchases
purchase_count_columns = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

df["total_purchases"] = df[purchase_count_columns].sum(axis=1)

# Step 9: Create deal purchase indicator
df["deal_purchase_indicator"] = (
    df["NumDealsPurchases"] > 0
).astype(int)

# Step 10: Create campaign exposure
campaign_columns = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5"
]

df["campaign_exposure"] = (
    df[campaign_columns].sum(axis=1) > 0
).astype(int)

# Step 11: Create campaign response
df["campaign_response"] = df["Response"]

# Step 12: Final validation
print("\n--- Data Quality Report ---")
print("Missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Final shape:", df.shape)

# Step 13: Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print(f"Cleaned dataset saved to: {OUTPUT_FILE}")

