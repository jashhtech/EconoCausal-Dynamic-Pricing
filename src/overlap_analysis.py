"""Week 4 Day 4: treatment overlap (positivity) and imbalance analysis.

Uses the cross-fitted propensity scores from src/treatment_model.py.
Reports score distribution by treatment group, how many customers sit near 0
or 1, and how many customers remain if scores are trimmed at common cut-offs.
Run with:  python src/overlap_analysis.py
"""
from pathlib import Path

import pandas as pd

try:
    from src.nuisance_models import DATA_PATH, TREATMENT
    from src.treatment_model import class_balance, propensity_scores
except ImportError:  # when run as: python src/overlap_analysis.py
    from nuisance_models import DATA_PATH, TREATMENT
    from treatment_model import class_balance, propensity_scores

RESULTS_PATH = Path(__file__).resolve().parent.parent / "results" / "overlap_analysis.csv"
CUTOFFS = [(0.01, 0.99), (0.05, 0.95), (0.10, 0.90)]


def group_summary(scores, t):
    """Propensity score distribution for treated and untreated customers."""
    rows = []
    for label, mask in [("treated (T=1)", t == 1), ("untreated (T=0)", t == 0)]:
        s = scores[mask]
        rows.append({"group": label, "n": int(mask.sum()),
                     "min": round(s.min(), 4), "p25": round(s.quantile(0.25), 4),
                     "median": round(s.median(), 4), "p75": round(s.quantile(0.75), 4),
                     "max": round(s.max(), 4)})
    return pd.DataFrame(rows)


def trimming_table(scores, t):
    """Customers kept, and treated/untreated left, after trimming at each cut-off."""
    rows = []
    for low, high in CUTOFFS:
        keep = scores.between(low, high)
        rows.append({"cutoff": f"[{low}, {high}]",
                     "kept": int(keep.sum()),
                     "kept_share": round(float(keep.mean()), 4),
                     "treated_kept": int((keep & (t == 1)).sum()),
                     "untreated_kept": int((keep & (t == 0)).sum()),
                     "treated_dropped": int((~keep & (t == 1)).sum()),
                     "untreated_dropped": int((~keep & (t == 0)).sum())})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    t = df[TREATMENT]
    scores = propensity_scores(df)

    print("Treatment class balance:")
    print(class_balance(df))
    print("\nPropensity score by treatment group:")
    groups = group_summary(scores, t)
    print(groups.to_string(index=False))

    common_low = max(scores[t == 1].min(), scores[t == 0].min())
    common_high = min(scores[t == 1].max(), scores[t == 0].max())
    print(f"\nCommon support (range where both groups have customers): "
          f"[{common_low:.4f}, {common_high:.4f}]")

    print("\nTrimming sensitivity:")
    trim = trimming_table(scores, t)
    print(trim.to_string(index=False))

    RESULTS_PATH.parent.mkdir(exist_ok=True)
    pd.concat([groups.assign(section="group_summary"),
               trim.assign(section="trimming")], ignore_index=True).to_csv(
        RESULTS_PATH, index=False)
    print("\nSaved:", RESULTS_PATH)