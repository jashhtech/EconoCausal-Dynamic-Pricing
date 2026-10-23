# EconoCausal - Feature Definitions

## Objective
Prepare features for the Dynamic Pricing causal inference pipeline.

## Dataset
- File: retail_data.csv
- Cleaned records: 2237

## Current Variable Configuration
- X (Confounders): age, total_purchases
- T (Treatment): deal_purchase_indicator
- Y (Outcome): total_purchase_amount

## Pipeline Validation
- Data loading: Successful
- Feature preprocessing: Successful
- Train-test split: Successful
- Training rows: 1789
- Testing rows: 448

## Pending Checks
- Confirm treatment definition with the team.
- Verify confounders are measured before treatment.
- Confirm compatibility with DML integration.

## Status
Feature engineering pipeline tested successfully.
Causal variable definitions require confirmation.