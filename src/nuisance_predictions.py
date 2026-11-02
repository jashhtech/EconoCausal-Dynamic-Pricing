"""Cross-fitted nuisance predictions and DML residuals, in one table.

Combines src/treatment_model.py and src/outcome_model.py. Every prediction is
out-of-fold: it comes from a model that did not train on that customer.
Row order and index are the same as the input data.
"""
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from src.nuisance_models import DATA_PATH, OUTCOME, TREATMENT, check_config
    from src.outcome_model import outcome_predictions
    from src.treatment_model import propensity_scores
except ImportError:  # when run as: python src/nuisance_predictions.py
    from nuisance_models import DATA_PATH, OUTCOME, TREATMENT, check_config
    from outcome_model import outcome_predictions
    from treatment_model import propensity_scores

PREDICTIONS_PATH = Path(__file__).resolve().parent.parent / "results" / "nuisance_predictions.csv"


def build_nuisance_predictions(df, outcome_model="random_forest",
                               treatment_model="random_forest"):
    """One row per customer: T, Y, propensity, outcome_pred, T_res, Y_res."""
    check_config()
    t_hat = propensity_scores(df, treatment_model)
    y_hat = outcome_predictions(df, outcome_model)
    out = pd.DataFrame({
        "T": df[TREATMENT],
        "Y": df[OUTCOME],
        "propensity": t_hat,
        "outcome_pred": y_hat,
    }, index=df.index)
    out["T_res"] = out["T"] - out["propensity"]
    out["Y_res"] = out["Y"] - out["outcome_pred"]
    validate_alignment(df, out)
    return out


def validate_alignment(df, out):
    """Predictions must line up with the original rows and have no gaps."""
    if len(out) != len(df):
        raise ValueError(f"Row count mismatch: {len(out)} vs {len(df)}")
    if not out.index.equals(df.index):
        raise ValueError("Output index does not match the input data index.")
    if out.isna().any().any():
        raise ValueError("Nuisance predictions contain missing values.")
    if not (out["T"].values == df[TREATMENT].values).all():
        raise ValueError("Treatment column is not aligned with the input data.")
    if not (out["Y"].values == df[OUTCOME].values).all():
        raise ValueError("Outcome column is not aligned with the input data.")


def check_reproducible(df, **kwargs):
    """Two runs with the same seed must give identical residuals."""
    a = build_nuisance_predictions(df, **kwargs)
    b = build_nuisance_predictions(df, **kwargs)
    return bool(np.allclose(a[["T_res", "Y_res"]].values, b[["T_res", "Y_res"]].values))


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    preds = build_nuisance_predictions(df)
    print(f"Rows: {len(preds)} (input rows: {len(df)})")
    print("\nSummary:")
    print(preds.describe().round(4).T[["mean", "std", "min", "max"]])
    print("\nReproducible (two runs identical):", check_reproducible(df))
    PREDICTIONS_PATH.parent.mkdir(exist_ok=True)
    preds.to_csv(PREDICTIONS_PATH, index=False)
    print("Saved:", PREDICTIONS_PATH)