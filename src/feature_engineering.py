import pandas as pd

DATA_PATH = "data/retail_data.csv"

# Provisional choices: verify the dataset definitions
# before using these for causal estimation.
TREATMENT_COLUMN = "deal_purchase_indicator"
OUTCOME_COLUMN = "total_purchase_amount"

CONFOUNDER_COLUMNS = [
    "age",
    "total_purchases",
]

def load_and_prepare_features(data_path=DATA_PATH):
    """Load the retail dataset and prepare X, T and Y."""

    df = pd.read_csv(data_path)

    required_columns = (
        [TREATMENT_COLUMN, OUTCOME_COLUMN]
        + CONFOUNDER_COLUMNS
    )

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    selected = df[required_columns].copy()

    for col in required_columns:
        selected[col] = pd.to_numeric(
            selected[col], errors="coerce"
        )

    selected = selected.dropna()

    X = selected[CONFOUNDER_COLUMNS]
    T = selected[TREATMENT_COLUMN]
    Y = selected[OUTCOME_COLUMN]

    print("Dataset loaded successfully.")
    print("Rows after cleaning:", len(selected))
    print("Confounder features:", X.columns.tolist())
    print("Treatment column:", T.name)
    print("Outcome column:", Y.name)

    return X, T, Y

if __name__ == "__main__":
    X, T, Y = load_and_prepare_features()

    print("X shape:", X.shape)
    print("T shape:", T.shape)
    print("Y shape:", Y.shape)