# Week 4 – DML Sensitivity Analysis and Diagnostics

## 1. Overview

Week 4 focuses on evaluating the reliability and consistency of the Double Machine Learning (DML) treatment effect estimates. Sensitivity analysis and propensity score overlap diagnostics were implemented to assess model stability and treatment-control comparability.

## 2. Sensitivity Analysis

Three nuisance model configurations were compared:

- Logistic Regression
- Random Forest
- Gradient Boosting

The estimated treatment effects were relatively consistent across the three configurations. This suggests that the estimates are not highly dependent on a single nuisance model choice.

The Random Forest configuration was retained as the primary model based on the evaluation performed during Week 3.

## 3. Propensity Score Overlap Diagnostics

Propensity scores were examined to understand how treated and control customers overlap.

The analysis included:

- Summary statistics for propensity scores.
- Separate distributions for treated and control customers.
- Identification of the shared propensity score range.
- Calculation of the proportion of observations within the shared range.
- Visualization of propensity score distributions.

The results showed substantial coverage within the shared min-max range. However, min-max coverage alone does not establish dense distributional overlap.

## 4. Visualization

The propensity score overlap plot is saved at:

`graphs/propensity_score_overlap.png`

This visualization compares the propensity score distributions of treated and control customers.

## 5. Implementation and Testing

The Week 4 implementation includes:

- Sensitivity analysis across multiple nuisance model configurations.
- Propensity score overlap analysis.
- Propensity score visualization.
- Execution and validation of the updated nuisance model pipeline.

The implementation was executed successfully, and the changes were checked using `git diff --check`.

## 6. Additional Work: Propensity-Score Trimming and DML Robustness Analysis

Following the initial Week 4 diagnostics, additional robustness analysis was performed to examine whether the DML treatment-effect estimates remained stable after restricting observations based on propensity scores.

Three samples were evaluated:

- Full sample: 2,237 customers.
- Propensity scores between 0.05 and 0.95: 2,121 customers.
- Propensity scores between 0.10 and 0.90: 1,670 customers.

All three sample sizes matched the counts from the team's overlap analysis.

Two feature specifications were compared:

- **Without purchase columns:** Used the original demographic and customer-related features.
- **With purchase columns:** Additionally included `total_purchase_amount` and `total_purchases`.

### 6.1 DML Robustness Results

| Sample | Without Purchase Columns | With Purchase Columns |
|---|---:|---:|
| Full sample (2,237) | 0.2835 | 0.2473 |
| 0.05–0.95 (2,121) | 0.2829 | 0.2538 |
| 0.10–0.90 (1,670) | 0.2745 | 0.2386 |

### 6.2 95% Confidence Intervals

| Sample | Without Purchase Columns | With Purchase Columns |
|---|---|---|
| Full sample | [0.2376, 0.3294] | [0.1996, 0.2950] |
| 0.05–0.95 | [0.2362, 0.3296] | [0.2053, 0.3023] |
| 0.10–0.90 | [0.2257, 0.3233] | [0.1878, 0.2893] |

### 6.3 Observations

- All six treatment-effect estimates were positive.
- All six 95% confidence intervals excluded zero.
- Estimates without purchase columns remained relatively stable across the three sample restrictions.
- Including purchase-related features resulted in smaller estimates.
- The results indicate stability across the examined propensity-score trimming thresholds.

The analysis suggests that the estimated effects are not highly sensitive to the two trimming thresholds examined.

**Additional limitation:** Purchase-related features may be post-treatment variables. Therefore, the specification without purchase columns is treated as the primary analysis, while the specification with purchase columns is used as a sensitivity comparison.

## 7. Additional Implementation and GitHub Deliverables

The additional robustness analysis was implemented using:

- `src/trimmed_dml_analysis.py` – Script for propensity-score trimming and DML estimation.
- `results/trimmed_dml_results.csv` – Stores the six DML estimation results.

The changes were committed and pushed to the `hepsiba` branch.

**Commit ID:** `a666127`

**Commit Message:** Add DML propensity trimming robustness analysis.

## 8. Conclusion

Week 4 strengthened the DML implementation through nuisance-model sensitivity analysis, propensity-score overlap diagnostics, and additional robustness checks using trimmed samples.

The treatment-effect estimates remained positive and relatively stable across the examined sample restrictions. The comparison of feature specifications also highlighted the influence of purchase-related variables on the estimated effects.

**Overall limitation:** The available treatment variable represents historical campaign exposure, not a randomly assigned discount amount. Therefore, the estimated treatment effects should be interpreted as exploratory adjusted associations rather than proven causal effects of specific discount amounts.