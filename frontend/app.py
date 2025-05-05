# frontend/app.py
import streamlit as st
import requests
import plotly.express as px
import pandas as pd

# Set the page layout to wide for better use of space
st.set_page_config(layout="wide")

# Title and introduction for the webpage
st.title("📦 Supply Chain Demand Predictor")
st.markdown("""
Welcome to our Supply Chain Demand Predictor! This tool helps predict how many products a company will sell (demand) and explains why. It’s designed to help supply chain managers make better decisions, like ordering the right amount of stock. Try it out below!
""")

# Sidebar with instructions and additional info
st.sidebar.header("How to Use This Tool")
st.sidebar.markdown("""
1. **Choose a Mode:** Use "Demo Mode" for a quick example, or "Manual Input" to enter your own values.
2. **Enter Details:** Input information like sales amount, discount, and shipping days.
3. **Click Predict:** See the predicted demand and a chart explaining the key factors.
4. **Understand the Results:** The chart shows why the prediction was made (e.g., "Discounts increased demand").
""")
st.sidebar.info("Built for an undergraduate project to make AI transparent and useful in supply chains!")

# Option to switch between demo mode (for presentation) and manual input
st.subheader("Step 1: Choose Your Mode")
mode = st.radio("Would you like to try a demo or enter your own values?", ["Demo (Pre-filled Values)", "Manual Input"])

# Default values for demo mode
if mode == "Demo (Pre-filled Values)":
    # Pre-filled values for demo (Spring, $100 sales, $10 discount, 3 days shipping)
    season = 1
    sales = 100.0
    order_item_discount = 10.0
    days_for_shipping = 3.0
    st.markdown("### Step 2: Demo Values (Spring Season Example)")
    st.write("Here’s an example scenario:")
    st.write(f"- **Season:** Spring (1)")
    st.write(f"- **Sales Amount:** $100")
    st.write(f"- **Discount on Order:** $10")
    st.write(f"- **Shipping Days:** 3 days")
else:
    # Manual input section with descriptive labels and tooltips
    st.subheader("Step 2: Enter Your Details")
    st.markdown("Fill in the details below to predict demand. Hover over the ❓ for help!")
    
    # Season selection with a tooltip
    season = st.selectbox(
        "Season ❓", 
        options=[0, 1, 2, 3], 
        format_func=lambda x: ["Winter", "Spring", "Summer", "Fall"][x],
        help="Choose the season for your sales. For example, demand might be higher in Winter for holiday shopping."
    )
    
    # Sales input with a tooltip
    sales = st.number_input(
        "Sales Amount ($) ❓", 
        min_value=0.0, 
        value=100.0, 
        step=1.0,
        help="Enter the total sales amount for the order. For example, $100 means the customer spent $100."
    )
    
    # Discount input with a tooltip
    order_item_discount = st.number_input(
        "Discount on Order ($) ❓", 
        min_value=0.0, 
        value=10.0, 
        step=1.0,
        help="Enter the discount given on the order. Discounts often increase demand. For example, a $10 discount might attract more buyers."
    )
    
    # Shipping days input with a tooltip
    days_for_shipping = st.number_input(
        "Days for Shipping ❓", 
        min_value=0.0, 
        max_value=10.0, 
        value=3.0, 
        step=1.0,
        help="Enter how many days it takes to ship the order. Faster shipping might increase demand."
    )

# Button to make a prediction
st.subheader("Step 3: Get Your Prediction")
if st.button("Predict Demand 🚀"):
    # Send the user's input to the backend
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
        
        # Show the predicted demand in a highlighted box
        st.markdown("### Prediction Result")
        st.success(f"**Predicted Demand:** {result['forecast']:.2f} units")
        
        # Show any warnings (e.g., if the AI is biased)
        if "warning" in result:
            st.warning(result["warning"])
        
        # Show a chart explaining why the AI made this prediction
        st.markdown("### Why This Prediction? (Explanation)")
        st.write("The chart below shows the key factors affecting the predicted demand. Larger bars mean that factor had a bigger impact.")
        shap_df = pd.DataFrame(result["shap_values"])
        
        # Customize the chart for better readability
        fig = px.bar(
            shap_df, 
            x="feature", 
            y="value", 
            title="Key Factors Influencing Demand",
            labels={"value": "Impact on Prediction", "feature": "Factor"},
            color="value",  # Color bars based on impact
            color_continuous_scale="Blues"  # Use a blue gradient for clarity
        )
        fig.update_layout(
            title_font_size=20,
            xaxis_title_font_size=16,
            yaxis_title_font_size=16,
            xaxis_tickangle=45  # Rotate labels for readability
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary of results for better understanding
        st.markdown("### Summary")
        top_factor = shap_df.loc[shap_df['value'].abs().idxmax()]['feature']
        top_impact = shap_df['value'].abs().max()
        st.write(f"The biggest factor affecting demand is **{top_factor}**, with an impact of {top_impact:.2f}.")
        st.write("This means the AI thinks this factor is the main reason for the predicted demand.")
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error: Could not connect to backend. Make sure the backend is running! ({e})")

# Footer with project info
st.markdown("---")
st.markdown("**Built for an Undergraduate Project** | Submitted to Benson Idahosa University, Edo State | Using DataCo SMART SUPPLY CHAIN Dataset | Making AI Transparent and Useful!")