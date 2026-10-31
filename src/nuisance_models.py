
"""
EconoCausal - Nuisance Models
Week 3: DML Integration and Evaluation

Outcome model   : Y ~ X
Treatment model : T ~ X

This is an exploratory configuration.
Final treatment, outcome and confounders require team confirmation.
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


# ======================= CONFIGURATION =======================

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "retail_data.csv"
)

# Exploratory treatment and outcome
TREATMENT = "campaign_exposure"
OUTCOME = "campaign_response"

# Provisional pre-treatment confounders
NUMERIC = [
    "age",
    "Income",
    "Kidhome",
    "Teenhome",
    "Recency",
]

CATEGORICAL = [
    "Education",
    "Marital_Status",
]

# These columns must never be used as confounders
LEAKAGE_COLUMNS = [
    "Response",
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
]

SEED = 42
N_SPLITS = 5

# =============================================================


def check_config():
    """Validate feature configuration and prevent leakage."""

    banned = set(LEAKAGE_COLUMNS) | {TREATMENT, OUTCOME}
    features = NUMERIC + CATEGORICAL

    bad = [column for column in features if column in banned]

    if bad:
        raise ValueError(
            f"Leakage risk: these columns cannot be features: {bad}"
        )

    if len(features) != len(set(features)):
        raise ValueError("Duplicate columns found in feature configuration.")


def load_data():
    """Load dataset and validate required columns."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required_columns = (
        NUMERIC
        + CATEGORICAL
        + [TREATMENT, OUTCOME]
    )

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {missing}"
        )

    if df[required_columns].isnull().any().any():
        raise ValueError(
            "Missing values found in required columns. "
            "Handle them before model evaluation."
        )

    return df


def make_preprocessor():
    """Create preprocessing pipeline for numeric and categorical features."""

    return ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            CATEGORICAL,
        ),
    ])


def candidate_models():
    """Return candidate classification models."""

    return {
        "logistic": LogisticRegression(max_iter=1000),

        "random_forest": RandomForestClassifier(
            n_estimators=200,
            min_samples_leaf=5,
            random_state=SEED,
            n_jobs=-1,
        ),

        "grad_boosting": GradientBoostingClassifier(
            random_state=SEED
        ),
    }


def oof_predict(df, target, model):
    """Generate out-of-fold probability predictions."""

    X = df[NUMERIC + CATEGORICAL]
    y = df[target]

    if y.nunique() != 2:
        raise ValueError(
            f"{target} must contain exactly two classes."
        )

    if y.value_counts().min() < N_SPLITS:
        raise ValueError(
            f"Not enough observations in each class for "
            f"{N_SPLITS}-fold stratified cross-fitting."
        )

    cv = StratifiedKFold(
        n_splits=N_SPLITS,
        shuffle=True,
        random_state=SEED,
    )

    pipeline = make_pipeline(
        make_preprocessor(),
        model,
    )

    predictions = cross_val_predict(
        pipeline,
        X,
        y,
        cv=cv,
        method="predict_proba",
    )[:, 1]

    return predictions


def evaluate(df, target):
    """Evaluate candidate models using AUC and log loss."""

    y = df[target]
    rows = []

    for name, model in candidate_models().items():

        predictions = oof_predict(
            df,
            target,
            model,
        )

        rows.append({
            "target": target,
            "model": name,
            "auc": round(
                roc_auc_score(y, predictions), 4
            ),
            "log_loss": round(
                log_loss(y, predictions), 4
            ),
        })

    return rows


def dml_residuals(
    df,
    outcome_model="grad_boosting",
    treatment_model="random_forest",
):
    """
    Generate cross-fitted DML residuals.

    Y residual = actual outcome - predicted outcome
    T residual = actual treatment - predicted treatment
    """

    y_hat = oof_predict(
        df,
        OUTCOME,
        candidate_models()[outcome_model],
    )

    t_hat = oof_predict(
        df,
        TREATMENT,
        candidate_models()[treatment_model],
    )

    y_residual = df[OUTCOME] - y_hat
    t_residual = df[TREATMENT] - t_hat

    return y_residual, t_residual


if __name__ == "__main__":

    check_config()

    df = load_data()

    print("Dataset loaded successfully.")
    print(f"Number of observations: {len(df)}")

    print("\nTreatment:", TREATMENT)
    print("Outcome:", OUTCOME)
    print("Numeric confounders:", NUMERIC)
    print("Categorical confounders:", CATEGORICAL)

    print("\nEvaluating nuisance models...")

    results = (
        evaluate(df, OUTCOME)
        + evaluate(df, TREATMENT)
    )

    print("\nModel evaluation results:")
    print(
        pd.DataFrame(results).to_string(index=False)
    )

    # Propensity-score summary
    t_hat = oof_predict(
        df,
        TREATMENT,
        candidate_models()["random_forest"],
    )

    print("\nPropensity score summary:")
    print(
        pd.Series(t_hat).describe().round(4)
    )

    print("\nNuisance model evaluation completed.")
    print(
        "Note: These results are exploratory, "
        "not proof of causal effects."
    )
