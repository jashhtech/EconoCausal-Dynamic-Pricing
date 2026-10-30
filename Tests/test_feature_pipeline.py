import pandas as pd
import pytest

from src.feature_pipeline import build_feature_pipeline


def create_sample_data():
    """Create sample input data for testing."""

    X = pd.DataFrame({
        "age": [22, 25, 30, 35, 40, 45, 50, 55, 60, 65],
        "total_purchases": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    })

    T = pd.Series([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])

    Y = pd.Series([100, 150, 120, 180, 130, 200, 160, 220, 190, 250])

    return X, T, Y


def test_pipeline_returns_six_outputs():
    X, T, Y = create_sample_data()

    result = build_feature_pipeline(X, T, Y)

    assert len(result) == 6


def test_pipeline_preserves_row_alignment():
    X, T, Y = create_sample_data()

    X_train, X_test, T_train, T_test, Y_train, Y_test = (
        build_feature_pipeline(X, T, Y)
    )

    assert len(X_train) == len(T_train) == len(Y_train)
    assert len(X_test) == len(T_test) == len(Y_test)


def test_pipeline_rejects_empty_features():
    X = pd.DataFrame()
    T = pd.Series(dtype=float)
    Y = pd.Series(dtype=float)

    with pytest.raises((ValueError, TypeError)):
        build_feature_pipeline(X, T, Y)


def test_pipeline_rejects_mismatched_rows():
    X, T, Y = create_sample_data()

    T = T.iloc[:-1]

    with pytest.raises(ValueError):
        build_feature_pipeline(X, T, Y)


def test_pipeline_rejects_missing_values():
    X, T, Y = create_sample_data()

    X.loc[0, "age"] = float("nan")

    with pytest.raises(ValueError):
        build_feature_pipeline(X, T, Y)