#To find autumnal arctic anomaly we import ARCTIC_ANOMALY_CALC.py which contains function that calculates autumnal arctic anomaly
import ARCTIC_ANOMALY_CALC
# To plot time series we import Arctic_Timeseries_Plot which contains functions for plotting 
import Arctic_Timeseries_Plot

anomalyseaice = ARCTIC_ANOMALY_CALC.arctic_autumnal_anomaly()
MSLP_winterplotter = Arctic_Timeseries_Plot.plot_winter_timeseries_ARCTIC('MSLP')
MSLP_springplotter = Arctic_Timeseries_Plot.plot_spring_timeseries_ARCTIC('MSLP')
TEMP1000MB_winterplotter = Arctic_Timeseries_Plot.plot_winter_timeseries_ARCTIC('1000MBTEMP')
TEMP1000MB_springplotter = Arctic_Timeseries_Plot.plot_spring_timeseries_ARCTIC('1000MBTEMP')
