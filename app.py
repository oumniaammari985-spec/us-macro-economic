import streamlit as st
import pandas as pd
from fredapi import Fred
from datetime import datetime
import yfinance as yf

# ===== CONFIG =====
FRED_API_KEY = "7f5eae04be2947e58f155c52922d7145"
fred = Fred(api_key=FRED_API_KEY)

# ===== INDICATORS =====
indicators = {
    "CPI": "CPIAUCSL",
    "Core CPI (MoM)": "CPILFESL",
    "PPI": "PPIACO",
    "Core PPI (MoM)": "PPICTOT",
    "Unemployment Rate": "UNRATE",
    "Non-Farm Payrolls": "PAYEMS",
    "Average Hourly Earnings": "CES0500000003",
    "Retail Sales (MoM)": "RSAFS",
    "Core Retail Sales (MoM)": "RSXFS",
    "ISM Manufacturing PMI": "NAPM",
    "ISM Services PMI": "NAPM_SERV",
    "ISM Manufacturing Prices": "NAPM_PRICES",
    "JOLTS Job Openings": "JTSJOL",
    "Michigan Consumer Sentiment": "UMCSENT",
    "PCE": "PCE",
    "Core PCE (MoM)": "PCEPILFE",
    "GDP (QoQ)": "GDP",
    "Durable Goods Orders": "DGORDER",
    "Trade Balance": "NETEXP",
    "Building Permits": "PERMIT",
    "New Home Sales": "NHSLTOT",
    "Industrial Production": "INDPRO",
    "Participation Rate": "CIVPART",
}

# ===== STREAMLIT SETUP =====
st.set_page_config(page_title="🇺🇸 U.S Macro Economic Dashboard", layout="wide")
st.title("🇺🇸 U.S Macro Economic Dashboard")
st.markdown("Automatic updates — Official economic indicators")

# ===== BUTTON FOR MANUAL UPDATE =====
if st.button("🔄 Update Data Manually"):
    st.experimental_rerun()

# ===== FETCH DATA =====
data = []
for name, code in indicators.items():
    try:
        series = fred.get_series(code)
        latest = series.dropna().iloc[-1]
        prev = series.dropna().iloc[-2] if len(series.dropna())>1 else latest
        trend = "📈 UP" if latest > prev else "📉 DOWN" if latest < prev else "➡️ Stable"
        data.append({"Indicator": name, "Latest Value": latest, "Trend": trend})
    except:
        data.append({"Indicator": name, "Latest Value": "N/A", "Trend": "❌ Error"})

df = pd.DataFrame(data)

# ===== DISPLAY TABLE =====
st.subheader("📊 Macro Economic Indicators")
st.dataframe(df.style.background_gradient(subset=["Latest Value"], cmap="coolwarm"))

# ===== CURRENT QUARTER =====
st.subheader("📅 Current Economic Quarter")
gdp = df.loc[df["Indicator"]=="GDP (QoQ)", "Latest Value"].values[0]
if isinstance(gdp, (int, float)):
    if gdp > 1000:
        quarter_status = "🔥 نمو مع التضخم"
        monetary_policy = "💹 تشديد → احتمال رفع أسعار الفائدة"
    else:
        quarter_status = "⚡ نمو ضعيف"
        monetary_policy = "⚖️ سياسة معتدلة"
else:
    quarter_status = "❌ بيانات غير متوفرة"
    monetary_policy = "❌ بيانات غير متوفرة"

st.markdown(f"Status: {quarter_status}")
st.markdown(f"Policy: {monetary_policy}")

# ===== MARKETS ANALYSIS =====
st.subheader("💹 Financial Markets Analysis")
symbols = {
    "Gold": "GC=F",
    "BTCUSD": "BTC-USD",
    "US Tech 100": "^NDX",
    "US Dollar Index": "DX-Y.NYB",
    "US30": "^DJI"
}
market_data = []
for name, sym in symbols.items():
    try:
        ticker = yf.Ticker(sym)
        price = ticker.history(period="2d")['Close'].iloc[-1]
        prev_price = ticker.history(period="2d")['Close'].iloc[-2]
        trend = "📈 UP" if price > prev_price else "📉 DOWN" if price < prev_price else "➡️ Stable"
        market_data.append({"Market": name, "Price": price, "Trend": trend})
    except:
        market_data.append({"Market": name, "Price": "N/A", "Trend": "❌ Error"})
market_df = pd.DataFrame(market_data)
st.dataframe(market_df.style.background_gradient(subset=["Price"], cmap="viridis"))

# ===== LAST UPDATED =====
st.subheader("🗓️ Last Updated")
st.markdown(datetime.now().strftime("%B %d, %Y %H:%M:%S"))
