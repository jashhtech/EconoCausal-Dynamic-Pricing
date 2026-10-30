
from pathlib import Path
import subprocess
import sys
import pandas as pd
from pandas.testing import assert_frame_equal

# Step 1: Define paths
DATA_DIR = Path(__file__).resolve().parent
PROJECT_DIR = DATA_DIR.parent

PREPARE_SCRIPT = DATA_DIR / "prepare_dataset.py"
OUTPUT_FILE = DATA_DIR / "retail_data.csv"

# Step 2: Execute dataset preparation
print("Running dataset preparation - First execution")

subprocess.run(
    [sys.executable, str(PREPARE_SCRIPT)],
    cwd=PROJECT_DIR,
    check=True
)

# Step 3: Load first output
df_first = pd.read_csv(OUTPUT_FILE)

print("\nFirst execution shape:", df_first.shape)

# Step 4: Execute dataset preparation again
print("\nRunning dataset preparation - Second execution")

subprocess.run(
    [sys.executable, str(PREPARE_SCRIPT)],
    cwd=PROJECT_DIR,
    check=True
)

# Step 5: Load second output
df_second = pd.read_csv(OUTPUT_FILE)

print("Second execution shape:", df_second.shape)

# Step 6: Compare both datasets
try:
    assert_frame_equal(
        df_first,
        df_second,
        check_dtype=True,
        check_exact=True
    )

    print("\nPASS: Both executions produced identical datasets.")

except AssertionError as error:
    print("\nFAIL: Dataset outputs are different.")
    print(error)
    raise

# Step 7: Final validation
print("\n--- Reproducibility Report ---")
print("Rows:", len(df_second))
print("Columns:", len(df_second.columns))
print("Missing values:", df_second.isnull().sum().sum())
print("Duplicate rows:", df_second.duplicated().sum())

print("\nReproducibility testing completed.")


