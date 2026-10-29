import numpy as np
import pandas as pd


def validate_features(X):
    """
    Validate the feature matrix before DML estimation.
    """

    if not isinstance(X, (pd.DataFrame, np.ndarray)):
        raise TypeError(
            "Features must be a pandas DataFrame or NumPy array."
        )

    if X.shape[0] == 0:
        raise ValueError("Feature matrix contains no rows.")

    if X.shape[1] == 0:
        raise ValueError("Feature matrix contains no columns.")

    if isinstance(X, pd.DataFrame):
        if X.columns.duplicated().any():
            raise ValueError("Duplicate feature columns detected.")

        if X.isnull().any().any():
            raise ValueError("Missing values detected in features.")

        values = X.to_numpy()
    else:
        values = X

    if not np.issubdtype(values.dtype, np.number):
        raise TypeError("Features must contain numeric values.")

    if not np.isfinite(values).all():
        raise ValueError(
            "Infinite or invalid numeric values detected in features."
        )

    return True


def validate_treatment_outcome(X, T, Y):
    """
    Check whether features, treatment, and outcome have
    matching record counts.
    """

    if len(X) != len(T):
        raise ValueError(
            "Feature and treatment record counts do not match."
        )

    if len(X) != len(Y):
        raise ValueError(
            "Feature and outcome record counts do not match."
        )

    if len(X) == 0:
        raise ValueError("No records available for validation.")

    return True