import pandas as pd
from sklearn.model_selection import train_test_split


def split_features(X, Y, test_size=0.2, random_state=42):
    """
    Split features and target into training and testing sets.
    """

    if X.empty or Y.empty:
        raise ValueError("Features and target cannot be empty.")

    if len(X) != len(Y):
        raise ValueError("Features and target must have equal rows.")

    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")

    X_train, X_test, Y_train, Y_test = train_test_split(
        X,
        Y,
        test_size=test_size,
        random_state=random_state
    )

    print("Train-test split completed.")
    print("Training features:", X_train.shape)
    print("Testing features:", X_test.shape)
    print("Training target:", Y_train.shape)
    print("Testing target:", Y_test.shape)

    return X_train, X_test, Y_train, Y_test


if __name__ == "__main__":
    sample_X = pd.DataFrame({
        "PastPurchases": [2, 5, 3, 6, 4, 7, 1, 8, 9, 3],
        "PastSpending": [100, 250, 150, 300, 200, 350, 80, 400, 450, 160]
    })

    sample_Y = pd.Series(
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
        name="Purchase"
    )

    split_features(sample_X, sample_Y)