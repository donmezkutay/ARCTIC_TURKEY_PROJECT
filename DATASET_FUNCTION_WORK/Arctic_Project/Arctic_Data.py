import matplotlib.pyplot as plt
import numpy as np
import scipy
import cartopy
import matplotlib  as mpl
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import xarray as xr
import netCDF4
import pandas as pd

#including 1979 and 2009 years.
def wrap_seaice_1979_2009_average(data_sea_ice):
    """returns winter sea ice values Autumn average time series between 1979 and 2009"""
    #divide data into as sep, oct and nov
    
    
    
    september = data_sea_ice[data_sea_ice['0'].isin(np.arange(1979,2010))
                                 & (data_sea_ice['1'] == 9)]['5'].values

    october = data_sea_ice[data_sea_ice['0'].isin(np.arange(1979,2010))
                               & (data_sea_ice['1'] == 10)]['5'].values

    november = data_sea_ice[data_sea_ice['0'].isin(np.arange(1979,2010))
                                & (data_sea_ice['1'] == 11)]['5'].values
        
    
        
        
    
    #get average of these 3 which means the Autumn value for sea ice
    average = (september+october+november)/3
    return average

#including 2010 and 2018 years.
def wrap_seaice_2010_2018_average(data_sea_ice):
    """returns winter sea ice values Autumn average time series between 2010 and 2018"""
    #divide data into as sep, oct and nov
    
    
    september = data_sea_ice[data_sea_ice['0'].isin(np.arange(2010,2019))
                                 & (data_sea_ice['1'] == 9)]['5'].values

    october = data_sea_ice[data_sea_ice['0'].isin(np.arange(2010,2019))
                               & (data_sea_ice['1'] == 10)]['5'].values

    november = data_sea_ice[data_sea_ice['0'].isin(np.arange(2010,2019))
                                & (data_sea_ice['1'] == 11)]['5'].values
    
   
        
    
    #get average of these 3 which means the Autumn value for sea ice
    average = (september+october+november)/3
    return average

def compute_seaice_anomaly(average, anomalies_list ):
    """returns the anomaly from given average time series and given anomaly data interval"""
    #find anomaly
    anomalyseaice = average - np.mean(anomalies_list)
    return anomalyseaice

#turn the base data into 
def wrap_data_1980_2010(data, var_name, season):
    """returns each 10 year interval for 1980-2010 interval"""
    #starting data from 1980 december through 2010 february
    
    #check which season
    if season == 'winter':
        data_cfsr = data[var_name][2:-1,:,:]
    if season == 'spring':
        data_cfsr = data[var_name][3:,:,:]
    
    #making a list includes each year's 3 winter months seperately listed for 30 years.
    data_30year_3month_list = [] 
    t = 0
    for i in range(31):

        dt = data_cfsr.isel(time = slice(t,t+3))
        t+=3
        data_30year_3month_list.append(dt)
        
    #getting the average of list's each element's 3 winter months. -->This corresponds to each years winter season
    data_30year_winter_list = []
    for i in range(31):
        a = data_30year_3month_list[i].mean(dim='time')
        data_30year_winter_list.append(a)
        
    #now let's compute the each 10 year interval (1980-1989), (1990-1999), (2000,2010)
    wintertimeseries1of10 = xr.concat(data_30year_winter_list[:10],dim='time')
    wintertimeseries2of10 = xr.concat(data_30year_winter_list[10:20],dim='time')
    wintertimeseries3of10 = xr.concat(data_30year_winter_list[20:31],dim='time')
    
    #now return each of these 10 year interval data to user
    return wintertimeseries1of10, wintertimeseries2of10, wintertimeseries3of10

def wrap_data_2011_2019(data, var_name):
    """returns 10 year interval for 2011-2019 interval"""
    #starting data from 2010 december through 2019 february
    
    data = data[var_name]
        
    #making a list includes each year's 3 winter months seperately listed for 30 years.
    data_30year_3month_list = [] 
    t = 0
    for i in range(9):

        dt = data.isel(time = slice(t,t+3))
        t+=3
        data_30year_3month_list.append(dt)
        
    #getting the average of list's each element's 3 winter months. -->This corresponds to each years winter season
    data_30year_winter_list = []
    for i in range(len(data_30year_3month_list)):
        a = data_30year_3month_list[i].mean(dim='time')
        data_30year_winter_list.append(a)
        
    #now let's compute the each 10 year interval (1980-1989), (1990-1999), (2000,2010)
    wintertimeseries1of10 = xr.concat(data_30year_winter_list, dim='time')
    #now return each of these 10 year interval data to user
    return wintertimeseries1of10