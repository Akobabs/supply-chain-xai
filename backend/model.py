import xgboost as xgb
from preprocess import preprocess_data

def train_model():
    X, y, scaler, _ = preprocess_data("data/DataCoSupplyChainDataset.csv")
    model = xgb.XGBRegressor(random_state=42)
    model.fit(X, y)
    model.save_model("demand_model.json")
    return model, scaler

if __name__ == "__main__":
    train_model()
    print("Model trained and saved as demand_model.json")