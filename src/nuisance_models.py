"""
EconoCausal - Week 2: Nuisance models (Double ML ka pehla hissa).

Do models chahiye:
    outcome model   : Y ~ X   (campaign_response ko confounders se predict karo)
    treatment model : T ~ X   (campaign_exposure ko confounders se predict karo)

Yahan hum alag-alag model types compare karte hain (cross-validation se),
taaki docs/model_selection.md mein sahi model chunne ka reason likh sakein.

NOTE: treatment/outcome/confounders abhi CANDIDATE hain, Jaswanth se confirm hone baad badal sakte hain.
Leakage se bachne ke liye Response, campaign_response aur AcceptedCmp1-5 confounders mein NAHI hain.

Chalane ka tareeka (repo root se):
    python src/nuisance_models.py
"""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_PATH = "data/retail_data.csv"
TREATMENT = "campaign_exposure"
OUTCOME = "campaign_response"
NUMERIC = ["age", "Income", "Kidhome", "Teenhome", "Recency",
           "total_purchase_amount", "total_purchases"]
CATEGORICAL = ["Education", "Marital_Status"]
SEED = 42


def make_preprocessor():
    return ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])


def candidate_models():
    return {
        "logistic": LogisticRegression(max_iter=1000),
        "random_forest": RandomForestClassifier(
            n_estimators=200, min_samples_leaf=5, random_state=SEED, n_jobs=-1),
        "grad_boosting": GradientBoostingClassifier(random_state=SEED),
    }


def evaluate(df, target):
    """Har model ke liye 5-fold cross-validated AUC aur log loss nikalo."""
    X, y = df[NUMERIC + CATEGORICAL], df[target]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    rows = []
    for name, model in candidate_models().items():
        pipe = make_pipeline(make_preprocessor(), model)
        p = cross_val_predict(pipe, X, y, cv=cv, method="predict_proba")[:, 1]
        rows.append({"target": target, "model": name,
                     "auc": round(roc_auc_score(y, p), 4),
                     "log_loss": round(log_loss(y, p), 4)})
    return rows


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    results = evaluate(df, OUTCOME) + evaluate(df, TREATMENT)
    print(pd.DataFrame(results).to_string(index=False))