# Week 4 – Day 3: Derived Variable Verification

## 1. Objective

The objective of this task is to verify the correctness of the engineered features in the cleaned retail dataset.

## 2. Features Verified

The following six derived variables were checked:

1. **age:** Calculated using `2025 - Year_Birth`.
2. **total_purchase_amount:** Sum of six product spending columns.
3. **total_purchases:** Sum of web, catalog and store purchases.
4. **deal_purchase_indicator:** Indicates whether a customer made at least one deal purchase.
5. **campaign_exposure:** Indicates whether a customer accepted at least one of the five campaigns.
6. **campaign_response:** Matches the original `Response` variable.

## 3. Validation Method

A Python validation script recalculated each feature using its source columns and compared the calculated values with the existing dataset.

## 4. Results

* Total features checked: 6
* Features passed: [Enter actual count]
* Features failed: [Enter actual count]

## 5. Output File

`data/week4_day3_feature_verification.csv`

## 6. Conclusion

The derived variables were checked for calculation consistency. Any failed validation must be investigated before the dataset is used for further analysis.

