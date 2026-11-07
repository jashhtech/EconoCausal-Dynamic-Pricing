"""Week 4 Day 5: robustness of a simple partialling-out (DML-style) estimate.

For each specification, nuisance models are cross-fitted and the effect is
estimated by regressing the outcome residual on the treatment residual:
    theta = sum(T_res * Y_res) / sum(T_res ** 2)
with a heteroskedasticity-robust standard error. This is a simple sanity check
that uses our own nuisance models. It does not replace the DML estimate in
dml_estimation.py, and it is not a validated causal effect.
Run with:  python src/robustness_check.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from src import nuisance_models as nm
    from src.nuisance_predictions import build_nuisance_predictions
except ImportError:  # when run as: python src/robustness_check.py
    import nuisance_models as nm
    from nuisance_predictions import build_nuisance_predictions

RESULTS_PATH = Path(__file__).resolve().parent.parent / "results" / "robustness_check.csv"
PURCHASE_COLUMNS = ["total_purchase_amount", "total_purchases"]


def plr_estimate(t_res, y_res):
    """Partialling-out estimate with a robust standard error."""
    t_res, y_res = np.asarray(t_res), np.asarray(y_res)
    n = len(t_res)
    theta = (t_res * y_res).sum() / (t_res ** 2).sum()
    eps = y_res - theta * t_res
    var = ((t_res ** 2) * (eps ** 2)).mean() / ((t_res ** 2).mean() ** 2) / n
    return theta, float(np.sqrt(var))


def run_spec(df, name, outcome_model="random_forest", treatment_model="random_forest",
             extra_numeric=None, trim=None):
    original = list(nm.NUMERIC)
    if extra_numeric:
        nm.NUMERIC = original + list(extra_numeric)
    try:
        preds = build_nuisance_predictions(df, outcome_model, treatment_model)
    finally:
        nm.NUMERIC = original
    if trim:
        preds = preds[preds["propensity"].between(*trim)]
    theta, se = plr_estimate(preds["T_res"], preds["Y_res"])
    return {"specification": name, "n": len(preds), "estimate": round(theta, 4),
            "std_error": round(se, 4), "ci_low": round(theta - 1.96 * se, 4),
            "ci_high": round(theta + 1.96 * se, 4)}


if __name__ == "__main__":
    df = pd.read_csv(nm.DATA_PATH)
    rows = [
        run_spec(df, "1 baseline (RF, final features)"),
        run_spec(df, "2 trim propensity [0.05, 0.95]", trim=(0.05, 0.95)),
        run_spec(df, "3 trim propensity [0.10, 0.90]", trim=(0.10, 0.90)),
        run_spec(df, "4 with purchase columns", extra_numeric=PURCHASE_COLUMNS),
        run_spec(df, "5 gradient boosting nuisance models",
                 outcome_model="grad_boosting", treatment_model="grad_boosting"),
        run_spec(df, "6 logistic nuisance models",
                 outcome_model="logistic", treatment_model="logistic"),
    ]
    result = pd.DataFrame(rows)
    print(result.to_string(index=False))
    RESULTS_PATH.parent.mkdir(exist_ok=True)
    result.to_csv(RESULTS_PATH, index=False)
    print("\nSaved:", RESULTS_PATH)