# -*- coding: utf-8 -*-
"""
Created on Wed May  1 22:39:47 2024

@author: Humam
"""

import pandas as pd

df=pd.read_csv('./nsw_road_crash_data_2016-2020_crash.csv')
    
########################################################################
# Here we count the total number of deaths on certain days of the week.         
########################################################################

weekday_sums=[]

#Make list to collect sums

l_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']

for d1 in l_days:
    
    df1=df[df["Day of week of crash" ]==d1]
    
    #counts deaths on a given day
   
    weekday_sums.append({'Weekday':d1,
                         'No. of People Killed':df1['No. killed'].sum()
                         })
    
df_days = pd.DataFrame(weekday_sums)
df_days=df_days.set_index('Weekday')
df_days.loc['total']= df_days.sum()

print("Number of Crashes on each Weekday between 2016-2020 in NSW\n \n", df_days)

df_days.to_csv('Days_and_Crashes')

###################################################################################
# Here we examine the effect of lighting on rate of injury and death in an accident        
###################################################################################

lighting_sums=[]

l_light = [ 'Dawn', 'Daylight', 'Dusk', 'Darkness']
  
for d1 in l_light:
    
    df1=df[df["Natural lighting" ]==d1]    
    
    killed=df1['No. killed'].sum()
   
    no_killed=df1['No. killed'].sum()/len(df1)
    
    no_injured=df1['No. seriously injured'].sum()/len(df1)
    
    lighting_sums.append({'Lighting':d1,
                     'No. of People Killed': killed,
                     '% of People Killed': f"{round(no_killed*100,2)}%",
                     '% of People Seriously Injured': f"{round(no_injured*100,2)}%"
                     })    

df_light= pd.DataFrame(lighting_sums)

print(df_light)

df_light.to_csv('Lighting_Conditons_and_Crashes', index=False)

##############################################################
# Impact of surface conditions on the rate of death and injury       
##############################################################

#The only categories for surface conditions are dry, wet, snow or ice.  

surface_sums=[]

l_wet = [ 'Dry', 'Wet', 'Snow or ice']

for d1 in l_wet:
    
    df1=df[df['Surface condition'  ]==d1]
    
    killed=df1['No. killed'].sum()
    
    no_killed=df1['No. killed'].sum()/len(df1)
    
    no_injured=df1['No. seriously injured'].sum()/len(df1)
    
    surface_sums.append({'Surface condition':d1,
                     'No. of People Killed': killed,
                     '% of People Killed': f"{round(no_killed*100,2)}%",
                     '% of People Seriously Injured': f"{round(no_injured*100,2)}%"
                     }) 

df_surface= pd.DataFrame(surface_sums)

print(df_surface)
   
df_surface.to_csv('Surface_Conditions_and_Crashes', index=False)

#####################################################################
# Invetigating the impact of weather on the rate of death and injury        
#####################################################################

#The only categories for weather conditions are Fine, Raining, Overcast, Fog or mist.

condition_sums=[]

l_weather = ['Fine', 'Raining', 'Overcast', 'Fog or mist']

for d1 in l_weather:
    
    df1=df[df['Weather']==d1]    
    
    killed=df1['No. killed'].sum()
    
    no_killed=df1['No. killed'].sum()/len(df1)
    
    no_injured=df1['No. seriously injured'].sum()/len(df1)
    
    condition_sums.append({'Weather Condition':d1,
                     'No. of People Killed': killed,
                     '% of People Killed': f"{round(no_killed*100,2)}%",
                     '% of People Seriously Injured': f"{round(no_injured*100,2)}%"
                     }) 

df_condition= pd.DataFrame(condition_sums)

print(df_condition)

df_condition.to_csv('Weather_Conditon_and_Crashes', index=False)

#################################################
# Impact of speed on the rate of death and injury        
#################################################

speeds=[]

l_speed = ['10 km/h','20 km/h','30 km/h','40 km/h','50 km/h','60 km/h','70 km/h','80 km/h','90 km/h','100 km/h','110 km/h']

for d1 in l_speed:
    
    df1=df[df['Speed limit'  ]==d1]    
    killed=df1['No. killed'].sum()
    no_killed=df1['No. killed'].sum()/len(df1)
    
    no_injured=df1['No. seriously injured'].sum()/len(df1)
    
    speeds.append({'Speed':d1,
                     'No. of People Killed': killed,
                     '% of People Killed': f"{round(no_killed*100,2)}%",
                     '% of People Seriously Injured': f"{round(no_injured*100,2)}%"
                     })
    
df_speeds= pd.DataFrame(speeds)

print(df_speeds)

df_speeds.to_csv('Speeds_and_Crashes', index=False)



    


