
#Dashboard PY
import streamlit as st
import pandas as pd
import numpy as np
 
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")
 
@st.cache_data
def load_data(seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2026-01-01", periods=180)
    regions = ["Central", "Eastern", "Northern", "Western"]
    products = ["Laptop", "Phone", "Tablet", "Headset"]
    df = pd.DataFrame({
        "date": rng.choice(dates, 1000),
        "region": rng.choice(regions, 1000),
        "product": rng.choice(products, 1000),
        "units": rng.integers(1, 20, 1000),
        "price": rng.uniform(50, 900, 1000).round(2),
    })
    df["revenue"] = df["units"] * df["price"]
    return df
 
st.title("📊 Sales Dashboard")
df = load_data(seed=42)
 
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", df["region"].unique(), default=df["region"].unique())
products = st.sidebar.multiselect("Product", df["product"].unique(), default=df["product"].unique())
date_range = st.sidebar.date_input("Date range", value=(df["date"].min().date(), df["date"].max().date()))
 
filtered = df[df["region"].isin(regions) & df["product"].isin(products)]
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range)
    filtered = filtered[filtered["date"].between(start, end)]
 
col1, col2, col3 = st.columns(3)
col1.metric("Total revenue", f"${filtered['revenue'].sum():,.0f}")
col2.metric("Units sold", f"{filtered['units'].sum():,}")
col3.metric("Avg order value", f"${filtered['revenue'].mean():,.0f}" if len(filtered) else "$0")
 
left, right = st.columns(2)
with left:
    st.subheader("Revenue over time")
    st.line_chart(filtered.groupby("date")["revenue"].sum())
with right:
    st.subheader("Revenue by region")
    st.bar_chart(filtered.groupby("region")["revenue"].sum())
 
st.subheader("Top products")
top = filtered.groupby("product")[["units", "revenue"]].sum().sort_values("revenue", ascending=False)
st.dataframe(top, use_container_width=True)
 
with st.expander("Raw data"):
    st.dataframe(filtered)
 

