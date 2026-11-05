\# Week 3 Day 7: Final Reproducibility Review



\## 1. Objective



The objective of Day 7 was to verify that the nuisance prediction and evaluation scripts execute successfully and produce consistent outputs.



\## 2. Reproducibility Checks



\### Nuisance Predictions



Script executed:



```bash

python src/nuisance\_predictions.py

```



Results:



\- Input rows: 2,237

\- Output rows: 2,237

\- Reproducibility check reported: True

\- Output generated: `results/nuisance\_predictions.csv`



\### Nuisance Model Evaluation



Script executed:



```bash

python src/nuisance\_evaluation.py

```



The evaluation script was executed twice.



Both runs produced identical displayed evaluation metrics.



| Model | ROC-AUC | Log Loss | Brier Score |

|---|---:|---:|---:|

| Treatment | 0.7264 | 0.4456 | 0.1382 |

| Outcome | 0.7780 | 0.3538 | 0.1062 |



Output generated:



`results/nuisance\_evaluation.csv`



\## 3. Output Consistency Review


The generated nuisance prediction CSV was compared with the previously committed version.

Both CSV files contained 2,237 rows and 6 columns, with identical column names.

The comparison showed:
- Treatment (`T`) and outcome (`Y`) columns were exactly identical.
- Small floating-point differences were observed in the prediction and residual columns.
- The maximum absolute difference was approximately 5.0e-16.
- A tolerance-based comparison using an absolute tolerance of 1e-12 and relative tolerance of 0 passed.

Therefore, the old and newly generated prediction outputs are numerically equivalent within the selected tolerance. The small differences are consistent with floating-point precision variation and do not indicate a meaningful change in predictions.

The previously committed prediction CSV was retained to avoid an unnecessary output-only change.

