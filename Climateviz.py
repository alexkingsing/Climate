#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# needed for dynamic axis
import matplotlib.ticker as ticker
# needed for multicolor line
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


# In[2]:


sns.set_theme(style="darkgrid")


# In[3]:


data = pd.read_csv("data/Environment_Temperature_change_E_All_Data_NOFLAG.csv", encoding= "latin1")
data.head()


# In[4]:


# ELIMINATING USELESS COLUMNS
data = data.drop(labels = ["Unit", "Months Code"], axis=1)


# In[5]:


# STANDARIZING COLUMN NAMES

# standard cleaning
data.columns = [column.lower().strip() for column in list(data.columns)]

# eliminating "Y" from year columns and casting them as integers
    ## retrieving years with "y"
years = [year for year in list(data.columns) if year[0] == "y"]
    ## creating fixed years
f_years = [year.replace("y","") for year in years]
    ## merging lists
mapped_years = zip(years, f_years)
    ## dictionary comprehension for creating new_cols dictionary. This is the argument of the name method
new_cols = {key:int(value) for key,value in mapped_years}
    ## executing rename
data = data.rename(columns = new_cols)
    ## cleaining temp variables
del years
del f_years
del mapped_years
del new_cols
data.head()


# In[6]:


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


# In[7]:


# CLEANING MONTHS NAMES
    ## Cleaning Quarters with encoding difficulties
data["months"] = data["months"].str.replace("\x96", "-")


# In[8]:


# creating sliced country dataframe
    ## instantiating limiting variables
country = "Nicaragua"
element = "Temperature change"
month = "April"
    ## filtering
country_data = data[(data["area"] == country) & (data["element"] == element) & (data["months"] == month)]
    ## transposing and deleting unnecesary data
country_data = country_data.T
country_data = country_data.drop(['area code','area','months','element code','element'], axis=0)
    ## reassigning column and adjusting type again
country_data.columns = [month]
country_data = country_data.astype("float")
    ## creating color map of result
country_data["color"] = np.where(country_data[month] > 0, "red", "blue")
    ## grouping by color as per https://stackoverflow.com/questions/33560789/seaborn-or-matplotlib-line-chart-line-color-depending-on-variable
color_country_data = country_data


# In[10]:


# setting figsize
plt.figure(figsize=(25,10))
plt.title(country + ", " + month + ", " + element, fontdict={'fontsize':20})
# setting tick range dynamically
    # deprecated solution
    # ax = plt.gca()
    # ax.set_xticks("lowerbound", "upperbound", "step"))
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))

# creating general line plot
plt.plot(country_data.index, country_data[month], alpha = 0.5)
plt.plot(country_data.index, [0]*country_data.index.shape[0], color="black", linewidth = 1)

# adding points above 0 in red
plt.scatter(country_data.index, country_data[month], c = country_data["color"])

plt.show()



