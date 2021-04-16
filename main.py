import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# needed for dynamic axis
import matplotlib.ticker as ticker
from Climateviz import load_data, config_data


data, years = load_data("data/Environment_Temperature_change_E_All_Data_NOFLAG.csv")

st.sidebar.title("Display options")
low, high = st.sidebar.slider("Year", min_value = min(years), max_value = max(years), value = (min(years), max(years)))
country = st.sidebar.selectbox("Countries", data["area"].unique())
period = st.sidebar.selectbox("Period", data["months"].unique())

st.header(f"Visualizing **Land** temperature anomalies for **{country}**")
st.subheader(f"Period: **{low}**-**{high}**, displaying **{period}**")

parsed_data = config_data(data, country, low, high, period)

st.dataframe(parsed_data, width=800, height=800)