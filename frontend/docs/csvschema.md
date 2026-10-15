# CSV Data Dictionary (Proposed Schema)

Status: proposed by frontend, to be confirmed with the dataset teammate.

## Columns

| Column | Type | Allowed values | Role |
|---|---|---|---|
| customer_id | integer | unique per customer | identifier |
| age | integer | years, e.g. 18 to 80 | confounder |
| past_spend | number | total past spend in $ | confounder |
| visits_per_month | number | average visits per month | confounder |
| tenure_months | integer | months since signup | confounder |
| region | text | North, South, East, West | confounder |
| discount_given | integer | 0, 10, 20 (in $) | treatment |
| purchased | integer | 0 or 1 | outcome |

## Causal roles (for the DoWhy DAG)

- Treatment: `discount_given` (the discount the customer was shown)
- Outcome: `purchased` (did the customer buy)
- Confounders: `age`, `past_spend`, `visits_per_month`, `tenure_months`, `region`
  (they can affect both who got a discount and who buys)

## Frontend validation status

- Done: the upload page checks that all 8 columns exist.
- Pending: null or empty values, wrong data types, and values outside the allowed range.

## Sample files

- `sample_data/test_campaign.csv`: valid file with 12 rows
- `sample_data/bad.csv`: invalid file with missing columns, used to test the error message