# Databricks notebook source
# MAGIC %md
# MAGIC # CSAI-382 – Instructor Demo Notebook: Model Refinement & Hyperparameter Tuning (STEDI)
# MAGIC 
# MAGIC **Week 5–6: Lab 5.5 – Model Refinement & Hyperparameter Tuning (Round 2)**
# MAGIC 
# MAGIC **Audience:** Instructors. Feel free to simplify or copy/paste sections for students.
# MAGIC 
# MAGIC **Learning goals for students (you will demo):**
# MAGIC - See how to reload a previously tuned model and transformed features.
# MAGIC - Practice a *refinement* hyperparameter search (smaller, smarter grid).
# MAGIC - Compare old vs new models and decide whether to keep or replace the best model.
# MAGIC - Model responsible AI thinking (fairness, stability, and documentation) during tuning.
# MAGIC 
# MAGIC **What this live demo shows:**
# MAGIC - Loading saved artifacts from `/dbfs/FileStore` or creating synthetic data if missing.
# MAGIC - Designing a narrower grid based on prior results (and SHAP insights).
# MAGIC - Running `GridSearchCV`, comparing metrics, and saving an updated best model when appropriate.
# MAGIC - Instructor talking points for ethics and gospel-oriented reflection.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Setup: Imports and Helper Functions
# MAGIC 
# MAGIC This section loads the libraries and helper functions. If STEDI files are missing, we create a small synthetic dataset so you can still run the demo.

# COMMAND ----------
import os
import joblib
import numpy as np
import pandas as pd

from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score

# Helper: load transformed data if present, otherwise create synthetic

def load_or_create_demo_data(random_state: int = 42):
    """Load transformed STEDI data from /dbfs/FileStore or create a small synthetic set."""
    base_path = "/dbfs/FileStore"
    X_train_path = os.path.join(base_path, "X_train_transformed.npy")
    X_test_path = os.path.join(base_path, "X_test_transformed.npy")
    y_train_path = os.path.join(base_path, "y_train.pkl")
    y_test_path = os.path.join(base_path, "y_test.pkl")

    try:
        X_train = np.load(X_train_path)
        X_test = np.load(X_test_path)
        y_train = joblib.load(y_train_path)
        y_test = joblib.load(y_test_path)
        print("Loaded transformed STEDI datasets from /dbfs/FileStore.")
    except FileNotFoundError:
        print("Files not found. Creating a small synthetic dataset for demo.")
        X, y = make_classification(
            n_samples=400,
            n_features=10,
            n_informative=6,
            n_redundant=2,
            n_classes=2,
            weights=[0.55, 0.45],
            random_state=random_state,
        )
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=random_state, stratify=y
        )
    return X_train, X_test, y_train, y_test


def safe_load_model(path: str, default_model):
    """Try to load a model; fall back to default_model if missing."""
    try:
        model = joblib.load(path)
        print(f"Loaded model from {path}")
        return model
    except Exception as exc:  # noqa: BLE001 (explicitly catching load errors for demo)
        print(f"Could not load {path}: {exc}\nUsing provided default model instead.")
        return default_model

# COMMAND ----------
# MAGIC %md
# MAGIC ## Section 1 – Loading the Existing Model & Data
# MAGIC 
# MAGIC In class you can show how to load the previously saved artifacts:
# MAGIC - `stedi_best_model.pkl`: model chosen after first tuning.
# MAGIC - `stedi_feature_pipeline.pkl`: preprocessing pipeline (encoders, scalers, etc.).
# MAGIC - `X_train_transformed.npy` / `X_test_transformed.npy`: transformed features.
# MAGIC - `y_train.pkl` / `y_test.pkl`: labels (e.g., fall risk category).
# MAGIC 
# MAGIC If these files are missing, this notebook will create synthetic data so the demo still runs.

# COMMAND ----------
# Load data (real or synthetic)
X_train, X_test, y_train, y_test = load_or_create_demo_data()

# Try to load the prior best model; fall back to a quick-fit RandomForest
best_model_path = "/dbfs/FileStore/stedi_best_model.pkl"
old_model = safe_load_model(best_model_path, RandomForestClassifier(random_state=42))

# If we loaded a fresh default model, fit it quickly so metrics make sense
if not hasattr(old_model, "feature_importances_") and isinstance(old_model, RandomForestClassifier):
    old_model.fit(X_train, y_train)

# Baseline performance
train_acc = accuracy_score(y_train, old_model.predict(X_train))
test_acc = accuracy_score(y_test, old_model.predict(X_test))

print(f"Loaded model type: {type(old_model)}")
print(f"Train accuracy: {train_acc:.3f}")
print(f"Test accuracy: {test_acc:.3f}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Section 2 – Quick Review: What We Learned From SHAP (Instructor Talking Points)
# MAGIC 
# MAGIC - SHAP tells us which features are most important for predictions.
# MAGIC - If SHAP shows strange or unfair behavior, we may need to adjust the model or data.
# MAGIC - We use SHAP insights to design a **smarter** hyperparameter search, not just guess.
# MAGIC 
# MAGIC **Questions to ask students:**
# MAGIC - Which features looked most important in your SHAP plot?
# MAGIC - Did any feature behave in a surprising or unfair way?
# MAGIC - What might that mean for our next tuning step?
# MAGIC - How could we simplify the model if some features add noise?

# COMMAND ----------
# MAGIC %md
# MAGIC ## Section 3 – Designing a Smarter Hyperparameter Grid
# MAGIC 
# MAGIC Refinement means **narrowing** the search instead of repeating a huge grid. We focus on promising regions based on:
# MAGIC - Initial performance (signs of overfitting or underfitting).
# MAGIC - SHAP insights about important or risky features.
# MAGIC - Runtime limits of the current cluster.
# MAGIC 
# MAGIC **Example grids:**
# MAGIC - **RandomForestClassifier:** explore tree depth and leaf sizes to control complexity.
# MAGIC - **LogisticRegression:** explore regularization strength to balance bias/variance.
# MAGIC 
# MAGIC **Key hyperparameters (plain language):**
# MAGIC - `n_estimators`: number of trees (more trees can capture more patterns but cost time).
# MAGIC - `max_depth`: how deep each tree can grow (None lets trees grow fully; risk of overfitting).
# MAGIC - `min_samples_leaf`: minimum samples in a leaf (higher values simplify the tree).
# MAGIC - `C` (LogReg): strength of regularization (higher C = less regularization).
# MAGIC - `penalty`, `solver`: how the optimizer handles regularization.

# COMMAND ----------
# Example parameter grids
rf_param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 10, 20],
    "min_samples_leaf": [1, 2, 4],
}

