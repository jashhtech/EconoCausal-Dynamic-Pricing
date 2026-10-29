import pandas as pd

from feature_engineering import load_and_prepare_features
from feature_preprocessing import preprocess_features
from feature_split import split_features
from feature_validation import (
    validate_features,
    validate_treatment_outcome,
)


def build_feature_pipeline(X, T, Y):
    """
    Preprocess features, validate data, and split X, T, and Y
    while preserving row alignment.
    """

    # Validate input types
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame.")

    if not isinstance(T, (pd.Series, pd.DataFrame)):
        raise TypeError("T must be a pandas Series or DataFrame.")

    if not isinstance(Y, (pd.Series, pd.DataFrame)):
        raise TypeError("Y must be a pandas Series or DataFrame.")

    # Validate non-empty inputs
    if X.empty or T.empty or Y.empty:
        raise ValueError("X, T, and Y cannot be empty.")

    # Validate original features and row alignment
    validate_features(X)
    validate_treatment_outcome(X, T, Y)

    # Preprocess features
    X_processed = preprocess_features(X)

    # Validate processed features
    validate_features(X_processed)
    validate_treatment_outcome(X_processed, T, Y)

    # Split features, treatment, and outcome
    (
        X_train,
        X_test,
        T_train,
        T_test,
        Y_train,
        Y_test,
    ) = split_features(X_processed, T, Y)

    # Validate training data
    validate_features(X_train)
    validate_treatment_outcome(X_train, T_train, Y_train)

    # Validate testing data
    validate_features(X_test)
    validate_treatment_outcome(X_test, T_test, Y_test)

    print("\nFeature validation completed successfully.")
    print("Feature pipeline executed successfully.")
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