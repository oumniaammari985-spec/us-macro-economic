# app.py
import streamlit as st
import pandas as pd
import datetime
from fredapi import Fred

# -------------------
# إعداد مفتاح FRED API
# -------------------
FRED_API_KEY = "7f5eae04be2947e58f155c52922d7145"
fred = Fred(api_key=FRED_API_KEY)

st.set_page_config(page_title="U.S Macro Economic Dashboard", layout="wide")

# -------------------
# عنوان التطبيق
# -------------------
st.title("🇺🇸 U.S Macro Economic Dashboard")
st.subheader("Automatic updates — Official economic indicators")

# -------------------
# التاريخ التلقائي
# -------------------
current_time = datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")
st.markdown(f"🗓️ **Last Updated:** {current_time}")

# -------------------
# المؤشرات الاقتصادية
# -------------------
indicators = {
    "CPI": "CPIAUCSL",
    "Core CPI (MoM)": "CPILFESL",
    "PPI": "PPIACO",
    "Core PPI (MoM)": "PPICTPI",
    "Unemployment Rate": "UNRATE",
    "Non-Farm Payrolls": "PAYEMS",
    "GDP (QoQ)": "GDP"
}

data = {}
for name, series_id in indicators.items():
    try:
        series_data = fred.get_series(series_id)
        latest_value = series_data.iloc[-1]
        prev_value = series_data.iloc[-2]
        trend = latest_value - prev_value
        data[name] = [latest_value, trend]
    except Exception as e:
        data[name] = ["N/A", "N/A"]

# -------------------
# تحويل البيانات إلى جدول
# -------------------
df = pd.DataFrame(data, index=["Latest Value", "Change vs Last Month"]).T

# تلوين الجدول
st.dataframe(df.style.background_gradient(subset=["Latest Value"], cmap="coolwarm"))

# -------------------
# تحديد الربع الاقتصادي الحالي (مبسّط)
# -------------------
gdp_trend = data.get("GDP (QoQ)", [0, 0])[1]
cpi_trend = data.get("CPI", [0, 0])[1]

if gdp_trend > 0 and cpi_trend > 0:
    quarter_status = "🔥 نمو مع التضخم"
elif gdp_trend > 0 and cpi_trend <= 0:
    quarter_status = "📈 نمو اقتصادي"
elif gdp_trend <= 0 and cpi_trend > 0:
    quarter_status = "⚠️ تضخم بدون نمو"
else:
    quarter_status = "📉 انكماش"

st.subheader("📅 Current Economic Quarter")
st.markdown(f"**Status:** {quarter_status}")

# -------------------
# اقتراح السياسة النقدية
# -------------------
if cpi_trend > 0.5:
    policy = "💹 تشديد → احتمال رفع أسعار الفائدة"
else:
    policy = "🟢 تيسير → دعم الاقتصاد"

st.subheader("🏦 Monetary Policy Suggestion")
st.markdown(f"**Policy:** {policy}")

# -------------------
# زر تحديث يدوي
# -------------------
if st.button("🔄 تحديث البيانات"):
    st.experimental_rerun()
