# EconoCausal — Initial Causal DAG Assumptions (Week 1)

## Purpose
Represent the initial assumptions about how customer history, discount assignment,
and purchase behavior may be related. This is the starting point for later causal
effect estimation; it does not prove that the relationships are true.

## Variables
- **Discount Received (treatment):** whether a customer receives a discount.
- **Purchase (outcome):** whether the customer makes a purchase.
- **Past Purchases (potential confounder):** prior purchase behavior may influence
  both discount assignment and the chance of purchasing.
- **Past Spending (potential confounder):** prior spending may influence both
  discount assignment and the chance of purchasing.

## Directed edges
1. Past Purchases -> Discount Received
2. Past Purchases -> Purchase
3. Past Spending -> Discount Received
4. Past Spending -> Purchase
5. Discount Received -> Purchase

## Important validation notes
- These arrows are proposed assumptions based on a possible retail scenario.
- Confirm them with the project team and the actual dataset/business process.
- The dataset's real column names may differ; map these concepts to the agreed columns.
- If discounts are randomly assigned, some assumed arrows into `Discount Received`
  may not be appropriate.
- Do not claim this DAG proves causation. The quality of causal estimates depends on
  assumptions and data quality.
