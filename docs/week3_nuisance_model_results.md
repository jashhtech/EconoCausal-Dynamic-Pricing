\# Week 3: Nuisance Model Results and Integration Notes



\## 1. Overview



This document records the Week 3 nuisance-model evaluation and integration notes for the Dynamic Pricing DML workflow.



The two nuisance models are:



\- Treatment model: predicts `campaign\_exposure`.

\- Outcome model: predicts `campaign\_response`.



\## 2. Model Evaluation Results



\### 2.1 Overall Metrics



| Model | ROC-AUC | Log Loss | Brier Score |

|---|---:|---:|---:|

| Treatment (`campaign\_exposure`) | 0.7264 | 0.4456 | 0.1382 |

| Outcome (`campaign\_response`) | 0.7780 | 0.3538 | 0.1062 |



\### 2.2 Threshold-Based Metrics



| Model | Threshold | Precision | Recall | Predicted Positive Share |

|---|---:|---:|---:|---:|

| Treatment | 0.5000 | 0.6455 | 0.2641 | 0.0845 |

| Treatment | 0.2065 | 0.3736 | 0.6364 | 0.3518 |

| Outcome | 0.5000 | 0.7170 | 0.1138 | 0.0237 |

| Outcome | 0.1493 | 0.2981 | 0.7425 | 0.3719 |



The base-rate thresholds increase recall and predicted-positive share, while precision decreases.



\## 3. Evaluation Files



| File | Purpose |

|---|---|

| `src/nuisance\_evaluation.py` | Calculates model evaluation metrics |

| `results/nuisance\_evaluation.csv` | Stores evaluation results |

| `src/nuisance\_predictions.py` | Generates combined nuisance predictions |

| `results/nuisance\_predictions.csv` | Stores combined predictions and residuals |



\## 4. Integration Notes for DML



The model interfaces used by the evaluation script are:



\- `propensity\_scores(df)` from `src/treatment\_model.py`

\- `outcome\_predictions(df

