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



Small floating-point differences were observed in some decimal values. These differences were limited to numerical precision in the displayed examples.



The prediction CSV was not included in the Day 7 commit because the differences had not been fully investigated.



\## 4. Git Verification



The Week 3 Day 5 and Day 6 work was committed and pushed successfully.



Commit:



`2

