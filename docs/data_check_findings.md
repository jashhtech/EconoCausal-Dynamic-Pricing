# Data Check Findings (retail_data.csv)

Script: `src/data_check.py` | Dataset: `data/retail_data.csv`
Rows: 2237 | Columns: 35

## 1. Treatment balance (campaign_exposure)
| Value | Count |
|-------|-------|
| 0 (not exposed) | 1775 |
| 1 (exposed) | 462 |

About 20.7% of customers are exposed. The treatment is imbalanced but both groups have enough rows for the treatment model.

## 2. campaign_response vs Response (leakage check)
The two columns are equal in 100% of rows, so they are duplicates.
Decision: `campaign_response` is used as the outcome and `Response` must NOT be used as a feature, otherwise the outcome leaks into the model.

## 3. deal_purchase_indicator
| Value | Count |
|-------|-------|
| 1 | 2191 |
| 0 | 46 |

The column is almost constant (about 98% ones), so it carries very little information as a confounder.

## 4. Confounder balance (exposed vs not exposed)
| Confounder | Mean exposed | Mean not exposed | SMD |
|------------|--------------|------------------|-----|
| total_purchase_amount | 1095.40 | 478.29 | 1.035 |
| total_purchases | 16.68 | 11.47 | 0.767 |
| Income | 65095.90 | 48877.97 | 0.711 |
| Kidhome | 0.23 | 0.50 | -0.547 |
| Teenhome | 0.40 | 0.53 | -0.247 |
| age | 56.77 | 55.92 | 0.070 |
| Recency | 48.25 | 49.33 | -0.037 |

Rule of thumb: |SMD| > 0.1 means the groups are imbalanced.
Only age and Recency are balanced. The rest differ a lot between exposed and not exposed customers.

## 5. Overlap (propensity scores)
Cross-fitted Random Forest propensity scores for campaign_exposure:

| Statistic | Value |
|-----------|-------|
| count | 2237 |
| mean | 0.2083 |
| std | 0.1802 |
| min | 0.0088 |
| 25% | 0.0779 |
| median | 0.1448 |
| 75% | 0.2750 |
| max | 0.8901 |

- No score is exactly 0 or 1, so every customer has some chance of being exposed or not exposed.
- The mean (0.208) matches the exposed share (20.7%).
- Scores are skewed low and the minimum is below 0.01, so overlap is thin at the low end. Effect estimates for those customers may be unstable. Plan: clip propensity scores to [0.01, 0.99] and check that results do not change much.

## Implications
- A naive comparison of exposed vs not exposed would be biased, because exposed customers spend more, earn more and have fewer kids at home.
- This supports using Double ML to adjust for confounders.
- Overlap was checked in section 5: acceptable, but thin at the low end of the propensity scores.
- Treatment and outcome roles are still to be confirmed with Jaswanth.