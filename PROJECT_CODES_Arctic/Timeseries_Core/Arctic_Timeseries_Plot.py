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

#To find autumnal arctic anomaly we import ARCTIC_ANOMALY_CALC.py which contains function that calculates autumnal arctic anomaly
import .ARCTIC_ANOMALY_CALC

anomalyseaice = ARCTIC_ANOMALY_CALC.arctic_autumnal_anomaly()

def plot_winter_timeseries_ARCTIC(var):
    """ Return timeseries plot that includes Autumnal Arctic Sea Ice Anomalies and
        desired variable values between the years 1979-2019
        var : Desired variable to plot with Autumnal Arctic Sea Ice Anomaly (Given as str)
              (MSLP, 1000MBTEMP, SNWCOV, PRECIPWATER)
    """
    import matplotlib.pyplot as plt
    import numpy as np
    if var == 'MSLP':
        data_winter = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\CFSR_1979_2019_MSLP_winter.nc')
        data_winter = data_winter['PRMSL_L101_Avg']
        plot_lim_A = 1015
        plot_lim_B = 1026
        plot_lim_sep = 2
        plot_title_ext = 'Pressure(hPa)'
        plot_title = 'MSLP(hPa)'
    elif var == '1000MBTEMP':
        data_winter = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\CFSR_1979_2019_1000MBTEMP_winter.nc')  
        data_winter = data_winter['TMP_L100_Avg']
        plot_lim_A = 5
        plot_lim_B = 12
        plot_lim_sep = 1
        plot_title_ext = 'Temperature(ºC)'
        plot_title = '1000 mb Temperature(ºC)'
    #####elif var == 'SNOWCOV':
     #####   data_winter = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\CFSR_1979_2019_SNOWCOV_winter.nc')  
     #####   data_winter = data_winter['SNOWC_L1_FcstAvg6hr']
     #####   plot_lim_A = 0
     #####   plot_lim_B = 35
     #####   plot_lim_sep = 5
     #####   plot_title_ext = 'Snow Cover (%)'
     #####   plot_title = 'Snow Cover (%)'
    #_____________________________________________________#
    #                     PROCESS1                        #
    #_____________________________________________________#
    #Set winter months dec,jan,feb seperately for 30 years in a list
    #1980[mart,nisan,mayıs], 1981[mart,nisan,mayıs]  NOTE:slice() funsction used be careful!
    data_winter_yearly_months = [] 
    time_iter = 0
    for i in range(41):

        dt = data_winter.isel(time = slice(time_iter,time_iter+3))
        time_iter+=3
        data_winter_yearly_months.append(dt)
        
    #_____________________________________________________#
    #                     PROCESS2                        #
    #_____________________________________________________#
    #Average value of each seperate year is calculated(i.e. ave(1979[dec,jan,feb]), ave(1980[dec,jan,feb]) ... )
    #It results in winter values for each year in each latitude and longitude
    data_winter_yearly = []
    for i in range(41):
        a = data_winter_yearly_months[i].mean(dim='time')
        data_winter_yearly.append(a)
    
    #_____________________________________________________#
    #                     PROCESS3                        #
    #_____________________________________________________#
    #Concat 31 seperate dataset with respect to time
    #From 1980 winter to 2019 winter
    wintertimeseries_data_40years = xr.concat(data_winter_yearly[:-1],dim='time')
    wintertimeseries_data_40years_turkey_mean = wintertimeseries_data_40years.sel(lat=slice(42,36),lon=slice(26,45)).mean(dim=['lat','lon'])
    if var == 'MSLP':
        wintertimeseries_data_40years_turkey_mean_array = np.array(wintertimeseries_data_40years_turkey_mean.values)/100
    elif var == '1000MBTEMP':
        wintertimeseries_data_40years_turkey_mean_array = np.array(wintertimeseries_data_40years_turkey_mean.values)-273.15
    #####elif var == 'SNOWCOV':
        #####wintertimeseries_data_40years_turkey_mean_array = np.array(wintertimeseries_data_40years_turkey_mean.values)
    
    mean_for_plot_line = np.mean(wintertimeseries_data_40years_turkey_mean_array) 
    
    #_____________________________________________________#
    #                     PROCESS4                        #
    #_____________________________________________________#
    
    plt.style.use('seaborn-white')
    plt.rcParams['figure.figsize'] = 19, 12
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    yearsall = np.arange(1979,2019)
    yearsall1 = np.arange(1980,2020)
    mesh1,=ax1.plot(yearsall,anomalyseaice[:],color='blue')
    #mesh2,=ua_10_2006_2099['ua'].plot.line(ax=ax1,color='red')


    plt.ylabel('Sea Ice Area Anomaly', fontsize=15,weight='bold')
    plt.xlabel('Year', fontsize=15,weight='bold')
    ax1.tick_params(axis='y', labelsize=14)
    ax1.tick_params(axis='x', labelsize=14)
    plt.yticks(np.arange(-2,1.6,0.5))
    plt.xticks(rotation=0)
    plt.axhline(y=0, linewidth=0.4)



    ax2 = ax1.twinx()
    mesh2,=ax2.plot(yearsall1,wintertimeseries_data_40years_turkey_mean_array,color='red')

    plt.ylabel('{}'.format(plot_title_ext), fontsize=15,weight='bold')
    plt.yticks(np.arange(plot_lim_A,plot_lim_B,plot_lim_sep))                          
    plt.axhline(y=int(mean_for_plot_line), linewidth=0.4,color='red')

    plt.axvline(x = 1980, linewidth=0.4,color='k')
    plt.axvline(x = 1990, linewidth=0.4,color='k')
    plt.axvline(x = 2000, linewidth=0.4,color='k')
    plt.axvline(x = 2010, linewidth=0.4,color='k')
    plt.axvline(x = 2020, linewidth=0.4,color='k')

    ax2.tick_params(axis='y', labelsize=14)

    plt.legend([mesh1,  mesh2], ["Sea Ice Area Anomaly", "{}".format(plot_title_ext)],prop={'size': 17}, loc='lower center')

    title4 = ax1.text(0.12, 0.92,'1ºst Ten Years', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.35, 0.92,'2ºnd Ten Years', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.58, 0.92,'3ºrd Ten Years', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.81, 0.92,'4ºrd Ten Years', transform=ax1.transAxes,fontsize=17)

    title1 = ax1.text(0,1.03,'Autumn Arctic Sea Ice Anomaly And Turkey Regional Mean Winter {}'.format(plot_title),weight='bold',transform=ax1.transAxes,fontsize=20)

    title3 = ax1.text(0.917,1.03,'1980-2019',weight='bold',transform=ax1.transAxes,fontsize=19)
    plt.savefig(r'C:\Users\Lenovo\ML\Elcinhoca_proje\DATASET_WORKS\pictures\Sea_Ice_{}_Winter_Time_Series.png'.format(var) , bbox_inches='tight')
