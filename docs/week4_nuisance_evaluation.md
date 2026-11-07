\# Week 4 Nuisance Model Evaluation (Vridhi)



Status: in progress. Sections are added day by day and finalised on Day 7.



\## Day 3: Model configuration comparison



Script: `python src/model\_comparison.py` (results in `results/model\_comparison.csv`).

Same 5-fold cross-fitted procedure, preprocessing, seed and metrics as

`src/nuisance\_models.py`. The three Week 2 models are taken unchanged from

`candidate\_models()`, so their numbers match the earlier results.



\### campaign\_response (outcome)



| Model | AUC | Log loss |

|---|---|---|

| random\_forest depth10 | 0.7809 | 0.3521 |

| random\_forest (current) | 0.7780 | 0.3538 |

| grad\_boosting depth2 | 0.7741 | 0.3559 |

| random\_forest leaf10 | 0.7754 | 0.3565 |

| grad\_boosting (current) | 0.7718 | 0.3576 |

| lightgbm small | 0.7725 | 0.3577 |

| random\_forest depth5 | 0.7699 | 0.3623 |

| lightgbm | 0.7661 | 0.3655 |

| logistic (baseline) | 0.7489 | 0.3726 |



\### campaign\_exposure (treatment)



| Model | AUC | Log loss |

|---|---|---|

| grad\_boosting depth2 | 0.7272 | 0.4437 |

| random\_forest (current) | 0.7264 | 0.4456 |

| random\_forest depth10 | 0.7270 | 0.4456 |

| random\_forest depth5 | 0.7236 | 0.4478 |

| random\_forest leaf10 | 0.7241 | 0.4479 |

| grad\_boosting (current) | 0.7238 | 0.4484 |

| lightgbm small | 0.7244 | 0.4522 |

| lightgbm | 0.7113 | 0.4685 |

| logistic (baseline) | 0.7148 | 0.4699 |



\### Basis for the preferred models

\- The best alternative differs from the current Random Forest by about 0.003 AUC

&#x20; for the outcome model and about 0.001 AUC for the treatment model. This is

&#x20; small and comes from a single 5-fold split, so it is not evidence that the

&#x20; alternative is better.

\- LightGBM did not improve on Random Forest for either target.

\- All tree models beat the Logistic Regression baseline.

\- Decision: keep Random Forest (`n\_estimators=200`, `min\_samples\_leaf=5`) as the

&#x20; default for both nuisance models. This also keeps the DML estimates in

&#x20; `dml\_estimation.py` unchanged.



\### Limitations

\- One cross-validation split and one seed, so small differences are not tested

&#x20; for significance.

\- Only a few hyperparameter settings were tried; this is not a full search.







\## Day 4: Treatment overlap and imbalance



Script: `python src/overlap\_analysis.py` (results in `results/overlap\_analysis.csv`).

Propensity scores are the cross-fitted Random Forest scores from

`src/treatment\_model.py`.



\### Class balance

| campaign\_exposure | Count | Share |

|---|---|---|

| 0 (untreated) | 1775 | 0.7935 |

| 1 (treated) | 462 | 0.2065 |



\### Propensity score by treatment group

| Group | n | Min | p25 | Median | p75 | Max |

|---|---|---|---|---|---|---|

| Treated | 462 | 0.0201 | 0.1502 | 0.2900 | 0.5113 | 0.7895 |

| Untreated | 1775 | 0.0130 | 0.0926 | 0.1432 | 0.2160 | 0.7525 |



Common support (range where both groups have customers): 0.0201 to 0.7525.



\### Trimming sensitivity

| Cut-off | Kept | Kept share | Treated dropped | Untreated dropped |

|---|---|---|---|---|

| \[0.01, 0.99] | 2237 | 1.0000 | 0 | 0 |

| \[0.05, 0.95] | 2121 | 0.9481 | 11 | 105 |

| \[0.10, 0.90] | 1670 | 0.7465 | 51 | 516 |



\### Findings

\- Treated customers have higher scores than untreated ones (median 0.29 versus

&#x20; 0.14), so the confounders carry some information about exposure.

\- Both groups cover almost the whole score range and no customer has a score

&#x20; near 1 (maximum 0.7895). Positivity does not look seriously violated.

\- The lower tail is thin: 116 customers (5.2 percent) have scores below 0.05, and

&#x20; 105 of them are untreated. No customer is above 0.95, so upper trimming has no

&#x20; effect.



\### Limitations caused by treatment imbalance

\- Only 462 treated customers (20.65 percent) are available, so estimates for

&#x20; treated customers are noisier than for untreated ones.

\- Trimming at 0.10 removes about 25 percent of the sample (51 treated and 516

&#x20; untreated). The result would then describe the remaining subgroup rather than

&#x20; all customers, so it should not be treated as the same estimate.

\- Scores come from one model (Random Forest) and one cross-validation split, so

&#x20; the overlap picture depends on that model.

\- Overlap says nothing about unmeasured confounding or about whether the purchase

&#x20; columns are valid confounders; both are still open.

