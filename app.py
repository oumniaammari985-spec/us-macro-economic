import streamlit as st
import pandas as pd
import requests

st.title("U.S Macro Economic Dashboard")
st.write("Welcome! This app will display automatic macroeconomic data.")

# -----------------------------
# GDP Data
# -----------------------------
st.header("GDP")

# Example: Fetching GDP data from FRED API
FRED_API_KEY = "ضع المفتاح هنا"
fred_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key={FRED_API_KEY}&file_type=json"

try:
    response = requests.get(fred_url)
    data = response.json()
    df = pd.DataFrame(data['observations'])
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    st.line_chart(df.set_index('date')['value'])
except Exception as e:
    st.error(f"Failed to fetch GDP data: {e}")

# -----------------------------
# Example Additional Data
# -----------------------------
st.header("Other Economic Data")
st.write("This section can display more macroeconomic indicators automatically.")

# You can add more sections here, e.g., Unemployment Rate, Inflation, etc.
