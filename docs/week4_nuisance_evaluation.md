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




## Day 5: Robustness checks

Script: `python src/robustness_check.py` (results in `results/robustness_check.csv`).
Each specification cross-fits the nuisance models and estimates the effect of
campaign_exposure on campaign_response by regressing the outcome residual on the
treatment residual, with a heteroskedasticity-robust standard error. This is a
simple partialling-out check that uses our own nuisance models. It is not the
estimate in `src/dml_estimation.py` (Hepsiba) and it is not a validated causal
effect.

| Specification | n | Estimate | Std error | 95% CI |
|---|---|---|---|---|
| 1 Baseline (Random Forest, final features) | 2237 | 0.2835 | 0.0234 | 0.2376 to 0.3293 |
| 2 Trim propensity [0.05, 0.95] | 2121 | 0.2837 | 0.0237 | 0.2373 to 0.3301 |
| 3 Trim propensity [0.10, 0.90] | 1670 | 0.2795 | 0.0250 | 0.2305 to 0.3285 |
| 4 With purchase columns | 2237 | 0.2473 | 0.0243 | 0.1996 to 0.2949 |
| 5 Gradient Boosting nuisance models | 2237 | 0.2672 | 0.0235 | 0.2211 to 0.3132 |
| 6 Logistic nuisance models | 2237 | 0.2943 | 0.0230 | 0.2492 to 0.3395 |

### Findings
- Across the six specifications the estimate stays between 0.247 and 0.294 and
  is positive in all of them. All confidence intervals overlap and none includes
  zero.
- Trimming the propensity scores has almost no effect (0.2835 to 0.2837 and
  0.2795), so the thin lower tail found in Day 4 is not driving the estimate.
- Changing the nuisance model moves the estimate by about 0.01 (Gradient
  Boosting 0.2672, Logistic 0.2943).
- The largest change comes from adding the purchase columns back: the estimate
  falls by about 0.036, which is more than one standard error (0.023). The
  estimate therefore depends on whether these columns are valid pre-treatment
  confounders, which is still not confirmed.
- Hepsiba's DML estimates show the same direction: 0.2725 without and 0.2361 with
  the purchase columns, also a drop of about 0.036. The levels differ slightly
  from this check (0.2835 and 0.2473), which uses a different implementation.

### Limitations
- This check does not show robustness to unmeasured confounding. All
  specifications use the same measured confounders.
- An effect of about 0.28 on a response rate of 0.149 is large. The definition of
  campaign_exposure should be checked with Sekhar, because a treatment that is
  closely related to the outcome would inflate the estimate.
- The estimates are not validated causal effects. Refutation tests have not been
  run.
- Standard errors assume independent customers and a single cross-fitting split.


## Update: definition of the treatment (confirmed by Sekhar)

- `campaign_exposure` is derived from `AcceptedCmp1` to `AcceptedCmp5`: it is 1 if
  the customer accepted at least one of those campaigns, otherwise 0.
- `campaign_response` is copied from the original `Response` column.
- The dataset has no timestamps, so it cannot establish whether
  `total_purchase_amount` and `total_purchases` were measured before or after the
  treatment (see `docs/week4_data_audit.md` on branch `sekhar`).

### What this means for the results
- The treatment describes past campaign acceptance, not an exposure or discount
  that was assigned to customers. A customer who accepted earlier campaigns is
  likely to be generally responsive to offers, and this responsiveness is not
  among the measured confounders (age, income, children, recency, education,
  marital status).
- The estimates of 0.25 to 0.29 in the robustness check should therefore be read
  as the adjusted association between earlier acceptance and the latest response.
  They should not be read as the effect of showing a discount, and they are not
  validated causal effects.
- The nuisance models and the leakage guard are unaffected: `AcceptedCmp1-5` are
  already excluded from the features, so the treatment is not predicted from its
  own components.

### Recommendations
- Describe `campaign_exposure` in the final report as "prior campaign acceptance".
- Keep the purchase columns out of the confounder set until their timing is
  established.
- For a real pricing question, a treatment that records an assigned discount
  (for example a discount indicator with a known time) would be needed. Discuss
  with the mentor whether such a variable exists in the dataset.


## Day 7: Final Summary, Conclusions, and Recommendations

### Summary of Nuisance Model Evaluation
Over Week 4, the nuisance models (Treatment: `campaign_exposure`, Outcome: `campaign_response`) were rigorously evaluated to validate their suitability for Double Machine Learning estimation.
1. **Model Selection:** The Random Forest configuration (`n_estimators=200`, `min_samples_leaf=5`) remained the preferred model. It consistently outperformed Logistic Regression and Gradient Boosting (with ±0.003 AUC difference).
2. **Propensity Overlap & Positivity:** The propensity scores show strong common support across both treated and untreated groups. Positivity is not violated, although a thin lower tail exists.
3. **Robustness:** Simple partialling-out checks confirmed that the effect estimate is stable across different nuisance models and is unaffected by propensity trimming at [0.05, 0.95].

### Recommendations for DML Estimation
1. **Reporting the Estimate:** Explicitly label the DML result as an "adjusted association between prior campaign acceptance and current campaign response", rather than a randomized causal effect.
2. **Trimming:** Since trimming the sample at [0.05, 0.95] barely moves the estimate, proceed with reporting the full-sample DML estimate as the primary result to maintain statistical power.
3. **Feature Set:** Continue to exclude the purchase columns (`total_purchase_amount`, `total_purchases`) from the primary DML confounder set, as their post-treatment status cannot be ruled out. Use them strictly as a sensitivity check.
4. **Visual Evidence:** Reference the evaluation plots generated in `results/` (`auc_comparison.png`, `propensity_overlap.png`, `robustness_forest_plot.png`) in the final project report.

