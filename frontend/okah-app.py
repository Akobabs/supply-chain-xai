import streamlit as st
import requests
import plotly.express as px
import pandas as pd

# Set page configuration
st.set_page_config(layout="centered", page_title="Demand Forecast Hub")

# Custom CSS for modern card-based design
st.markdown("""
<style>
    .card {
        background-color: #f9fafb;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header {
        background-color: #1e3a8a;
        color: white;
        padding: 20px;
        border-radius: 10px 10px 0 0;
        text-align: center;
    }
    .predict-button {
        background-color: #22c55e;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    .predict-button:hover {
        background-color: #16a34a;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header"><h1>📊 Demand Forecast Hub</h1><p>Predict product demand with AI-powered insights for smarter supply chain decisions.</p></div>', unsafe_allow_html=True)

# Introduction card
st.markdown("""
<div class="card">
    <h3>Welcome to Demand Forecast Hub</h3>
    <p>Use this tool to predict product demand based on key factors like season, sales, discounts, and shipping time. Choose between a quick demo or custom inputs to see predictions and understand the driving factors!</p>
</div>
""", unsafe_allow_html=True)

# Mode selection card
st.markdown('<div class="card"><h3>1. Select Mode</h3>', unsafe_allow_html=True)
mode = st.radio("", ["Quick Demo", "Custom Input"], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# Input card
st.markdown('<div class="card"><h3>2. Input Details</h3>', unsafe_allow_html=True)
if mode == "Quick Demo":
    season = 1
    sales = 100.0
    order_item_discount = 10.0
    days_for_shipping = 3.0
    st.write("**Demo Scenario (Spring)**")
    st.write(f"Season: Spring | Sales: $100 | Discount: $10 | Shipping: 3 days")
else:
    col1, col2 = st.columns(2)
    with col1:
        season = st.selectbox("Season", options=[0, 1, 2, 3], format_func=lambda x: ["Winter", "Spring", "Summer", "Fall"][x], help="Select the season for your sales.")
        sales = st.number_input("Sales Amount ($)", min_value=0.0, value=100.0, step=1.0, help="Total sales amount for the order.")
    with col2:
        order_item_discount = st.number_input("Discount ($)", min_value=0.0, value=10.0, step=1.0, help="Discount applied to the order.")
        days_for_shipping = st.number_input("Shipping Days", min_value=0.0, max_value=10.0, value=3.0, step=1.0, help="Days taken for shipping.")
st.markdown('</div>', unsafe_allow_html=True)

# Prediction button and results
st.markdown('<div class="card"><h3>3. Get Prediction</h3>', unsafe_allow_html=True)
if st.button("Predict Now", key="predict", help="Click to generate demand prediction"):
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
        
        # Display prediction
        st.markdown(f'<p><strong>Predicted Demand:</strong> {result["forecast"]:.2f} units</p>', unsafe_allow_html=True)
        
        # Display warnings if any
        if "warning" in result:
            st.warning(result["warning"])
        
        # Explanation chart
        st.markdown('<h4>Why This Prediction?</h4><p>The chart below shows the factors driving the demand prediction.</p>', unsafe_allow_html=True)
        shap_df = pd.DataFrame(result["shap_values"])
        fig = px.bar(
            shap_df, 
            x="value", 
            y="feature", 
            orientation='h',
            title="Factors Influencing Demand",
            labels={"value": "Impact", "feature": "Factor"},
            color="value",
            color_continuous_scale="Viridis"
        )
        fig.update_layout(title_font_size=18, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary
        top_factor = shap_df.loc[shap_df['value'].abs().idxmax()]['feature']
        top_impact = shap_df['value'].abs().max()
        st.markdown(f'<p><strong>Key Factor:</strong> {top_factor} (Impact: {top_impact:.2f})</p>', unsafe_allow_html=True)
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error: Could not connect to backend. Ensure backend is running! ({e})")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="card"><p><strong>Undergraduate Project</strong> | Benson Idahosa University </p></div>', unsafe_allow_html=True)