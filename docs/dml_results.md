\# Double Machine Learning (DML) Results



\## 1. Objective



The objective is to estimate how promotional discounts influence customer purchasing behavior and, where the data supports it, identify differences in treatment effects across customer profiles.



\## 2. Planned Method



The DML pipeline uses three inputs:



\- \*\*X — Confounders:\*\* Customer characteristics that may influence treatment assignment and purchasing behavior.

\- \*\*T — Treatment:\*\* The promotional offer actually assigned or received by a customer.

\- \*\*Y — Outcome:\*\* The purchasing outcome measured after treatment.



The pipeline uses cross-fitting to generate out-of-fold predictions for the outcome and treatment. It then uses residuals from these predictions to estimate a treatment effect.



\## 3. Dataset and Current Limitations



The current retail dataset contains 2,237 customer records and 35 columns.



The available columns include customer characteristics, deal-purchase counts, campaign acceptance indicators, and campaign response.



The dataset does not currently contain an explicit discount-amount variable identifying $10 and $20 offers. Therefore, a direct causal comparison between these two discount amounts cannot yet be reported.



Campaign acceptance and deal-purchase counts must not automatically be treated as randomized discount assignments. Their meanings and timing must be verified before selecting a treatment variable.



\## 4. Evaluation Plan



The following checks are planned:



\- Validate the definitions of X, T, and Y.

\- Check missing values, data types, and treatment variation.

\- Evaluate nuisance-model predictions using held-out data.

\- Report the estimated treatment effect and uncertainty.

\- Examine whether the estimate is sensitive to model choices and assumptions.

\- Assess whether the data supports comparisons between relevant customer groups.



\## 5. Results Status



\*\*Status: Integration scaffold prepared; causal results pending.\*\*



The initial Python module has been created and executed successfully. No treatment-effect estimate has been produced yet because the treatment and outcome definitions must be confirmed and the pipeline must be evaluated with valid inputs.



\## 6. Future Work



1\. Integrate the team's data-preprocessing component.

2\. Use the agreed feature definitions and treatment/outcome variables.

3\. Integrate the nuisance models.

4\. Run and validate the DML estimation pipeline.

5\. Record the estimated effect, uncertainty, evaluation findings, and limitations.

6\. Provide suitable results for the project dashboard.



\## 7. Interpretation Caution



A DML estimate does not establish causality by itself. Its interpretation depends on appropriate treatment assignment, sufficient overlap, suitable confounder adjustment, and defensible causal assumptions.





## Week 2 Progress — October 21, 2026

* Created the initial DML estimation module with cross-fitting and treatment-effect uncertainty estimation.
* Added documentation covering the planned method, evaluation steps, and current limitations.
* Reviewed the team's feature engineering and DML implementations to identify integration requirements.
* Identified a mismatch between the feature names in the feature engineering code and the shared retail dataset.
* Pending confirmation of the treatment, outcome, and confounder variables before running causal estimation.

**Status:** Initial implementation committed and pushed. Team integration and validation are in progress.





\# Double Machine Learning (DML) Results Report



\## 1. Project Objective



The objective is to estimate how promotional offers influence customer purchasing behavior using Double Machine Learning (DML), with the long-term goal of improving promotional budget allocation.



\## 2. DML Implementation



The estimator is implemented in `src/dml\_estimation.py`.



It accepts three inputs:



\- \*\*X — Confounders:\*\* relevant customer characteristics measured before treatment.

\- \*\*T — Treatment:\*\* the treatment actually assigned or received.

\- \*\*Y — Outcome:\*\* the outcome measured after treatment.



The implementation uses cross-fitting and residual-based effect estimation. It returns an estimated treatment effect, standard error, confidence interval, and sample size.



\## 3. Testing and Validation



Two test modules are available:



\- `src/test\_dml\_estimation.py` checks estimator behavior and input validation.

\- `src/test\_dml\_synthetic.py` checks whether the estimator can recover a known treatment effect from synthetic data.



The three existing tests passed in the previous test run. They should be rerun after the latest documentation changes and any further code changes.



\## 4. Dataset Summary



The cleaned dataset, `data/retail\_data.csv`, contains 2,237 customer records and 35 columns.



It includes customer characteristics, purchase amounts, deal-purchase counts, campaign acceptance indicators, and campaign response.



\## 5. Important Data Limitations



The dataset does not contain a verified assigned discount amount distinguishing $10 and $20 offers.



\- `NumDealsPurchases` records deal-purchase counts, not assigned discount amounts.

\- `campaign\_exposure` is derived from campaign acceptance indicators.

\- `campaign\_response` duplicates `Response`.



Consequently, the current dataset does not yet support a defensible direct causal comparison of $10 versus $20 discounts.



\## 6. Current Results Status



\*\*Status: DML estimator implemented; synthetic validation tests available; real-data causal results pending.\*\*



No real discount-effect estimate is reported in this document because the treatment and outcome definitions require confirmation.



Synthetic validation demonstrates performance on simulated data only. It is not evidence of actual customer behavior or business impact.



\## 7. Remaining Work



1\. Confirm the treatment, outcome, and pre-treatment confounders with the team.

2\. Obtain valid discount-assignment data if the project requires comparing $10 and $20 offers.

3\. Evaluate treatment overlap and nuisance-model performance on suitable data.

4\. Assess the sensitivity of estimates to model choices and assumptions.

