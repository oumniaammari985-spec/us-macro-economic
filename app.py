import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="U.S Economic Dashboard", layout="wide")

st.title("🇺🇸 U.S Macro Economic Dashboard")
st.write("Automatic updates — Official economic indicators")

# -------------------
# Fake temporary data for indicators
# -------------------
data = {
    "Indicator": [
        "CPI (Inflation)", "Core CPI (MoM)", "PPI", "Core PPI (MoM)", "Unemployment Rate",
        "NFP", "Average Hourly Earnings", "Retail Sales (MoM)", "Core Retail Sales (MoM)",
        "ISM Manufacturing PMI", "ISM Services PMI", "ISM Manufacturing Prices",
        "JOLTS Job Openings", "Michigan Consumer Sentiment", "PCE", "Core PCE (MoM)",
        "GDP (QoQ)", "Durable Goods Orders", "Trade Balance", "Building Permits",
        "New Home Sales", "ADP Employment", "Industrial Production", "Participation Rate"
    ],
    "Latest Value": [
        3.4, 0.3, 2.1, 0.2, 3.7,
        150000, 0.4, -0.2, 0.1,
        51.2, 54.1, 50.5,
        8.9, 62.3, 2.8, 0.2,
        2.9, 1.1, -64.3, 1234,
        730, 205000, 0.3, 62.1
    ],
    "Trend": ["Up", "Up", "Up", "Down", "Neutral", "Up", "Up", "Down", "Up",
              "Up", "Up", "Neutral", "Up", "Neutral", "Up", "Down",
              "Up", "Down", "Down", "Up", "Down", "Up", "Neutral", "Neutral"]
}

df = pd.DataFrame(data)

# -------------------
# Color Trend
# -------------------
def color_trend(val):
    if val == "Up":
        return "background-color: red; color: white"
    elif val == "Down":
        return "background-color: green; color: white"
    return ""

st.subheader("📊 Macro Economic Indicators")
st.dataframe(df.style.applymap(color_trend, subset=["Trend"]))

# -------------------
# Economic Quarter & Monetary Policy
# -------------------
quarter_data = {
    "Current Quarter": ["Q4 2025"],
    "Status": ["🔥 Growth + Inflation (Stagflation)"],
    "Monetary Policy": ["💹 Tightening → Possible Interest Rate Hike"]
}

df_quarter = pd.DataFrame(quarter_data)

st.subheader("📅 Current Economic Quarter & Monetary Policy")
st.table(df_quarter)  # <-- عرض جدولي منظم وألوان نقدر نزيدها لاحقاً

# -------------------
# Last update
# -------------------
st.markdown(f"🗓️ **Last Updated:** {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
