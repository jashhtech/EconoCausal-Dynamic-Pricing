
"""
EconoCausal - Nuisance Models
Week 3: DML Integration and Evaluation
Week 4: Treatment Overlap Diagnostics

Outcome model   : Y ~ X
Treatment model : T ~ X

Exploratory configuration. Historical campaign exposure is not
an assigned discount amount.
"""

from pathlib import Path
import matplotlib.pyplot as plt

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from dml_estimation import estimate_dml_from_residuals


# ======================= CONFIGURATION =======================

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "retail_data.csv"
)

TREATMENT = "campaign_exposure"
OUTCOME = "campaign_response"

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

# Diagnostic thresholds, not automatic exclusion rules
LOW_PROPENSITY = 0.05
HIGH_PROPENSITY = 0.95

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
        raise ValueError(
            "Duplicate columns found in feature configuration."
        )


def load_data():
    """Load dataset and validate required columns."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required_columns = NUMERIC + CATEGORICAL + [TREATMENT, OUTCOME]

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

    for target in [TREATMENT, OUTCOME]:
        if set(df[target].unique()) != {0, 1}:
            raise ValueError(
                f"{target} must contain only binary values 0 and 1."
            )

    return df


def make_preprocessor():
    """Create preprocessing pipeline."""

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

    return pd.Series(predictions, index=df.index)


def evaluate(df, target):
    """Evaluate candidate models using AUC and log loss."""

    y = df[target]
    rows = []

    for name, model in candidate_models().items():

        predictions = oof_predict(df, target, model)

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
    outcome_model="random_forest",
    treatment_model="random_forest",
):
    """Generate cross-fitted DML residuals."""

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


def treatment_overlap_analysis(df, t_hat):
    """
    Examine propensity-score distributions and common support
    for treated and control observations.
    """

    treated = t_hat[df[TREATMENT] == 1]
    control = t_hat[df[TREATMENT] == 0]

    print("\nTREATMENT OVERLAP ANALYSIS")
    print("==========================")

    print("\nTreated group propensity scores:")
    print(treated.describe().round(4))

    print("\nControl group propensity scores:")
    print(control.describe().round(4))

    if treated.empty or control.empty:
        print("\nWARNING: One treatment group is empty.")
        return

    # Range shared by both groups
    overlap_lower = max(treated.min(), control.min())
    overlap_upper = min(treated.max(), control.max())

    print("\nCommon support range:")
    print(f"Lower bound: {overlap_lower:.4f}")
    print(f"Upper bound: {overlap_upper:.4f}")

    if overlap_lower >= overlap_upper:
        print("WARNING: No common support detected.")
        return

    print("Common support exists.")

    # Extreme propensity scores
    print("\nExtreme Propensity Score Check")
    print("--------------------------------")

    low_count = (t_hat < LOW_PROPENSITY).sum()
    high_count = (t_hat > HIGH_PROPENSITY).sum()

    central_count = (
        (t_hat >= LOW_PROPENSITY)
        & (t_hat <= HIGH_PROPENSITY)
    ).sum()

    print(f"Scores below {LOW_PROPENSITY}: {low_count}")
    print(f"Scores above {HIGH_PROPENSITY}: {high_count}")
    print(
        f"Scores between {LOW_PROPENSITY} and "
        f"{HIGH_PROPENSITY}: {central_count}"
    )

    # Common support coverage
    in_common_support = (
        (t_hat >= overlap_lower)
        & (t_hat <= overlap_upper)
    )

    overlap_count = in_common_support.sum()
    overlap_percentage = overlap_count / len(t_hat) * 100

    print("\nCommon Support Coverage")
    print("-----------------------")

    print(f"Customers in common support: {overlap_count}")
    print(f"Common support coverage: {overlap_percentage:.2f}%")

    # Coverage by treatment group
    treated_inside = (
        (treated >= overlap_lower)
        & (treated <= overlap_upper)
    ).sum()

    control_inside = (
        (control >= overlap_lower)
        & (control <= overlap_upper)
    ).sum()

    print("\nCoverage by Treatment Group")
    print("---------------------------")

    print(
        f"Treated inside support: {treated_inside}/{len(treated)} "
        f"({treated_inside / len(treated) * 100:.2f}%)"
    )

    print(
        f"Control inside support: {control_inside}/{len(control)} "
        f"({control_inside / len(control) * 100:.2f}%)"
    )

    print(
        "\nNote: Shared min-max ranges do not prove adequate "
        "distributional overlap. Further diagnostics are needed."
    )


def plot_propensity_overlap(df, t_hat):
    """Plot propensity-score distributions for treated and control groups."""

    plt.figure(figsize=(10, 6))

    plt.hist(
        t_hat[df[TREATMENT] == 1],
        bins=25,
        alpha=0.6,
        density=True,
        label="Treated",
    )

    plt.hist(
        t_hat[df[TREATMENT] == 0],
        bins=25,
        alpha=0.6,
        density=True,
        label="Control",
    )

    plt.xlabel("Propensity Score")
    plt.ylabel("Density")
    plt.title("Propensity Score Overlap: Treated vs Control")
    plt.legend()
    plt.grid(alpha=0.3)

    output_dir = (
        Path(__file__).resolve().parent.parent / "graphs"
    )
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "propensity_score_overlap.png"

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

    print(f"\nOverlap plot saved to: {output_path}")


def run_sensitivity_analysis(df):
    """Compare DML estimates across nuisance-model configurations.

    Each configuration uses the same model family for the outcome and
    treatment nuisance models. Estimates are exploratory and depend on
    the chosen feature set and historical campaign variables.
    """

    models = ["logistic", "random_forest", "grad_boosting"]
    rows = []

    print("\nDML SENSITIVITY ANALYSIS")
    print("========================")

    for model_name in models:
        print(f"\nEvaluating: {model_name}")

        y_residual, t_residual = dml_residuals(
            df,
            outcome_model=model_name,
            treatment_model=model_name,
        )

        result = estimate_dml_from_residuals(y_residual, t_residual)

        rows.append({
            "model": model_name,
            "effect": result.effect,
            "standard_error": result.standard_error,
            "ci_lower": result.ci_lower,
            "ci_upper": result.ci_upper,
            "sample_size": result.sample_size,
        })

    results_df = pd.DataFrame(rows)
    print("\nSensitivity Analysis Results:")
    print(results_df.round(4).to_string(index=False))
    return results_df


# ======================= MAIN EXECUTION =======================

if __name__ == "__main__":
    check_config()
    df = load_data()

    print("Dataset loaded successfully.")
    print(f"Number of observations: {len(df)}")

    print("\nTreatment:", TREATMENT)
    print("Outcome:", OUTCOME)
    print("Numeric confounders:", NUMERIC)
    print("Categorical confounders:", CATEGORICAL)

    # Evaluate nuisance models
    print("\nEvaluating nuisance models...")
    results = evaluate(df, OUTCOME) + evaluate(df, TREATMENT)
    print("\nModel evaluation results:")
    print(pd.DataFrame(results).to_string(index=False))

    # Main DML estimate using the selected random-forest configuration
    print("\nRunning DML estimation...")
    y_residual, t_residual = dml_residuals(
        df,
        outcome_model="random_forest",
        treatment_model="random_forest",
    )
    result = estimate_dml_from_residuals(y_residual, t_residual)

    print("\nDML ESTIMATION RESULTS")
    print("----------------------")
    print(f"Estimated coefficient: {result.effect:.4f}")
    print(f"Standard error: {result.standard_error:.4f}")
    print(
        f"95% confidence interval: "
        f"[{result.ci_lower:.4f}, {result.ci_upper:.4f}]"
    )
    print(f"Sample size: {result.sample_size}")

    # Compare estimates across nuisance-model configurations
    sensitivity_results = run_sensitivity_analysis(df)

    # Propensity-score diagnostics using the random-forest treatment model
    print("\nPropensity score summary:")
    t_hat = oof_predict(
        df,
        TREATMENT,
        candidate_models()["random_forest"],
    )
    print(t_hat.describe().round(4))

    # Week 4 overlap diagnostics
    treatment_overlap_analysis(df, t_hat)
    plot_propensity_overlap(df, t_hat)

    print("\nDML integration completed.")
    print(
        "\nIMPORTANT: The treatment represents historical campaign "
        "exposure, not an assigned discount amount. The estimate is "
        "exploratory and must not be interpreted as a verified causal "
        "discount effect."
    )
