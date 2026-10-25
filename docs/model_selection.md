# Model Selection for Nuisance Models (Vridhi)

Status: first results, 20 Oct. Treatment, outcome and confounder columns are
still candidates and must be confirmed with Jaswanth and Sekhar.

## Setup
- Data: data/retail_data.csv (2237 customers)
- Outcome model: Y = campaign_response
- Treatment model: T = campaign_exposure
- Confounders: age, Income, Kidhome, Teenhome, Recency,
  total_purchase_amount, total_purchases, Education, Marital_Status
- Excluded to avoid leakage: Response, campaign_response, AcceptedCmp1-5
- Method: 5-fold stratified cross-validation, metrics ROC-AUC (higher is better)
  and log loss (lower is better)
- Script: python src/nuisance_models.py

## Results

| Target | Model | AUC | Log loss |
|---|---|---|---|
| campaign_response | Logistic Regression | 0.7905 | 0.3469 |
| campaign_response | Random Forest | 0.8120 | 0.3358 |
| campaign_response | Gradient Boosting | 0.8161 | 0.3375 |
| campaign_exposure | Logistic Regression | 0.7467 | 0.4349 |
| campaign_exposure | Random Forest | 0.7745 | 0.4166 |
| campaign_exposure | Gradient Boosting | 0.7696 | 0.4218 |

## Observations
- Outcome model: Gradient Boosting has the best AUC and Random Forest has the
  best log loss. The two are very close, so either works.
- Treatment model: Random Forest is best on both metrics.
- Tree models beat the Logistic Regression baseline on both targets.
- Treatment AUC is about 0.77, so the confounders do predict who was exposed.
  This is why adjusting for confounders (Double ML) is needed.

## Limitations
- Roles of the columns are not yet confirmed by the team.
- Data checks are in `data_check_findings.md`. campaign_exposure has 462 ones and 1775 zeros, so the treatment is imbalanced but usable.
- campaign_response and Response are identical in all rows, so Response must not be used as a feature.
- LightGBM was not tried yet.


## Sensitivity: purchase columns
`total_purchase_amount` and `total_purchases` may be post-treatment (measured after the campaign). Their timing is not yet confirmed with Jaswanth, so the models were also run without them (`src/nuisance_sensitivity.py`).

| Target | Model | AUC (all confounders) | AUC (without purchase columns) |
|--------|-------|-----------------------|--------------------------------|
| campaign_response | Logistic Regression | 0.7905 | 0.7489 |
| campaign_response | Random Forest | 0.8120 | 0.7780 |
| campaign_response | Gradient Boosting | 0.8161 | 0.7718 |
| campaign_exposure | Logistic Regression | 0.7467 | 0.7148 |
| campaign_exposure | Random Forest | 0.7745 | 0.7264 |
| campaign_exposure | Gradient Boosting | 0.7696 | 0.7238 |

Observations:
- Removing the purchase columns lowers AUC for every model and both targets (about 0.03 to 0.05), so these columns carry a lot of information about both exposure and response.
- Treatment AUC stays above 0.72 without them, so the remaining confounders still predict exposure.
- Without the purchase columns, Random Forest becomes the best outcome model (0.7780 vs 0.7718), so the best-model choice depends on this decision.
- DML sensitivity (Hepsiba, `src/dml_estimation.py`, branch hepsiba): the estimate is 0.2361 with all confounders and 0.2725 without the purchase columns. Both are sensitive to this choice and neither is a validated causal effect yet.
- Decision pending: if the purchase columns are measured before the campaign, they are valid confounders and should stay. If they include purchases after the campaign, they should be dropped.