
"""
EconoCausal: Double Machine Learning integration.

Estimates an average treatment effect using cross-fitting and
residual-on-residual regression.

Inputs:
    X: Numeric, pre-treatment confounders/features
    T: Observed treatment (binary 0/1 or continuous numeric)
    Y: Observed outcome (numeric)

Important:
    A model alone cannot prove causation. Valid treatment definitions,
    appropriate confounders, and defensible causal assumptions are required.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_predict


@dataclass
class DMLResult:
    """Summary of an estimated average treatment effect."""
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

    Binary treatment:
        T must contain exactly 0 and 1. The effect compares treatment=1
        with treatment=0 under the model and causal assumptions.

    Continuous treatment:
        The effect represents the estimated outcome change per one-unit
        increase in treatment.

    X must contain numeric, pre-treatment confounders only.
    """

    # 1. Validate input types and dimensions.
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame.")

    if not isinstance(T, pd.Series) or not isinstance(Y, pd.Series):
        raise TypeError("T and Y must be pandas Series.")

    if X.empty or len(X) < 10:
        raise ValueError("X must contain at least 10 observations.")

    if not (len(X) == len(T) == len(Y)):
        raise ValueError("X, T, and Y must have the same number of rows.")

    if not X.index.equals(T.index) or not X.index.equals(Y.index):
        raise ValueError(
            "X, T, and Y must have matching indexes and row order."
        )

    if not X.columns.is_unique:
        raise ValueError("X must not contain duplicate column names.")

    if "_treatment" in X.columns or "_outcome" in X.columns:
        raise ValueError(
            "X cannot contain columns named '_treatment' or '_outcome'."
        )

    # 2. Combine inputs and remove rows with missing or infinite values.
    data = X.copy()
    data["_treatment"] = T
    data["_outcome"] = Y

    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    if len(data) < 10:
        raise ValueError(
            "Too few complete observations after removing missing values."
        )

    X_clean = data.drop(columns=["_treatment", "_outcome"])
    T_clean = pd.to_numeric(data["_treatment"], errors="raise").astype(float)
    Y_clean = pd.to_numeric(data["_outcome"], errors="raise").astype(float)

    if X_clean.empty:
        raise ValueError("X must contain at least one feature.")

    for column in X_clean.columns:
        X_clean[column] = pd.to_numeric(
            X_clean[column], errors="raise"
        )

    if not np.isfinite(X_clean.to_numpy(dtype=float)).all():
        raise ValueError("X must contain only finite numeric values.")

    if not np.isfinite(T_clean.to_numpy()).all():
        raise ValueError("T must contain only finite numeric values.")

    if not np.isfinite(Y_clean.to_numpy()).all():
        raise ValueError("Y must contain only finite numeric values.")

    if T_clean.nunique() < 2:
        raise ValueError("Treatment must contain at least two distinct values.")

    if n_splits < 2 or n_splits > len(data):
        raise ValueError(
            "n_splits must be between 2 and the number of complete rows."
        )

    # 3. Identify whether treatment is binary.
    treatment_values = set(T_clean.unique())
    is_binary = treatment_values.issubset({0.0, 1.0})

    # 4. Set default nuisance models.
    if treatment_model is None:
        if is_binary:
            treatment_model = RandomForestClassifier(
                n_estimators=200,
                min_samples_leaf=10,
                random_state=random_state,
            )
        else:
            treatment_model = RandomForestRegressor(
                n_estimators=200,
                min_samples_leaf=10,
                random_state=random_state,
            )

    if outcome_model is None:
        outcome_model = RandomForestRegressor(
            n_estimators=200,
            min_samples_leaf=10,
            random_state=random_state,
        )

    # 5. Cross-fitting: each observation is predicted by a model
    # that was not trained on that observation.
    cv = KFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state,
    )

    y_hat = cross_val_predict(
        clone(outcome_model),
        X_clean,
        Y_clean,
        cv=cv,
        method="predict",
    )

    if is_binary:
        # Treatment values are exactly 0 and 1, so the fitted classifier
        # should expose both classes. Check the class ordering explicitly.
        fitted_treatment_model = clone(treatment_model)
        t_hat = cross_val_predict(
            fitted_treatment_model,
            X_clean,
            T_clean,
            cv=cv,
            method="predict_proba",
        )

        classes = getattr(fitted_treatment_model, "classes_", None)

        # cross_val_predict does not leave the estimator fitted on all data.
        # Fit a cloned estimator to establish the class-column ordering.
        fitted_treatment_model.fit(X_clean, T_clean)
        classes = fitted_treatment_model.classes_

        if len(classes) != 2 or 1.0 not in classes:
            raise ValueError(
                "The binary treatment model must support classes 0 and 1."
            )

        positive_column = int(np.flatnonzero(classes == 1.0)[0])
        t_hat = t_hat[:, positive_column]
    else:
        t_hat = cross_val_predict(
            clone(treatment_model),
            X_clean,
            T_clean,
            cv=cv,
            method="predict",
        )

    # 6. Calculate residuals after adjusting for X.
    y_residual = Y_clean.to_numpy() - np.asarray(y_hat)
    t_residual = T_clean.to_numpy() - np.asarray(t_hat)

    denominator = float(np.dot(t_residual, t_residual))

    if np.var(t_residual) < 1e-8 or denominator <= 0:
        raise ValueError(
            "Treatment has too little residual variation after adjusting for X."
        )

    # 7. Estimate the residual-on-residual treatment effect.
    effect = float(
        np.dot(t_residual, y_residual) / denominator
    )

    errors = y_residual - effect * t_residual
    n = len(data)

    # 8. Heteroskedasticity-robust (HC1-style) standard error for
    # the residual regression coefficient.
    # This is an approximate inference calculation, not a substitute
    # for a fully validated DML inference procedure.
    robust_meat = float(np.sum((t_residual * errors) ** 2))
    variance = (n / (n - 1)) * robust_meat / (denominator ** 2)
    standard_error = float(np.sqrt(max(variance, 0.0)))

    # Approximate 95% confidence interval.
    ci_lower = effect - 1.96 * standard_error
    ci_upper = effect + 1.96 * standard_error

    return DMLResult(
        effect=effect,
        standard_error=standard_error,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        sample_size=n,
    )


if __name__ == "__main__":
    print("EconoCausal DML integration module")
    print("Waiting for confirmed treatment, outcome, and confounder definitions.")
    print("No causal estimate is calculated until valid inputs are supplied.")
