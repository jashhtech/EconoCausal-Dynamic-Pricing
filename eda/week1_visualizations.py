
import os
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "retail_data.csv"

df = pd.read_csv(DATA_PATH)


# # Load the dataset
# df = pd.read_csv("../data/retail_data.csv")

# # Create a folder for the graphs
# os.makedirs("graphs", exist_ok=True)

GRAPHS_DIR = PROJECT_ROOT / "eda" / "graphs"
GRAPHS_DIR.mkdir(parents=True, exist_ok=True)

# Graph 1: Customer income distribution
plt.figure(figsize=(8, 5))
plt.hist(df["Income"].dropna(), bins=30)
plt.title("Distribution of Customer Income")
plt.xlabel("Income")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig(GRAPHS_DIR / "customer_income_distribution.png", dpi=300)
plt.close()

# Graph 2: Deal purchase comparison
deal_counts = [
    (df["NumDealsPurchases"] > 0).sum(),
    (df["NumDealsPurchases"] == 0).sum()
]

plt.figure(figsize=(7, 5))
plt.bar(["Deal Purchases", "No Deal Purchases"], deal_counts)
plt.title("Customers With and Without Deal Purchases")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig(GRAPHS_DIR / "deal_purchase_comparison.png", dpi=300)
plt.close()

# Graph 3: Deal purchases versus total spending
plt.figure(figsize=(8, 5))
plt.scatter(
    df["NumDealsPurchases"],
    df["total_purchase_amount"],
    alpha=0.5
)
plt.title("Deal Purchases vs Total Spending")
plt.xlabel("Number of Deal Purchases")
plt.ylabel("Total Purchase Amount")
plt.tight_layout()
plt.savefig(GRAPHS_DIR / "deal_purchases_vs_spending.png", dpi=300)
plt.close()

print("All three graphs were saved in the eda/graphs folder.")
