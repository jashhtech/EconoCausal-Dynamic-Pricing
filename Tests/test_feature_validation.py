import numpy as np
import pandas as pd
import pytest

from src.feature_validation import (
    validate_features,
    validate_treatment_outcome,
)


def test_valid_features():
    X = pd.DataFrame({
        "age": [25, 30, 40],
        "Income": [30000, 45000, 60000],
    })

    assert validate_features(X) is True


def test_empty_features():
    X = pd.DataFrame()

    with pytest.raises(ValueError):
        validate_features(X)


def test_missing_values():
    X = pd.DataFrame({
        "age": [25, np.nan, 40],
    })

    with pytest.raises(ValueError):
        validate_features(X)


def test_matching_record_counts():
    X = pd.DataFrame({"age": [25, 30, 40]})
    T = np.array([0, 1, 0])
    Y = np.array([100, 200, 150])

    assert validate_treatment_outcome(X, T, Y) is True


def test_mismatched_record_counts():
    X = pd.DataFrame({"age": [25, 30, 40]})
    T = np.array([0, 1])
    Y = np.array([100, 200, 150])

    with pytest.raises(ValueError):
        validate_treatment_outcome(X, T, Y)