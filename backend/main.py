# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import xgboost as xgb
import shap
import pandas as pd
import numpy as np
from preprocess import preprocess_data

app = FastAPI()
model = xgb.XGBRegressor()
model.load_model("demand_model.json")

class DemandInput(BaseModel):
    season: int
    Sales: float
    Order_Item_Discount: float
    Days_for_shipping_real: float

@app.post("/predict/demand")
async def predict_demand(input: DemandInput):
    input_data = pd.DataFrame([{
        'season': input.season,
        'Sales': input.Sales,
        'Order Item Discount': input.Order_Item_Discount,
        'Days for shipping (real)': input.Days_for_shipping_real
    }])
    X = input_data[['season', 'Sales', 'Order Item Discount', 'Days for shipping (real)']]
    _, _, scaler, feature_names = preprocess_data("data/DataCoSupplyChainDataset.csv")
    X_scaled = scaler.transform(X)
    forecast = model.predict(X_scaled)[0]
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_scaled)
    shap_output = [
        {"feature": feature_names[i], "value": float(shap_values[0][i])}
        for i in range(len(feature_names))
    ]
    # Bias check
    if max(abs(shap_values[0])) / sum(abs(shap_values[0])) > 0.7:
        return {
            "forecast": float(forecast),
            "shap_values": shap_output,
            "warning": "Potential bias: Single feature dominates prediction"
        }
    return {"forecast": float(forecast), "shap_values": shap_output}