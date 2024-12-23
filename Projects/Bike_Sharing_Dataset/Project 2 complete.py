# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 13:42:36 2024

@author: Humam
"""

#############################################   Loading Necessary Libraries   ######################################

import pandas as pd
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt

file=pd.read_csv("./BikeSharing Dataset.csv")
df=pd.DataFrame(file)

#I want to analyse the change in summary analytics after cleaning the data

describe_before=df.describe()

#################################################   Cleaning the Data Set   ########################################

###############################################   Dealing with Missing Values   ####################################

missing_values=df.isnull()
print(missing_values.sum(),"\n")
print("Percentage missing values: ",round(missing_values.sum().sum()/len(df)*100,2),"%")
df=df.dropna()

###########################################   Dealing with Duplicate Rows of Data   ################################

duplicated=df[df.duplicated()]
print(duplicated)
df=df.drop_duplicates()

##################################################   Dealing with Outliers   #######################################

numerical_columns=df.select_dtypes(include=[np.number]).columns
z_scores=zscore(df[numerical_columns])
outliers=(np.abs(z_scores)>3).any(axis=1)

# Categorize holidays to avoid outliers generated from the numerical values

z_scores=zscore(df['holiday'])
outliers=(np.abs(z_scores)>3)

print(df['holiday'][outliers])

holiday_mapping={
    0:'Not a Holiday',
    1:'Holiday'
    }

df['holiday'] = df['holiday'].replace(holiday_mapping)

numerical_columns=df.select_dtypes(include=[np.number]).columns
z_scores=zscore(df[numerical_columns])
outliers=(np.abs(z_scores)>3).any(axis=1)

print("Number of rows with outliers in the Bike Sharing Dataset: ",len(df[outliers]))
print("Percentage of outliers: ", round(len(df[outliers])/len(df)*100,2), "%")

# Visualizing using Boxplots to detect source of outliers

plt.figure(figsize=(12,8))

plt.subplot(2,2,1)
plt.boxplot(df['registered'], showfliers=True)
plt.xticks([1],labels=['registered'])

plt.subplot(2,2,2)
plt.boxplot(df['count'], showfliers=True)
plt.tight_layout()
plt.xticks([1],labels=['counts'])

plt.subplot(2,2,3)
plt.boxplot(df['casual'], showfliers=True)
plt.xticks([1],labels=['casual'])

plt.subplot(2,2,4)
plt.boxplot(df['windspeed'], showfliers=True)
plt.xticks([1],labels=['windspeed'])
plt.show()


plt.figure(figsize=(12,8))

plt.subplot(2,2,1)
plt.boxplot(df['temp'], showfliers=True)
plt.xticks([1],labels=['temp'])

plt.subplot(2,2,2)
plt.boxplot(df['hum'], showfliers=True)
plt.xticks([1],labels=['hum'])

plt.subplot(2,2,3)
plt.boxplot(df['atemp'], showfliers=True)
plt.xticks([1],labels=['atemp'])

plt.figure(figsize=(12,12))
plt.subplot(2,2,1)

z_scores=zscore(df['casual'])
outliers=(np.abs(z_scores)>3)

# Visulaizing outliers detected in boxplots using scatter plots

plt.scatter(df.index[~outliers], df['casual'][~outliers], marker='o', label='Non-outliers', color='blue')
plt.scatter(df.index[outliers], df['casual'][outliers], marker='x', label='Outliers', color='red')
plt.xticks(ticks=np.arange(0,1122, step=374),labels=['2011','2012','2013'])
plt.xlabel('Year')
plt.ylabel('Number of Casual Bike Users')
plt.legend()
plt.title('Casual bike in Washington D.C. use over 2011-2012')

print(df[outliers])

z_scores=zscore(df['windspeed'])
outliers=(np.abs(z_scores)>3)

plt.subplot(2,2,2)
plt.scatter(df.index[~outliers], df['windspeed'][~outliers], marker='o', label='Non-outliers', color='blue')
plt.scatter(df.index[outliers], df['windspeed'][outliers], marker='x', label='Outliers', color='red')
plt.xticks(ticks=np.arange(0,1122, step=374),labels=['2011','2012','2013'])
plt.xlabel('Year')
plt.ylabel('Wind Speed')
plt.title('Windspeed of Days in Washington D.C. from 2011-2012')
plt.legend()

print(df[outliers])

z_scores=zscore(df['temp'])
outliers=(np.abs(z_scores)>3)

plt.subplot(2,2,3)
plt.scatter(df.index[~outliers], df['temp'][~outliers], marker='o', label='Non-outliers', color='blue')
plt.scatter(df.index[outliers], df['temp'][outliers], marker='x', label='Outliers', color='red')
plt.xticks(ticks=np.arange(0,1122, step=374),labels=['2011','2012','2013'])
plt.xlabel('Year')
plt.ylabel('Temperature')
plt.title('Temperature of Days in Washington D.C. from 2011-2012')
plt.legend()

print(df[outliers])

z_scores=zscore(df['hum'])
outliers=(np.abs(z_scores)>3)

plt.subplot(2,2,4)
plt.scatter(df.index[~outliers], df['hum'][~outliers], marker='o', label='Non-outliers', color='blue')
plt.scatter(df.index[outliers], df['hum'][outliers], marker='x', label='Outliers', color='red')
plt.xticks(ticks=np.arange(0,1122, step=374),labels=['2011','2012','2013'])
plt.xlabel('Year')
plt.ylabel('Humidity')
plt.title('Humidity of Days in Washington D.C. from 2011-2012')
plt.legend()

print(df[outliers])

df=df.set_index('dteday')

# Imputing outliers assuming there was a recording error
# by normalizing the values given the data recording protocols
 
impute_temp=['19/11/2011','16/02/2012','18/12/2012']
for i in impute_temp:
    if i in df.index:
        df.loc[i, 'temp']=df.loc[i, 'temp']/41
        
        
impute_hum=['1/01/2011','2/04/2011','13/05/2011']
for i in impute_hum:
    if i in df.index:
        df.loc[i, 'hum']=df.loc[i, 'hum']/100


numerical_columns=df.select_dtypes(include=[np.number]).columns
z_scores=zscore(df[numerical_columns])
outliers=(np.abs(z_scores)>3).any(axis=1)

print("Percentage of outliers: ", round(len(df[outliers])/len(df)*100,2), "%")

df=df[~outliers]

# Determining the change of the dataset after cleaning to determine the impact on the dataset

describe_after = df.describe()


percentage_change = ((describe_after - describe_before) / describe_before) * 100

print("Descriptive Statistics Before Cleaning:")
print(describe_before)
print("\nDescriptive Statistics After Cleaning:")
print(describe_after)
print("\nPercentage Change:")
print(percentage_change)

######################################   Exploring the relations between variables   ###############################

total_registered=df['registered'].sum()
total_casual=df['casual'].sum()

# Investigating the porportion of casual and registered bike users 
# to better understand how the bike user population is divided

plt.figure(figsize=(12,8))
plt.pie([total_registered,total_casual],labels=['Registered','Casual'],autopct='%1.1f%%')
plt.title('Number of Registered vs. Casual Bike Users from 2011-2012')

###################################################################################################################

# Preliminary investigation in understanding how bike usage varies over time, considering no other variables

weekdays=df.groupby(['weekday'])
wvc=weekdays['count'].mean().sort_index()
weekday_mapping=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
index_mapping=dict(zip(wvc.index,weekday_mapping))
wvc.index=wvc.index.map(index_mapping)

plt.figure(figsize=(12,6))
plt.pie(wvc,labels=wvc.index, autopct='%1.1f%%')
plt.title('Distribution of Bikes over Days of the Week')

###################################################################################################################

# Investigating the shape of the registered bike users of the dataset 
# helps to understand future trends in the data

plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.hist(df['registered'],bins=10,edgecolor='black',density=True)
df['registered'].plot.kde(color='red')
plt.xlabel('Number of Registered Bikes')
plt.ylabel('Probability Density Estimate')
plt.title('Distribution of Registered Bikes')

###################################################################################################################

# Understanding the shape of the casual bike users of the dataset
# helps to understand future trends in the data

plt.subplot(1,2,2)
plt.hist(df['casual'],bins=10,edgecolor='black',density=True)
df['casual'].plot.kde(color='red')
plt.xlabel('Number of Casually Used Bikes')
plt.ylabel('Probability Density Estimate')
plt.title('Distribution of Casually Used Bikes')

###################################################################################################################

# Understanding thedistribution of weather events over the last 2 years from the dataset
# This will be helpful to understand the relationship between bike users and the weather situation later

weather_count=df.groupby('weathersit').size()

plt.figure(figsize=(12,8))
plt.pie(weather_count, labels=['Clear','Overcast','Obscured'],autopct='%1.1f%%')
plt.title('Distribution of Weather Situations from 2011-2012')

###################################################################################################################

# Here we are creating a subset dataframe wto understand the distribution of weather situation in seasons
# We know that weather changes with seasons, as the scatter plots before demonstrate seasonal trends it may be 
# weather related

s_weather=df.groupby(['season','weathersit']).size()

s_data = {
    'Clear': [107,109,135,102],
    'Overcast': [63,67,46,65],
    'Obscured': [3,3,4,9],  
}


df_season = pd.DataFrame(s_data, index=[1,2,3,4])
df_season.index.name = 'season'
df_season.plot(kind="bar",figsize=(8,4))
plt.xlabel('Season')
plt.ylabel('Number of Days')
plt.title('Number of days of each weather situation and their months from 2011-2012')
plt.xticks([0,1,2,3], labels=['Springer','Summer','Fall','Winter'],rotation=0)

###################################################################################################################

# A quick insight into the relationship between temperature and bike usage, we do this before we begin to 
# do more deep analysis, also temperature also varied with season

plt.figure(figsize=(12,6))

plt.scatter(df['temp'], df['count'])
plt.xlabel('Normalized Temperature')
plt.ylabel('Number of Bikes Used')
plt.title('Number of Bikes Used at Different Temperatures from 2011-2012')


###############################################   Correlation index   ##############################################

#Remapping the holiday using a likert scale to understand the relationship between holiday and bike usage

holiday_mapping={
    'Not a Holiday':0,
    'Holiday':1
    }

df['holiday'] = df['holiday'].replace(holiday_mapping)
correlation=df.corr(method='pearson')
fig, ax = plt.subplots(figsize=(14,14))
im = ax.imshow(correlation, interpolation='nearest',cmap='coolwarm')
fig.colorbar(im, orientation='vertical', fraction = 0.05)
plt.title('Correlation Matrix')
plt.xticks(np.arange(0,14,1), labels=df.columns, rotation=20)
plt.yticks(np.arange(0,14,1), labels=df.columns)


for i in range(len(df.columns)):
    for j in range(len(df.columns)):
        text = ax.text(j, i, round(correlation.to_numpy()[i, j], 1),
                       ha="center", va="center", color="black")

#######################################   Linking Weather, Weekday and Bike Usage   ################################

g_weather = df.groupby(['weathersit', 'weekday'])['count'].mean()
w_data = {
    'Sunday': [4317.753425, 4040.433333, 1027.000000],
    'Monday': [4485.651515, 4183.888889, 1393.500000],
    'Tuesday': [4980.606557, 3899.605263, 2887.500000],
    'Wednesday': [5334.328125, 3744.375000, 1414.666667],
    'Thursday': [5064.800000, 4310.303030, 1383.333333],
    'Friday': [5078.682540, 4171.605263, 0.000000], 
    'Saturday': [4874.118644, 4042.133333, 2012.500000]
}


df_weather = pd.DataFrame(w_data, index=[1,2,3])
df_weather.index.name = 'weathersit'
df_weather.plot(kind="bar",figsize=(8,4))
plt.xlabel('Weather Situation')
plt.ylabel('Mean Number of Bikes Used')
plt.title('Mean of Bikes Used per day in Different Weather Situations')
plt.xticks([0,1,2], labels=['Clear','Overcast','Obscuring'],rotation=0)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()

##########################################   Change of Bike Usage Over the Years   #################################

g_yr=df.groupby('yr')['count'].agg(['mean','median'])

print(g_yr)

g_yr.plot(kind="bar",figsize=(8,4))

plt.xlabel('Year')
plt.ylabel('Number of Bikes Used')
plt.title('Mean and Median of Bikes Used per Year')
plt.xticks([0,1], labels=['2011','2012'],rotation=0)

####################################   Change of Bike Usage over Seasons with Variation   ##########################

g_season = df.groupby('season')['count'].agg(['std', 'count','mean'])
g_season['std_err'] = g_season['std'] / np.sqrt(g_season['count'])


plt.figure(figsize=(12,8))

plt.bar(g_season.index, g_season['mean'], yerr=g_season['std_err'], capsize=5, color='skyblue', edgecolor='black')

plt.xlabel('Season')
plt.ylabel('Number of Bikes Used')
plt.title('Bikes Used by Season with Standard Deviation')
plt.xticks([1,2,3,4], labels=['Springer','Summer','Fall', 'Winter'])

