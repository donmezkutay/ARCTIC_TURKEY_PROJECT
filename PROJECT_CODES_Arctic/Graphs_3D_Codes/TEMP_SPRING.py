#!/usr/bin/env python
# coding: utf-8

# In[4]:


import xarray as xr
import netCDF4
import pandas as pd
from Arctic_Project import Arctic_Data
from Arctic_Project import Arctic_Vis
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
plt.rcParams['figure.figsize'] = 19, 12


data_sea_ice = pd.read_csv(r'C:\Users\Kutay\DATASPROJECT\dataset_adjusted\Sea_ice_extent_area.csv')
data_cfsrs = xr.open_dataset(r'C:\Users\Kutay\DATASPROJECT\dataset_adjusted\CFSR_1000MB_TEMP_NORTH_SPRING.nc')
data_cfsr_2011_2019 = xr.open_dataset(r'C:\Users\Kutay\DATASPROJECT\dataset_adjusted\2011_2020_CFSR_1000MBTEMP_SPRING.nc')


# In[ ]:





# In[5]:


#find anomaly for 1979-2009
seaice_average_1979 = Arctic_Data.wrap_seaice_1979_2009_average(data_sea_ice)
sea_ice_anomaly_1979 = Arctic_Data.compute_seaice_anomaly(seaice_average_1979,seaice_average_1979)

#find anomaly for 2010-2018
seaice_average_2010= Arctic_Data.wrap_seaice_2010_2018_average(data_sea_ice)
sea_ice_anomaly_2010 = Arctic_Data.compute_seaice_anomaly(seaice_average_2010,seaice_average_1979)


# In[6]:


season = 'spring'
var_name = 'TMP_L100_Avg'

# find 1979-2010 data each 10 years(
first_10_1980, first_20_1980, first_30_1980 = Arctic_Data.wrap_data_1980_2010(data_cfsrs, var_name=var_name, season=season)

# find 2010-2019 data 10 years
first_10_2011 = Arctic_Data.wrap_data_2011_2019(data_cfsr_2011_2019, var_name=var_name)


# In[7]:


#plotting first 10 years
decade = 'first'
year_interval = '80-89'
season = 'SPRI'
var_name = 'TEMP'
save_where = r'C:\Users\Kutay\DATASPROJECT\DATASET_WORKS\PICTURES\1000MBTEMPSEAICECORRELATION\1000MBTEMP_SPRING_1of10_ORTHOGRAPHIC.png'

mesh = Arctic_Vis.visualize_arctic(data=first_10_1980, 
                                   anomalyseaice=sea_ice_anomaly_1979,
                                   decade=decade,
                                   year_interval=year_interval,
                                   season=season,
                                   save_where=save_where,
                                   var_name=var_name)


# In[8]:


#plotting second 10 years
decade = 'second'
year_interval = '90-99'
season = 'SPRI'
var_name = 'TEMP'
save_where = r'C:\Users\Kutay\DATASPROJECT\DATASET_WORKS\PICTURES\1000MBTEMPSEAICECORRELATION\1000MBTEMP_SPRING_2of10_ORTHOGRAPHIC.png'


mesh = Arctic_Vis.visualize_arctic(data=first_20_1980, 
                                   anomalyseaice=sea_ice_anomaly_1979,
                                   decade=decade,
                                   year_interval=year_interval,
                                   season=season,
                                   save_where=save_where,
                                   var_name=var_name)


# In[9]:


#plotting third 10 years
decade = 'third'
year_interval = '00-10'
season = 'SPRI'
var_name = 'TEMP'
save_where = r'C:\Users\Kutay\DATASPROJECT\DATASET_WORKS\PICTURES\1000MBTEMPSEAICECORRELATION\1000MBTEMP_SPRING_3of10_ORTHOGRAPHIC.png'


mesh = Arctic_Vis.visualize_arctic(data=first_30_1980, 
                                   anomalyseaice=sea_ice_anomaly_1979,
                                   decade=decade,
                                   year_interval=year_interval,
                                   season=season,
                                   save_where=save_where,
                                   var_name=var_name)


# In[10]:


#plotting fourth 10 years
decade = 'first'
year_interval = '11-19'
season = 'SPRI'
var_name = 'TEMP'
save_where = r'C:\Users\Kutay\DATASPROJECT\DATASET_WORKS\PICTURES\1000MBTEMPSEAICECORRELATION\1000MBTEMP_SPRING_4of10_ORTHOGRAPHIC.png'


mesh = Arctic_Vis.visualize_arctic(data=first_10_2011, 
                                   anomalyseaice=sea_ice_anomaly_2010,
                                   decade=decade,
                                   year_interval=year_interval,
                                   season=season,
                                   save_where=save_where,
                                   var_name=var_name)


# In[ ]:




