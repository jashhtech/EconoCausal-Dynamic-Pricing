# Week 3 — DML Integration Plan and Validation

## Objective
Integrate nuisance models with the DML estimator and validate the end-to-end exploratory workflow.

## Pipeline
1. Load `data/retail_data.csv`.
2. Validate required columns, missing values, binary treatment/outcome values, and feature configuration.
3. Preprocess numeric and categorical confounders.
4. Evaluate Logistic Regression, Random Forest, and Gradient Boosting using five-fold stratified out-of-fold predictions.
5. Select candidate nuisance models using AUC and log loss.
6. Generate out-of-fold predictions for outcome and treatment nuisance functions.
7. Calculate outcome and treatment residuals.
8. Pass residuals to `estimate_dml_from_residuals`.
9. Report the coefficient, standard error, confidence interval, sample size, and propensity-score summary.

## Current configuration

| Component | Value |
|---|---|
| Dataset | `data/retail_data.csv` |
| Treatment | `campaign_exposure` |
| Outcome | `campaign_response` |
| Numeric features | `age`, `Income`, `Kidhome`, `Teenhome`, `Recency` |
| Categorical features | `Education`, `Marital_Status` |
| Cross-fitting | 5 folds |
| Random seed | 42 |
| Outcome nuisance model | Random Forest |
| Treatment nuisance model | Random Forest |

The configuration is exploratory and requires team confirmation.

## Validation performed
- Required columns are checked before execution.
- Missing values in required columns raise a validation error.
- Treatment and outcome are checked for binary values.
- Leakage columns, treatment, outcome, and duplicate feature names are excluded from the confounder configuration.
- Each target is checked for two classes and sufficient class counts for stratified cross-fitting.
- Preprocessing is contained within the pipeline, so transformations are fitted within each training fold.
- The integrated script completed on 2,237 observations and produced nuisance-model metrics, a DML estimate, and propensity-score diagnostics.

## Unit tests
Previously recorded test command:

```bash
python -m pytest src/test_dml_estimation.py src/test_dml_synthetic.py -v
```

Previously recorded result: **4 tests passed**. These tests cover the DML estimator and synthetic known-effect recovery; they do not cover every validation branch in `nuisance_models.py`.

For final sign-off, rerun the command after the final edits and record the fresh result.

## Execution

```bash
python src/nuisance_models.py
```

The integrated run completed successfully. Numerical outputs are recorded in `week3_dml_results.md`.

## Outstanding scientific checks
- Confirm historical campaign exposure is an appropriate treatment for the research question.
- Confirm campaign response occurs after treatment.
- Confirm selected confounders are pre-treatment.
- Assess propensity-score overlap by treatment group and conduct sensitivity checks.
- Do not interpret this as a specific discount effect: there is no assigned discount amount or randomized discount assignment in this dataset.

## Week 3 status
Core integration, nuisance-model comparison, cross-fitted residual generation, initial estimation, and initial diagnostics have been executed. These documents record the work. Final sign-off still requires a fresh test run, team review of causal assumptions, and committing/pushing the files to the project branch.
