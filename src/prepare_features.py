import pandas as pd


def prepare_features(
    df,
    treatment_column,
    outcome_column,
    confounder_columns,
):
    """
    Prepare X (confounders), T (treatment), and Y (outcome)
    for the EconoCausal Double Machine Learning pipeline.
    """

    required_columns = [
        treatment_column,
        outcome_column,
        *confounder_columns,
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Columns missing from dataset: {missing_columns}"
        )

    selected_data = df[required_columns].copy()

    # Remove rows with missing values in selected variables.
    selected_data = selected_data.dropna()

    X = selected_data[confounder_columns]
    T = selected_data[treatment_column]
    Y = selected_data[outcome_column]

    print("Feature preparation completed.")
    print("X shape:", X.shape)
    print("T shape:", T.shape)
    print("Y shape:", Y.shape)

    return X, T, Y


if __name__ == "__main__":
    print("EconoCausal feature preparation module is ready.")
    print("Provide a dataset and verified column names to use it.")