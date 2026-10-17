import pandas as pd


def prepare_features(df):
    treatment_col = "Discount Received"
    outcome_col = "Purchase"

    confounder_cols = [
        "Past Purchases",
        "Past Spending"
    ]

    required_cols = (
        confounder_cols
        + [treatment_col, outcome_col]
    )

    missing_cols = [
        col for col in required_cols
        if col not in df.columns
    ]

    if missing_cols:
        raise ValueError(
            f"Missing required columns: {missing_cols}"
        )

    data = df[required_cols].copy()
    data = data.dropna()

    X = data[confounder_cols]
    T = data[treatment_col]
    Y = data[outcome_col]

    return X, T, Y


if __name__ == "__main__":
    print("Feature engineering module ready.")