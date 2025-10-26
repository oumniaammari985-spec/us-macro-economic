import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="U.S Macro Economic Dashboard", layout="wide")
st.title("🇺🇸 U.S Macro Economic Dashboard")
st.markdown(f"### 🗓️ Last Updated: {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")

# -------------------
# مؤشرات اقتصادية (قيم مؤقتة)
# -------------------
data = {
    "Indicator": [
        "CPI (Consumer Price Index)", "Core CPI (MoM)", "PPI", "Core PPI (MoM)",
        "Unemployment Rate", "NFP", "Average Hourly Earnings", "Retail Sales (MoM)",
        "Core Retail Sales (MoM)", "ISM Manufacturing PMI", "ISM Services PMI",
        "ISM Manufacturing Prices", "JOLTS Job Openings", "Michigan Consumer Sentiment",
        "PCE", "Core PCE (MoM)", "GDP (QoQ)", "Durable Goods Orders", "Trade Balance",
        "Building Permits", "New Home Sales", "ADP Employment Change",
        "Industrial Production", "Participation Rate"
    ],
    "Latest Value": [
        3.4, 0.3, 2.1, 0.2,
        3.7, 150000, 0.4, -0.2,
        0.1, 51.2, 55.3, 49.8,
        10200, 67.5, 2.8, 0.2,
        2.9, 1.1, -64.3, 1800,
        820, 200000, 0.3, 62.1
    ],
    "Trend": [
        "Up", "Up", "Up", "Down",
        "Neutral", "Up", "Up", "Down",
        "Up", "Up", "Up", "Down",
        "Up", "Up", "Up", "Neutral",
        "Up", "Up", "Down", "Up",
        "Down", "Up", "Up", "Neutral"
    ]
}

df = pd.DataFrame(data)

# لون الاتجاه
def color_trend(val):
    if val == "Up":
        return "background-color: red; color: white; font-weight: bold"
    elif val == "Down":
        return "background-color: green; color: white; font-weight: bold"
    return "background-color: gray; color: white; font-weight: bold"

# -------------------
# جدول المؤشرات الاقتصادية
# -------------------
st.subheader("📊 Macro Economic Indicators")
st.dataframe(df.style.applymap(color_trend, subset=["Trend"]).set_properties(**{'font-size':'16px','text-align':'center'}))

# -------------------
# أسواق مالية مرتبطة بالمؤشرات
# -------------------
markets_data = {
    "Market": ["Gold Spot", "BTCUSD", "US Tech 100", "US Dollar Index", "US30"],
    "Latest Value": [1930, 29850, 14000, 107.5, 34800],
    "Trend": ["Up", "Down", "Up", "Up", "Down"]
}

df_markets = pd.DataFrame(markets_data)
st.subheader("💹 Financial Markets")
st.dataframe(df_markets.style.applymap(color_trend, subset=["Trend"]).set_properties(**{'font-size':'16px','text-align':'center'}))

# -------------------
# الربع الاقتصادي والسياسة النقدية
# -------------------
st.subheader("📅 Current Economic Quarter")
st.success("🔥 Growth + Inflation (Stagflation)")

st.subheader("🏦 Monetary Policy Suggestion")
st.info("💹 Tightening → Possible Interest Rate Hike")
