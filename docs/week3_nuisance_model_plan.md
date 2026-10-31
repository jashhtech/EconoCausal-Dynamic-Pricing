\# Week 3 Nuisance Model Plan (Vridhi)



Date: 30 Oct 2026



\## Purpose

In Double ML, two nuisance models remove the effect of confounders X from the

treatment T and the outcome Y. The residuals of both models are then used by the

DML estimator (Hepsiba) to estimate the treatment effect.



\## Variable definitions (current, pending final team confirmation)

\- Treatment T: campaign\_exposure (binary; 462 ones, 1775 zeros, 2237 rows)

\- Outcome Y: campaign\_response (binary)

\- Confounders X: age, Income, Kidhome, Teenhome, Recency (numeric);

&#x20; Education, Marital\_Status (categorical)

\- Excluded: Response, AcceptedCmp1-5 (leakage; Response is identical to

&#x20; campaign\_response)

\- Excluded for now: total\_purchase\_amount, total\_purchases. Their timing relative

&#x20; to the campaign is not confirmed, so they are left out until the team confirms

&#x20; they are measured before the campaign.



\## Model choices

\- Treatment model (propensity): classifier predicting P(T = 1 | X), because T is binary.

\- Outcome model: classifier predicting P(Y = 1 | X), because Y is binary. It uses

&#x20; X only (partialling-out DML formulation), not T.

\- Candidates: Logistic Regression (baseline), Random Forest, Gradient Boosting.

\- Preprocessing: StandardScaler on numeric columns, one-hot encoding on

&#x20; categorical columns.



\## Cross-fitting

\- 5-fold stratified cross-validation, fixed seed 42.

\- Each observation's prediction comes from a model that did not train on it

&#x20; (out-of-fold). Predictions stay aligned with the original row order.

\- Residuals: Y\_res = Y - Y\_hat, T\_res = T - T\_hat (`dml\_residuals()` in

&#x20; src/nuisance\_models.py).



\## Evaluation (binary targets)

\- ROC-AUC and log loss for both models.

\- Treatment model: class distribution and propensity score range for the overlap

&#x20; check.



\## Current results (final feature set)

\- Outcome: Random Forest AUC 0.7780, log loss 0.3538.

\- Treatment: Random Forest AUC 0.7264, log loss 0.4456.

\- Propensity range 0.013 to 0.79 (mean 0.208), so overlap looks acceptable.

\- Full table: results/nuisance\_model\_results.csv and docs/model\_selection.md.



\## Module layout

src/nuisance\_models.py holds the shared logic. Thin wrappers will expose the

interfaces named in the Week 3 allocation:

\- src/treatment\_model.py

\- src/outcome\_model.py

\- src/nuisance\_predictions.py



\## Risks and open questions

\- Final treatment, outcome and confounder roles are not yet confirmed by the team.

\- Timing of the purchase columns is unconfirmed (Sekhar's variable timing check).

\- Treatment is imbalanced (about 21 percent exposed).

\- LightGBM has not been tried.

