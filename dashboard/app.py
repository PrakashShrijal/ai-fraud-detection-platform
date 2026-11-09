import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import subprocess
import sys
import os
import time

# ── Start FastAPI backend as a background process (once per container) ──────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

PID_FILE = "/tmp/backend.pid"

def _backend_running():
    """Check if the backend process is still alive."""
    if not os.path.exists(PID_FILE):
        return False
    try:
        pid = int(open(PID_FILE).read().strip())
        os.kill(pid, 0)   # signal 0 = existence check only, no actual signal
        return True
    except (ProcessLookupError, ValueError, OSError):
        return False

if not _backend_running():
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn",
         "backend.main:app",
         "--host", "0.0.0.0",
         "--port", "8000"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    with open(PID_FILE, "w") as f:
        f.write(str(proc.pid))
    time.sleep(4)   # Give the backend time to initialise
# ───────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="wide"
)

st.title("🚨 Real-Time Fraud Detection Dashboard")

# Auto Refresh Every 5 Seconds
st_autorefresh(interval=5000, key="dashboard_refresh")

# API URLs
TRANSACTION_API = "http://127.0.0.1:8000/transactions"
ANALYTICS_API   = "http://127.0.0.1:8000/analytics"

# Fetch Transactions
try:
    transactions_response = requests.get(TRANSACTION_API, timeout=5)
    transactions = transactions_response.json()
except Exception:
    st.warning("⏳ Backend is starting up, please wait a moment...")
    st.stop()

# Fetch Analytics
try:
    analytics_response = requests.get(ANALYTICS_API, timeout=5)
    analytics = analytics_response.json()
except Exception:
    st.warning("⏳ Backend is starting up, please wait a moment...")
    st.stop()

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