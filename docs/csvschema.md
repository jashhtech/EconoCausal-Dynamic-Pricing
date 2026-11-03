\# EconoCausal CSV Schema



Status: Updated to match the real retail dataset columns used by the nuisance models.



\## Required Columns

The following columns are required in the uploaded historical campaign data for the dashboard and the DML pipeline:



\- `ID`: Customer identifier

\- `age`: Customer's age (numeric)

\- `Income`: Customer's income (numeric)

\- `Kidhome`: Number of kids in the household (numeric)

\- `Teenhome`: Number of teens in the household (numeric)

\- `Recency`: Number of days since the last purchase (numeric)

\- `Education`: Categorical variable for education level

\- `Marital\_Status`: Categorical variable for marital status

\- `campaign\_exposure`: Treatment variable (1 if exposed, 0 otherwise)

\- `campaign\_response`: Outcome variable (1 if responded, 0 otherwise)



\*Note: Purchase-related columns (`total\_purchase\_amount`, `total\_purchases`) are excluded from this schema pending confirmation of their timing relative to the campaign.\*

