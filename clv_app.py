import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go 
import requests

# --- 1. Load the Machine Learning Model ---
@st.cache_resource
def load_model():
    return joblib.load('rf_clv_nlp_model.pkl')

model = load_model()

# --- 2. Currency Logic ---
def get_live_exchange_rate():
    try:
        response = requests.get("https://api.frankfurter.app/latest?from=USD&to=INR")
        return response.json()['rates']['INR']
    except:
        return 83.0  # Fallback rate
    
# --- 3. Build the Web App UI ---
st.set_page_config(page_title="CLV Predictor", page_icon="🛍️")
st.title("🛍️ E-Commerce CLV Predictor")
st.write("Adjust the customer's behavior below to predict how much revenue they will generate in the next 6 months.")

# Sidebar setup
st.sidebar.header("Global Settings")
currency_choice = st.sidebar.selectbox("Select Currency", ["USD ($)", "INR (₹)"])

# Dynamic Rate Handling
if currency_choice == "INR (₹)":
    rate = get_live_exchange_rate()
    symbol = "₹"
    st.sidebar.caption(f"Live Rate: 1 USD = ₹{rate:.2f}")
else:
    rate = 1.0
    symbol = "$"

st.sidebar.divider()
st.sidebar.header("Customer Behavior") # Fixed missing parenthesis here

# Recency
st.sidebar.markdown("**1. Recency (Days since last purchase)**")
recency_text = st.sidebar.number_input("Type Days:", min_value=1, max_value=365, value=15)
recency = st.sidebar.slider("Or slide:", min_value=1, max_value=365, value=int(recency_text), label_visibility="collapsed")

# Frequency
st.sidebar.markdown("**2. Frequency (Total number of orders)**")
freq_text = st.sidebar.number_input("Type Orders:", min_value=1, max_value=20, value=2)
frequency = st.sidebar.slider("Or slide:", min_value=1, max_value=50, value=int(freq_text), label_visibility="collapsed")

# Monetary (Dynamic for USD/INR)
st.sidebar.markdown(f"**3. Monetary (Total spend in {symbol})**")
mon_text = st.sidebar.number_input(
    f"Type Spend ({symbol}):", 
    min_value=1.0 * rate, 
    max_value=10000.0 * rate, 
    value=150.0 * rate,
    step=10.0 * rate
)
monetary_val = st.sidebar.slider(
    "Or slide:", 
    min_value=1.0 * rate, 
    max_value=10000.0 * rate, 
    value=float(mon_text), 
    label_visibility="collapsed"
)
# Convert back to USD for the model
mon_usd = monetary_val / rate

# NLP Sentiment
st.sidebar.markdown("**4. Customer Satisfaction (1 = Angry, 5 = Happy)**")
nlp_text = st.sidebar.number_input("Type Score:", min_value=1.0, max_value=5.0, value=3.0, step=0.5)
nlp_score = st.sidebar.slider("Or slide:", min_value=1.0, max_value=5.0, value=float(nlp_text), step=0.5, label_visibility="collapsed")

# --- 4. Make the Prediction ---
if st.button("Predict Future Lifetime Value"):
    # Create dataframe (Ensure these column names match your trained model exactly)
    input_data = pd.DataFrame({
        'Recency': [recency],
        'Frequency': [frequency],
        'Monetary': [mon_usd], # Fixed: use the USD version for the model
        'NLP_Sentiment_Score': [nlp_score] 
    })
    
    # Pass the data to the model
    prediction_usd = model.predict(input_data)[0]
    pred_final = prediction_usd * rate
    
    # Display the result
    st.subheader(f"Predicted Value: {symbol}{pred_final:,.2f}")
    
    
    # Business Logic Tiers (Tucked inside the button click)
    if prediction_usd >= 200:
        st.balloons()
        st.success("🌟 **VIP Customer!** High future value. Offer white-glove treatment.")
    elif prediction_usd >= 100:
        st.info("📈 **Potential Loyalist.** Strong growth potential. Target with cross-sell campaigns.")
    elif prediction_usd >= 50:
        st.warning("🤝 **Steady Customer.** Moderate value. Keep engaged with regular newsletters.")
    elif prediction_usd >= 20:
        st.error("📉 **At-Risk Customer.** Value is dropping. Send a personalized win-back coupon.")
    else:
        st.error("⚠️ **High Churn Risk.** Predicted spend is nearly zero. Send a final automated win-back email.")
        
    # Upgrade to Solid, Explicit Gauge Chart with Labels
    max_range = 300 * rate 
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = pred_final,
        number = {'prefix': symbol, 'font': {'size': 55, 'color': "white", 'family': "Arial-Bold"}},
        title = {'text': "Customer Value Breakdown", 'font': {'size': 26, 'color': "white"}},
        gauge = {
            'axis': {'range': [0, max_range], 'tickwidth': 1, 'tickcolor': "white", 'tickfont': {'color': "white"}},
            'bar': {'color': "#131341", 'thickness': 0.30}, # Sleek white needle for dark theme
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, max_range*0.2], 'color': "#E74C3C"},
                {'range': [max_range*0.2, max_range*0.4], 'color': "#E67E22"}, 
                {'range': [max_range*0.4, max_range*0.6], 'color': "#F1C40F"}, 
                {'range': [max_range*0.6, max_range*0.8], 'color': "#2ECC71"}, 
                {'range': [max_range*0.8, max_range], 'color': "#27AE60"} 
            ],
        }
    ))

    # Precision placement for labels along the arch
    labels = [
        {"x": 0.16, "y": 0.30, "text": "CHURN"},
        {"x": 0.28, "y": 0.58, "text": "AT-RISK"},
        {"x": 0.50, "y": 0.70, "text": "STEADY"},
        {"x": 0.72, "y": 0.58, "text": "LOYALIST"},
        {"x": 0.83, "y": 0.30, "text": "VIP"}
    ]

    for label in labels:
        fig.add_annotation(
            x=label["x"], y=label["y"],
            xref="paper", yref="paper",
            text=f"{label['text']}", 
            showarrow=False,
            font=dict(size=12, color="white", family="Arial Black") # Forced white and larger
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=80, b=40),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
