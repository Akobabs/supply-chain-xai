# backend/generate_dataset_snippet.py
import pandas as pd

# Load the dataset
df = pd.read_csv("data/DataCoSupplyChainDataset.csv", encoding='latin1')

# Filter for COMPLETE orders
df = df[df['Order Status'] == 'COMPLETE']

# Derive season from order date
df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
df['season'] = df['order date (DateOrders)'].dt.month % 12 // 3

# Select relevant columns
snippet = df[[
    'order date (DateOrders)', 
    'season', 
    'Sales', 
    'Order Item Discount', 
    'Days for shipping (real)', 
    'Order Item Quantity', 
    'Order Status'
]].head()

# Save to CSV for appendix
snippet.to_csv("data/dataset_snippet.csv", index=False)
print(snippet)