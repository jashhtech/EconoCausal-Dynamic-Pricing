"""Treatment (propensity) model: P(T = 1 | X).

Thin wrapper over src/nuisance_models.py so that the Week 3 interface exists
without duplicating code. Scores are cross-fitted (out-of-fold).
"""
import pandas as pd

try:
    from src.nuisance_models import (
        DATA_PATH, TREATMENT, candidate_models, check_config, evaluate, oof_predict)
except ImportError:  # when run as: python src/treatment_model.py
    from nuisance_models import (
        DATA_PATH, TREATMENT, candidate_models, check_config, evaluate, oof_predict)


def propensity_scores(df, model_name="random_forest"):
    """Cross-fitted propensity scores P(T=1 | X), aligned with df's rows."""
    check_config()
    scores = oof_predict(df, TREATMENT, candidate_models()[model_name])
    scores = pd.Series(scores, index=df.index, name="propensity")
    validate_scores(scores)
    return scores


def validate_scores(scores):
    """Scores must be valid probabilities, with no missing values."""
    if scores.isna().any():
        raise ValueError("Propensity scores contain missing values.")
    if not scores.between(0, 1).all():
        raise ValueError("Propensity scores must be between 0 and 1.")


def class_balance(df):
    """Counts and share of treated and untreated customers."""
    counts = df[TREATMENT].value_counts().sort_index()
    return pd.DataFrame({"count": counts, "share": (counts / len(df)).round(4)})


def overlap_summary(scores, low=0.05, high=0.95):
    """Range of scores and the share of customers close to 0 or 1."""
    return {
        "min": round(float(scores.min()), 4),
        "max": round(float(scores.max()), 4),
        "mean": round(float(scores.mean()), 4),
        f"share_below_{low}": round(float((scores < low).mean()), 4),
        f"share_above_{high}": round(float((scores > high).mean()), 4),
    }


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    print("Treatment class balance:")
    print(class_balance(df))
    print("\nTreatment model comparison (cross-validated):")
    print(pd.DataFrame(evaluate(df, TREATMENT)).to_string(index=False))
    scores = propensity_scores(df)
    print("\nOverlap summary (random_forest):")
    for k, v in overlap_summary(scores).items():
        print(f"  {k}: {v}")