
# Week 2 DML Results, Evaluation, and Limitations

## 1. Objective

Prepare the retail customer dataset and evaluate a Double Machine Learning (DML) model for the team's proposed causal question.

## 2. Dataset

- Input: `data/retail_data.csv`
- Rows: 2237 (previously validated)
- Columns: 35 (previously validated)
- Missing values: 0 (previously validated)
- Duplicate rows: 0 (previously validated)

Re-run the validation script before final submission.

## 3. Causal Variables

- Treatment: `deal_purchase_indicator` (candidate)
- Outcome: `total_purchase_amount` (candidate)
- Confounders: `age`, `Income`, `Education`,
  `Marital_Status`, `Recency` (candidates)

Team approval status: PENDING

## 4. Evaluation

- Dataset validation: record the actual test result.
- Unit tests: record the number passed and failed.
- Estimation: PENDING team approval of causal variables.
- Effect estimate: Not reported yet.
- Confidence interval: Not reported yet.

Replace pending fields only after running the approved model.

## 5. Limitations

1. Deal-based purchases do not prove that a discount was assigned.
2. Unobserved customer preferences may influence both treatment and spending.
3. Total spending and deal-based purchases may be closely related by construction.
4. Results depend on treatment overlap, nuisance-model quality, and causal assumptions.
5. Observational data cannot establish causality without defensible identification assumptions.
6. Results may not generalize to a new dynamic-pricing policy.

## 6. Conclusion

The dataset validation and software tests are separate from causal validation. Final causal interpretation requires team-approved variables, a reviewed estimator, and actual estimation results.

