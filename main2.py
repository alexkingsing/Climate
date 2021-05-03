import pandas as pd
from Climatevizv2 import *

st.set_page_config(layout="wide")

# loading data and caching
data = load_data("data/Environment_Temperature_change_E_All_Data_NOFLAG.csv")

# Sidebar label
st.sidebar.title("Display options")

#Selecting visualization paths
viz_opt = st.sidebar.selectbox(label="Select what you wish to see!", options=["None","One country", "Multiple countries"])

if viz_opt == "Multiple countries":
    countries = st.sidebar.multiselect("Select countries to visualize", data["area"].unique()) # displaying list of available countries , default option is an empty list for flow control
    
    if len(countries) > 1:
        years = multic_year_range(data, countries) # extracting available year range for the country selected
        low, high = st.sidebar.slider("Select years from the available period", min_value = min(years), max_value = max(years), value = (min(years), max(years))) # creating slider to retrieve desired period based on available years
        period_list = list(data["months"].unique())
        period_list.append("")
        period = st.sidebar.selectbox("Period to visualize", period_list, index = (len(period_list) - 1)) # period to display from slider , default option is an empty string for flow control
        
        if period != "":

            parsed_data = config_data_multi(data, countries, low, high, period) # extracting countries specific data based on current parameters
            fig = plot_multic(parsed_data, countries, low, high) # creating figure

            # TODO: extracting index of value of max and min anomalies ---- > CONTINUE WITH THIS. LAST MISSING PART
            #idxmax = parsed_data["Temperature Anomaly"].idxmax()
            # idxmin = parsed_data["Temperature Anomaly"].idxmin()

            if len(countries) < 4: # Decisions for responsiveness and better text representation
                st.header(f"Visualizing **LAND** temperature anomalies for **{' & '.join(countries)}**")
                st.subheader(f"Period: **{low}**-**{high}**, **{period}**")
                col1, col2 = st.beta_columns([3,1]) # creating display sections
                with col1:
                    st.plotly_chart(fig, use_container_width = True) # instantiating figure and sizing to container

            elif len(countries) >= 4:
                st.header(f"Visualizing **LAND** temperature anomalies for **many countries!**")
                st.subheader(f"Period: **{low}**-**{high}**, **{period}**")
                col1, col2 = st.beta_columns([3,1]) # creating display sections
                with col1:
                    st.plotly_chart(fig, use_container_width = True) # instantiating figure and sizing to container


elif viz_opt == "One country":
    country_list = list(data["area"].unique())
    country_list.append("")
    country = st.sidebar.selectbox("Select a country to visualize", country_list, index= (len(country_list) - 1)) # displaying list of available countries, default option is an empty string for flow control
    
    if country != "": # placeholder decision used for responsiveness and easier visualization 
        years = onec_year_range(data, country) # extracting available year range for the country selected
        low, high = st.sidebar.slider("Select years from the available period", min_value = min(years), max_value = max(years), value = (min(years), max(years))) # creating slider to retrieve desired period based on available years
        period_list = list(data["months"].unique())
        period_list.append("")
        period = st.sidebar.selectbox("Select period to visualize", period_list, index = (len(period_list) - 1)) # period to display from slider , default option is an empty string for flow control
        
        if period != "": # placeholder decision used for responsiveness and easier visualization 
            parsed_data = config_data_onec(data, country, low, high, period) # extracting country specific data based on current parameters
            # extracting max and min indexes
            idxmax = parsed_data["Temperature Anomaly"].idxmax()
            idxmin = parsed_data["Temperature Anomaly"].idxmin()
            st.header(f"Visualizing **LAND** temperature anomalies for **{country}**")
            st.subheader(f"Period: **{low}**-**{high}**, **{period}**")
            fig = plot_onec(parsed_data, low, high) # creating figure

            col1, col2 = st.beta_columns([4,1]) # creating display sections for better visualization. The syntax means the "portions" of the page width each col takes.

            with col1: # plot section
                st.plotly_chart(fig, use_container_width = True) # instantiating figure and sizing to container

            with col2: # small tables section
                st.write("Year of **max** temperature anomaly")
                if isinstance(parsed_data.loc[idxmax]["Temperature Anomaly"], np.float64) == True:
                    st.table(pd.DataFrame({parsed_data.loc[idxmax]["Year"]:parsed_data.loc[idxmin]["Temperature Anomaly"]}, index = ["Temp. Anomaly"]))
                else:
                    st.table(parsed_data.loc[idxmax]["Temperature Anomaly"])

                st.write("Year of **min** temperature anomaly")
                if isinstance(parsed_data.loc[idxmax]["Temperature Anomaly"], np.float64) == True:
                    st.table(pd.DataFrame({parsed_data.loc[idxmin]["Year"]:parsed_data.loc[idxmin]["Temperature Anomaly"]}, index = ["Temp. Anomaly"]))
                else:
                    st.table(parsed_data.loc[idxmin]["Temperature Anomaly"])
            
            # hold data at the bottom of the app
            with st.beta_expander(label = "Click to see data", expanded = False):
                st.dataframe(parsed_data.set_index("Year")["Temperature Anomaly"])
else:
    pass    