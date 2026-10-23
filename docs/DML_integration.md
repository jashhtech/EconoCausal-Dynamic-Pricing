# DML Integration Guide

## 1. Objective

This module estimates the average treatment effect of a treatment on an outcome using Double Machine Learning (DML). The estimator is implemented in `src/dml_estimation.py`.

## 2. Inputs

The estimator requires three inputs:

- **X — Confounders:** customer characteristics measured before treatment.
- **T — Treatment:** the treatment actually assigned or received.
- **Y — Outcome:** the outcome measured after treatment.

The function returns the estimated treatment effect, standard error, confidence interval, and sample size.

## 3. Implementation

The estimator uses cross-fitting to generate out-of-fold predictions for the treatment and outcome models. It then uses residuals to estimate the treatment effect.

The implementation includes input validation and handles missing or non-finite observations according to its validation rules.

## 4. Validation

Run the existing tests from the repository root:

```cmd
python -m unittest src.test_dml_estimation src.test_dml_synthetic -v
```

The synthetic test generates data with a known treatment effect of 5 and checks whether the estimator recovers an estimate within the specified tolerance.

Passing synthetic tests demonstrates that the implementation works for the tested simulated scenario. It does not establish that the real dataset supports a causal conclusion.

## 5. Current Dataset Limitations

The current `data/retail_data.csv` dataset contains 2,237 records and 35 columns. It does not contain a verified assigned discount amount distinguishing $10 from $20 offers.

- `NumDealsPurchases` counts deal purchases; it is not the assigned discount.
- `campaign_exposure` is derived from campaign acceptance indicators.
- `campaign_response` duplicates `Response`.

These variables must not be treated as a valid discount assignment without further evidence.

## 6. Requirements for Real-Data Integration

Before running a real causal analysis, confirm:

1. The treatment variable and its meaning.
2. The outcome and when it was measured.
3. Which features were measured before treatment.
4. Whether comparable customers could receive different treatment levels.
5. Whether the selected variables avoid outcome leakage.

## 7. Scope and Limitations

The current estimator returns an average treatment effect. It does not estimate a separate treatment effect for every customer or independently identify persuadable customers.

A causal interpretation also depends on defensible assumptions, appropriate confounder adjustment, and adequate treatment overlap.

**Current status:** The estimator and synthetic tests are implemented. Real-data causal estimation remains pending confirmation of valid treatment and outcome variables.