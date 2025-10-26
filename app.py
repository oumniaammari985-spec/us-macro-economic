import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="U.S Macro Economic Dashboard", layout="wide")
st.title("🇺🇸 U.S Macro Economic Dashboard")
st.markdown(f"### 🗓️ Last Updated: {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")

# -------------------
# مؤشرات اقتصادية (قيم مؤقتة)
# -------------------
data = {
    "Indicator": [
        "CPI (Consumer Price Index)", "Core CPI (MoM)", "PPI", "Core PPI (MoM)",
        "Unemployment Rate", "NFP", "Average Hourly Earnings", "Retail Sales (MoM)",
        "Core Retail Sales (MoM)", "ISM Manufacturing PMI", "ISM Services PMI",
        "ISM Manufacturing Prices", "JOLTS Job Openings", "Michigan Consumer Sentiment",
        "PCE", "Core PCE (MoM)", "GDP (QoQ)", "Durable Goods Orders", "Trade Balance",
        "Building Permits", "New Home Sales", "ADP Employment Change",
        "Industrial Production", "Participation Rate"
    ],
    "Latest Value": [
        3.4, 0.3, 2.1, 0.2,
        3.7, 150000, 0.4, -0.2,
        0.1, 51.2, 55.3, 49.8,
        10200, 67.5, 2.8, 0.2,
        2.9, 1.1, -64.3, 1800,
        820, 200000, 0.3, 62.1
    ],
    "Trend": [
        "Up", "Up", "Up", "Down",
        "Neutral", "Up", "Up", "Down",
        "Up", "Up", "Up", "Down",
        "Up", "Up", "Up", "Neutral",
        "Up", "Up", "Down", "Up",
        "Down", "Up", "Up", "Neutral"
    ]
}

df = pd.DataFrame(data)

# لون الاتجاه
def color_trend(val):
    if val == "Up":
        return "background-color: red; color: white; font-weight: bold"
    elif val == "Down":
        return "background-color: green; color: white; font-weight: bold"
    return "background-color: gray; color: white; font-weight: bold"

# -------------------
# جدول المؤشرات الاقتصادية
# -------------------
st.subheader("📊 Macro Economic Indicators")
st.dataframe(df.style.applymap(color_trend, subset=["Trend"]).set_properties(**{'font-size':'16px','text-align':'center'}))

# -------------------
# أسواق مالية مرتبطة بالمؤشرات
# -------------------
markets_data = {
    "Market": ["Gold Spot", "BTCUSD", "US Tech 100", "US Dollar Index", "US30"],
    "Latest Value": [1930, 29850, 14000, 107.5, 34800],
    "Trend": ["Up", "Down", "Up", "Up", "Down"]
}

df_markets = pd.DataFrame(markets_data)
st.subheader("💹 Financial Markets")
st.dataframe(df_markets.style.applymap(color_trend, subset=["Trend"]).set_properties(**{'font-size':'16px','text-align':'center'}))

# -------------------
# الربع الاقتصادي والسياسة النقدية
# -------------------
st.subheader("📅 Current Economic Quarter")
st.success("🔥 Growth + Inflation (Stagflation)")

st.subheader("🏦 Monetary Policy Suggestion")
st.info("💹 Tightening → Possible Interest Rate Hike")
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="U.S Macro Economic Dashboard", layout="wide")
st.title("🇺🇸 U.S Macro Economic Dashboard")
st.write("Automatic updates — Official economic indicators")

# -------------------
# جدول الأرباع الاقتصادية
# -------------------
quarter_data = {
    "Quarter": ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"],
    "Status": ["Growth", "Growth + Inflation", "Stagflation", "Recession?"],
    "Trend": ["↑", "↑", "↔", "↓"]
}
df_quarter = pd.DataFrame(quarter_data)

def color_quarter(val):
    if val == "↑":
        return "background-color: green; color: white"
    elif val == "↓":
        return "background-color: red; color: white"
    elif val == "↔":
        return "background-color: orange; color: white"
    return ""

st.subheader("📅 Economic Quarters Overview")
st.dataframe(df_quarter.style.applymap(color_quarter, subset=["Trend"]))

# -------------------
# جدول السياسة النقدية
# -------------------
policy_data = {
    "Policy Aspect": ["Current Rate", "Monetary Policy", "Expected Action"],
    "Value": ["5.25%", "Tightening", "Possible Interest Rate Hike"]
}
df_policy = pd.DataFrame(policy_data)

def color_policy(val):
    if "Tightening" in val:
        return "background-color: red; color: white"
    elif "Easing" in val:
        return "background-color: green; color: white"
    return ""

st.subheader("🏦 Monetary Policy Overview")
st.dataframe(df_policy.style.applymap(color_policy, subset=["Value"]))

# -------------------
# آخر تحديث
# -------------------
st.markdown(f"🗓️ **Last Updated:** {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
# ---------------------------------------------
# جلب البيانات من FRED API
# ---------------------------------------------
from fredapi import Fred
import pandas as pd

# حط المفتاح ديالك هنا
FRED_API_KEY = "7f5eae04be2947e58f155c52922d7145"
fred = Fred(api_key=FRED_API_KEY)

# تعريف المؤشرات وSeries ID الخاص بها في FRED
indicators = {
    "CPI": "CPIAUCSL",
    "Core CPI (MoM)": "CPILFESL",
    "PPI": "PPIACO",
    "Core PPI (MoM)": "PPIFGS",
    "Unemployment Rate": "UNRATE",
    "Non-Farm Payrolls (NFP)": "PAYEMS",
    "Average Hourly Earnings": "CES0500000003",
    "Retail Sales (MoM)": "RSAFS",
    "Core Retail Sales (MoM)": "RSXFS",
    "ISM Manufacturing PMI": "NAPM",
    "ISM Services PMI": "SERVPMI",
    "ISM Manufacturing Prices": "PMIIP",
    "JOLTS Job Openings": "JTSJOL",
    "Michigan Consumer Sentiment": "UMCSENT",
    "PCE": "PCE",
    "Core PCE (MoM)": "PCEPILFE",
    "GDP (QoQ)": "A191RL1Q225SBEA",
    "Durable Goods Orders": "DGORDER",
    "Trade Balance": "NETEXP",
    "Building Permits": "PERMIT",
    "New Home Sales": "HSN1F",
    "ADP Employment": "ADP",
    "Industrial Production": "INDPRO",
    "Participation Rate": "CIVPART"
}

# جلب آخر قيمة لكل مؤشر
latest_data = {}
for name, series_id in indicators.items():
    try:
        series = fred.get_series(series_id)
        latest_data[name] = series.iloc[-1]  # آخر قيمة متوفرة
    except Exception as e:
        latest_data[name] = None  # إذا لم تتوفر البيانات

# تحويلها ل DataFrame
df_indicators = pd.DataFrame({
    "Indicator": list(latest_data.keys()),
    "Latest Value": list(latest_data.values())
})

# عرض DataFrame في Streamlit (يمكن تستخدم اللون لاحقاً)
import streamlit as st
st.subheader("📊 Macro Economic Indicators (Real Data)")
st.dataframe(df_indicators)
