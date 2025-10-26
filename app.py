import streamlit as st
import pandas as pd
import requests
import plotly.express as px

FRED_API_KEY = "f034076778e256cc6652d0e249b13f67"

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
    df = df.dropna().reset_index(drop=True)
    return df.rename(columns={"value": title})

st.title("🇺🇸 U.S Macro Economic Dashboard")
st.write("Automatic updates — Official economic indicators")

# CPI
cpi_df = get_fred_data("CPIAUCSL", "CPI")
st.subheader("📊 CPI (Inflation Indicator)")
fig_cpi = px.line(cpi_df, x="date", y="CPI", title="CPI Over Time")
st.plotly_chart(fig_cpi)
st.dataframe(cpi_df.tail(12).style.format({"CPI":"{:.2f}"}))

latest = cpi_df.iloc[-1]["CPI"]
previous = cpi_df.iloc[-2]["CPI"]
change = latest - previous
if change > 0:
    st.success(f"📈 Inflation trending UP (+{change:.2f}) → Negative for economy")
else:
    st.error(f"📉 Inflation trending DOWN ({change:.2f}) → Positive for economy")

# GDP
gdp_df = get_fred_data("GDP", "GDP (Billions USD)")
st.subheader("📌 GDP (Billions USD)")
fig_gdp = px.line(gdp_df, x="date", y="GDP (Billions USD)", title="GDP Over Time")
st.plotly_chart(fig_gdp)
st.dataframe(gdp_df.tail(12).style.format({"GDP (Billions USD)":"{:,.2f}"}))

