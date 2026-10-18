# Nuisance Models: Week 2 Plan (Vridhi)

Status: draft, written on 18 Oct. Column roles below are NOT final and must be
confirmed with Jaswanth (feature engineering) and Sekhar (dataset).

## Dataset observed (sekhar branch, data/retail_data.csv)
- 2238 lines (about 2237 customers), 35 columns.
- Looks like the public marketing campaign dataset (Income, Kidhome, MntWines, AcceptedCmp1-5, Response).
- Columns added by Sekhar: age, total_purchase_amount, total_purchases,
  deal_purchase_indicator, campaign_exposure, campaign_response.

## Candidate roles (to be confirmed)
- Treatment (T): campaign_exposure
- Outcome (Y): campaign_response
- Confounders (X): age, Income, Kidhome, Teenhome, Recency,
  total_purchase_amount, total_purchases, Education, Marital_Status

## Things to verify before training
1. How many rows have campaign_exposure = 1 vs 0. In the first rows seen, almost all were 0.
3. Whether campaign_response is identical to Response.
4. deal_purchase_indicator looked constant (all 1) in the first rows.
5. Avoid data leakage: do not use Response, campaign_response or AcceptedCmp1-5 as confounders.

## What the two nuisance models do
- Outcome model: predicts Y from X.
- Treatment model: predicts T from X.
- Double ML uses the residuals of both models to estimate the treatment effect.

## Models to compare
- Logistic Regression (baseline)
- Random Forest
- LightGBM (if it installs on Python 3.14)

Metrics: ROC-AUC and log loss with cross-validation.

## Deliverables
- src/nuisance_models.py
- docs/model_selection.md