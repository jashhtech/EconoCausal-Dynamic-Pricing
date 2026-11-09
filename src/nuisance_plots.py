"""Week 4 Day 6: Evaluation plots for nuisance models and robustness."""
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    from src import nuisance_models as nm
    from src.treatment_model import propensity_scores
except ImportError:
    import nuisance_models as nm
    from treatment_model import propensity_scores

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

def plot_auc_comparison():
    csv_path = RESULTS_DIR / "model_comparison.csv"
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, y="model", x="auc", hue="target", palette="viridis")
    plt.title("Nuisance Models: ROC-AUC Comparison")
    plt.xlabel("ROC-AUC Score")
    plt.ylabel("Model Configuration")
    plt.xlim(0.65, 0.85)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "auc_comparison.png")
    plt.close()

def plot_propensity_overlap(scores, t):
    plt.figure(figsize=(8, 5))
    sns.histplot(scores[t == 1], color="blue", label="Treated (Exposure=1)", kde=True, stat="density", alpha=0.5, bins=30)
    sns.histplot(scores[t == 0], color="red", label="Untreated (Exposure=0)", kde=True, stat="density", alpha=0.5, bins=30)
    plt.title("Propensity Score Overlap")
    plt.xlabel("Predicted Probability of Treatment")
    plt.ylabel("Density")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "propensity_overlap.png")
    plt.close()

def plot_robustness_forest():
    csv_path = RESULTS_DIR / "robustness_check.csv"
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(8, 4))
    xerr = [df["estimate"] - df["ci_low"], df["ci_high"] - df["estimate"]]
    plt.errorbar(df["estimate"], df.index, xerr=xerr, fmt='o', color='black', capsize=5)
    plt.yticks(df.index, df["specification"])
    plt.axvline(0, color='red', linestyle='--')
    plt.title("Robustness Checks: Partialling-out Estimates")
    plt.xlabel("Estimated Effect")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "robustness_forest_plot.png")
    plt.close()

if __name__ == "__main__":
    print("Generating Week 4 evaluation plots...")
    plot_auc_comparison()
    
    print("Calculating propensity scores for overlap plot...")
    df_data = pd.read_csv(nm.DATA_PATH)
    scores = propensity_scores(df_data)
    plot_propensity_overlap(scores, df_data[nm.TREATMENT])
    
    plot_robustness_forest()
    print(f"Success! Plots saved in: {RESULTS_DIR}")