# Model Selection for Nuisance Models (Vridhi)

Status: updated 29 Oct. Final feature set excludes `total_purchase_amount` and
`total_purchases` (team decision of 25 Oct), because their timing relative to the
campaign is not confirmed. Treatment/outcome roles still need Jaswanth's confirmation.

## Setup
- Data: data/retail_data.csv (2237 customers)
- Outcome model: Y = campaign_response
- Treatment model: T = campaign_exposure
- Confounders: age, Income, Kidhome, Teenhome, Recency, Education, Marital_Status
- Excluded as possibly post-treatment: total_purchase_amount, total_purchases
- Excluded to avoid leakage: Response, campaign_response, AcceptedCmp1-5
- Method: 5-fold stratified cross-validation (cross-fitted predictions), metrics
  ROC-AUC (higher is better) and log loss (lower is better)
- Script: python src/nuisance_models.py (saves results/nuisance_model_results.csv)

## Results (final feature set)

| Target | Model | AUC | Log loss |
|---|---|---|---|
| campaign_response | Logistic Regression | 0.7489 | 0.3726 |
| campaign_response | Random Forest | 0.7780 | 0.3538 |
| campaign_response | Gradient Boosting | 0.7718 | 0.3576 |
| campaign_exposure | Logistic Regression | 0.7148 | 0.4699 |
| campaign_exposure | Random Forest | 0.7264 | 0.4456 |
| campaign_exposure | Gradient Boosting | 0.7238 | 0.4484 |

## Selected models
- Outcome model: Random Forest (best AUC and best log loss).
- Treatment model: Random Forest (best on both metrics).
- Tree models beat the Logistic Regression baseline on both targets.

## Overlap check
Propensity scores (Random Forest, cross-fitted) range from 0.013 to 0.79 with mean
0.208, so no customer is close to 0 or 1. Overlap looks acceptable for Double ML.

## How to use dml_residuals()
From the repo root:

    import pandas as pd
    from src.nuisance_models import dml_residuals

    df = pd.read_csv("data/retail_data.csv")
    y_res, t_res = dml_residuals(df)   # Y - Y_hat, T - T_hat (cross-fitted)

Defaults are random_forest for both outcome and treatment models. Change models
or feature roles only in the CONFIG block of src/nuisance_models.py.

## Limitations
- Roles of the columns are not yet confirmed by the team.
- Data checks are in `data_check_findings.md`. campaign_exposure has 462 ones and
  1775 zeros, so the treatment is imbalanced but usable.
- campaign_response and Response are identical in all rows, so Response must not
  be used as a feature.
- LightGBM was not tried yet.

## Sensitivity: purchase columns
`total_purchase_amount` and `total_purchases` may be post-treatment (measured after
the campaign). The models were also run with them (`src/nuisance_sensitivity.py`).

| Target | Model | AUC (all confounders) | AUC (final set, without purchase columns) |
|--------|-------|-----------------------|-------------------------------------------|
| campaign_response | Logistic Regression | 0.7905 | 0.7489 |
| campaign_response | Random Forest | 0.8120 | 0.7780 |
| campaign_response | Gradient Boosting | 0.8161 | 0.7718 |
| campaign_exposure | Logistic Regression | 0.7467 | 0.7148 |
| campaign_exposure | Random Forest | 0.7745 | 0.7264 |
| campaign_exposure | Gradient Boosting | 0.7696 | 0.7238 |

Observations:
- Removing the purchase columns lowers AUC for every model and both targets
  (about 0.03 to 0.05), so these columns carry a lot of information about both
  exposure and response.
- Treatment AUC stays above 0.71 without them, so the remaining confounders
  still predict exposure.
- Without the purchase columns, Random Forest is the best outcome model
  (0.7780 vs 0.7718), so the best-model choice depends on this decision.
- DML sensitivity (Hepsiba, `src/dml_estimation.py`, branch hepsiba): the estimate
  is 0.2361 with all confounders and 0.2725 without the purchase columns. Both are
  sensitive to this choice and neither is a validated causal effect yet.
- If the purchase columns are confirmed to be measured before the campaign, they
  are valid confounders and should be added back to NUMERIC.