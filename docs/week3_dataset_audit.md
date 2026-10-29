# Week 3 – Day 1: Dataset Audit

**Name:** Kolli Chandra Sekhar  
**Project:** EconoCausal – Dynamic Pricing via Double Machine Learning (DML)

## Objective
Inspect the original marketing campaign dataset and identify potential data quality issues before model integration.

## Tasks
1. Inspected `data/marketing_campaign.csv`.
2. Checked the number of rows and columns.
3. Reviewed column names and data types.
4. Identified missing values.
5. Checked for duplicate records.
6. Reviewed the availability of variables required for downstream analysis.

## Dataset Details
- **Original dataset:** `marketing_campaign.csv`
- **Expected dimensions:** 2,240 rows × 29 columns
- **Known missing values:** 24 entries in the `Income` column
- **Known duplicate records:** 0

## Outcome
The initial dataset audit identifies the dataset structure and data quality issues that need to be considered during preparation.

## Next Steps
- Review missing values and invalid records.
- Confirm the treatment, outcome, and confounder definitions with the team.
- Continue with the Week 3 data quality validation tasks.
