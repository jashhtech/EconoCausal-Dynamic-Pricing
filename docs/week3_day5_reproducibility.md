# Week 3 – Day 5: Reproducibility Testing

**Name:** Kolli Chandra Sekhar

**Project:** EconoCausal – Dynamic Pricing via Double Machine Learning (DML)

## Objective

Verify that the dataset preparation process produces consistent and reproducible results across multiple executions.

## Tasks Performed

1. Reviewed the existing dataset preparation script.
2. Executed `prepare_dataset.py` for the first time.
3. Loaded and recorded the generated dataset.
4. Executed the preparation script a second time.
5. Compared both generated datasets.
6. Checked dataset dimensions, missing values, and duplicate records.

## Testing Script

`data/test_reproducibility.py`

## Validation Criteria

* Consistent dataset dimensions.
* Identical output across repeated executions.
* No unexpected missing values.
* No duplicate records.

## Outcome

The reproducibility test was designed to verify that repeated executions of the dataset preparation script produce identical outputs.

## Next Steps

Prepare the final data quality report and organize the dataset documentation for project integration.
