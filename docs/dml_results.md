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



