# backend/data/generate_data.py
import pandas as pd
import numpy as np

def generate_data(n_samples=1000):
    np.random.seed(42)
    data = {
        "season": np.random.choice([0, 1, 2, 3], n_samples),  # 0: Winter, 1: Spring, 2: Summer, 3: Fall
        "price": np.random.uniform(50, 150, n_samples),
        "promotions": np.random.uniform(0, 0.5, n_samples),
        "weather": np.random.uniform(10, 35, n_samples),
        "demand": np.zeros(n_samples)
    }
    df = pd.DataFrame(data)
    # Simulate demand (example formula)
    df["demand"] = (1000 + 200 * df["season"] - 5 * df["price"] + 500 * df["promotions"] + 10 * df["weather"] + np.random.normal(0, 50, n_samples))
    df.to_csv("demand_data.csv", index=False)
    return df

if __name__ == "__main__":
    generate_data()