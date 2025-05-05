import streamlit as st
import requests
import plotly.express as px
import pandas as pd

st.title("Supply Chain XAI Dashboard")
st.header("Demand Forecasting")
st.info("All data is processed securely and complies with GDPR.")

st.subheader("Enter Parameters")
season = st.selectbox("Season", options=[0, 1, 2, 3], format_func=lambda x: ["Winter", "Spring", "Summer", "Fall"][x])
sales = st.number_input("Sales ($)", min_value=0.0, value=100.0, step=1.0)
order_item_discount = st.number_input("Order Item Discount ($)", min_value=0.0, value=10.0, step=1.0)
days_for_shipping = st.number_input("Days for Shipping", min_value=0.0, max_value=10.0, value=3.0, step=1.0)

if st.button("Predict Demand"):
    data = {
        "season": season,
        "Sales": sales,
        "Order_Item_Discount": order_item_discount,
        "Days_for_shipping_real": days_for_shipping
    }
    try:
        response = requests.post("http://localhost:8000/predict/demand", json=data)
        response.raise_for_status()
        result = response.json()
        st.success(f"Predicted Demand: {result['forecast']:.2f} units")
        if "warning" in result:
            st.warning(result["warning"])
        shap_df = pd.DataFrame(result["shap_values"])
        st.subheader("Key Factors Influencing Demand")
        fig = px.bar(shap_df, x="feature", y="value", title="Feature Importance (SHAP)", 
                     labels={"value": "SHAP Value", "feature": "Feature"})
        st.plotly_chart(fig)
    except requests.exceptions.RequestException as e:
        st.error(f"Error: Could not connect to backend. {e}")