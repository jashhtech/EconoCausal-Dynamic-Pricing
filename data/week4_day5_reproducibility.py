import pandas as pd
import subprocess
import sys
import hashlib
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

PREPARE_SCRIPT = DATA_DIR / "prepare_dataset.py"
DATASET_FILE = DATA_DIR / "retail_data.csv"
REPORT_FILE = DATA_DIR / "week4_day5_reproducibility_report.csv"

if not PREPARE_SCRIPT.exists():
    raise FileNotFoundError(f"Preparation script not found: {PREPARE_SCRIPT}")

if not DATASET_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET_FILE}")


def calculate_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def run_preparation():
    """Run the dataset preparation script."""
    result = subprocess.run(
        [sys.executable, str(PREPARE_SCRIPT)],
        cwd=str(PROJECT_DIR),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("Dataset preparation failed.")

    print(result.stdout)


print("WEEK 4 - DAY 5 REPRODUCIBILITY TEST")
print("-" * 50)

# First execution
print("\nFirst execution:")
run_preparation()

first_hash = calculate_hash(DATASET_FILE)
first_df = pd.read_csv(DATASET_FILE)

# Second execution
print("\nSecond execution:")
run_preparation()

second_hash = calculate_hash(DATASET_FILE)
second_df = pd.read_csv(DATASET_FILE)

# Compare results
same_hash = first_hash == second_hash
same_shape = first_df.shape == second_df.shape
same_data = first_df.equals(second_df)

results = [
    {
        "test": "SHA256 file comparison",
        "status": "PASS" if same_hash else "FAIL",
        "details": "Both dataset files have identical hashes."
        if same_hash else "Dataset hashes are different."
    },
    {
        "test": "Dataset shape comparison",
        "status": "PASS" if same_shape else "FAIL",
        "details": f"First: {first_df.shape}, Second: {second_df.shape}"
    },
    {
        "test": "Dataset content comparison",
        "status": "PASS" if same_data else "FAIL",
        "details": "Both datasets contain identical values."
        if same_data else "Dataset contents are different."
    }
]

report = pd.DataFrame(results)
report.to_csv(REPORT_FILE, index=False)

print("\nREPRODUCIBILITY RESULTS")
print(report.to_string(index=False))

print("\nReport saved to:", REPORT_FILE)

if (report["status"] == "PASS").all():
    print("\nRESULT: Dataset preparation is reproducible.")
else:
    print("\nRESULT: Reproducibility issues detected.")
    print("Investigate failed tests before proceeding.")
    