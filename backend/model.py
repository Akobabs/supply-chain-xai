# backend/model.py
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from preprocess import preprocess_data

def train_and_evaluate_model():
    # Load and prepare the data
    X, y, scaler, feature_names = preprocess_data("data/DataCoSupplyChainDataset.csv")
    
    # Split data into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model on the training set
    model = xgb.XGBRegressor(random_state=42)
    model.fit(X_train, y_train)
    
    # Save the model
    model.save_model("demand_model.json")
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Calculate accuracy metrics
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Print evaluation results
    print(f"Model Evaluation Results:")
    print(f"- Mean Absolute Error (MAE): {mae:.2f} units")
    print(f"- R-squared (R²): {r2:.2f}")
    
    return model, scaler, X_test, y_test, y_pred, feature_names

if __name__ == "__main__":
    model, scaler, X_test, y_test, y_pred, feature_names = train_and_evaluate_model()