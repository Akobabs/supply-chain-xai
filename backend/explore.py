import pandas as pd

# Load the dataset
df = pd.read_csv("data/DataCoSupplyChainDataset.csv", encoding='latin1')  # encoding='latin1' to handle potential special characters
print("Columns:", df.columns.tolist())
print("\nHead:\n", df.head())
print("\nMissing Values:\n", df[[
    'order date (DateOrders)', 
    'Sales', 
    'Order Item Discount', 
    'Days for shipping (real)', 
    'Order Item Quantity'
]].isnull().sum())
print("\nOrder Status Values:", df['Order Status'].unique())
print("\nData Types:\n", df.dtypes)