# Week 4 – Day 5: Reproducibility Testing

## 1. Objective

The objective of this task is to verify that the dataset preparation pipeline generates consistent output across multiple executions.

## 2. Testing Method

The following steps were performed:

1. Executed the dataset preparation script.
2. Generated the cleaned retail dataset.
3. Calculated the SHA256 hash of the generated dataset.
4. Executed the preparation script a second time.
5. Compared the hashes, dataset dimensions, and dataset contents.

## 3. Validation Results

- SHA256 comparison: [PASS/FAIL]
- Dataset shape comparison: [PASS/FAIL]
- Dataset content comparison: [PASS/FAIL]

## 4. Output File

`data/week4_day5_reproducibility_report.csv`

## 5. Conclusion

The reproducibility test evaluated whether repeated executions of the dataset preparation pipeline produced identical outputs. The results were recorded for review.

Any failed checks should be investigated before the pipeline is considered reproducible.

