import pandas as pd
import numpy as np
import pytest

from src.feature_validation import validate_features


def test_duplicate_columns():
    X = pd.DataFrame(
        [[20, 30], [25, 35]],
        columns=["age", "age"]
    )

    with pytest.raises(ValueError):
        validate_features(X)


def test_infinite_values():
    X = pd.DataFrame({
        "age": [20, np.inf, 30],
        "income": [1000, 2000, 3000]
    })

    with pytest.raises(ValueError):
        validate_features(X)


def test_non_numeric_values():
    X = pd.DataFrame({
        "age": [20, 25, 30],
        "city": ["Vizag", "Hyderabad", "Chennai"]
    })

    with pytest.raises(TypeError):
        validate_features(X)


def test_valid_numeric_data():
    X = pd.DataFrame({
        "age": [20, 25, 30],
        "income": [1000, 2000, 3000]
    })

    assert validate_features(X) is True