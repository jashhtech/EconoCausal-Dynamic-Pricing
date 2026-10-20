import pandas as pd




def preprocess_features(X):
    """
    Preprocess confounder features for machine learning.

    - Convert categorical columns using one-hot encoding.
    - Preserve numerical columns.
    - Return the processed feature DataFrame.
    """


    if X.empty:
        raise ValueError("Feature dataset is empty.")

    # Convert categorical columns into numerical columns.
    X_processed = pd.get_dummies(
        X,
        drop_first=True,
        dtype=int
    )

    # Validate the processed output.
    if X_processed.isnull().any().any():
        raise ValueError(
            "Missing values detected. Handle them before model training."
        )

    print("Feature preprocessing completed.")
    print("Original feature shape:", X.shape)
    print("Processed feature shape:", X_processed.shape)

    return X_processed



if __name__ == "__main__":
    # Small sample for testing only; not actual project data.
    sample_data = pd.DataFrame({
        "PastPurchases": [2, 5, 3, 6],
        "CustomerType": ["New", "Returning", "New", "Returning"],
    })

    processed_data = preprocess_features(sample_data)

    print("\nProcessed sample:")
    print(processed_data)
