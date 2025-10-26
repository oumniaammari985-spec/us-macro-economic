import streamlit as st
import pandas as pd
from fredapi import Fred
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt

# ==========================
# إعداد FRED API
# ==========================
FRED_API_KEY = "7f5eae04be2947e58f155c52922d7145"
fred = Fred(api_key=FRED_API_KEY)

# ==========================
# قائمة المؤشرات الاقتصادية
# ==========================
indicators = {
    "CPI": "CPIAUCNS",
    "Core CPI (MoM)": "CPILFESL",
    "PPI": "PPIACO",
    "Core PPI (MoM)": "PPIFESL",
    "Unemployment Rate": "UNRATE",
    "Non-Farm Payrolls (NFP)": "PAYEMS",
    "Average Hourly Earnings": "CES0500000003",
    "Retail Sales (MoM)": "RSAFS",
    "Core Retail Sales (MoM)": "RSXFS",
    "ISM Manufacturing PMI": "NAPM",
    "ISM Services PMI": "NAPM_SERV",
    "ISM Manufacturing Prices": "PPIACO",
    "JOLTS Job Openings": "JTSJOL",
    "Michigan Consumer Sentiment": "UMCSENT",
    "PCE (Personal Consumption Expenditures)": "PCE",
    "Core PCE (MoM)": "PCEPILFE",
    "GDP (QoQ)": "A191RL1Q225SBEA",
    "Durable Goods Orders": "DGORDER",
    "Trade Balance": "NETEXP",
    "Building Permits": "PERMIT",
    "New Home Sales": "NHSPST",
    "Industrial Production": "INDPRO",
    "Participation Rate": "CIVPART",
    "ADP Employment": "ADP7400",
    "Earnings Productivity": "PRS85006023"
}

# ==========================
# جلب البيانات الاقتصادية
# ==========================
data = []
for name, series in indicators.items():
    try:
        latest = fred.get_series_latest_release(series)
        data.append({"Indicator": name, "Latest Value": latest})
    except:
        data.append({"Indicator": name, "Latest Value": "N/A"})

df = pd.DataFrame(data)

# ==========================
# جلب أسعار الأسواق المالية
# ==========================
assets = {
    "Gold": "GC=F",
    "BTC/USD": "BTC-USD",
    "US Tech 100": "^NDX",
    "US Dollar Index": "DX-Y.NYB",
    "US30": "^DJI"
}

asset_data = {}
for name, ticker in assets.items():
    try:
        price = yf.download(ticker, period="1d")["Close"][-1]
        asset_data[name] = price
    except:
        asset_data[name] = "N/A"

# ==========================
# واجهة Streamlit
# ==========================
st.title("🇺🇸 U.S Macro Economic Dashboard")
st.write("Automatic updates — Official economic indicators")

st.subheader("📊 Macro Economic Indicators")
st.dataframe(df.style.background_gradient(subset=["Latest Value"], cmap="coolwarm"))

st.subheader("💹 Financial Market Snapshot")
for asset, price in asset_data.items():
    st.write(f"{asset}: {price}")

# ==========================
# تحليل الربع الاقتصادي
# ==========================
gdp_value = df.loc[df["Indicator"]=="GDP (QoQ)", "Latest Value"].values[0]
cpi_value = df.loc[df["Indicator"]=="CPI", "Latest Value"].values[0]

if gdp_value != "N/A" and cpi_value != "N/A":
    if gdp_value > 2 and cpi_value < 2:
        quarter_status = "🟢 نمو اقتصادي"
    elif gdp_value > 2 and cpi_value >= 2:
        quarter_status = "🔥 نمو مع التضخم"
    elif gdp_value <= 0 and cpi_value >= 2:
        quarter_status = "🔴 انكماش اقتصادي مع تضخم"
    else:
        quarter_status = "🟡 انكماش اقتصادي"
else:
    quarter_status = "❓ بيانات غير كافية"

# ==========================
# السياسة النقدية
# ==========================
if cpi_value != "N/A":
    if cpi_value > 2:
        monetary_policy = "💹 تشديد → احتمال رفع أسعار الفائدة"
    else:
        monetary_policy = "⚪ تيسير → أسعار الفائدة مستقرة أو منخفضة"
else:
    monetary_policy = "❓ بيانات غير كافية"

st.subheader("📅 Current Economic Quarter")
st.write("Status:", quarter_status)

st.subheader("🏦 Monetary Policy Suggestion")
st.write("Policy:", monetary_policy)

st.write("🗓️ Last Updated:", datetime.now().strftime("%B %d, %Y %H:%M:%S"))

# ==========================
# تحديث يدوي
# ==========================
if st.button("🔄 تحديث يدوي"):
    st.experimental_rerun()
