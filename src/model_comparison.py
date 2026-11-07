"""Week 4 Day 3: compare alternative nuisance model configurations.

Uses the same 5-fold cross-fitted procedure as src/nuisance_models.py
(oof_predict applies the shared preprocessing, same seed, same metrics), so
numbers are directly comparable. The baseline models are taken directly from
nuisance_models.candidate_models(). The core module and the dml_residuals()
defaults are not changed.
Run with:  python src/model_comparison.py
"""
from pathlib import Path

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import log_loss, roc_auc_score

try:
    from src import nuisance_models as nm
except ImportError:  # when run as: python src/model_comparison.py
    import nuisance_models as nm

RESULTS_PATH = Path(__file__).resolve().parent.parent / "results" / "model_comparison.csv"


def configurations():
    """Week 2 baselines (unchanged) plus the Week 4 alternatives."""
    seed = nm.SEED
    base = nm.candidate_models()
    configs = {
        "logistic (baseline)": base["logistic"],
        "random_forest (current)": base["random_forest"],
        "grad_boosting (current)": base["grad_boosting"],
        "random_forest depth5": RandomForestClassifier(
            n_estimators=200, max_depth=5, min_samples_leaf=5,
            random_state=seed, n_jobs=-1),
        "random_forest depth10": RandomForestClassifier(
            n_estimators=200, max_depth=10, min_samples_leaf=5,
            random_state=seed, n_jobs=-1),
        "random_forest leaf10": RandomForestClassifier(
            n_estimators=200, min_samples_leaf=10,
            random_state=seed, n_jobs=-1),
        "grad_boosting depth2": GradientBoostingClassifier(
            max_depth=2, learning_rate=0.05, n_estimators=200, random_state=seed),
    }
    try:
        from lightgbm import LGBMClassifier
        configs["lightgbm"] = LGBMClassifier(
            n_estimators=200, learning_rate=0.05, num_leaves=15,
            random_state=seed, verbose=-1)
        configs["lightgbm small"] = LGBMClassifier(
            n_estimators=150, learning_rate=0.05, num_leaves=7, min_child_samples=30,
            random_state=seed, verbose=-1)
    except ImportError:
        print("lightgbm is not installed; skipping LightGBM (pip install lightgbm)")
    return configs


def compare(df):
    nm.check_config()
    rows = []
    for target in [nm.OUTCOME, nm.TREATMENT]:
        y = df[target]
        for name, model in configurations().items():
            p = nm.oof_predict(df, target, model)
            rows.append({"target": target, "model": name,
                         "auc": round(roc_auc_score(y, p), 4),
                         "log_loss": round(log_loss(y, p), 4)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = pd.read_csv(nm.DATA_PATH)
    result = compare(df)
    for target, group in result.groupby("target", sort=False):
        print(f"\n{target} (sorted by log loss, lower is better)")
        print(group.sort_values("log_loss").drop(columns="target").to_string(index=False))
    RESULTS_PATH.parent.mkdir(exist_ok=True)
    result.to_csv(RESULTS_PATH, index=False)
    print("\nSaved:", RESULTS_PATH)