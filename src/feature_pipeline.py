import pandas as pd

from feature_engineering import load_and_prepare_features
from feature_preprocessing import preprocess_features
from feature_split import split_features


def build_feature_pipeline(X, T, Y):
    """
    Preprocess features and split X, T, and Y
    while preserving row alignment.
    """

    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame.")

    if not isinstance(T, (pd.Series, pd.DataFrame)):
        raise TypeError("T must be a pandas Series or DataFrame.")

    if not isinstance(Y, (pd.Series, pd.DataFrame)):
        raise TypeError("Y must be a pandas Series or DataFrame.")

    if X.empty or T.empty or Y.empty:
        raise ValueError("X, T, and Y cannot be empty.")

    if not (len(X) == len(T) == len(Y)):
        raise ValueError("X, T, and Y must have equal rows.")

    X_processed = preprocess_features(X)

    (
        X_train,
        X_test,
        T_train,
        T_test,
        Y_train,
        Y_test,
    ) = split_features(X_processed, T, Y)

    print("\nFeature pipeline executed successfully.")
    print("Training features:", X_train.shape)
    print("Testing features:", X_test.shape)
    print("Training treatment:", T_train.shape)
    print("Testing treatment:", T_test.shape)
    print("Training outcome:", Y_train.shape)
    print("Testing outcome:", Y_test.shape)

    return (
        X_train,
        X_test,
        T_train,
        T_test,
        Y_train,
        Y_test,
    )


if __name__ == "__main__":
    X, T, Y = load_and_prepare_features()
    build_feature_pipeline(X, T, Y)