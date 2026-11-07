# Week 4 – Dataset and Variable Audit

## 1. Objective

The objective of this audit is to examine the construction of treatment, outcome, and purchase-related variables in the EconoCausal-Dynamic-Pricing project. It also documents the limitations of the available dataset and identifies potential issues affecting causal estimation.

## 2. Treatment Variable: campaign_exposure

The `campaign_exposure` variable is derived from the following original dataset columns:

- AcceptedCmp1
- AcceptedCmp2
- AcceptedCmp3
- AcceptedCmp4
- AcceptedCmp5

The variable is assigned:

- `1` if the customer accepted at least one of the five campaigns.
- `0` if the customer did not accept any of the five campaigns.

Therefore, campaign exposure represents whether a customer accepted at least one of the recorded campaigns.

**Important limitation:** These columns record campaign acceptance. They do not independently establish the timing of campaign exposure or prove that the treatment occurred before the outcome.

## 3. Outcome Variable: campaign_response

The `campaign_response` variable is copied from the original `Response` column.

It represents the customer's recorded response.

- `1` indicates a recorded positive response.
- `0` indicates no recorded positive response.

The dataset documentation does not establish whether this response occurred after the campaign exposure represented by `campaign_exposure`.

Therefore, a possible relationship between the treatment and outcome requires further investigation.

## 4. Purchase-Related Variables

### 4.1 total_purchase_amount

This variable is calculated using the sum of six original columns:

- MntWines
- MntFruits
- MntMeatProducts
- MntFishProducts
- MntSweetProducts
- MntGoldProds

It represents the customer's recorded total spending across these product categories.

### 4.2 total_purchases

This variable is calculated using:

- NumWebPurchases
- NumCatalogPurchases
- NumStorePurchases

It represents the total recorded purchase count across web, catalog, and store channels.

## 5. Purchase Variable Timing

The available dataset does not provide sufficient transaction-level timestamps to establish whether `total_purchase_amount` and `total_purchases` were measured before or after the relevant campaign exposure.

Consequently:

- These variables cannot automatically be classified as pre-treatment confounders.
- Their timing must be confirmed using additional dataset documentation.
- If they were measured after treatment, including them as controls could introduce post-treatment bias or change the causal estimand.

For this reason, their role in causal estimation requires careful consideration.

## 6. Robustness Check Considerations

A teammate reported an estimated effect of approximately 0.28 on `campaign_response`, with an overall response rate of approximately 14.9%.

The teammate also reported that adding purchase-related variables reduced the estimate by approximately 0.036.

These figures require verification against the corresponding robustness evaluation files.

A relatively large estimate should not automatically be treated as an error. The relationship between campaign acceptance and campaign response, variable timing, confounding, and model specification should be investigated.

## 7. Data Limitations

The following limitations were identified:

1. The exact timing of campaign exposure is not established.
2. The timing of purchase-related variables is unclear.
3. The relationship between campaign acceptance and the recorded response requires further investigation.
4. The available data does not independently establish that purchase variables are pre-treatment confounders.
5. Additional documentation may be required to confirm the causal interpretation of the estimated effect.

## 8. Implications for DML Estimation

Double Machine Learning requires carefully defined treatment, outcome, and confounder variables.

Before finalizing causal estimates:

- Confirm the temporal relationship between treatment and outcome.
- Investigate possible overlap between campaign acceptance and campaign response.
- Confirm that selected confounders are measured before treatment.
- Avoid automatically including variables whose timing is uncertain.
- Document assumptions and limitations when interpreting the estimates.

## 9. Conclusion

The dataset contains useful customer campaign and purchase information. However, the exact timing of campaign exposure, campaign response, and purchase-related measurements cannot be fully established from the available columns alone.

Therefore, the causal interpretation of the estimated campaign effect should be treated cautiously until these limitations are addressed.

This audit documents the available variable construction and the assumptions that require further validation.

## 10. Related Project Files

- `data/prepare_dataset.py`
- `data/retail_data.csv`
- `data/data_dictionary.csv`
- `data/final_data_quality_report.csv`
- `src/dml_estimation.py`
- `docs/dml_results.md`