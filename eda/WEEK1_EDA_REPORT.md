# Week 1 Report: EDA and ML Preparation

**Project:** EconoCausal-Dynamic-Pricing  
**Task:** Exploratory Data Analysis and Machine Learning Preparation

## 1. Objective

The objective of Week 1 was to explore the retail customer dataset, examine its quality, identify important purchasing patterns, validate derived columns, and prepare data for future Machine Learning tasks.

## 2. Dataset Overview

- Total records: 2,237
- Total columns: 35
- Missing values: 0
- Duplicate rows: 0
- Duplicate customer IDs: 0

The dataset contains customer demographics, income, purchase counts, product spending, campaign responses, and deal-purchase information.

## 3. Key Findings

1. Customer ages range from 29 to 85.
2. Customer income ranges from 1,730 to 666,666. The unusually high value of 666,666 requires further investigation.
3. The average number of deal purchases is approximately 2.33.
4. A total of 2,191 customers made at least one deal purchase, while 46 made none.
5. There are 334 campaign responders and 1,903 non-responders.
6. The campaign response rate is approximately 14.93%.
7. The calculated product-spending total matches the existing `total_purchase_amount` column.
8. The `total_purchases` column matches the sum of web, catalog, and store purchase counts.

## 4. Data Validation

- `deal_purchase_indicator` matches whether `NumDealsPurchases` is greater than zero.
- `campaign_exposure` matches acceptance of at least one of the five campaign indicators. Its name should be reviewed because campaign acceptance is not the same as campaign exposure.
- `campaign_response` duplicates `Response` and should not be used as an input feature when predicting `Response`.
- Adding deal-purchase counts to channel-purchase counts causes mismatches. Deal purchases may overlap with channel purchases, so they should not be added without confirming their definitions.

## 5. Machine Learning Preparation

For a practice classification task, `Response` was selected as the target.

The selected features were:

- `Income`
- `age`
- `Kidhome`
- `Teenhome`
- `Recency`
- `NumWebPurchases`
- `NumCatalogPurchases`
- `NumStorePurchases`
- `NumWebVisitsMonth`
- `NumDealsPurchases`

The feature matrix contains 2,237 records and 10 features. The target contains 2,237 values.

An 80/20 stratified train-test split was created:

- Training records: 1,789
- Testing records: 448

## 6. Optional Baseline Model Experiment

A Decision Tree Classifier was trained as an additional practice exercise.

- Accuracy: 69.9%
- Precision for campaign responders: approximately 0.29
- Recall for campaign responders: approximately 0.69
- F1-score for campaign responders: approximately 0.41

The confusion matrix was:

`[[267, 114], [21, 46]]`

The model identified 46 actual responders but also incorrectly predicted that 114 non-responders would respond. Therefore, accuracy alone is insufficient to assess the model's usefulness.

## 7. Limitations and Next Steps

1. Investigate the unusually high income value before deciding whether to retain or remove it.
2. Keep duplicate target information out of the model's input features.
3. Save EDA visualizations and share the findings with the team.
4. Treat the Decision Tree as a baseline experiment rather than a completed pricing model.
5. Obtain appropriate price and discount data to investigate how pricing changes affect purchasing behavior.

The current dataset includes deal-purchase counts but does not provide actual discount percentages or product-level price histories. Therefore, it cannot by itself establish the causal effect of discounts on purchases.


### Feature Importance Analysis

A Decision Tree classifier was used to examine the relative importance of the selected input features when predicting campaign response.

The three highest-ranked features were:
1. **NumCatalogPurchases:** 26.35%
2. **Recency:** 20.77%
3. **Income:** 18.83%

`NumWebVisitsMonth` ranked fourth at 12.73%. `NumDealsPurchases` and `NumWebPurchases` had relatively low importance in this baseline model.

These values indicate how the trained Decision Tree used each feature to make predictions. They do not establish causal relationships. The findings can help guide future analysis, but they should be validated before informing pricing or marketing decisions.


### Customer Age Distribution

As part of the exploratory data analysis, customer ages were examined to understand the age profile of the dataset.

The analysis calculates:
- Average customer age
- Median customer age
- Minimum and maximum customer ages
- Number of customers in different age groups

Customers are grouped into five categories: under 30, 30–39, 40–49, 50–59, and 60 years or older.

This analysis helps us understand the age distribution of customers and provides an overview of the dataset before further modeling.






The customer age analysis showed the following results:

- **Average age:** 56.1 years
- **Median age:** 55 years
- **Youngest customer:** 29 years
- **Oldest customer:** 85 years

**Age group distribution:**

| Age group | Number of customers |
|---|---:|
| Under 30 | 2 |
| 30–39 | 187 |
| 40–49 | 506 |
| 50–59 | 685 |
| 60 and above | 857 |

The largest age group is 60 and above, with 857 customers. The dataset contains relatively few customers under 30. This analysis helps describe the age profile of the customers included in the dataset.

These findings are descriptive and do not establish that age causes a customer to respond to a marketing campaign.

## 8. Conclusion

Week 1 established an understanding of the dataset, checked data quality, validated important derived columns, identified candidate Machine Learning features, and prepared training and testing datasets. This work provides a foundation for subsequent modeling and causal analysis in the EconoCausal-Dynamic-Pricing project.
