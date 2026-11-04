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

## 6. Conclusion

Week 4 strengthened the DML implementation through sensitivity analysis and propensity score diagnostics. The results provide additional information about model stability and treatment-control overlap.

**Limitation:** The available treatment variable represents historical campaign exposure, not a randomly assigned discount amount. Therefore, the estimated treatment effects should be interpreted as exploratory adjusted associations rather than proven causal effects of specific discount amounts.