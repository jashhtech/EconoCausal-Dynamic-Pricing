
import unittest

import numpy as np
import pandas as pd

from src.dml_estimation import estimate_dml


class TestDMLEstimation(unittest.TestCase):

    def setUp(self):
        rng = np.random.default_rng(42)
        n = 300

        age = rng.integers(20, 70, n)
        income = rng.normal(40000, 10000, n)
        treatment_probability = 1 / (
            1 + np.exp(-(-0.5 + age / 70 + income / 80000))
        )
        treatment = rng.binomial(1, treatment_probability)

        outcome = (
            2.0 * treatment
            + 0.03 * age
            + income / 10000
            + rng.normal(0, 1, n)
        )

        self.X = pd.DataFrame({
            "age": age,
            "income": income,
        })
        self.T = pd.Series(treatment)
        self.Y = pd.Series(outcome)

    def test_returns_valid_result(self):
        result = estimate_dml(self.X, self.T, self.Y)

        self.assertEqual(result.sample_size, 300)
        self.assertTrue(np.isfinite(result.effect))
        self.assertTrue(np.isfinite(result.standard_error))
        self.assertLessEqual(result.ci_lower, result.ci_upper)

    def test_rejects_too_few_observations(self):
        with self.assertRaises(ValueError):
            estimate_dml(
                self.X.iloc[:5],
                self.T.iloc[:5],
                self.Y.iloc[:5],
            )


if __name__ == "__main__":
    unittest.main()
