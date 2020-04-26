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
import ARCTIC_ANOMALY_CALC

anomalyseaice = ARCTIC_ANOMALY_CALC.arctic_autumnal_anomaly()

def plot_winter_timeseries_ARCTIC(var):
    """ Return timeseries plot that includes Autumnal Arctic Sea Ice Anomalies and
        desired variable values for winter between the years 1979-2019
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
    elif var == 'PRECIPWATER':
        data_winter = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\CFSR_1979_2019_PRECIPWATER_winter.nc')  
        data_winter = data_winter['P_WAT_L200_Avg']
        plot_lim_A = 7
        plot_lim_B = 14
        plot_lim_sep = 1
        plot_title_ext = 'Precipitable Water(kg/m2)'
        plot_title = 'Precipitable Water(kg/m2)'
    #_____________________________________________________#
    #                     PROCESS1                        #
    #_____________________________________________________#
    #Set winter months dec,jan,feb seperately for 30 years in a list
    #1980[dec, jan, feb], 1981[dec, jan, feb]  NOTE:slice() funsction used be careful!
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
    elif var == 'PRECIPWATER':
        wintertimeseries_data_40years_turkey_mean_array = np.array(wintertimeseries_data_40years_turkey_mean.values)
    
    mean_for_plot_line = np.mean(wintertimeseries_data_40years_turkey_mean_array) 
    
    first_corr = np.corrcoef(anomalyseaice[0:10], wintertimeseries_data_40years_turkey_mean_array[0:10])
    first_corr = np.round(first_corr[0,1], 3)
    
    second_corr = np.corrcoef(anomalyseaice[10:20], wintertimeseries_data_40years_turkey_mean_array[10:20])
    second_corr = np.round(second_corr[0,1], 3)
    
    third_corr = np.corrcoef(anomalyseaice[20:31], wintertimeseries_data_40years_turkey_mean_array[20:31])
    third_corr = np.round(third_corr[0,1], 3)
    
    fourth_corr = np.corrcoef(anomalyseaice[31:40], wintertimeseries_data_40years_turkey_mean_array[31:40])
    fourth_corr = np.round(fourth_corr[0,1], 3)
    
    corr_full = np.corrcoef(anomalyseaice[:], wintertimeseries_data_40years_turkey_mean_array[:])

    plt.style.use('seaborn-white')
    plt.rcParams['figure.figsize'] = 19, 12
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    yearsall = np.arange(1979,2019)
    yearsall1 = np.arange(1980,2020)
    mesh1,=ax1.plot(yearsall1,anomalyseaice[:],color='blue')
    #mesh2,=ua_10_2006_2099['ua'].plot.line(ax=ax1,color='red')


    plt.ylabel('Sea Ice Area Anomaly', fontsize=15,weight='bold')
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
    plt.axvline(x = 2011, linewidth=0.4,color='k')
    plt.axvline(x = 2020, linewidth=0.4,color='k')

    ax2.tick_params(axis='y', labelsize=14)
    
    ####################
    
    # Set second x-axis
    ax3 = ax2.twiny()
    newlabel = [1974, 1979, 1984, 1989, 1994, 1999, 2004, 2009, 2014, 2019] # labels of the xticklabels: 
    ax3.set_xticklabels(newlabel)
    ax3.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
    ax3.xaxis.set_label_position('bottom') # set the position of the second x-axis to bottom
    ax3.spines['bottom'].set_position(('outward', 36))
    ax3.set_xlabel('Consecutive Years', fontsize=14, fontweight='bold')
    ax3.set_xlim(ax2.get_xlim())
    ax3.tick_params(axis='x', labelsize=14, color='red')
    #ax3.spines["bottom"].set_color("blue")
    #ax1.spines["bottom"].set_color("red")
    #ax2.spines["bottom"].set_color("red")
    ax1.tick_params(axis='x', colors='red')
    ax2.tick_params(axis='x', colors='red')
    ax3.tick_params(axis='x', colors='blue')
    
    ####################

    plt.legend([mesh1,  mesh2], ["Sea Ice Area Anomaly", "{}".format(plot_title_ext)],prop={'size': 17}, loc='lower center')

    title4 = ax1.text(0.12, 0.92,'1ºst Decade', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.13, 0.86, '(c : {})'.format(first_corr), transform=ax1.transAxes,fontsize=14, fontweight='bold')
    
    title4 = ax1.text(0.35, 0.92,'2ºnd Decade', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.365, 0.86,'(c : {})'.format(second_corr), transform=ax1.transAxes,fontsize=14, fontweight='bold')    
    
    title4 = ax1.text(0.59, 0.92,'3ºrd Decade', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.605, 0.86,'(c : {})'.format(third_corr), transform=ax1.transAxes,fontsize=14, fontweight='bold') 
    
    title4 = ax1.text(0.83, 0.92,'4ºrd Decade', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.85, 0.86,'(c : {})'.format(fourth_corr), transform=ax1.transAxes,fontsize=14, fontweight='bold') 

    title1 = ax1.text(0,1.03,'Autumn Arctic Sea Ice Anomaly And Turkey Regional Mean Winter {}'.format(plot_title),weight='bold',transform=ax1.transAxes,fontsize=20)

    title3 = ax1.text(0.917,1.03,'1980-2019',weight='bold',transform=ax1.transAxes,fontsize=19)
    plt.savefig(r'C:\Users\Lenovo\ML\Elcinhoca_proje\DATASET_WORKS\pictures\Sea_Ice_{}_Winter_Time_Series.png'.format(var) , bbox_inches='tight')
    

def plot_spring_timeseries_ARCTIC(var):
    """ Return timeseries plot that includes Autumnal Arctic Sea Ice Anomalies and
        desired variable values for spring between the years 1979-2019
        var : Desired variable to plot with Autumnal Arctic Sea Ice Anomaly (Given as str)
              (MSLP, 1000MBTEMP, SNWCOV, PRECIPWATER)
    """
    import matplotlib.pyplot as plt
    import numpy as np
    if var == 'MSLP':
        data_spring = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\CFSR_1979_2019_MSLP_spring.nc')
        data_spring = data_spring['PRMSL_L101_Avg'][3:,:,:] # Starts from 1980 march
        plot_lim_A = 1010
        plot_lim_B = 1020
        plot_lim_sep = 2
        plot_title_ext = 'Pressure(hPa)'
        plot_title = 'MSLP(hPa)'
    elif var == '1000MBTEMP':
        data_spring = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\CFSR_1979_2019_1000MBTEMP_spring.nc')  
        data_spring = data_spring['TMP_L100_Avg'][3:,:,:] # Starts from 1980 march
        plot_lim_A = 12
        plot_lim_B = 20
        plot_lim_sep = 1
        plot_title_ext = 'Temperature(ºC)'
        plot_title = '1000 mb Temperature(ºC)'
        
    elif var == 'PRECIPWATER':
        data_spring = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\CFSR_1979_2019_PRECIPWATER_spring.nc')  
        data_spring = data_spring['P_WAT_L200_Avg']
        plot_lim_A = 7
        plot_lim_B = 14
        plot_lim_sep = 1
        plot_title_ext = 'Precipitable Water(kg/m2)'
        plot_title = 'Precipitable Water(kg/m2)'
        
    #####elif var == 'SNOWCOV':
     #####   data_spring = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\CFSR_1979_2019_SNOWCOV_spring.nc')  
     #####   data_spring = data_spring['SNOWC_L1_FcstAvg6hr']
     #####   plot_lim_A = 0
     #####   plot_lim_B = 35
     #####   plot_lim_sep = 5
     #####   plot_title_ext = 'Snow Cover (%)'
     #####   plot_title = 'Snow Cover (%)'
    
    #_____________________________________________________#
    #                     PROCESS1                        #
    #_____________________________________________________#
    #Set winter months march,april,may seperately for 30 years in a list
    #1980[mart,nisan,mayıs], 1981[mart,nisan,mayıs]  NOTE:slice() funsction used be careful!
    data_spring_yearly_months = [] 
    time_iter = 0
    for i in range(41):

        dt = data_spring.isel(time = slice(time_iter,time_iter+3))
        time_iter+=3
        data_spring_yearly_months.append(dt)
    
    #_____________________________________________________#
    #                     PROCESS2                        #
    #_____________________________________________________#
    #Average value of each seperate year is calculated(i.e. ave(1979[mar,apr,may]), ave(1980[mar,apr,may]) ... )
    #It results in spring values for each year in each latitude and longitude
    data_spring_yearly = []
    for i in range(41):
        a = data_spring_yearly_months[i].mean(dim='time')
        data_spring_yearly.append(a)
        
    #_____________________________________________________#
    #                     PROCESS3                        #
    #_____________________________________________________#
    #Concat 40 seperate dataset with respect to time
    #From 1980 spring to 2019 spring
    springtimeseries_data_40years = xr.concat(data_spring_yearly[:-1],dim='time')
    springtimeseries_data_40years_turkey_mean = springtimeseries_data_40years.sel(lat=slice(42,36),lon=slice(26,45)).mean(dim=['lat','lon'])
    if var == 'MSLP':
        springtimeseries_data_40years_turkey_mean_array = np.array(springtimeseries_data_40years_turkey_mean.values)/100
    elif var == '1000MBTEMP':
        springtimeseries_data_40years_turkey_mean_array = np.array(springtimeseries_data_40years_turkey_mean.values)-273.15
    elif var == 'PRECIPWATER':
        springtimeseries_data_40years_turkey_mean_array = np.array(springtimeseries_data_40years_turkey_mean.values)
    
    mean_for_plot_line = np.mean(springtimeseries_data_40years_turkey_mean_array) 
    
    first_corr = np.corrcoef(anomalyseaice[0:10], springtimeseries_data_40years_turkey_mean_array[0:10])
    first_corr = np.round(first_corr[0,1], 3)
    
    second_corr = np.corrcoef(anomalyseaice[10:20], springtimeseries_data_40years_turkey_mean_array[10:20])
    second_corr = np.round(second_corr[0,1], 3)
    
    third_corr = np.corrcoef(anomalyseaice[20:31], springtimeseries_data_40years_turkey_mean_array[20:31])
    third_corr = np.round(third_corr[0,1], 3)
    
    fourth_corr = np.corrcoef(anomalyseaice[31:40], springtimeseries_data_40years_turkey_mean_array[31:40])
    fourth_corr = np.round(fourth_corr[0,1], 3)
    
    corr_full = np.corrcoef(anomalyseaice[:], springtimeseries_data_40years_turkey_mean_array[:])
    
    
    plt.style.use('seaborn-white')
    plt.rcParams['figure.figsize'] = 19, 12
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    yearsall = np.arange(1979,2019)
    yearsall1 = np.arange(1980,2020)
    mesh1,=ax1.plot(yearsall1,anomalyseaice[:],color='blue')
    #mesh2,=ua_10_2006_2099['ua'].plot.line(ax=ax1,color='red')


    plt.ylabel('Sea Ice Area Anomaly', fontsize=15,weight='bold')
    ax1.tick_params(axis='y', labelsize=14)
    ax1.tick_params(axis='x', labelsize=14)
    plt.yticks(np.arange(-2,1.6,0.5))
    plt.xticks(rotation=0)
    plt.axhline(y=0, linewidth=0.4)



    ax2 = ax1.twinx()
    mesh2,=ax2.plot(yearsall1,springtimeseries_data_40years_turkey_mean_array,color='red')

    plt.ylabel('{}'.format(plot_title_ext), fontsize=15,weight='bold')
    plt.yticks(np.arange(plot_lim_A,plot_lim_B,plot_lim_sep))                          
    plt.axhline(y=int(mean_for_plot_line), linewidth=0.4,color='red')

    plt.axvline(x = 1980, linewidth=0.4,color='k')
    plt.axvline(x = 1990, linewidth=0.4,color='k')
    plt.axvline(x = 2000, linewidth=0.4,color='k')
    plt.axvline(x = 2011, linewidth=0.4,color='k')
    plt.axvline(x = 2020, linewidth=0.4,color='k')

    ax2.tick_params(axis='y', labelsize=14)
    
    ####################
    
    # Set second x-axis
    ax3 = ax2.twiny()
    newlabel = [1974, 1979, 1984, 1989, 1994, 1999, 2004, 2009, 2014, 2019] # labels of the xticklabels: 
    ax3.set_xticklabels(newlabel)
    ax3.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
    ax3.xaxis.set_label_position('bottom') # set the position of the second x-axis to bottom
    ax3.spines['bottom'].set_position(('outward', 36))
    ax3.set_xlabel('Consecutive Years', fontsize=14, fontweight='bold')
    ax3.set_xlim(ax2.get_xlim())
    ax3.tick_params(axis='x', labelsize=14, color='red')
    #ax3.spines["bottom"].set_color("blue")
    #ax1.spines["bottom"].set_color("red")
    #ax2.spines["bottom"].set_color("red")
    ax1.tick_params(axis='x', colors='red')
    ax2.tick_params(axis='x', colors='red')
    ax3.tick_params(axis='x', colors='blue')
    
    ####################

    plt.legend([mesh1,  mesh2], ["Sea Ice Area Anomaly", "{}".format(plot_title_ext)],prop={'size': 17}, loc='lower center')

    title4 = ax1.text(0.12, 0.92,'1ºst Decade', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.13, 0.86, '(c : {})'.format(first_corr), transform=ax1.transAxes,fontsize=14, fontweight='bold')
    
    title4 = ax1.text(0.35, 0.92,'2ºnd Decade', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.365, 0.86,'(c : {})'.format(second_corr), transform=ax1.transAxes,fontsize=14, fontweight='bold')    
    
    title4 = ax1.text(0.59, 0.92,'3ºrd Decade', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.605, 0.86,'(c : {})'.format(third_corr), transform=ax1.transAxes,fontsize=14, fontweight='bold') 
    
    title4 = ax1.text(0.83, 0.92,'4ºrd Decade', transform=ax1.transAxes,fontsize=17)
    title4 = ax1.text(0.845, 0.86,'(c : {})'.format(fourth_corr), transform=ax1.transAxes,fontsize=14, fontweight='bold') 

    
    title1 = ax1.text(0,1.03,'Autumn Arctic Sea Ice Anomaly And Turkey Regional Mean Spring {}'.format(plot_title),weight='bold',transform=ax1.transAxes,fontsize=20)

    title3 = ax1.text(0.917,1.03,'1980-2019',weight='bold',transform=ax1.transAxes,fontsize=19)
    plt.savefig(r'C:\Users\Lenovo\ML\Elcinhoca_proje\DATASET_WORKS\pictures\Sea_Ice_{}_Spring_Time_Series.png'.format(var) , bbox_inches='tight')
    
