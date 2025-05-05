from sklearn.preprocessing import StandardScaler
import pandas as pd

def preprocess_data(file_path):
    df = pd.read_csv(file_path, encoding='latin1')
    # Filter complete orders
    df = df[df['Order Status'] == 'COMPLETE']
    # Extract seasonality
    df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
    df['season'] = df['order date (DateOrders)'].dt.month % 12 // 3  # 0: Winter, 1: Spring, etc.
    # Select features
    X = df[['season', 'Sales', 'Order Item Discount', 'Days for shipping (real)']]
    y = df['Order Item Quantity']
    # Handle missing values
    X = X.fillna(X.mean())
    y = y.fillna(y.mean())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, scaler, X.columns

if __name__ == "__main__":
    X, y, scaler, feature_names = preprocess_data("data/DataCoSupplyChainDataset.csv")
    print("Feature Names:", feature_names)
    print("X Shape:", X.shape)
    print("y Shape:", y.shape)