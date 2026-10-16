# EconoCausal — Initial Causal DAG Assumptions (Week 1)

## Purpose

Represent the initial assumptions about how customer history, discount
assignment, and purchase behavior may be related. This is the starting
point for later causal effect estimation; it does not prove that the
relationships are true.

## Variables

- **Discount Received (treatment):** Whether a customer receives a discount.
- **Purchase (outcome):** Whether the customer makes a purchase.
- **Past Purchases (potential confounder):** Prior purchase behavior may
  influence both discount assignment and the chance of purchasing.
- **Past Spending (potential confounder):** Prior spending may influence
  both discount assignment and the chance of purchasing.

## Directed Edges

1. Past Purchases → Discount Received
2. Past Purchases → Purchase
3. Past Spending → Discount Received
4. Past Spending → Purchase
5. Discount Received → Purchase

## Important Validation Notes

- These arrows are proposed assumptions based on a possible retail scenario.
- Confirm them with the project team and the actual dataset/business process.
- The dataset's real column names may differ; map these concepts to the agreed columns.
- If discounts are randomly assigned, some assumed arrows into `Discount Received`
  may not be appropriate.
- Do not claim this DAG proves causation. The quality of causal estimates depends
  on assumptions and data quality.

## Next Steps

1. Confirm the proposed variables and relationships with the project team.
2. Check the actual dataset column names before building the causal model.
3. Use DoWhy to define the treatment, outcome, and potential confounders.
4. In Week 2, estimate discount treatment effects using Double Machine Learning
   (DML), if the data and assumptions support it.

## Conclusion

This causal DAG provides an initial structure for understanding the relationship
between customer history, discount assignment, and purchase behavior. It represents
proposed assumptions, not proven causal relationships.

## Limitations

- The causal relationships in this DAG are initial assumptions.
- The treatment and outcome variables must be mapped to the actual dataset columns.
- The meaning of the discount-related variable must be confirmed before causal analysis.
- The graph has not yet been validated using data.

## Week 1 Final Review

### Treatment
DiscountReceived

### Outcome
Purchase

### Potential Confounders
- PastPurchases
- PastSpending

### Assumptions and Limitations
- The causal relationships are preliminary assumptions.
- The actual dataset has not yet been integrated into this branch.
- The treatment, outcome, and confounders must be validated against the dataset.
- Causal effect estimation will be performed after data integration.