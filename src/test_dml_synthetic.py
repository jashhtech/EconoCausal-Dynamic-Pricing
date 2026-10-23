
import unittest

import numpy as np
import pandas as pd

from src.dml_estimation import estimate_dml


class TestDMKSyntheticData(unittest.TestCase):
    def test_estimator_recovers_known_effect(self):
        rng = np.random.default_rng(42)
        n = 3000

        # Customer characteristics (confounders)
        X = pd.DataFrame({
            "income": rng.normal(50000, 12000, n),
            "age": rng.normal(40, 10, n),
        })

        # Treatment assignment depends on customer characteristics.
        treatment_probability = 1 / (
            1 + np.exp(
                -(
                    (X["income"] - 50000) / 12000
                    + (X["age"] - 40) / 10
                ) * 0.4
            )
        )
        T = pd.Series(
            rng.binomial(1, treatment_probability),
            index=X.index,
        )

        # The true causal effect is 5.
        # Outcome also depends on the customer characteristics.
        Y = pd.Series(
            5 * T
            + 0.0001 * (X["income"] - 50000)
            + 0.3 * (X["age"] - 40)
            + rng.normal(0, 1, n),
            index=X.index,
        )

        result = estimate_dml(X, T, Y, random_state=42)

        # Allow a reasonable margin for estimation noise.
        self.assertAlmostEqual(result.effect, 5.0, delta=0.5)
        self.assertGreater(result.standard_error, 0)
        self.assertEqual(result.sample_size, n)


if __name__ == "__main__":
    unittest.main()
