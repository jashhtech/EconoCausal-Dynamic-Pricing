# Week 3 – Day 4: Treatment and Outcome Data Validation

**Name:** Kolli Chandra Sekhar

**Project:** EconoCausal – Dynamic Pricing via Double Machine Learning (DML)

## Objective

Validate campaign exposure and campaign response variables in the cleaned marketing campaign dataset.

## Tasks Performed

1. Loaded the cleaned retail dataset.
2. Checked the availability of campaign-related columns.
3. Examined missing values in campaign variables.
4. Calculated campaign exposure distribution.
5. Calculated campaign response distribution.
6. Checked binary values in treatment and outcome candidates.
7. Examined individual campaign acceptance distributions.
8. Generated a cross-tabulation between campaign exposure and campaign response.
9. Compared the engineered campaign response with the original Response column.

## Validation Script

`data/validate_campaign_data.py`

## Variables Reviewed

* `campaign_exposure`
* `campaign_response`
* `AcceptedCmp1`
* `AcceptedCmp2`
* `AcceptedCmp3`
* `AcceptedCmp4`
* `AcceptedCmp5`
* `Response`

## Outcome

Campaign-related variables were examined for missing values, value distributions, and consistency. The results will help the team review treatment and outcome definitions before DML integration.

## Important Observation

The treatment, outcome, and confounder definitions require team confirmation. Variable timing and potential post-treatment information must be considered before causal estimation.

## Next Steps

Finalize the campaign variable definitions with the project team and continue data reproducibility checks.

