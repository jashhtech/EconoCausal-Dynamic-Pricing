"""
EconoCausal - Week 2: Nuisance models (Double ML ka pehla hissa).

Do models chahiye:
    outcome model   : Y ~ X   (campaign_response ko confounders se predict karo)
    treatment model : T ~ X   (campaign_exposure ko confounders se predict karo)

Roles badalne ho (Jaswanth ke confirm karne ke baad) to SIRF neeche ka CONFIG block badlo.

Chalane ka tareeka (kahin se bhi):
    python src/nuisance_models.py
"""
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ======================= CONFIG (roles yahin badlo) =======================
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "retail_data.csv"
TREATMENT = "campaign_exposure"
OUTCOME = "campaign_response"
# total_purchase_amount and total_purchases are excluded until their timing
# (before or after campaign exposure) is confirmed by the team.
NUMERIC = ["age", "Income", "Kidhome", "Teenhome", "Recency"]
CATEGORICAL = ["Education", "Marital_Status"]
# Ye columns kabhi features mein nahi aane chahiye (leakage)
LEAKAGE_COLUMNS = ["Response", "AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
                   "AcceptedCmp4", "AcceptedCmp5"]
SEED = 42
N_SPLITS = 5
# ===========================================================================
RESULTS_PATH = Path(__file__).resolve().parent.parent / "results" / "nuisance_model_results.csv"

def check_config():
    """Galat column features mein ho to turant error do."""
    banned = set(LEAKAGE_COLUMNS) | {TREATMENT, OUTCOME}
    bad = [c for c in NUMERIC + CATEGORICAL if c in banned]
    if bad:
        raise ValueError(f"Leakage risk: these columns cannot be features: {bad}")


def make_preprocessor():
    return ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])


def candidate_models():
    return {
        "logistic": LogisticRegression(max_iter=1000),
        "random_forest": RandomForestClassifier(
            n_estimators=200, min_samples_leaf=5, random_state=SEED, n_jobs=-1),
        "grad_boosting": GradientBoostingClassifier(random_state=SEED),
    }


def oof_predict(df, target, model):
    """Cross-fitted (out-of-fold) probability predictions for `target`."""
    X, y = df[NUMERIC + CATEGORICAL], df[target]
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    pipe = make_pipeline(make_preprocessor(), model)
    return cross_val_predict(pipe, X, y, cv=cv, method="predict_proba")[:, 1]


def evaluate(df, target):
    """Har model ke liye cross-validated AUC aur log loss nikalo."""
    y = df[target]
    rows = []
    for name, model in candidate_models().items():
        p = oof_predict(df, target, model)
        rows.append({"target": target, "model": name,
                     "auc": round(roc_auc_score(y, p), 4),
                     "log_loss": round(log_loss(y, p), 4)})
    return rows


def dml_residuals(df, outcome_model="random_forest", treatment_model="random_forest"):
    """DML ke liye residuals: (Y - Y_hat, T - T_hat), dono cross-fitted."""
    y_hat = oof_predict(df, OUTCOME, candidate_models()[outcome_model])
    t_hat = oof_predict(df, TREATMENT, candidate_models()[treatment_model])
    return df[OUTCOME] - y_hat, df[TREATMENT] - t_hat


if __name__ == "__main__":
    check_config()
    df = pd.read_csv(DATA_PATH)
    results_df = pd.DataFrame(evaluate(df, OUTCOME) + evaluate(df, TREATMENT))
    print(results_df.to_string(index=False))
    RESULTS_PATH.parent.mkdir(exist_ok=True)
    results_df.to_csv(RESULTS_PATH, index=False)
    # Overlap check: propensity scores 0 ya 1 ke bahut paas to nahi
    t_hat = oof_predict(df, TREATMENT, candidate_models()["random_forest"])
    print("\nPropensity score (random_forest) summary:")
    print(pd.Series(t_hat).describe().round(4))