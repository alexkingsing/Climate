from numpy.core.fromnumeric import size
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

########################################################## DATA LOADING AND CLEANING SECTION ##########################################################

@st.cache
def load_data(path):
    data = pd.read_csv(path, encoding= "latin1")

    # ELIMINATING USELESS COLUMNS
    data = data.drop(labels = ["Unit", "Months Code"], axis=1)

    # STANDARIZING COLUMN NAMES

    # standard coumn cleaning cleaning
    data.columns = [column.lower().strip() for column in list(data.columns)]

    # eliminating "Y" from year columns and casting them as integers
        ## retrieving years with "y"
    years = [year for year in list(data.columns) if year[0] == "y"]
        ## creating fixed years
    f_years = [int(year.replace("y","")) for year in years]
        ## merging lists
    mapped_years = zip(years, f_years)
        ## dictionary comprehension for creating new_cols dictionary. This is the argument of the name method
    new_cols = {key:int(value) for key,value in mapped_years}
        ## executing rename
    data = data.rename(columns = new_cols)
        ## cleaining temp variables
    del years
    del mapped_years
    del new_cols

    # STANDARIZING COUNTRY NAMES
        ## extracting countries with paranthesis in their name and creating df
    country_df = data["area"].str.extract("(?P<country>.*)(?P<other>\(.*\))").dropna()
        ## eliminating annoying whitespace
    country_df["country"] = country_df["country"].str.strip()
        ## extracting indexes 
    indexes = (index for index in country_df.index)
        ## replacing indicated indeces in parent df
    for index in indexes:
        data.loc[index,"area"] = country_df.loc[index,"country"]

    # CLEANING MONTHS NAMES
        ## Cleaning Quarters with encoding difficulties
    data["months"] = data["months"].str.replace("\x96", "-")

    # ELIMINATING STANDARD DEVIATION
    data = data[data["element"] != "Standard Deviation"]
        
    return data

########################################################## RETRIVING AVAILABLE YEARS DATAFRAME SECTION ##########################################################
def onec_year_range(data = None, country = "Nicaragua"):
    if data is None:
        raise FileNotFoundError("ERROR LOADING DATA, ENDING.")
    country_data = data[(data["area"] == country)] # boolean masking based on country
    country_data = country_data.T # tranposing
    country_data = country_data.drop(index = ['area code','area','months','element code','element']) #dropping unnnecessary indexes
    country_data = country_data.dropna() # removing indexes with no data
    return country_data.index

def multic_year_range(data = None, countries = ["Nicaragua", "Costa Rica"] ):
    if data is None:
        raise FileNotFoundError("ERROR LOADING DATA, ENDING.")
    country_data = data[data["area"].apply(lambda x: x in countries)] # creating boolean mask by verifying if countries are inside the list
    country_data = country_data.T # tranposing
    country_data = country_data.drop(index = ['area code','area','months','element code','element']) #dropping unnnecessary indexes
    country_data = country_data.count(axis=1) # creating count of columns with data in them
    country_data = country_data[country_data >= 17] # removing all indexes where, for ANY country, there's no data
    return country_data.index

########################################################## SLICING DATAFRAME SECTION ##########################################################

def config_data_onec(data = None, country = "Nicaragua", year_bottom = 1992, year_top = 2019, period = "January"):
        # creating sliced country dataframe
        ## instantiating limiting variables
    if data is None:
        raise FileNotFoundError("DATA NOT LOAD FAILURE, ENDING.")
    country =  country
    month = period
    start_year =  year_bottom
    end_year = year_top
        ## filtering
    country_data = data[(data["area"] == country) & (data["months"] == month)]
        ## transposing and deleting unnecesary data. Final delete is the std dev.
    country_data = country_data.T
    country_data = country_data.drop(index = ['area code','area','months','element code','element'])
        ## reassigning column and adjusting type again
    country_data.columns = ["Temperature Anomaly"]
        ## filtering based on desired years
    country_data = country_data.loc[start_year:end_year]
    country_data = country_data.astype("float")
        ## creating color map of result for easier plotting
    country_data["color"] = np.where(country_data["Temperature Anomaly"] > 0, "red", "blue")
        ## fixing index dtype
    country_data.index = country_data.index.astype(int)
        ## setting index as column for plot purposes
    country_data = country_data.reset_index()
    country_data = country_data.rename(columns={"index":"Year"})
    return country_data

def config_data_multi(data = None, country_list = [], year_bottom = 1992, year_top = 2019, period = "January"):
    if data is None:
        raise FileNotFoundError("DATA NOT LOAD FAILURE, ENDING.")
    pass

########################################################## PLOT SECTION ##########################################################

def plot_onec(data):

    fig = go.Figure() # instantiate parent figure

    # create line to visualize actual data points
    fig.add_scatter(
    x = data["Year"], 
    y = data["Temperature Anomaly"], 
    mode="lines+markers", 
    marker=dict(
        color = data["color"],
        size = 10), 
    line=dict(color="grey")
    )

    # creating a reference line at 0
    fig.add_scatter(
    x = data["Year"],
    y = [0]*len(data), # instantiating a bunch of 0s
    mode = "lines",
    line = dict(
        color = "rgba(0, 43, 51, 0.3)", # setting color via RGB to set an alpha
        dash = "dash")
    )

    fig.update_layout(
        yaxis_title = "Temperature Anomaly",
        xaxis_title = "Year",
        xaxis = dict(
            tickmode = 'linear',
            tick0 = list(data["Year"])[0],
            dtick = 2), # setting ticks to be all years in the existing range for easier read
        font = dict(
            size=14),
        showlegend = False # hiding legend because its not needed here
        )
    
    return fig


''' DEPRECATED
def plot_chart(country_data, low = 1961, high = 2019):

    # setting figsize and titles
    fig = plt.figure()

    # setting X tick range dynamically and label
        # deprecated solution
        # ax = plt.gca()
        # ax.set_xticks("lowerbound", "upperbound", "step"))

    # setting a dynamic step size for visibility
    x_step = int((high - low) / 10)

    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_step))
    ax.set_xlabel("Year", fontdict = {"fontsize": 16})

    # setting Y tick range to a fixed lenght
    ax.yaxis.set_major_locator(ticker.MaxNLocator())
    ax.set_ylabel("Temperature Anomaly", fontdict = {"fontsize": 16})

    # creating general line plot
    plt.plot(country_data.index, country_data["Temperature Anomaly"], alpha = 0.3, color = "black", label = "Temperature Anomaly")
    plt.plot(country_data.index, [0]*country_data.index.shape[0], color="black", linewidth = 1)

    # adding points above 0 in red and rest in blue
    plt.scatter(country_data.index, country_data["Temperature Anomaly"], c = country_data["color"], s = 50)

    # adding signal to the highest and lowest values in the plot
    plt.axhline(country_data["Temperature Anomaly"].max(), linestyle = "--", color = "red", linewidth = 1)
    plt.axhline(country_data["Temperature Anomaly"].min(), linestyle = "--", color = "blue", linewidth = 1)

    return fig

'''