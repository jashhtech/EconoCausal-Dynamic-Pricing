\# Double Machine Learning (DML) Results



\## 1. Objective



The objective is to estimate how promotional discounts influence customer purchasing behavior and, where the data supports it, identify differences in treatment effects across customer profiles.



\## 2. Planned Method



The DML pipeline uses three inputs:



\- \*\*X — Confounders:\*\* Customer characteristics that may influence treatment assignment and purchasing behavior.

\- \*\*T — Treatment:\*\* The promotional offer actually assigned or received by a customer.

\- \*\*Y — Outcome:\*\* The purchasing outcome measured after treatment.



The pipeline uses cross-fitting to generate out-of-fold predictions for the outcome and treatment. It then uses residuals from these predictions to estimate a treatment effect.



\## 3. Dataset and Current Limitations



The current retail dataset contains 2,237 customer records and 35 columns.



The available columns include customer characteristics, deal-purchase counts, campaign acceptance indicators, and campaign response.



The dataset does not currently contain an explicit discount-amount variable identifying $10 and $20 offers. Therefore, a direct causal comparison between these two discount amounts cannot yet be reported.



Campaign acceptance and deal-purchase counts must not automatically be treated as randomized discount assignments. Their meanings and timing must be verified before selecting a treatment variable.



\## 4. Evaluation Plan



The following checks are planned:



\- Validate the definitions of X, T, and Y.

\- Check missing values, data types, and treatment variation.

\- Evaluate nuisance-model predictions using held-out data.

\- Report the estimated treatment effect and uncertainty.

\- Examine whether the estimate is sensitive to model choices and assumptions.

\- Assess whether the data supports comparisons between relevant customer groups.



\## 5. Results Status



\*\*Status: Integration scaffold prepared; causal results pending.\*\*



The initial Python module has been created and executed successfully. No treatment-effect estimate has been produced yet because the treatment and outcome definitions must be confirmed and the pipeline must be evaluated with valid inputs.



\## 6. Future Work



1\. Integrate the team's data-preprocessing component.

2\. Use the agreed feature definitions and treatment/outcome variables.

3\. Integrate the nuisance models.

4\. Run and validate the DML estimation pipeline.

5\. Record the estimated effect, uncertainty, evaluation findings, and limitations.

6\. Provide suitable results for the project dashboard.



\## 7. Interpretation Caution



A DML estimate does not establish causality by itself. Its interpretation depends on appropriate treatment assignment, sufficient overlap, suitable confounder adjustment, and defensible causal assumptions.





## Week 2 Progress — October 21, 2026

* Created the initial DML estimation module with cross-fitting and treatment-effect uncertainty estimation.
* Added documentation covering the planned method, evaluation steps, and current limitations.
* Reviewed the team's feature engineering and DML implementations to identify integration requirements.
* Identified a mismatch between the feature names in the feature engineering code and the shared retail dataset.
* Pending confirmation of the treatment, outcome, and confounder variables before running causal estimation.

**Status:** Initial implementation committed and pushed. Team integration and validation are in progress.





\# Double Machine Learning (DML) Results Report



\## 1. Project Objective



The objective is to estimate how promotional offers influence customer purchasing behavior using Double Machine Learning (DML), with the long-term goal of improving promotional budget allocation.



\## 2. DML Implementation



The estimator is implemented in `src/dml\_estimation.py`.



It accepts three inputs:



\- \*\*X — Confounders:\*\* relevant customer characteristics measured before treatment.

\- \*\*T — Treatment:\*\* the treatment actually assigned or received.

\- \*\*Y — Outcome:\*\* the outcome measured after treatment.



The implementation uses cross-fitting and residual-based effect estimation. It returns an estimated treatment effect, standard error, confidence interval, and sample size.



\## 3. Testing and Validation



Two test modules are available:



\- `src/test\_dml\_estimation.py` checks estimator behavior and input validation.

\- `src/test\_dml\_synthetic.py` checks whether the estimator can recover a known treatment effect from synthetic data.



The three existing tests passed in the previous test run. They should be rerun after the latest documentation changes and any further code changes.



\## 4. Dataset Summary



The cleaned dataset, `data/retail\_data.csv`, contains 2,237 customer records and 35 columns.



It includes customer characteristics, purchase amounts, deal-purchase counts, campaign acceptance indicators, and campaign response.



\## 5. Important Data Limitations



The dataset does not contain a verified assigned discount amount distinguishing $10 and $20 offers.



\- `NumDealsPurchases` records deal-purchase counts, not assigned discount amounts.

\- `campaign\_exposure` is derived from campaign acceptance indicators.

\- `campaign\_response` duplicates `Response`.



Consequently, the current dataset does not yet support a defensible direct causal comparison of $10 versus $20 discounts.



\## 6. Current Results Status



\*\*Status: DML estimator implemented; synthetic validation tests available; real-data causal results pending.\*\*



No real discount-effect estimate is reported in this document because the treatment and outcome definitions require confirmation.



Synthetic validation demonstrates performance on simulated data only. It is not evidence of actual customer behavior or business impact.



\## 7. Remaining Work



1\. Confirm the treatment, outcome, and pre-treatment confounders with the team.

2\. Obtain valid discount-assignment data if the project requires comparing $10 and $20 offers.

3\. Evaluate treatment overlap and nuisance-model performance on suitable data.

4\. Assess the sensitivity of estimates to model choices and assumptions.

5\. If the dashboard requires customer-specific effects, implement and validate an appropriate individualized-effect method.

6\. Integrate validated results into the dashboard.



\## 8. Interpretation



DML does not guarantee causal conclusions by itself. Reliable interpretation requires valid treatment and outcome definitions, suitable confounder adjustment, adequate treatment overlap, and defensible causal assumptions.

