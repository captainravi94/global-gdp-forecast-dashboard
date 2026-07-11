import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🔮 GDP Forecast (2027–2030)")

# ==========================
# Load datasets
# ==========================
hist = pd.read_csv("data/gdp_cleaned.csv")
forecast = pd.read_csv("data/gdp_forecast_2030.csv")

# ==========================
# Clean Country column
# ==========================
hist["Country"] = (
    hist["Country"]
    .fillna("")
    .astype(str)
    .str.strip()
)

forecast["Country"] = (
    forecast["Country"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Remove blank or invalid country names
hist = hist[
    (hist["Country"] != "") &
    (hist["Country"].str.lower() != "nan")
]

forecast = forecast[
    (forecast["Country"] != "") &
    (forecast["Country"].str.lower() != "nan")
]

# ==========================
# Country selector
# ==========================
country_list = sorted(hist["Country"].drop_duplicates().tolist())

country = st.selectbox(
    "Select Country",
    country_list
)

# ==========================
# Filter data
# ==========================
hist_country = hist[hist["Country"] == country]
forecast_country = forecast[forecast["Country"] == country]

st.subheader(f"{country} GDP Historical vs Forecast")

# ==========================
# Historical chart
# ==========================
fig = px.line(
    hist_country,
    x="Year",
    y="GDP",
    markers=True,
    labels={
        "GDP": "GDP (Billion USD)",
        "Year": "Year"
    }
)

# ==========================
# Forecast line
# ==========================
if not forecast_country.empty:
    fig.add_scatter(
        x=forecast_country["Year"],
        y=forecast_country["GDP_Predicted"],
        mode="lines+markers",
        name="Forecast (Billion USD)"
    )
else:
    st.warning("No forecast data available for this country.")

# ==========================
# Layout
# ==========================
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="GDP (Billion USD)"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("GDP values are expressed in Billion USD.")
