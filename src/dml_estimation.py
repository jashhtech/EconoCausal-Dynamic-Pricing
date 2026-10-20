
"""
EconoCausal: Double Machine Learning integration.

This module estimates a treatment effect using cross-fitting and
residual-on-residual regression. It expects the team to provide:
    X: pre-treatment confounders/features
    T: observed treatment
    Y: observed outcome

Important: a valid treatment and defensible causal assumptions are
required. A model alone cannot prove causation.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


@dataclass
class DMLResult:
    """Summary of the estimated average treatment effect."""
    effect: float
    standard_error: float
    ci_lower: float
    ci_upper: float
    sample_size: int


def estimate_dml(
    X: pd.DataFrame,
    T: pd.Series,
    Y: pd.Series,
    treatment_model=None,
    outcome_model=None,
    n_splits: int = 5,
    random_state: int = 42,
) -> DMLResult:
    """
    Estimate an average treatment effect with cross-fitted residuals.

    For a continuous treatment, T must be numeric and the estimate
    represents the effect per one-unit increase in T under the model.

    For a binary treatment, T must contain 0 and 1; the estimate
    represents the effect of treatment=1 versus treatment=0.

    X must contain pre-treatment confounders, not post-treatment
    variables or the outcome itself.
    """

    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame.")

    if X.empty or len(X) < 10:
        raise ValueError("X must contain at least 10 observations.")

    if not isinstance(T, pd.Series) or not isinstance(Y, pd.Series):
        raise TypeError("T and Y must be pandas Series.")

    if not (len(X) == len(T) == len(Y)):
        raise ValueError("X, T, and Y must have the same number of rows.")

    data = X.copy()
    data["_treatment"] = T.to_numpy()
    data["_outcome"] = Y.to_numpy()
    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    if len(data) < 10:
        raise ValueError("Too few complete observations after removing missing values.")

    X_clean = data.drop(columns=["_treatment", "_outcome"])
    T_clean = data["_treatment"].astype(float)
    Y_clean = data["_outcome"].astype(float)

    if not all(pd.api.types.is_numeric_dtype(X_clean[c]) for c in X_clean):
        raise ValueError(
            "X must be numeric. Encode categorical variables in feature engineering first."
        )

    if T_clean.nunique() < 2:
        raise ValueError("Treatment must contain at least two distinct values.")

    if n_splits < 2 or n_splits > len(data):
        raise ValueError("n_splits must be between 2 and the number of rows.")

    # Choose nuisance models appropriate to the treatment type.
    if treatment_model is None:
        if set(T_clean.unique()).issubset({0.0, 1.0}):
            treatment_model = RandomForestClassifier(
                n_estimators=200, min_samples_leaf=10,
                random_state=random_state
            )
        else:
            treatment_model = RandomForestRegressor(
                n_estimators=200, min_samples_leaf=10,
                random_state=random_state
            )

    if outcome_model is None:
        outcome_model = RandomForestRegressor(
            n_estimators=200, min_samples_leaf=10,
            random_state=random_state
        )

    cv = KFold(
        n_splits=n_splits, shuffle=True, random_state=random_state
    )

    # Cross-fitted prediction of outcome given X.
    y_hat = cross_val_predict(
        clone(outcome_model), X_clean, Y_clean,
        cv=cv, method="predict"
    )

    # Cross-fitted prediction of treatment given X.
    if set(T_clean.unique()).issubset({0.0, 1.0}):
        t_hat = cross_val_predict(
            clone(treatment_model), X_clean, T_clean,
            cv=cv, method="predict_proba"
        )[:, 1]
    else:
        t_hat = cross_val_predict(
            clone(treatment_model), X_clean, T_clean,
            cv=cv, method="predict"
        )

    # DML uses residuals to adjust for the observed confounders.
    y_residual = Y_clean.to_numpy() - y_hat
    t_residual = T_clean.to_numpy() - t_hat

    if np.var(t_residual) < 1e-8:
        raise ValueError(
            "Treatment has too little residual variation after adjusting for X."
        )

    # Estimate the effect from the residual-on-residual relationship.
    effect = float(
        np.dot(t_residual, y_residual) / np.dot(t_residual, t_residual)
    )

    # Approximate standard error for the residual regression coefficient.
    errors = y_residual - effect * t_residual
    n = len(data)
    variance = np.sum(errors**2) / (n - 1)
    se = float(np.sqrt(variance / np.sum(t_residual**2)))

    return DMLResult(
        effect=effect,
        standard_error=se,
        ci_lower=effect - 1.96 * se,
        ci_upper=effect + 1.96 * se,
        sample_size=n,
    )


if __name__ == "__main__":
    print("EconoCausal DML integration module")
    print("Waiting for the team's confirmed X, T, and Y definitions.")
    print("No causal estimate is calculated until valid inputs are supplied.")
