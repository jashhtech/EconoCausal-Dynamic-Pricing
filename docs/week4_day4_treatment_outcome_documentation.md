# Week 4 – Day 4: Treatment and Outcome Documentation

## 1. Objective

The objective of this task is to document the candidate treatment, outcome, and confounding variables required for Double Machine Learning (DML) estimation.

## 2. Candidate Treatment Variable

**Variable:** `campaign_exposure`

This variable indicates whether a customer accepted at least one of the five campaigns.

## 3. Candidate Outcome Variable

**Variable:** `campaign_response`

This variable represents the customer's response, copied from the original `Response` column.

## 4. Candidate Confounding Variables

The following variables are proposed for review:

* Income
* Age
* Kidhome
* Teenhome
* Recency
* NumWebVisitsMonth

These variables may capture differences in customer characteristics and purchasing behaviour. Their timing and suitability must be confirmed before DML estimation.

## 5. Validation

A Python script was used to check whether the candidate variables are available in the cleaned dataset and to summarize their missing and unique values.

Output file: `data/week4_day4_variable_summary.csv`

## 6. Important Causal Considerations

The treatment and outcome must represent distinct events with a defensible time order. If campaign exposure and response overlap or one is used to construct the other, the proposed causal interpretation may not be valid.

Confounders should be measured before treatment. Variables that may be affected by treatment should not be included as pre-treatment confounders.

The project team must approve the final treatment, outcome, and confounder definitions before interpreting a DML estimate as a causal effect.

## 7. Conclusion

The candidate variables have been documented and checked against the dataset. Final causal variable selection requires confirmation of the business question, event timing, and team agreement.
