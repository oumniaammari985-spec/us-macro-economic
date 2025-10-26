import streamlit as st
import pandas as pd
from fredapi import Fred
import datetime

# ✅ API Key
fred = Fred(api_key="f034076778e256cc6652d0e249b13f67")

st.title("🇺🇸 U.S. Macro Economic Dashboard")
st.write("📊 البيانات يتم جلبها تلقائياً من FRED (المصدر الرسمي للاقتصاد الأمريكي)")

# ✅ دالة لجلب البيانات
def get_data(series_id, title):
    data = fred.get_series(series_id)
    df = pd.DataFrame(data, columns=[title])
    df.index.name = "Date"
    return df

# ✅ المؤشرات
gdp = get_data("GDP", "GDP (Billions USD)")
cpi = get_data("CPIAUCSL", "CPI")
unemployment = get_data("UNRATE", "Unemployment Rate")

# ✅ عرض البيانات والرسوم
st.header("📌 GDP")
st.line_chart(gdp)

st.header("📌 CPI - Inflation")
st.line_chart(cpi)

st.header("📌 Unemployment Rate")
st.line_chart(unemployment)

st.success("✅ تم جلب البيانات بنجاح! 🚀")
