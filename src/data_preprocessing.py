from pathlib import Path
import runpy


# Get the project root directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Locate the existing preprocessing script
PREPROCESSING_SCRIPT = PROJECT_DIR / "data" / "prepare_dataset.py"


def main():
    """Run the existing dataset preprocessing script."""

    if not PREPROCESSING_SCRIPT.exists():
        raise FileNotFoundError(
            f"Preprocessing script not found: {PREPROCESSING_SCRIPT}"
        )

    print("Starting dataset preprocessing...")

    runpy.run_path(
        str(PREPROCESSING_SCRIPT),
        run_name="__main__"
    )

    print("Dataset preprocessing completed successfully.")


if __name__ == "__main__":
    main()