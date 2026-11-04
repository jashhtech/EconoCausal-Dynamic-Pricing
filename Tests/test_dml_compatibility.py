import pandas as pd
from src.feature_split import split_features


def test_dml_input_compatibility():
    X = pd.DataFrame({
        "age": [25, 30, 35, 40, 45, 50, 55, 60, 65, 70],
        "total_purchases": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    })

    T = pd.Series([0, 1] * 5, name="treatment")
    Y = pd.Series(range(10), name="outcome")

    X_train, X_test, T_train, T_test, Y_train, Y_test = (
        split_features(X, T, Y)
    )

    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(T_train, pd.Series)
    assert isinstance(Y_train, pd.Series)

    assert len(X_train) == len(T_train) == len(Y_train)
    assert len(X_test) == len(T_test) == len(Y_test)

    assert not X_train.isna().any().any()
    assert not T_train.isna().any()
    assert not Y_train.isna().any()