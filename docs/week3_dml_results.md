# Week 3 — DML Integration Results

## Objective
Integrate nuisance models with the DML estimator, generate cross-fitted residuals, evaluate candidate models, and run an initial exploratory estimate.

## Dataset and configuration
- Dataset: `data/retail_data.csv`
- Observations: 2,237
- Treatment: `campaign_exposure`
- Outcome: `campaign_response`
- Numeric confounders: `age`, `Income`, `Kidhome`, `Teenhome`, `Recency`
- Categorical confounders: `Education`, `Marital_Status`
- Cross-fitting: 5-fold stratified CV; random seed 42

This configuration is provisional and requires team confirmation.

## Nuisance-model evaluation

| Target | Model | AUC | Log loss |
|---|---|---:|---:|
| campaign_response | Logistic Regression | 0.7489 | 0.3726 |
| campaign_response | Random Forest | **0.7780** | **0.3538** |
| campaign_response | Gradient Boosting | 0.7718 | 0.3576 |
| campaign_exposure | Logistic Regression | 0.7148 | 0.4699 |
| campaign_exposure | Random Forest | **0.7264** | **0.4456** |
| campaign_exposure | Gradient Boosting | 0.7238 | 0.4484 |

Random Forest performed best among the tested candidates for both targets under this feature configuration. These are cross-validation results, not independent test-set results.

## DML estimation

Cross-fitted predictions were generated for `E[Y|X]` and `E[T|X]`. Residuals were calculated as actual minus predicted values and passed to `estimate_dml_from_residuals`.

| Metric | Result |
|---|---:|
| Estimated coefficient | 0.2835 |
| Standard error | 0.0234 |
| 95% confidence interval | [0.2376, 0.3294] |
| Sample size | 2,237 |

The coefficient is approximately 28.35 percentage points on the binary-outcome scale. It is an exploratory adjusted residual-regression association, not a verified causal effect.

## Propensity-score summary

| Statistic | Value |
|---|---:|
| Count | 2,237 |
| Mean | 0.2081 |
| Standard deviation | 0.1586 |
| Minimum | 0.0130 |
| 25th percentile | 0.0995 |
| Median | 0.1574 |
| 75th percentile | 0.2540 |
| Maximum | 0.7895 |

This is an initial diagnostic. A fuller overlap assessment by treatment group and sensitivity checks are still needed.

## Limitations
1. `campaign_exposure` represents historical campaign exposure/acceptance, not randomized or assigned discount treatment.
2. The dataset does not contain assigned discount amounts, so it cannot identify a $10-versus-$20 discount effect.
3. Temporal ordering between treatment and outcome must be confirmed.
4. The selected confounders are provisional and must be verified as pre-treatment variables.
5. Predictive nuisance-model performance does not establish causal identification.
6. The standard error and confidence interval are preliminary outputs from the current residual estimator, not a complete validation of causal uncertainty.

**Conclusion:** The Week 3 pipeline evaluated nuisance models, generated cross-fitted residuals, and ran the DML estimator on 2,237 observations. Results remain exploratory.

## Reproduction
From the repository root:

```bash
python src/nuisance_models.py
```
