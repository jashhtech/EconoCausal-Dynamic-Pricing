# Week 4 – Day 2: Data Quality Checks

## Objective

The objective of this task is to evaluate the quality and consistency of the cleaned retail dataset before using it for further analysis and causal estimation.

## Dataset

* Input file: `data/retail_data.csv`
* Output file: `data/week4_day2_quality_checks.csv`

## Validation Performed

1. Checked whether the dataset contains records.
2. Checked for missing values.
3. Checked for duplicate rows.
4. Verified the required engineered features.
5. Checked binary campaign variables for valid values (0 and 1).
6. Checked numeric purchase and spending columns for negative or invalid values.
7. Verified the age calculation against the existing data-preparation logic.

## Results

* Total rows: [Enter actual count]
* Total columns: [Enter actual count]
* Missing values: [Enter actual count]
* Duplicate rows: [Enter actual count]
* Checks passed: [Enter actual count]
* Checks failed: [Enter actual count]

## Output

The validation results were saved in `data/week4_day2_quality_checks.csv`.

## Conclusion

The dataset was evaluated using a set of automated data quality checks. Any failed checks must be reviewed and resolved before the dataset is used for further analysis.
