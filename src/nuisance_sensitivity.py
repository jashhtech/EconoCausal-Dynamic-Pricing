"""
Sensitivity check: nuisance model performance with and without the
purchase columns that may be post-treatment.
Run from repo root:  python src/nuisance_sensitivity.py
"""
import pandas as pd

import nuisance_models as nm

POST_TREATMENT_CANDIDATES = ["total_purchase_amount", "total_purchases"]

if __name__ == "__main__":
    df = pd.read_csv(nm.DATA_PATH)
    full = list(nm.NUMERIC)
    settings = [
        ("all confounders", full),
        ("without purchase columns", [c for c in full if c not in POST_TREATMENT_CANDIDATES]),
    ]
    rows = []
    for label, numeric in settings:
        nm.NUMERIC = numeric
        for r in nm.evaluate(df, nm.OUTCOME) + nm.evaluate(df, nm.TREATMENT):
            rows.append({"features": label, **r})
    print(pd.DataFrame(rows).to_string(index=False))