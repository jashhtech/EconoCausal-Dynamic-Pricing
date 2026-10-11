
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/retail_data.csv")

# Chart 1: Customer income distribution
plt.figure(figsize=(8, 5))
plt.hist(df["Income"], bins=30)
plt.title("Distribution of Customer Income")
plt.xlabel("Income")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.show()

# Chart 2: Customers who purchased using deals
deal_counts = [
    (df["NumDealsPurchases"] > 0).sum(),
    (df["NumDealsPurchases"] == 0).sum()
]

plt.figure(figsize=(7, 5))
plt.bar(["Deal Purchases", "No Deal Purchases"], deal_counts)
plt.title("Customers With and Without Deal Purchases")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.show()

# Chart 3: Deal purchases versus spending
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
plt.show()
