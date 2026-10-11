
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load our retail dataset
df = pd.read_csv("../data/retail_data.csv")

# 1. Check the number of rows and columns
print("Dataset shape:", df.shape)

# 2. Display the first five rows
print("\nFirst five rows:")
print(df.head())

# 3. Check column data types and non-missing values
print("\nDataset information:")
df.info()

# 4. Count missing values
print("\nMissing values:")
print(df.isnull().sum())

# 5. Count duplicate rows
print("\nDuplicate rows:", df.duplicated().sum())



# Step 2: Check numerical summaries

print("\nNumerical summary:")
print(df.describe())

# Check unique customer IDs
print("\nDuplicate customer IDs:", df["ID"].duplicated().sum())

# Check age range
print("\nAge range:")
print("Minimum age:", df["age"].min())
print("Maximum age:", df["age"].max())

# Check income range
print("\nIncome range:")
print("Minimum income:", df["Income"].min())
print("Maximum income:", df["Income"].max())

# Check campaign indicator values
campaign_columns = [
    "AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
    "AcceptedCmp4", "AcceptedCmp5", "Response",
    "deal_purchase_indicator", "campaign_exposure",
    "campaign_response"
]

print("\nUnique values in indicator columns:")
for column in campaign_columns:
    print(column, ":", sorted(df[column].unique()))



# Step 3: Investigate income and purchase amounts

print("\n--- Income analysis ---")
print("Lowest incomes:")
print(df["Income"].nsmallest(5).to_list())

print("Highest incomes:")
print(df["Income"].nlargest(10).to_list())

print("\n--- Total spending analysis ---")
spending_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

# Calculate spending directly from the original columns
calculated_spending = df[spending_columns].sum(axis=1)

print("Minimum total spending:", calculated_spending.min())
print("Maximum total spending:", calculated_spending.max())

# Compare our calculation with the existing column
print(
    "Rows where total_purchase_amount differs:",
    (calculated_spending != df["total_purchase_amount"]).sum()
)

print("\n--- Deal purchases ---")
print(df["NumDealsPurchases"].describe())

print(
    "Customers who made at least one deal purchase:",
    (df["NumDealsPurchases"] > 0).sum()
)

print(
    "Customers who made no deal purchases:",
    (df["NumDealsPurchases"] == 0).sum()
)


# Step 4: Validate derived columns

print("\n--- Validate total_purchases ---")

purchase_columns = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumDealsPurchases"
]

calculated_purchases = df[purchase_columns].sum(axis=1)

print(
    "Rows where total_purchases differs from channel + deal sum:",
    (calculated_purchases != df["total_purchases"]).sum()
)

print("\n--- Validate deal_purchase_indicator ---")

calculated_deal_indicator = (
    df["NumDealsPurchases"] > 0
).astype(int)

print(
    "Rows where deal_purchase_indicator is incorrect:",
    (
        calculated_deal_indicator
        != df["deal_purchase_indicator"]
    ).sum()
)

print("\n--- Validate campaign columns ---")

campaign_columns = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5"
]

calculated_campaign_acceptance = (
    df[campaign_columns].max(axis=1)
)

print(
    "Rows where campaign_exposure differs from "
    "campaign acceptance:",
    (
        calculated_campaign_acceptance
        != df["campaign_exposure"]
    ).sum()
)

print(
    "Rows where Response differs from campaign_response:",
    (df["Response"] != df["campaign_response"]).sum()
)

print("\n--- Investigate total_purchases ---")

channel_columns = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

calculated_channel_purchases = df[channel_columns].sum(axis=1)

print(
    "Rows where total_purchases differs from channel total:",
    (
        calculated_channel_purchases != df["total_purchases"]
    ).sum()
)

print("\nFirst 5 examples:")
print(
    df[
        [
            "ID",
            "NumWebPurchases",
            "NumCatalogPurchases",
            "NumStorePurchases",
            "NumDealsPurchases",
            "total_purchases"
        ]
    ].head()
)

# Check data types
print("\n--- Data Types ---")
print(df.dtypes)

# Check statistical summary
print("\n--- Statistical Summary ---")
print(df.describe())

# Check target column distribution
print("\n--- Campaign Response Counts ---")
print(df["Response"].value_counts())


# Prepare features and target for a practice ML model

target = "Response"

features = [
    "Income",
    "age",
    "Kidhome",
    "Teenhome",
    "Recency",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumWebVisitsMonth",
    "NumDealsPurchases"
]

X = df[features]
y = df[target]

print("\n--- ML Preparation ---")
print("Feature data shape:", X.shape)
print("Target data shape:", y.shape)
print("\nFeature columns:")
print(X.columns.tolist())
print("\nTarget distribution:")
print(y.value_counts())

# Split the dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\n--- Train-Test Split ---")
print("Training features:", X_train.shape)
print("Testing features:", X_test.shape)
print("Training targets:", y_train.shape)
print("Testing targets:", y_test.shape)


from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Create the model
model = DecisionTreeClassifier(
    max_depth=5,
    random_state=42,
    class_weight="balanced"
)

# Train the model
model.fit(X_train, y_train)

# Predict campaign responses for test customers
y_pred = model.predict(X_test)

# Evaluate the model
print("\n--- Model Evaluation ---")
print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Examine which features the model used most
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n--- Feature Importance ---")
print(importance.to_string(index=False))

