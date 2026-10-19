from pathlib import Path
import pandas as pd

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


def load_dataset(path=DATA_PATH):
    if not Path(path).exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)


def validate_dataset(df):
    required = [TREATMENT, OUTCOME, *CONFOUNDERS]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.empty:
        raise ValueError("Dataset is empty.")

    if df[required].isnull().any().any():
        raise ValueError("Required variables contain missing values.")

    if not set(df[TREATMENT].unique()).issubset({0, 1}):
        raise ValueError("Treatment must contain only 0 and 1.")

    if df[TREATMENT].nunique() < 2:
        raise ValueError("Treatment must contain both classes.")

    if not pd.api.types.is_numeric_dtype(df[OUTCOME]):
        raise ValueError("Outcome must be numeric.")

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def main():
    df = load_dataset()
    report = validate_dataset(df)

    print("Dataset validation passed.")
    for key, value in report.items():
        print(f"{key}: {value}")

    print("Candidate variables:", TREATMENT, OUTCOME, CONFOUNDERS)


if __name__ == "__main__":
    main()
    