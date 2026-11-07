# Data Quality Report

## 1. Introduction

This document describes the data quality checks performed on the retail marketing campaign dataset used in the EconoCausal-Dynamic-Pricing project.

The main objective is to ensure that the dataset is accurate, consistent, complete, and suitable for further analysis and machine learning tasks.

## 2. Dataset Information

- Original dataset: `marketing_campaign.csv`
- Processed dataset: `retail_data.csv`
- Dataset preparation script: `prepare_dataset.py`
- Data dictionary: `data_dictionary.csv`
- Quality report: `final_data_quality_report.csv`

The original dataset contains customer demographic information, campaign acceptance records, and purchasing behavior.

## 3. Data Cleaning Operations

The following preprocessing operations are performed:

1. Duplicate records are removed.
2. Missing values in the `Income` column are replaced using the median.
3. Invalid birth-year records below 1940 are filtered out.
4. Marital status categories are standardized.
5. Customer age is calculated.
6. Total purchase amount is calculated from product spending columns.
7. Total purchases are calculated using web, catalog, and store purchase counts.
8. Campaign-related indicator variables are generated.

## 4. Data Quality Checks

The following checks are included in the project:

| Check | Purpose |
|---|---|
| Missing values | Identify incomplete records |
| Duplicate records | Identify repeated observations |
| Column validation | Verify required dataset columns |
| Data type validation | Check appropriate column data types |
| Binary validation | Verify binary indicator variables |
| Non-negative values | Check purchase and spending values |
| Feature validation | Verify engineered features |
| Reproducibility | Check consistent dataset preparation |

## 5. Existing Data Quality Files

The project contains the following files:

- `data/data_quality_report.py` – Generates the initial data quality report.
- `data/data_quality_report.csv` – Stores the initial report.
- `data/final_data_quality_report.py` – Performs final data quality checks.
- `data/final_data_quality_report.csv` – Stores the final quality results.
- `data/validate_features.py` – Validates engineered features.
- `data/validate_campaign_data.py` – Checks campaign-related data.
- `data/test_reproducibility.py` – Checks preprocessing reproducibility.

## 6. Data Quality Results

The previously generated processed dataset contained:

| Metric | Recorded Result |
|---|---:|
| Number of rows | 2,237 |
| Number of columns | 35 |
| Missing values | 0 |
| Duplicate rows | 0 |

These are previously recorded results. The latest dataset should be checked again before final submission.

## 7. Limitations

1. Median imputation may affect the original distribution of income.
2. Filtering birth years may exclude some observations.
3. Campaign acceptance and response timing require further investigation.
4. Purchase-related variables do not contain sufficient timestamps to establish their temporal relationship with campaign exposure.
5. Data quality checks alone do not establish causal validity.

## 8. Conclusion

The preprocessing and data quality validation procedures improve the consistency and usability of the retail marketing campaign dataset.

The generated reports provide information about missing values, duplicate records, required columns, and engineered features.

The cleaned dataset can be used for further exploratory analysis and model development, subject to the documented limitations and validation of causal assumptions.