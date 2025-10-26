import streamlit as st
import pandas as pd
from datetime import datetime
from fredapi import Fred

# ==========================
# إعداد المفتاح للوصول لـ FRED API
# ==========================
FRED_API_KEY = "f034076778e256cc6652d0e249b13f67"
fred = Fred(api_key=FRED_API_KEY)

# ==========================
# عنوان التطبيق
# ==========================
st.set_page_config(page_title="🇺🇸 U.S Macro Economic Dashboard", layout="wide")
st.title("🇺🇸 U.S Macro Economic Dashboard")
st.subheader("Automatic updates — Official economic indicators")

# ==========================
# زر التحديث اليدوي
# ==========================
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

# ==========================
# المؤشرات الاقتصادية الأساسية
# ==========================
indicators = {
    "CPI": "CPIAUCSL",
    "Core CPI (MoM)": "CPILFESL",
    "PPI": "PPIACO",
    "Core PPI (MoM)": "PPIFESL",
    "Unemployment Rate": "UNRATE",
    "Non-Farm Payrolls": "PAYEMS",
    "Average Hourly Earnings": "CES0500000003",
    "Retail Sales (MoM)": "RSAFS",
    "Core Retail Sales (MoM)": "RSXFS",
    "ISM Manufacturing PMI": "NAPM",
    "ISM Services PMI": "NAPM_SERVICE",
    "GDP (QoQ)": "GDPC1",
    "Durable Goods Orders": "DGORDER",
    "Trade Balance": "NETEXP",
    "Building Permits": "PERMIT",
    "New Home Sales": "NHSPST",
    "Industrial Production": "INDPRO",
    "Participation Rate": "CIVPART"
}

# ==========================
# جلب البيانات وتحليل الاتجاه
# ==========================
data = {}
trend = {}

for name, code in indicators.items():
    try:
        series = fred.get_series(code)
        latest = series.iloc[-1]
        prev = series.iloc[-2] if len(series) > 1 else latest
        data[name] = latest
        trend[name] = "UP" if latest > prev else "DOWN" if latest < prev else "UNCHANGED"
    except Exception:
        data[name] = None
        trend[name] = "N/A"

# ==========================
# تحويل البيانات إلى DataFrame للعرض
# ==========================
df = pd.DataFrame(data.items(), columns=["Indicator", "Latest Value"])
df["Trend"] = df["Indicator"].map(trend)

# ==========================
# عرض البيانات في جدول منسق
# ==========================
st.markdown("### 📊 Macro Economic Indicators")
st.dataframe(df.style.background_gradient(subset=["Latest Value"], cmap="coolwarm"))

# ==========================
# تحليل الربع الاقتصادي
# ==========================
cpi_trend = trend.get("CPI", "UNCHANGED")
gdp_value = data.get("GDP (QoQ)", 0)

if cpi_trend == "UP" and gdp_value > 0:
    quarter_status = "🔥 نمو مع التضخم"
elif cpi_trend == "UP" and gdp_value < 0:
    quarter_status = "⚡ تضخم مع انكماش"
elif cpi_trend == "DOWN" and gdp_value > 0:
    quarter_status = "📈 نمو"
else:
    quarter_status = "📉 انكماش"

st.markdown("### 📅 Current Economic Quarter")
st.info(f"Status: {quarter_status}")

# ==========================
# السياسة النقدية بناءً على المؤشرات
# ==========================
if cpi_trend == "UP":
    policy = "💹 تشديد → احتمال رفع أسعار الفائدة"
elif cpi_trend == "DOWN":
    policy = "💸 تيسير → احتمال تخفيض أسعار الفائدة"
else:
    policy = "⚖️ مستقرة"

st.markdown("### 🏦 Monetary Policy Suggestion")
st.info(f"Policy: {policy}")

# ==========================
# التاريخ التلقائي
# ==========================
st.markdown("### 🗓️ Last Updated")
st.write(datetime.now().strftime("%B %d, %Y %H:%M:%S"))
