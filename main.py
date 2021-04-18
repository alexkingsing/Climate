import streamlit as st
import pandas as pd
import numpy as np
from Climateviz import *

# loading data and caching
data = load_data("data/Environment_Temperature_change_E_All_Data_NOFLAG.csv")

st.sidebar.title("Display options")

country = st.sidebar.selectbox("Countries", data["area"].unique())

# extracting available year range for the country selected
years = year_range(data, country)

# extracting years from slider
low, high = st.sidebar.slider("Year", min_value = min(years), max_value = max(years), value = (min(years), max(years)))
# period to display from slider
period = st.sidebar.selectbox("Period", data["months"].unique())

# extracting country specific data based on current parameters
parsed_data = config_data(data, country, low, high, period)

st.header(f"Visualizing **LAND** temperature anomalies for **{country}**")
st.subheader(f"Period: **{low}**-**{high}**, **{period}**")

# creating display sections
col1, col2 = st.beta_columns([3,1])

# extracting index of value of max and min anomalies
idxmax = parsed_data["Temperature Anomaly"].idxmax()
idxmin = parsed_data["Temperature Anomaly"].idxmin()

# drawing plot.
with col1:
    st.pyplot(plot_chart(parsed_data))

# displaying tables with max and min values
with col2:
    st.write("Year of **max** temperature anomaly")
    if isinstance(parsed_data.loc[idxmax]["Temperature Anomaly"], np.float64) == True:
        st.table(pd.DataFrame({idxmax:parsed_data.loc[idxmax]["Temperature Anomaly"]}, index = ["Temp. Anomaly"]))
    else:
        st.table(parsed_data.loc[idxmax]["Temperature Anomaly"])

    st.write("Year of **min** temperature anomaly")
    if isinstance(parsed_data.loc[idxmax]["Temperature Anomaly"], np.float64) == True:
        st.table(pd.DataFrame({idxmin:parsed_data.loc[idxmin]["Temperature Anomaly"]}, index = ["Temp. Anomaly"]))
    else:
        st.table(parsed_data.loc[idxmin]["Temperature Anomaly"])

# hold data at the bottom of the app
with st.beta_expander(label = "Click to see data", expanded = False):
    st.dataframe(parsed_data["Temperature Anomaly"])