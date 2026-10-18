"""
EconoCausal - Feature Configuration

Defines the structure required for Double Machine Learning.
Actual column names must be verified against the dataset.
"""

# Update these values only after checking the dataset documentation.
TREATMENT_COLUMN = None
OUTCOME_COLUMN = None
CONFOUNDER_COLUMNS = []

def validate_feature_config(columns):
    """Validate configured columns against dataset columns."""

    if TREATMENT_COLUMN is None or OUTCOME_COLUMN is None:
        raise ValueError(
            "Treatment and outcome columns must be confirmed "
            "from the actual dataset before proceeding."
        )

    required_columns = [
        TREATMENT_COLUMN,
        OUTCOME_COLUMN,
        *CONFOUNDER_COLUMNS,
    ]

    missing_columns = [
        column for column in required_columns
        if column not in columns
    ]

    if missing_columns:
        raise ValueError(
            f"Columns not found in dataset: {missing_columns}"
        )

    print("Feature configuration validated successfully.")
    print("Treatment:", TREATMENT_COLUMN)
    print("Outcome:", OUTCOME_COLUMN)
    print("Confounders:", CONFOUNDER_COLUMNS)