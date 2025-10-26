import streamlit as st
import pandas as pd
from fredapi import Fred
import datetime
import requests

# ======================================
# إعداد Streamlit
# ======================================
st.set_page_config(page_title="U.S Macro Economic Dashboard", layout="wide", page_icon="🇺🇸")
st.title("🇺🇸 U.S Macro Economic Dashboard")
st.markdown("Automatic updates — Official economic indicators")

# ======================================
# API Keys
# ======================================
FRED_API_KEY = "f034076778e256cc6652d0e249b13f67"
fred = Fred(api_key=FRED_API_KEY)

# ======================================
# دالة لجلب المؤشرات من FRED
# ======================================
@st.cache_data(ttl=3600)
def get_fred_data():
    data = {}
    today = datetime.date.today()

    # أمثلة على المؤشرات:
    data["CPI"] = fred.get_series("CPIAUCSL")[-1]          # Consumer Price Index
    data["Core CPI (MoM)"] = fred.get_series("CPILFESL")[-1] # Core CPI
    data["PPI"] = fred.get_series("PPIACO")[-1]            # Producer Price Index
    data["Unemployment Rate"] = fred.get_series("UNRATE")[-1]
    data["GDP (QoQ)"] = fred.get_series("A191RL1Q225SBEA")[-1] # GDP

    df = pd.DataFrame({
        "Indicator": list(data.keys()),
        "Value": list(data.values()),
        "Date": [today]*len(data)
    })
    return df

# ======================================
# جلب البيانات
# ======================================
df = get_fred_data()

# ======================================
# حساب الاتجاه وتحليله
# ======================================
def trend(value):
    if value > 0:
        return "📈 UP → Negative for economy", "red"
    elif value < 0:
        return "📉 DOWN → Positive for economy", "green"
    else:
        return "➡️ Stable", "gray"

df["Trend"], df["Color"] = zip(*df["Value"].apply(trend))

# ======================================
# عرض الجدول
# ======================================
st.subheader("📊 Economic Indicators")
st.dataframe(df.style.apply(lambda x: ["background-color: {}".format(c) for c in df["Color"]], axis=1))

# ======================================
# تحليل الربع الاقتصادي والسياسة النقدية
# ======================================
def economic_quarter(df):
    gdp = df.loc[df["Indicator"]=="GDP (QoQ)", "Value"].values[0]
    cpi = df.loc[df["Indicator"]=="CPI", "Value"].values[0]
    if gdp > 2 and cpi < 3:
        return "📈 Growth Phase"
    elif gdp > 2 and cpi >= 3:
        return "🔥 Growth with Inflation"
    elif gdp < 0:
        return "📉 Contraction"
    else:
        return "⚖ Stable / Mild Growth"

quarter_status = economic_quarter(df)
st.subheader("📅 Current Economic Quarter")
st.write(f"Status: **{quarter_status}**")

def monetary_policy(df):
    cpi = df.loc[df["Indicator"]=="CPI", "Value"].values[0]
    unemployment = df.loc[df["Indicator"]=="Unemployment Rate", "Value"].values[0]
    if cpi > 3 and unemployment < 5:
        return "💹 Tightening → Possible interest rate hike"
    elif cpi < 2 and unemployment > 5:
        return "📉 Easing → Possible rate cut"
    else:
        return "⚖ Neutral / Hold"

policy = monetary_policy(df)
st.subheader("🏦 Suggested Monetary Policy")
st.write(f"Policy: **{policy}**")

# ======================================
# زر التحديث اليدوي
# ======================================
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()
