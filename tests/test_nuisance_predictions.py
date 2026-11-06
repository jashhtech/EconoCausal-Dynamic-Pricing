"""Week 4 validation of the nuisance models (Day 1 and Day 2).

Day 1: confirm that the metrics match the model types (both targets are binary).
Day 2: verify out-of-fold predictions, alignment, leakage guard, reproducibility.
Run with:  python tests/test_nuisance_predictions.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import nuisance_models as nm
from nuisance_predictions import build_nuisance_predictions, check_reproducible

df = pd.read_csv(nm.DATA_PATH)
preds = build_nuisance_predictions(df)
results = []


def check(name, condition):
    results.append((name, bool(condition)))
    print(("PASS  " if condition else "FAIL  ") + name)


# Day 1: metric types
check("treatment is binary (0/1)", set(df[nm.TREATMENT].unique()) <= {0, 1})
check("outcome is binary (0/1)", set(df[nm.OUTCOME].unique()) <= {0, 1})

# Day 2: out-of-fold predictions and alignment
check("row count matches input", len(preds) == len(df))
check("index matches input", preds.index.equals(df.index))
check("no missing values", not preds.isna().any().any())
check("T and Y match the input columns",
      (preds["T"].values == df[nm.TREATMENT].values).all()
      and (preds["Y"].values == df[nm.OUTCOME].values).all())
check("propensity strictly inside (0, 1)", preds["propensity"].between(0, 1).all()
      and preds["propensity"].min() > 0 and preds["propensity"].max() < 1)
check("outcome predictions inside [0, 1]", preds["outcome_pred"].between(0, 1).all())
check("residual means close to 0 (abs < 0.01)",
      abs(preds["T_res"].mean()) < 0.01 and abs(preds["Y_res"].mean()) < 0.01)
check("predictions are not just the labels (not leaked)",
      not np.allclose(preds["propensity"], preds["T"])
      and not np.allclose(preds["outcome_pred"], preds["Y"]))

# Day 2: leakage guard must reject a leakage column
original = list(nm.NUMERIC)
nm.NUMERIC = original + ["Response"]
try:
    nm.check_config()
    guard_works = False
except Exception:
    guard_works = True
nm.NUMERIC = original
check("leakage guard rejects 'Response' as a feature", guard_works)

# Day 2: reproducibility
check("two runs give identical residuals", check_reproducible(df))

failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
sys.exit(1 if failed else 0)