log_reg_param_grid = {
    "C": [0.1, 1, 5, 10],
    "penalty": ["l2"],
    "solver": ["lbfgs"],
}

# Instructor tip: Use Random Forest when you expect non-linear relationships; use Logistic Regression when you prefer simpler, more explainable boundaries.
# Instructor tip: If the cluster is slow, shrink these lists to 1–2 values each.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Section 4 – Running GridSearchCV (Live Demo)
# MAGIC 
# MAGIC `GridSearchCV` tries each parameter combination with cross-validation and returns the best settings.
# MAGIC 
# MAGIC **Pause points for class:**
# MAGIC - What happens if the grid is too big? (Long runtime, risk of overfitting to CV.)
# MAGIC - What if the scoring metric does not match the business goal? (We might pick the wrong model.)

# COMMAND ----------
# Run a refinement grid search for RandomForestClassifier
rf_model = RandomForestClassifier(random_state=42)
rf_grid_search = GridSearchCV(
    estimator=rf_model,
    param_grid=rf_param_grid,
    cv=3,
    scoring="accuracy",
    n_jobs=-1,
)

rf_grid_search.fit(X_train, y_train)

print("Best params:", rf_grid_search.best_params_)
print(f"Best CV accuracy: {rf_grid_search.best_score_:.3f}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Optional:** How to adapt for Logistic Regression (smaller, faster grid).

# COMMAND ----------
log_reg_grid_search = GridSearchCV(
    estimator=LogisticRegression(max_iter=300),
    param_grid=log_reg_param_grid,
    cv=3,
    scoring="accuracy",
    n_jobs=-1,
)

log_reg_grid_search.fit(X_train, y_train)

print("LogReg best params:", log_reg_grid_search.best_params_)
print(f"LogReg best CV accuracy: {log_reg_grid_search.best_score_:.3f}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Section 5 – Comparing Old vs New Models
# MAGIC 
# MAGIC We compare test accuracy for the prior best model vs the tuned model. Remind students that stability, fairness, and simplicity also matter—sometimes we keep the old model if improvements are tiny or noisy.

# COMMAND ----------
old_test_acc = accuracy_score(y_test, old_model.predict(X_test))
new_test_acc = accuracy_score(y_test, rf_grid_search.best_estimator_.predict(X_test))

comparison_df = pd.DataFrame(
    {
        "model": ["old_model", "tuned_model"],
        "test_accuracy": [old_test_acc, new_test_acc],
    }
)
print(comparison_df)

# Instructor tip: Ask students whether a small accuracy gain is worth extra complexity or potential fairness risks.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Section 6 – Saving the Updated Best Model Responsibly
# MAGIC 
# MAGIC Overwrite `stedi_best_model.pkl` **only** if the new model is clearly as good or better and still reasonable. Modeling good practice includes logging decisions (even briefly) and noting open questions.

# COMMAND ----------
if new_test_acc >= old_test_acc:
    print("New model is as good or better — saving as new best model.")
    joblib.dump(rf_grid_search.best_estimator_, "/dbfs/FileStore/stedi_best_model.pkl")
else:
    print("Old model performed better. Keeping the old model.")

# Instructor tip: Invite students to explain why they would or would not overwrite the file.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Section 7 – Ethics & Gospel-Oriented Reflection (Instructor Notes)
# MAGIC 
# MAGIC - Careless tuning that only chases accuracy can create **unfair** or **unsafe** models. Always ask: who might be harmed if errors concentrate in a specific group?
# MAGIC - Document limitations honestly. Integrity means being transparent about what the model can and cannot do.
# MAGIC - Accountability: we are responsible for how these tools affect real people. Invite students to think about stewardship.
# MAGIC - “By their fruits ye shall know them” — our models are known by their real-world impact, not just their scores.
# MAGIC 
# MAGIC **Prompt for a 5-minute discussion:**
# MAGIC - Who benefits and who might be at risk from this fall-risk model?
# MAGIC - If SHAP shows a feature behaving unfairly, what could we change in data or modeling?
# MAGIC - How can we check that improvements are stable across different slices of the data?

# COMMAND ----------
# MAGIC %md
# MAGIC ## Section 8 – Instructor Checklist for Live Demo
# MAGIC 
# MAGIC - ✅ Cluster is started and has enough workers.
# MAGIC - ✅ Paths to `/dbfs/FileStore/...` are correct.
# MAGIC - ✅ Synthetic demo data works if files are missing.
# MAGIC - ✅ Example grids are small enough for the current cluster.
# MAGIC - ✅ Key talking points:
# MAGIC   - What refinement means (narrower, smarter search).
# MAGIC   - How to interpret `best_params_` and `best_score_`.
# MAGIC   - Why we compare old vs new models before saving.
# MAGIC   - How ethics connect to model selection and deployment.
