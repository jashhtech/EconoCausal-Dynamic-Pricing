"""Outcome model: P(Y = 1 | X).

Thin wrapper over src/nuisance_models.py so that the Week 3 interface exists
without duplicating code. Predictions are cross-fitted (out-of-fold) and use the
confounders X only (partialling-out DML formulation).
"""
import pandas as pd

try:
    from src.nuisance_models import (
        DATA_PATH, OUTCOME, candidate_models, check_config, evaluate, oof_predict)
except ImportError:  # when run as: python src/outcome_model.py
    from nuisance_models import (
        DATA_PATH, OUTCOME, candidate_models, check_config, evaluate, oof_predict)


def outcome_predictions(df, model_name="random_forest"):
    """Cross-fitted outcome probabilities P(Y=1 | X), aligned with df's rows."""
    check_config()
    preds = oof_predict(df, OUTCOME, candidate_models()[model_name])
    preds = pd.Series(preds, index=df.index, name="outcome_pred")
    validate_predictions(preds)
    return preds


def validate_predictions(preds):
    """Predictions must be valid probabilities, with no missing values."""
    if preds.isna().any():
        raise ValueError("Outcome predictions contain missing values.")
    if not preds.between(0, 1).all():
        raise ValueError("Outcome predictions must be between 0 and 1.")


def class_balance(df):
    """Counts and share of responders and non-responders."""
    counts = df[OUTCOME].value_counts().sort_index()
    return pd.DataFrame({"count": counts, "share": (counts / len(df)).round(4)})


def prediction_summary(preds):
    """Range and mean of the predicted outcome probabilities."""
    return {
        "min": round(float(preds.min()), 4),
        "max": round(float(preds.max()), 4),
        "mean": round(float(preds.mean()), 4),
    }


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    print("Outcome class balance:")
    print(class_balance(df))
    print("\nOutcome model comparison (cross-validated):")
    print(pd.DataFrame(evaluate(df, OUTCOME)).to_string(index=False))
    preds = outcome_predictions(df)
    print("\nPrediction summary (random_forest):")
    for k, v in prediction_summary(preds).items():
        print(f"  {k}: {v}")