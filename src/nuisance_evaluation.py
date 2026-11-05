
"""Week 3 evaluation of nuisance models."""

import pandas as pd
from pathlib import Path
from sklearn.metrics import (
    brier_score_loss,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)

try:
    from src.nuisance_models import DATA_PATH, OUTCOME, TREATMENT
    from src.outcome_model import outcome_predictions
    from src.treatment_model import propensity_scores
except ImportError:
    from nuisance_models import DATA_PATH, OUTCOME, TREATMENT
    from outcome_model import outcome_predictions
    from treatment_model import propensity_scores

RESULTS_PATH = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "nuisance_evaluation.csv"
)


def evaluate_model(name, y, p):
    rows = []
    base_rate = float(y.mean())

    for label, threshold in [
        ("0.5", 0.5),
        ("base_rate", base_rate),
    ]:
        pred = (p >= threshold).astype(int)

        rows.append({
            "model": name,
            "threshold_type": label,
            "threshold": round(threshold, 4),
            "roc_auc": round(roc_auc_score(y, p), 4),
            "log_loss": round(log_loss(y, p), 4),
            "brier": round(brier_score_loss(y, p), 4),
            "precision": round(
                precision_score(y, pred, zero_division=0), 4
            ),
            "recall": round(
                recall_score(y, pred, zero_division=0), 4
            ),
            "predicted_positive_share": round(
                float(pred.mean()), 4
            ),
        })

    return rows


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)

    t_hat = propensity_scores(df)
    y_hat = outcome_predictions(df)

    rows = (
        evaluate_model("treatment (campaign_exposure)",
                       df[TREATMENT], t_hat)
        + evaluate_model("outcome (campaign_response)",
                         df[OUTCOME], y_hat)
    )

    result = pd.DataFrame(rows)

    print(result.to_string(index=False))

    RESULTS_PATH.parent.mkdir(exist_ok=True)
    result.to_csv(RESULTS_PATH, index=False)

    print("\nSaved:", RESULTS_PATH)
