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
- Earlier rows suggested campaign_exposure may have very few 1 values and
  campaign_response may equal Response. Both still need to be checked.
- LightGBM was not tried yet.