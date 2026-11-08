
from pathlib import Path
import pandas as pd

import nuisance_models as nm
from dml_estimation import estimate_dml_from_residuals


PURCHASE_COLUMNS = [
    "total_purchase_amount",
    "total_purchases",
]

EXPECTED_COUNTS = {
    "Full sample": 2237,
    "0.05-0.95": 2121,
    "0.10-0.90": 1670,
}


def main():
    nm.check_config()
    df = nm.load_data()

    print("Generating full-sample propensity scores...")

    # Use the original confounders for consistent sample trimming.
    propensity = nm.oof_predict(
        df,
        nm.TREATMENT,
        nm.candidate_models()["random_forest"],
    )

    samples = {
        "Full sample": pd.Series(True, index=df.index),
        "0.05-0.95": propensity.between(0.05, 0.95),
        "0.10-0.90": propensity.between(0.10, 0.90),
    }

    print("\nChecking trimmed sample sizes:")
    for name, mask in samples.items():
        actual = int(mask.sum())
        expected = EXPECTED_COUNTS[name]
        print(f"{name}: {actual} customers (expected: {expected})")

        if actual != expected:
            print("WARNING: Count differs from teammate's overlap results.")

    # Save customer-level propensity scores for reproducibility.
    output_dir = Path(__file__).resolve().parent.parent / "results"
    output_dir.mkdir(exist_ok=True)

    pd.DataFrame({
        "customer_index": df.index,
        "propensity_score": propensity.values,
    }).to_csv(output_dir / "propensity_scores.csv", index=False)

    # Two feature specifications.
    feature_specs = {
        "Without purchase columns": nm.NUMERIC.copy(),
        "With purchase columns": nm.NUMERIC.copy() + PURCHASE_COLUMNS,
    }

    missing = [
        col for col in PURCHASE_COLUMNS if col not in df.columns
    ]
    if missing:
        raise ValueError(f"Missing purchase columns: {missing}")

    results = []

    for sample_name, mask in samples.items():
        subset = df.loc[mask].copy()

        for spec_name, numeric_features in feature_specs.items():
            print(f"\nRunning: {sample_name} | {spec_name}")

            # Update the feature list used by the existing pipeline.
            nm.NUMERIC = numeric_features

            y_residual, t_residual = nm.dml_residuals(
                subset,
                outcome_model="random_forest",
                treatment_model="random_forest",
            )

            result = estimate_dml_from_residuals(
                y_residual,
                t_residual,
            )

            results.append({
                "sample": sample_name,
                "feature_specification": spec_name,
                "effect": result.effect,
                "standard_error": result.standard_error,
                "ci_lower": result.ci_lower,
                "ci_upper": result.ci_upper,
                "sample_size": result.sample_size,
            })

    # Restore the original feature configuration.
    nm.NUMERIC = feature_specs["Without purchase columns"]

    results_df = pd.DataFrame(results)

    output_path = output_dir / "trimmed_dml_results.csv"
    results_df.to_csv(output_path, index=False)

    print("\n========== TRIMMED DML RESULTS ==========")
    print(results_df.round(4).to_string(index=False))
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
