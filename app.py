# app.py

import streamlit as st
import pandas as pd
from datetime import datetime
from fredapi import Fred

# ===== إعداد API =====
fred = Fred(api_key=st.secrets["FRED_API_KEY"])

st.set_page_config(page_title="U.S Macro Economic Dashboard", layout="wide")
st.title("🇺🇸 U.S Macro Economic Dashboard")
st.markdown("Automatic updates — Official economic indicators")

# ===== المؤشرات الاقتصادية =====
indicators = {
    "CPI": "CPIAUCSL",
    "Core CPI (MoM)": "CPILFESL",
    "PPI": "PPIACO",
    "Core PPI (MoM)": "PPICTPI",
    "Unemployment Rate": "UNRATE",
    "Non-Farm Payrolls": "PAYEMS",
    "Average Hourly Earnings": "CES0500000003",
    "Retail Sales (MoM)": "RSXFS",
    "Core Retail Sales (MoM)": "RSAFS",
    "ISM Manufacturing PMI": "NAPM",
    "ISM Services PMI": "SERVPMI",
    "ISM Manufacturing Prices": "PPIACO",
    "JOLTS Job Openings": "JTSJOL",
    "Michigan Consumer Sentiment": "UMCSENT",
    "PCE": "PCE",
    "Core PCE (MoM)": "PCEPILFE",
    "GDP (QoQ)": "GDPC1",
    "Durable Goods Orders": "DGORDER",
    "Trade Balance": "NETEXP",
    "Building Permits": "PERMIT",
    "New Home Sales": "HSN1F",
    "Industrial Production": "INDPRO",
    "Participation Rate": "CIVPART",
}

# ===== دالة لجلب البيانات =====
def fetch_data(series_id):
    try:
        data = fred.get_series(series_id)
        df = pd.DataFrame(data, columns=["Value"])
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        return df
    except Exception as e:
        st.error(f"Error fetching {series_id}: {e}")
        return pd.DataFrame()

# ===== جدول المؤشرات =====
st.header("📊 Economic Indicators")

indicator_data = {}
for name, series in indicators.items():
    df = fetch_data(series)
    if not df.empty:
        # آخر قيمتين لمقارنة الاتجاه
        last_val = df["Value"].iloc[-1]
        prev_val = df["Value"].iloc[-2] if len(df) > 1 else last_val
        trend = "↗️ Up" if last_val > prev_val else "↘️ Down" if last_val < prev_val else "→ Stable"
        indicator_data[name] = {
            "Date": df.index[-1].strftime("%Y-%m-%d"),
            "Value": last_val,
            "Trend": trend
        }

indicator_df = pd.DataFrame(indicator_data).T
st.dataframe(indicator_df.style.format({"Value": "{:.2f}"}))

# ===== تحديد الربع الاقتصادي =====
st.header("📌 Current Economic Quarter Analysis")
# بسيط: استخدام GDP + Unemployment + CPI لتقدير الربع
gdp_trend = indicator_df.loc["GDP (QoQ)","Trend"] if "GDP (QoQ)" in indicator_df.index else "Unknown"
cpi_trend = indicator_df.loc["CPI","Trend"] if "CPI" in indicator_df.index else "Unknown"
unemp_trend = indicator_df.loc["Unemployment Rate","Trend"] if "Unemployment Rate" in indicator_df.index else "Unknown"

quarter_analysis = "Unknown"
if gdp_trend=="↗️ Up" and cpi_trend=="↘️ Down":
    quarter_analysis = "Growth"
elif gdp_trend=="↗️ Up" and cpi_trend=="↗️ Up":
    quarter_analysis = "Inflationary Growth"
elif gdp_trend=="↘️ Down" and cpi_trend=="↘️ Down":
    quarter_analysis = "Contraction"
elif gdp_trend=="↘️ Down" and cpi_trend=="↗️ Up":
    quarter_analysis = "Stagflation"

st.info(f"Current Economic Quarter: **{quarter_analysis}**")

# ===== السياسة النقدية =====
st.header("💰 Monetary Policy Suggestion")
policy = "Unknown"
if quarter_analysis in ["Growth", "Inflationary Growth"]:
    policy = "Consider tightening / rate hikes likely"
elif quarter_analysis in ["Contraction"]:
    policy = "Consider easing / stimulus likely"
elif quarter_analysis in ["Stagflation"]:
    policy = "Mixed signals, monitor CPI and Unemployment"

st.success(f"Suggested Monetary Policy: **{policy}**")

# ===== تحديث البيانات =====
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

# ===== Footer =====
st.markdown("---")
st.markdown("Data source: [FRED](https://fred.stlouisfed.org/)")
st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
