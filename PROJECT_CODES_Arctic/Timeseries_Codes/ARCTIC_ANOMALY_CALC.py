import numpy as np
import xarray as xr
import netCDF4
import pandas as pd

def arctic_autumnal_anomaly():
    """ Returns Autumnal Arctic Sea Ice Anomaly time series between 1979-2019
        With respect to the 30 years average value(1979-2009)
        
    """
    # Get the Data
    data_sea_ice = pd.read_csv(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\Sea_ice_extent_area_refined.csv')
    data_sea_ice.set_index('year', inplace=True)
    
    # Create masks that corresponds to the months of September, October, November between 1979-2010(2010 is not included!)
    mask_september_foranomaly = data_sea_ice[data_sea_ice['month']==9].index.isin(np.arange(1979,2010))
    mask_october_foranomaly = data_sea_ice[data_sea_ice['month']==10].index.isin(np.arange(1979,2010))
    mask_november_foranomaly = data_sea_ice[data_sea_ice['month']==11].index.isin(np.arange(1979,2010))
    
    # Pulling Autumn Months from the Dataset for anomaly  calculation using masks
    september_foranomaly = data_sea_ice[data_sea_ice['month']==9][mask_september_foranomaly]['area'].values # 30 year values
    october_foranomaly = data_sea_ice[data_sea_ice['month']==10][mask_october_foranomaly]['area'].values # 30 year values
    november_foranomaly = data_sea_ice[data_sea_ice['month']==11][mask_november_foranomaly]['area'].values # 30 year values

    september = data_sea_ice[data_sea_ice['month']==9]['area'][:-1].values # 40 year values 
    october = data_sea_ice[data_sea_ice['month']==10]['area'][:-1].values # 40 year values
    november = data_sea_ice[data_sea_ice['month']==11]['area'][:-1].values # 40 year values

    #Get the Averages for the usage of anomaly
    average_yearly_foranomaly = (september_foranomaly+october_foranomaly+november_foranomaly)/3 # average time series for 30yr
    average_yearly = (september+october+november)/3 # time series of yearly average values for 40 yr for the use of anomalies
    average_foranomaly = np.mean(average_yearly_foranomaly) #30 year average for the use of anomaly [1979,2010](2010 is not included)
    sea_ice_anomalies = average_yearly - average_foranomaly # anomaly values
    
    return sea_ice_anomalies