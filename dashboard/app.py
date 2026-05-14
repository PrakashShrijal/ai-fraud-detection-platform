import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="wide"
)

st.title("🚨 Real-Time Fraud Detection Dashboard")

# Auto Refresh Every 5 Seconds
st_autorefresh(interval=5000, key="dashboard_refresh")

# API URLs
TRANSACTION_API = "http://127.0.0.1:8000/transactions"
ANALYTICS_API = "http://127.0.0.1:8000/analytics"

# Fetch Transactions
transactions_response = requests.get(TRANSACTION_API)

transactions = transactions_response.json()

# Fetch Analytics
analytics_response = requests.get(ANALYTICS_API)

analytics = analytics_response.json()

# Analytics Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Transactions",
    analytics["total_transactions"]
)

col2.metric(
    "High Risk Transactions",
    analytics["high_risk_transactions"]
)

col3.metric(
    "Anomaly Transactions",
    analytics["anomaly_transactions"]
)

col4.metric(
    "Fraud Percentage",
    f"{analytics['fraud_percentage']}%"
)

df = pd.DataFrame(transactions)

# Live Fraud Alerts
st.subheader("🚨 Live Fraud Alerts")

high_risk_df = df[df["risk_level"] == "HIGH"]

if not high_risk_df.empty:

    latest_alert = high_risk_df.iloc[-1]

    st.error(f"""
    HIGH RISK TRANSACTION DETECTED

    Amount: ₹{latest_alert['amount']}
    Hour: {latest_alert['hour']}
    ML Prediction: {latest_alert['ml_prediction']}
    """)

else:
    st.success("No high-risk transactions detected.")

st.divider()

# Transactions Table
st.subheader("📄 Transaction History")



st.dataframe(df, use_container_width=True)

# Risk Level Chart
st.subheader("📊 Risk Distribution")

risk_counts = df["risk_level"].value_counts()

risk_chart = px.pie(
    names=risk_counts.index,
    values=risk_counts.values,
    title="Risk Level Distribution"
)

st.plotly_chart(risk_chart, use_container_width=True)

# ML Prediction Chart
st.subheader("🤖 ML Prediction Distribution")

ml_counts = df["ml_prediction"].value_counts()

ml_chart = px.bar(
    x=ml_counts.index,
    y=ml_counts.values,
    title="ML Anomaly Detection"
)

st.plotly_chart(ml_chart, use_container_width=True)