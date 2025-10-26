import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="U.S Macro Economic Dashboard", layout="wide")

st.title("🇺🇸 U.S Macro Economic Dashboard")
st.write("Automatic updates — Official economic indicators")

# -------------------
# Fake data for preview (24 indicators)
# -------------------
data = {
    "Indicator": [
        "CPI (Consumer Price Index)", "Core CPI (MoM)", "PPI", "Core PPI (MoM)", "Unemployment Rate",
        "Non-Farm Payrolls", "Average Hourly Earnings", "Retail Sales (MoM)", "Core Retail Sales (MoM)",
        "ISM Manufacturing PMI", "ISM Services PMI", "ISM Manufacturing Prices", "JOLTS Job Openings",
        "Michigan Consumer Sentiment", "PCE", "Core PCE (MoM)", "GDP (QoQ)", "Durable Goods Orders",
        "Trade Balance", "Building Permits", "New Home Sales", "ADP Employment Change", "Industrial Production",
        "Participation Rate"
    ],
    "Latest Value": [
        3.4, 0.3, 2.1, 0.2, 3.7,
        150000, 0.4, -0.2, 0.3,
        51.2, 54.1, 49.8, 10450,
        65.1, 2.8, 0.2, 2.9, 1.1,
        -64.3, 1560, 620, 200000, 0.8, 62.1
    ],
    "Trend": [
        "Up","Up","Up","Down","Neutral",
        "Up","Up","Down","Up",
        "Up","Up","Down","Up",
        "Up","Up","Neutral","Up","Down",
        "Down","Up","Up","Up","Up","Neutral"
    ]
}

df = pd.DataFrame(data)

# Color rendering for Trend column
def color_trend(val):
    if val == "Up":
        return "background-color: red; color: white"
    elif val == "Down":
        return "background-color: green; color: white"
    return ""

# -------------------
# Display table
# -------------------
st.subheader("📊 Macro Economic Indicators")
st.dataframe(df.style.applymap(color_trend, subset=["Trend"]))

# -------------------
# Economic Quarter Analysis
# -------------------
st.subheader("📅 Current Economic Quarter")
st.success("🔥 Growth + Inflation (Stagflation)")

# -------------------
# Monetary Policy Suggestion
# -------------------
st.subheader("🏦 Monetary Policy Suggestion")
st.info("💹 Tightening → Possible Interest Rate Hike")

# -------------------
# Last update
# -------------------
st.markdown(f"🗓️ **Last Updated:** {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
