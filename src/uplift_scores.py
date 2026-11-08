"""Customer-level uplift scores (R-learner on the cross-fitted DML residuals).

Each customer gets an out-of-fold estimate of how much the probability of
responding changes with exposure. Scores are checked by splitting customers
into deciles of predicted uplift and estimating the adjusted effect inside
each decile (partialling-out). This is a preliminary estimate under the
stated assumptions, not a validated causal effect.
Run with:  python src/uplift_scores.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline

try:
    from src import nuisance_models as nm
    from src.nuisance_predictions import build_nuisance_predictions
except ImportError:  # when run as: python src/uplift_scores.py
    import nuisance_models as nm
    from nuisance_predictions import build_nuisance_predictions

RESULTS = Path(__file__).resolve().parent.parent / "results"


def out_of_fold_uplift(df, preds):
    """R-learner: weighted regression of Y_res / T_res on X, cross-fitted."""
    X = df[nm.NUMERIC + nm.CATEGORICAL]
    t_res, y_res = preds["T_res"].values, preds["Y_res"].values
    target = np.clip(y_res / t_res, -1, 1)   # an effect on a probability lies in [-1, 1]
    weight = t_res ** 2
    uplift = np.zeros(len(df))
    for train, test in KFold(5, shuffle=True, random_state=nm.SEED).split(X):
        model = make_pipeline(
            nm.make_preprocessor(),
            GradientBoostingRegressor(n_estimators=100, max_depth=2, learning_rate=0.05,
                                      subsample=0.8, random_state=nm.SEED))
        model.fit(X.iloc[train], target[train],
                  gradientboostingregressor__sample_weight=weight[train])
        uplift[test] = model.predict(X.iloc[test])
    return uplift


def decile_table(uplift, preds):
    """Adjusted effect inside each decile of predicted uplift (should rise)."""
    d = pd.DataFrame({"uplift": uplift, "t": preds["T_res"].values, "y": preds["Y_res"].values})
    d["decile"] = pd.qcut(d["uplift"].rank(method="first"), 10, labels=range(1, 11))
    rows = []
    for k, g in d.groupby("decile", observed=True):
        theta = (g["t"] * g["y"]).sum() / (g["t"] ** 2).sum()
        eps = g["y"] - theta * g["t"]
        se = np.sqrt(((g["t"] ** 2) * (eps ** 2)).mean() / ((g["t"] ** 2).mean() ** 2) / len(g))
        rows.append({"decile": int(k), "n": len(g),
                     "mean_predicted_uplift": round(g["uplift"].mean(), 4),
                     "adjusted_effect": round(theta, 4), "std_error": round(se, 4)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = pd.read_csv(nm.DATA_PATH)
    preds = build_nuisance_predictions(df)
    uplift = out_of_fold_uplift(df, preds)

    deciles = decile_table(uplift, preds)
    print("Adjusted effect by decile of predicted uplift (decile 10 = highest score):")
    print(deciles.to_string(index=False))
    print("\nPredicted uplift summary:")
    print(pd.Series(uplift).describe().round(4))

    out = pd.DataFrame({
        "ID": df["ID"], "uplift": uplift.round(4),
        "propensity": preds["propensity"].round(4),
        "outcome_pred": preds["outcome_pred"].round(4),
        "campaign_exposure": df[nm.TREATMENT], "campaign_response": df[nm.OUTCOME],
    })
    RESULTS.mkdir(exist_ok=True)
    out.to_csv(RESULTS / "customer_uplift.csv", index=False)
    deciles.to_csv(RESULTS / "uplift_deciles.csv", index=False)
    print("\nSaved: results/customer_uplift.csv and results/uplift_deciles.csv")