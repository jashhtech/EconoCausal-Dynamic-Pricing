import numpy as np
import pandas as pd

from src.feature_pipeline import build_feature_pipeline
from src.dml_estimation import estimate_dml, DMLResult


def test_feature_pipeline_dml_integration():
    np.random.seed(42)

    n = 200

    X = pd.DataFrame({
        "age": np.random.randint(20, 70, n),
        "income": np.random.randint(20000, 100000, n),
    })

    T = pd.Series(
        np.random.binomial(1, 0.5, n),
        name="treatment"
    )

    Y = pd.Series(
        5 + 2 * T + 0.03 * X["age"]
        + 0.0001 * X["income"]
        + np.random.normal(0, 1, n),
        name="outcome"
    )

    X_train, X_test, T_train, T_test, Y_train, Y_test = (
        build_feature_pipeline(X, T, Y)
    )

    result = estimate_dml(
        X_train,
        T_train,
        Y_train,
        n_splits=5
    )

    assert isinstance(result, DMLResult)
    assert np.isfinite(result.effect)
    assert np.isfinite(result.standard_error)
    assert result.sample_size == len(X_train)
    assert result.ci_lower <= result.ci_upper