import pandas as pd
from pathlib import Path

# Project paths
DATA_DIR = Path(__file__).resolve().parent
CLEANED_FILE = DATA_DIR / "retail_data.csv"
ORIGINAL_FILE = DATA_DIR / "marketing_campaign.csv"
OUTPUT_FILE = DATA_DIR / "week4_day3_feature_verification.csv"

# Check files
if not CLEANED_FILE.exists():
    raise FileNotFoundError(f"Missing file: {CLEANED_FILE}")

if not ORIGINAL_FILE.exists():
    raise FileNotFoundError(f"Missing file: {ORIGINAL_FILE}")

# Load datasets
cleaned = pd.read_csv(CLEANED_FILE)
original = pd.read_csv(ORIGINAL_FILE, sep="\t")

results = []

def record_check(feature, passed, details):
    results.append({
        "feature": feature,
        "status": "PASS" if passed else "FAIL",
        "details": details
    })

print("WEEK 4 - DAY 3 FEATURE VERIFICATION")
print("-" * 50)

# 1. Age verification
if "Year_Birth" in cleaned.columns and "age" in cleaned.columns:
    expected_age = 2025 - cleaned["Year_Birth"]
    passed = expected_age.equals(cleaned["age"])

    record_check(
        "age",
        passed,
        "Compared age with 2025 - Year_Birth"
    )
else:
    record_check("age", False, "Required columns are missing")

# 2. Total purchase amount
spending_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

if all(col in cleaned.columns for col in spending_columns + ["total_purchase_amount"]):
    expected = cleaned[spending_columns].sum(axis=1)
    passed = expected.equals(cleaned["total_purchase_amount"])

    record_check(
        "total_purchase_amount",
        passed,
        "Compared with the sum of six spending columns"
    )
else:
    record_check(
        "total_purchase_amount",
        False,
        "Required spending columns or feature are missing"
    )

# 3. Total purchases
purchase_columns = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

if all(col in cleaned.columns for col in purchase_columns + ["total_purchases"]):
    expected = cleaned[purchase_columns].sum(axis=1)
    passed = expected.equals(cleaned["total_purchases"])

    record_check(
        "total_purchases",
        passed,
        "Compared with web, catalog and store purchases"
    )
else:
    record_check(
        "total_purchases",
        False,
        "Required purchase columns or feature are missing"
    )

# 4. Deal purchase indicator
if all(col in cleaned.columns for col in ["NumDealsPurchases", "deal_purchase_indicator"]):
    expected = (cleaned["NumDealsPurchases"] > 0).astype(int)
    passed = expected.equals(cleaned["deal_purchase_indicator"])

    record_check(
        "deal_purchase_indicator",
        passed,
        "1 indicates at least one deal purchase; otherwise 0"
    )
else:
    record_check(
        "deal_purchase_indicator",
        False,
        "Required columns are missing"
    )

# 5. Campaign exposure
campaign_columns = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5"
]

if all(col in cleaned.columns for col in campaign_columns + ["campaign_exposure"]):
    expected = (
        cleaned[campaign_columns].sum(axis=1) > 0
    ).astype(int)

    passed = expected.equals(cleaned["campaign_exposure"])

    record_check(
        "campaign_exposure",
        passed,
        "1 indicates acceptance of at least one of five campaigns"
    )
else:
    record_check(
        "campaign_exposure",
        False,
        "Required campaign columns are missing"
    )

# 6. Campaign response
if all(col in cleaned.columns for col in ["Response", "campaign_response"]):
    passed = cleaned["Response"].equals(cleaned["campaign_response"])

    record_check(
        "campaign_response",
        passed,
        "Compared with original Response column"
    )
else:
    record_check(
        "campaign_response",
        False,
        "Required columns are missing"
    )

# Generate report
report = pd.DataFrame(results)
report.to_csv(OUTPUT_FILE, index=False)

print("\nFEATURE VERIFICATION RESULTS")
print(report.to_string(index=False))

passed_count = (report["status"] == "PASS").sum()
failed_count = (report["status"] == "FAIL").sum()

print("\nPassed:", passed_count)
print("Failed:", failed_count)
print("Report saved to:", OUTPUT_FILE)

if failed_count == 0:
    print("\nAll derived features are verified successfully.")
else:
    print("\nSome features need investigation.")
    