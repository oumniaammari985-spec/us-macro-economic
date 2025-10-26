import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="U.S Economic Dashboard", layout="wide")

st.title("🇺🇸 U.S Macro Economic Dashboard")
st.write("Automatic updates — Official economic indicators")

# -------------------
# Fake temporary data (only for design preview)
# -------------------
data = {
    "Indicator": [
        "CPI (Inflation)", "Core CPI (MoM)", "PPI", "Core PPI (MoM)", "Unemployment Rate",
        "NFP", "Average Hourly Earnings", "Retail Sales (MoM)", "ISM Manufacturing PMI",
        "GDP (QoQ)", "PCE", "Core PCE (MoM)", "Durable Goods Orders", "Trade Balance"
    ],
    "Latest Value": [
        3.4, 0.3, 2.1, 0.2, 3.7,
        150000, 0.4, -0.2, 51.2,
        2.9, 2.8, 0.2, 1.1, -64.3
    ],
    "Trend": ["Up", "Up", "Up", "Down", "Neutral", "Up", "Up", "Down", "Up", "Up", "Up", "Neutral", "Up", "Down"]
}

df = pd.DataFrame(data)

# Color rendering
def color_trend(val):
    if val == "Up":
        return "background-color: red; color: white"
    elif val == "Down":
        return "background-color: green; color: white"
    return ""

st.subheader("📊 Macro Economic Indicators")
st.dataframe(df)
st.dataframe(df.style.applymap(color_trend, subset=["Trend"]))

# Economic Quarter
st.subheader("📅 Current Economic Quarter")
st.success("🔥 Growth + Inflation (Stagflation)")

# Monetary Policy
st.subheader("🏦 Monetary Policy Suggestion")
st.info("💹 Tightening → Possible Interest Rate Hike")

# Last update
st.markdown(f"🗓️ **Last Updated:** {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
