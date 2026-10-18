from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "retail_data.csv"


def load_dataset(path=DATA_PATH):
    """Load the cleaned retail customer dataset."""
    if not Path(path).exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return pd.read_csv(path)


def main():
    df = load_dataset()

    print("Dataset loaded successfully.")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))


if __name__ == "__main__":
    main()
    
    