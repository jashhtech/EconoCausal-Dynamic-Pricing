"""
EconoCausal - data check script (Week 2).

Teen purane checks + ek naya: treated vs untreated group ka balance
(standardized mean difference). Ye batata hai ki kaun se confounders
exposure ke saath sabse zyada jude hain.

Chalane ka tareeka (repo root se):
    python src/data_check.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "retail_data.csv"
TREATMENT = "campaign_exposure"
OUTCOME = "campaign_response"
CONFOUNDERS = ["age", "Income", "Kidhome", "Teenhome", "Recency",
               "total_purchase_amount", "total_purchases"]


def smd(treated, control):
    """Standardized mean difference. 0.1 se upar = dono group kaafi alag hain."""
    pooled_sd = np.sqrt((treated.var() + control.var()) / 2)
    return (treated.mean() - control.mean()) / pooled_sd


def main():
    if not DATA_PATH.exists():
        print(f"File not found: {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    needed = [TREATMENT, OUTCOME, "Response", "deal_purchase_indicator"] + CONFOUNDERS
    missing_cols = [c for c in needed if c not in df.columns]
    if missing_cols:
        print("These columns are not in the file:", missing_cols)
        return

    print("Shape (rows, columns):", df.shape)

    print(f"\n1. {TREATMENT} counts")
    print(df[TREATMENT].value_counts(dropna=False))

    print(f"\n2. {OUTCOME} vs Response (leakage check)")
    same_share = (df[OUTCOME] == df["Response"]).mean()
    print(f"Rows where both columns are equal: {same_share:.1%}")

    print("\n3. deal_purchase_indicator values")
    print(df["deal_purchase_indicator"].value_counts(dropna=False))

    print(f"\n4. Balance of confounders (exposed vs not exposed)")
    treated = df[df[TREATMENT] == 1]
    control = df[df[TREATMENT] == 0]
    rows = [{"confounder": c,
             "mean_exposed": round(treated[c].mean(), 2),
             "mean_not_exposed": round(control[c].mean(), 2),
             "smd": round(smd(treated[c], control[c]), 3)} for c in CONFOUNDERS]
    table = pd.DataFrame(rows).sort_values("smd", key=abs, ascending=False)
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()