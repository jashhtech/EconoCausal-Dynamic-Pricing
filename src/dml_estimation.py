
from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "retail_data.csv"

TREATMENT = "deal_purchase_indicator"
OUTCOME = "total_purchase_amount"

CONFOUNDERS = [
    "age",
    "Income",
    "Education",
    "Marital_Status",
    "Recency",
]

# Change to True only after the team approves these variables.
VARIABLES_APPROVED = True

def load_dataset(path=DATA_PATH):
    if not Path(path).exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)

def validate_dataset(df):
    required = [TREATMENT, OUTCOME, *CONFOUNDERS]
    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if df.empty or df[required].isnull().any().any():
        raise ValueError("Dataset is empty or required values are missing.")

    if not set(df[TREATMENT].unique()).issubset({0, 1}):
        raise ValueError("Treatment must contain only 0 and 1.")

    if df[TREATMENT].nunique() != 2:
        raise ValueError("Both treatment groups are required.")

    if not pd.api.types.is_numeric_dtype(df[OUTCOME]):
        raise ValueError("Outcome must be numeric.")

    if len(df) < 10:
        raise ValueError("Not enough observations for cross-fitting.")

def make_preprocessor(X):
    numeric = X.select_dtypes(include="number").columns.tolist()
    categorical = X.select_dtypes(exclude="number").columns.tolist()

    transformers = []

    if numeric:
        transformers.append((
            "numeric",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median"))
            ]),
            numeric,
        ))

    if categorical:
        transformers.append((
            "categorical",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]),
            categorical,
        ))

    return ColumnTransformer(transformers)

def estimate_dml(df, n_splits=5, random_state=42):
    X = df[CONFOUNDERS].copy()
    treatment = df[TREATMENT].to_numpy(dtype=float)
    outcome = df[OUTCOME].to_numpy(dtype=float)

    counts = np.bincount(treatment.astype(int), minlength=2)
    if counts.min() < n_splits:
        raise ValueError(
            "Each treatment group must have at least n_splits observations."
        )

    # Separate nuisance models for outcome and treatment.
    outcome_model = Pipeline([
        ("preprocess", make_preprocessor(X)),
        ("model", RandomForestRegressor(
            n_estimators=200, min_samples_leaf=5,
            random_state=random_state, n_jobs=-1
        )),
    ])

    treatment_model = Pipeline([
        ("preprocess", make_preprocessor(X)),
        ("model", RandomForestClassifier(
            n_estimators=200, min_samples_leaf=5,
            random_state=random_state, n_jobs=-1
        )),
    ])

    outcome_prediction = np.zeros(len(df))
    treatment_prediction = np.zeros(len(df))

    folds = StratifiedKFold(
        n_splits=n_splits, shuffle=True, random_state=random_state
    )

    for train_idx, test_idx in folds.split(X, treatment):
        g_model = clone(outcome_model)
        m_model = clone(treatment_model)

        g_model.fit(X.iloc[train_idx], outcome[train_idx])
        m_model.fit(X.iloc[train_idx], treatment[train_idx])

        outcome_prediction[test_idx] = g_model.predict(X.iloc[test_idx])
        treatment_prediction[test_idx] = m_model.predict_proba(
            X.iloc[test_idx]
        )[:, 1]

    y_residual = outcome - outcome_prediction
    d_residual = treatment - treatment_prediction

    denominator = np.mean(d_residual ** 2)
    if denominator < 1e-8:
        raise ValueError(
            "Treatment residual variance is too small; check overlap."
        )

    effect = np.mean(d_residual * y_residual) / denominator

    # Approximate standard error for the cross-fitted PLR estimate.
    influence = d_residual * (y_residual - effect * d_residual)
    standard_error = (
        np.sqrt(np.mean(influence ** 2) / len(df)) / denominator
    )

    return {
        "estimate": float(effect),
        "standard_error": float(standard_error),
        "ci_lower_95": float(effect - 1.96 * standard_error),
        "ci_upper_95": float(effect + 1.96 * standard_error),
        "n_observations": int(len(df)),
        "n_splits": n_splits,
    }

def main():
    df = load_dataset()
    validate_dataset(df)

    if not VARIABLES_APPROVED:
        raise RuntimeError(
            "DML estimation is blocked until the team approves "
            "treatment, outcome, and confounders. Update "
            "VARIABLES_APPROVED only after confirmation."
        )

    results = estimate_dml(df)

    print("DML estimation completed.")
    for name, value in results.items():
        print(f"{name}: {value}")

    output_path = PROJECT_ROOT / "docs" / "dml_estimate.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([results]).to_csv(output_path, index=False)
    print("Saved:", output_path)

if __name__ == "__main__":
    main()