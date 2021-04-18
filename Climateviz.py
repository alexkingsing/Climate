import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# needed for dynamic axis
import matplotlib.ticker as ticker
import streamlit as st

sns.set_theme(style="whitegrid")

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

########################################################## SLICING DATAFRAME SECTION ##########################################################
def year_range(data, country = "Nicaragua"):
    country_data = data[(data["area"] == country)]
    country_data = country_data.T
    country_data = country_data.drop(index = ['area code','area','months','element code','element'])
    country_data = country_data.dropna()
    return country_data.index

########################################################## SLICING DATAFRAME SECTION ##########################################################

def config_data(data = None, country = "Nicaragua", year_bottom = 1992, year_top = 2019, period = "April"):
        # creating sliced country dataframe
        ## instantiating limiting variables
    if data is None:
        raise FileNotFoundError("DATA NOT PROVIDED, ENDING.")
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
    return country_data

########################################################## PLOT SECTION ##########################################################

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