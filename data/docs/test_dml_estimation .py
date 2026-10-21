
import unittest
import pandas as pd

from dml_estimation import validate_dataset


class TestDMLValidation(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "deal_purchase_indicator": [0, 1, 0, 1],
            "total_purchase_amount": [100, 200, 150, 250],
            "age": [25, 35, 45, 55],
            "Income": [30000, 40000, 50000, 60000],
            "Education": ["A", "B", "A", "B"],
            "Marital_Status": ["Single", "Married", "Single", "Married"],
            "Recency": [10, 20, 30, 40],
        })

    def test_valid_dataset_passes(self):
        validate_dataset(self.df)

    def test_missing_column_fails(self):
        invalid = self.df.drop(columns=["Income"])
        with self.assertRaises(ValueError):
            validate_dataset(invalid)

    def test_missing_required_value_fails(self):
        invalid = self.df.copy()
        invalid.loc[0, "Income"] = None
        with self.assertRaises(ValueError):
            validate_dataset(invalid)

    def test_non_binary_treatment_fails(self):
        invalid = self.df.copy()
        invalid.loc[0, "deal_purchase_indicator"] = 2
        with self.assertRaises(ValueError):
            validate_dataset(invalid)


if __name__ == "__main__":
    unittest.main()

