import pandas as pd
import numpy as np
import plotly.express as px
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
        
<<<<<<< HEAD:Climatevizv2.py
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
=======
    return data, f_years
>>>>>>> parent of f9d0f69 (final commit):Climateviz.py

########################################################## SLICING DATAFRAME SECTION ##########################################################

def config_data_onec(data = None, country = "Nicaragua", year_bottom = 1992, year_top = 2019, period = "January"):
        # creating sliced country dataframe
        ## instantiating limiting variables
    if data is None:
<<<<<<< HEAD:Climatevizv2.py
        raise FileNotFoundError("DATA NOT LOAD FAILURE, ENDING.")
=======
        raise FileNotFoundError("DATA NOT PROVIDED ENDING.")
>>>>>>> parent of f9d0f69 (final commit):Climateviz.py
    country =  country
    month = period
    start_year =  year_bottom
    end_year = year_top
        ## filtering
    country_data = data[(data["area"] == country) & (data["months"] == month)]
        ## transposing and deleting unnecesary data
    country_data = country_data.T
    country_data = country_data.drop(['area code','area','months','element code','element'], axis=0)
        ## reassigning column and adjusting type again
    country_data.columns = ["Temperature Anomaly", "Deviation of Anomaly"]
        ## filtering based on desired years
    country_data = country_data.loc[start_year:end_year]
        ## adding std limits
    country_data["+1 std"] = country_data["Temperature Anomaly"] + country_data["Deviation of Anomaly"]
    country_data["-1 std"] = country_data["Temperature Anomaly"] - country_data["Deviation of Anomaly"]
    country_data = country_data.astype("float")
        ## creating color map of result for easier plotting
    country_data["color"] = np.where(country_data["Temperature Anomaly"] > 0, "red", "blue")
        ## fixing index dtype
    country_data.index = country_data.index.astype(int)
    
    return country_data

<<<<<<< HEAD:Climatevizv2.py
def config_data_multi(data = None, country_list = [], year_bottom = 1992, year_top = 2019, period = "January"):
    if data is None:
        raise FileNotFoundError("DATA NOT LOAD FAILURE, ENDING.")
    pass

########################################################## PLOT SECTION ##########################################################
=======
>>>>>>> parent of f9d0f69 (final commit):Climateviz.py

########################################################## PLOT SECTION ##########################################################
'''
def plot_chart(country_data):

    # setting figsize and titles
    fig = plt.figure(figsize=(25,10))

    # setting X tick range dynamically and label
        # deprecated solution
        # ax = plt.gca()
        # ax.set_xticks("lowerbound", "upperbound", "step"))
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.set_xlabel("Year", fontdict = {"fontsize": 14})

    # setting Y tick range to a fixed lenght
    ax.set_ylim(-1,2)
    ax.set_ylabel("Temperature Anomaly", fontdict = {"fontsize": 14})

    # creating general line plot
    plt.plot(country_data.index, country_data["Temperature Anomaly"], alpha = 0.3, color = "black", label = "Temperature Anomaly")
    plt.plot(country_data.index, [0]*country_data.index.shape[0], color="black", linewidth = 1)

    
    # STD lines
    plt.plot(country_data.index, country_data["+1 std"], alpha = 0.2, color = "red", label = "+1 Standard dev")
    plt.plot(country_data.index, country_data["-1 std"], alpha = 0.2, color = "blue", label = "-1 Standard dev")
    plt.fill_between(country_data.index, y1 = country_data["+1 std"], y2 = country_data["-1 std"], alpha = 0.1, facecolor = "grey")
    

    # adding points above 0 in red and rest in blue
    plt.scatter(country_data.index, country_data["Temperature Anomaly"], c = country_data["color"], s = 50)

    # adding signal to the highest value in the plot
    plt.axhline(max(country_data["Temperature Anomaly"]), linestyle = "--", color = "red", linewidth = 1)

    plt.legend(loc = "upper center")

    return fig

fig_td = plot_chart(country_data)
plt.show()
'''