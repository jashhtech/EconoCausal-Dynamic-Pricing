# EconoCausal – Dynamic Pricing

## 1. Project Overview

EconoCausal – Dynamic Pricing is a data analytics and causal inference project that explores customer behaviour and marketing campaign responses using Double Machine Learning (DML).

The project focuses on preparing customer data, validating features, documenting causal variables, and evaluating the reliability of the analytical pipeline.

## 2. Project Objectives

- Prepare and clean the customer marketing dataset.
- Perform data quality checks.
- Generate meaningful engineered features.
- Validate derived variables.
- Document candidate treatment, outcome, and confounding variables.
- Support reproducible DML analysis.

## 3. Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Double Machine Learning
- Git and GitHub
- CSV datasets

## 4. Dataset Description

The project uses the Customer Personality Analysis marketing campaign dataset.

Original dataset:
`data/marketing_campaign.csv`

Cleaned dataset:
`data/retail_data.csv`

The dataset includes customer demographics, purchasing behaviour, campaign acceptance, and marketing response information.

## 5. Data Preparation

The data preparation process includes:

1. Removing duplicate records.
2. Handling missing income values.
3. Filtering invalid birth-year records.
4. Generating customer age.
5. Standardizing marital-status categories.
6. Calculating total purchase amount.
7. Calculating total purchases.
8. Generating campaign-related features.

## 6. Engineered Features

| Feature | Description |
|---|---|
| age | Customer age |
| total_purchase_amount | Total spending across product categories |
| total_purchases | Total web, catalog, and store purchases |
| deal_purchase_indicator | Indicates deal-purchase activity |
| campaign_exposure | Indicates acceptance of at least one campaign |
| campaign_response | Customer response copied from the original Response column |

## 7. Project Structure

```text
EconoCausal-Dynamic-Pricing/
│
├── data/
│   ├── marketing_campaign.csv
│   ├── retail_data.csv
│   ├── prepare_dataset.py
│   ├── data_dictionary.py
│   ├── data_dictionary.csv
│   ├── data_quality_report.py
│   └── data_quality_report.csv
│
├── src/
│   └── dml_estimation.py
│
├── docs/
│   ├── dml_results.md
│   ├── week3_dataset_audit.md
│   └── Week 4 documentation files
│
├── README.md
└── requirements.txt
```

*Note: Update this structure to match the files actually present in your repository.*

## 8. Data Validation and Testing

The project includes validation activities for:

- Missing values and duplicate records.
- Required engineered features.
- Binary campaign variables.
- Non-negative purchase and spending values.
- Derived feature calculations.
- Dataset reproducibility.
- Final dataset quality.

## 9. DML Analysis

The project uses Double Machine Learning to estimate a treatment effect while accounting for observed confounding variables.

The candidate treatment and outcome variables are:

- Candidate treatment: `campaign_exposure`
- Candidate outcome: `campaign_response`

The final variable definitions and causal interpretation require team approval and confirmation of event timing.

## 10. How to Run the Project

Clone the repository and navigate to the project directory.

Install dependencies:

```bash
pip install -r requirements.txt
```

Prepare the dataset:

```bash
python data/prepare_dataset.py
```

Run DML estimation:

```bash
python src/dml_estimation.py
```

Run tests:

```bash
python -m unittest discover -s src -p "test_*.py" -v
```

## 11. Limitations

- The analysis depends on the quality of the available dataset.
- Missing or unobserved confounders may affect causal estimates.
- Campaign acceptance and response must be clearly distinguished.
- The dataset does not directly establish a pricing treatment.
- Causal conclusions require suitable treatment timing and assumptions.

## 12. Conclusion

This project establishes a structured workflow for customer data preparation, validation, documentation, and causal analysis. Reproducibility and clear variable definitions are important for reliable results.

## 13. Contributors

Project team: EconoCausal – Dynamic Pricing

Branch used for individual development: `sekhar`