5\. If the dashboard requires customer-specific effects, implement and validate an appropriate individualized-effect method.

6\. Integrate validated results into the dashboard.



\## 8. Interpretation



DML does not guarantee causal conclusions by itself. Reliable interpretation requires valid treatment and outcome definitions, suitable confounder adjustment, adequate treatment overlap, and defensible causal assumptions.



## 9. Team Integration and Sensitivity Analysis — October 25, 2026

### Nuisance Model Integration

Integrated `src/nuisance_models.py` from teammate Vridhi's branch (`vridhi-gautam`, commit `47d888b`).

The nuisance models use five-fold cross-fitting to estimate treatment and outcome probabilities.

Selected models and evaluation results:

| Target | Selected model | AUC | Log loss |
|---|---|---:|---:|
| campaign_response | Gradient Boosting | 0.8161 | 0.3375 |
| campaign_exposure | Random Forest | 0.7745 | 0.4166 |

The `dml_residuals()` function provides cross-fitted outcome and treatment residuals. These were integrated with `estimate_dml_from_residuals()` in `src/dml_estimation.py`.

### Exploratory DML Results

| Configuration | Coefficient | Standard error | Approximate 95% CI |
|---|---:|---:|---|
| Including purchase totals | 0.2361 | 0.0243 | 0.1885–0.2838 |
| Excluding purchase totals | 0.2725 | 0.0236 | 0.2263–0.3187 |

Both analyses used 2,237 customer records.

Removing `total_purchase_amount` and `total_purchases` increased the coefficient by approximately 0.0364. These variables may contain post-treatment information, so their inclusion requires confirmation of measurement timing.

### Propensity-Score Sensitivity

Using the feature configuration without purchase totals:

- Without clipping: 0.2725
- With clipping to [0.01, 0.99]: 0.2725
- Predictions requiring clipping: 0

Clipping did not affect this configuration. This does not establish sufficient treatment overlap.

### Validation

Four automated tests passed, including the new test for residual-based estimation.

### Interpretation and Limitations

These results describe exploratory associations after residual-based adjustment. They are not validated causal effects of discounts.

The treatment variable `campaign_exposure` is derived from campaign acceptance indicators rather than a verified discount-assignment variable. The outcome `campaign_response` records campaign response rather than a confirmed post-discount purchase outcome.

The estimated standard errors and confidence intervals are approximate and require further validation before inferential claims.

The current estimator reports an average coefficient, not individualized customer treatment effects.

### Integration Status

The nuisance-model integration, residual-based estimation, initial model evaluation, feature-sensitivity analysis, propensity-clipping check, and automated testing have been completed locally.

The initial DML integration was committed and pushed to the
hepsiba branch. Further Week 3 configuration updates are in progress.


## Final Exploratory Analysis Configuration

Treatment (T): `campaign_exposure`
- Defined as acceptance of at least one historical campaign.
- This is not verified discount assignment.

Outcome (Y): `campaign_response`
- Defined using the `Response` column.

Confounders (X):
- `age`
- `Income`
- `Kidhome`
- `Teenhome`
- `Recency`
- `Education`
- `Marital_Status`

The purchase totals were excluded from the primary specification
because their timing relative to historical campaigns cannot
be established from the available data.

The reduced-feature DML coefficient was approximately 0.2725,
compared with 0.2361 when purchase totals were included.

These results describe exploratory adjusted associations.
They should not be interpreted as validated causal effects
of discounts or used to recommend specific discount amounts.

The existing dataset does not contain verified discount
assignment or discount amount information.



## Week 3 Update — Nuisance Model Evaluation

### Exploratory Feature Configuration

Treatment (T): `campaign_exposure`

Outcome (Y): `campaign_response`

Numeric confounders:
- `age`
- `Income`
- `Kidhome`
- `Teenhome`
- `Recency`

Categorical confounders:
- `Education`
- `Marital_Status`

The purchase-total variables `total_purchase_amount` and
`total_purchases` were excluded because their measurement timing
relative to campaign exposure has not been confirmed.

### Nuisance Model Evaluation

The updated nuisance-model pipeline was executed using
2,237 customer records and five-fold cross-validation.

| Target | Model | AUC | Log loss |
|---|---|---:|---:|
| campaign_response | Logistic Regression | 0.7489 | 0.3726 |
| campaign_response | Random Forest | 0.7780 | 0.3538 |
| campaign_response | Gradient Boosting | 0.7718 | 0.3576 |
| campaign_exposure | Logistic Regression | 0.7148 | 0.4699 |
| campaign_exposure | Random Forest | 0.7264 | 0.4456 |
| campaign_exposure | Gradient Boosting | 0.7238 | 0.4484 |

Random Forest achieved the highest AUC and lowest log loss
among the tested models for both targets.

### Propensity Score Summary

Using the Random Forest treatment model:

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

These summary statistics do not independently establish
adequate treatment overlap.

### Automated Testing

The following test modules were executed:

- `src/test_dml_estimation.py`
- `src/test_dml_synthetic.py`

Result: 4 tests passed.

### Interpretation and Limitations

These nuisance-model metrics describe predictive performance
for the selected exploratory treatment and outcome variables.

They do not establish that historical campaign acceptance
represents randomized discount assignment or that campaign
response is a confirmed post-treatment purchasing outcome.

The results must not be interpreted as validated causal
discount effects.

Final variable definitions, timing, treatment overlap,
and end-to-end integration require further team validation.
