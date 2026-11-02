import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def encode_categorical_features(X):
    """Encode categorical columns using One-Hot Encoding."""

    categorical_columns = X.select_dtypes(
        include=["object", "str"]
    ).columns.tolist()

    if not categorical_columns:
        print("No categorical columns found.")
        return X

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    )

    encoded_values = encoder.fit_transform(
        X[categorical_columns]
    )

    encoded_df = pd.DataFrame(
        encoded_values,
        columns=encoder.get_feature_names_out(
            categorical_columns
        ),
        index=X.index
    )

    numerical_df = X.drop(columns=categorical_columns)

    result = pd.concat(
        [numerical_df, encoded_df],
        axis=1
    )

    print("Categorical columns encoded:", categorical_columns)
    print("Original shape:", X.shape)
    print("Encoded shape:", result.shape)

    return result