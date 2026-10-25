
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


    def test_residual_integration(self):
        from src.dml_estimation import estimate_dml_from_residuals

        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)
        n = 1000

        t_residual = pd.Series(rng.normal(0, 1, n))
        y_residual = pd.Series(
            3 * t_residual + rng.normal(0, 0.1, n)
        )

        result = estimate_dml_from_residuals(
            y_residual, t_residual
        )

        self.assertAlmostEqual(result.effect, 3.0, delta=0.1)
        self.assertGreater(result.standard_error, 0)
        self.assertLess(result.ci_lower, result.ci_upper)
        self.assertEqual(result.sample_size, n)



if __name__ == "__main__":
    unittest.main()
