import shap
import xgboost as xgb
import pandas as pd
import numpy as np
from preprocess import preprocess_data

# Load data and model
X, y, scaler, feature_names = preprocess_data("data/DataCoSupplyChainDataset.csv")
model = xgb.XGBRegressor()
model.load_model("demand_model.json")

# Use a small subset of data for SHAP analysis
X_subset = X[:10]  # First 10 samples
y_subset = y[:10]

# Compute SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_subset)

# Print SHAP explanations for the first few predictions
print("SHAP Explanations for First 5 Predictions:")
for i in range(5):
    print(f"\nPrediction {i+1}:")
    print(f"Actual Demand: {y_subset.iloc[i]:.2f} units")
    print(f"Predicted Demand: {model.predict(X_subset[i:i+1])[0]:.2f} units")
    print("Key Factors (SHAP Values):")
    for feature, value in zip(feature_names, shap_values[i]):
        print(f"- {feature}: {value:.2f}")