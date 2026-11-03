import pandas as pd
from src.categorical_encoding import encode_categorical_features


def test_categorical_encoding():
    X = pd.DataFrame({
        "age": [25, 30, 35],
        "Education": ["Graduate", "Master", "PhD"],
        "Marital_Status": ["Single", "Married", "Divorced"]
    })

    result = encode_categorical_features(X)

    assert "age" in result.columns
    assert "Education" not in result.columns
    assert "Marital_Status" not in result.columns
    assert result.select_dtypes(include=["object"]).empty
    assert result.isnull().sum().sum() == 0


def test_encoded_data_shape():
    X = pd.DataFrame({
        "age": [25, 30, 35],
        "Education": ["Graduate", "Master", "PhD"]
    })

    result = encode_categorical_features(X)

    assert result.shape[0] == X.shape[0]
    assert result.shape[1] > X.shape[1]