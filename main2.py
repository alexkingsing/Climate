import pandas as pd
from streamlit.elements import data_frame
from Climatevizv2 import *
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# loading data and caching
data = load_data("data/Environment_Temperature_change_E_All_Data_NOFLAG.csv")

# Sidebar label
st.sidebar.title("Display options")

#Selecting visualization paths
viz_opt = st.sidebar.selectbox(label="Select what you wish to see!", options=["None","One country", "Multiple countries"])

if viz_opt == "Multiple countries":
    countries = st.sidebar.multiselect("Select countries to visualize", data["area"].unique()) # displaying list of available countries , default option is an empty list for flow control
    if len(countries) != 0:
        years = multic_year_range(data, countries)
        low, high = st.sidebar.slider("Select years from the available period", min_value = min(years), max_value = max(years), value = (min(years), max(years))) # creating slider to retrieve desired period based on available years
        period_list = list(data["months"].unique())
        period_list.append("")
        period = st.sidebar.selectbox("Period to visualize", period_list, index = (len(period_list) - 1)) # period to display from slider , default option is an empty string for flow control
        if period != "":
            st.header(f"Visualizing **LAND** temperature anomalies for **{' & '.join(countries)}**")
            
            ### PARSING OF DATAFRAME MISSING
            ### PLOTTING IN PLOTLY MISSING

elif viz_opt == "One country":
    country_list = list(data["area"].unique())
    country_list.append("")
    country = st.sidebar.selectbox("Select a country to visualize", country_list, index= (len(country_list) - 1)) # displaying list of available countries, default option is an empty string for flow control
    if country != "":
        years = onec_year_range(data, country) # extracting available year range for the country selected
        low, high = st.sidebar.slider("Select years from the available period", min_value = min(years), max_value = max(years), value = (min(years), max(years))) # creating slider to retrieve desired period based on available years
        period_list = list(data["months"].unique())
        period_list.append("")
        period = st.sidebar.selectbox("Select period to visualize", period_list, index = (len(period_list) - 1)) # period to display from slider , default option is an empty string for flow control
        if period != "":
            parsed_data = config_data_onec(data, country, low, high, period) # extracting country specific data based on current parameters
            st.header(f"Visualizing **LAND** temperature anomalies for **{country}**") # header
            fig = plot_onec(parsed_data) # creating figure
            st.plotly_chart(fig, use_container_width = True) #instantiating figure and sizing to container

else:
    pass

#####################################################################################################################################################################################
'''

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
'''