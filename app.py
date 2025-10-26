import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ✅ API Key
FRED_API_KEY = "f034076778e256cc6652d0e249b13f67"

# ✅ Function to get CPI data from FRED
def get_fred_data(series_id, title):
    url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
    }
    r = requests.get(url, params=params)
    data = r.json()["observations"]
    df = pd.DataFrame(data)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna()
    
    return df

# ✅ Page Title
st.title("🇺🇸 U.S Macro Economic Dashboard")
st.write("Automatic updates — Official economic indicators")

st.subheader("📊 CPI (Inflation Indicator)")

# ✅ Get CPI (Consumer Price Index)
cpi_df = get_fred_data("CPIAUCSL", "CPI")

# ✅ Plot CPI Chart
fig = px.line(cpi_df, x="date", y="value", title="CPI Over Time")
st.plotly_chart(fig)

# ✅ Show Table
st.dataframe(cpi_df.tail(12))

# ✅ Trend Analysis
latest = cpi_df.iloc[-1]["value"]
previous = cpi_df.iloc[-2]["value"]
change = latest - previous

if change > 0:
    st.success(f"📈 Inflation trending UP (+{change:.2f}) → Negative for economy")
else:
    st.error(f"📉 Inflation trending DOWN ({change:.2f}) → Positive for economy")
