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

def visualize_arctic(data, anomalyseaice, decade, year_interval, season, save_where, var_name):
    """returns plot for arctic sea ice-data correlation map
       decade=which ten year is going to be plotted:(str)
                            decade can be 'first' or 
                                          'second'or
                                          'third'
        year_interval='80-89' etc.. string
        season = 'WINT' or 'SPRI' string
        save_where = 'string path for saving'
    """
    
    newdata = data.isel(time=0).copy()
    if decade == 'first':
        for lat in range(len(data['lat'])):
            for lon in range(len(data['lon'])):
                d = data.isel(lat=lat,lon=lon)
                corr = np.corrcoef(d,anomalyseaice[:10])
                newdata[lat,lon] = corr[0,1]
    elif decade == 'second':
        for lat in range(len(data['lat'])):
            for lon in range(len(data['lon'])):
                d = data.isel(lat=lat,lon=lon)
                corr = np.corrcoef(d,anomalyseaice[10:20])
                newdata[lat,lon] = corr[0,1]
    elif decade == 'third':
        for lat in range(len(data['lat'])):
            for lon in range(len(data['lon'])):
                d = data.isel(lat=lat,lon=lon)
                corr = np.corrcoef(d,anomalyseaice[20:31])
                newdata[lat,lon] = corr[0,1]
                
                
    import matplotlib.pyplot as plt
    
    

    lon_iso =newdata.lon[:].values
    lat_iso = newdata.lat[:].values

    fig = plt.figure()



    ax = fig.add_subplot(1,1,1, projection=cartopy.crs.Orthographic(central_longitude=0.0, central_latitude=30.0, globe=None))




        #ax.add_feature(cartopy.feature.LAKES.with_scale('10m'), linewidths = 0.7, zorder=10, facecolor='lightblue')

    #ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'), linewidths = 0.7,, facecolor='white')

        #ax.add_feature(cartopy.feature.STATES.with_scale('10m'), linewidths = 0.4,zorder=13)
    ax.add_feature(cartopy.feature.BORDERS.with_scale('10m') , linewidths = 0.55, zorder=13,)
    ax.add_feature(cartopy.feature.COASTLINE.with_scale('10m') , linewidths=1, zorder=14)
    ax.add_feature(cartopy.feature.LAND.with_scale('10m') ,facecolor='lightgrey')
    #ax.set_extent([0,360,30,89])

    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.35
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)

    #ax.set_boundary(circle, transform=ax.transAxes)

    tm=np.arange(-1,1.02,0.01)



    mesh2=ax.pcolormesh(lon_iso,lat_iso,newdata, cmap='bwr',
                        #gnuplot2
                          norm=mpl.colors.Normalize(vmin=-1, vmax=1),
                          transform = cartopy.crs.PlateCarree())#cmap = plt.cm.gist_earth_r )



    title = ax.text(0.,0.97,var_name,transform=ax.transAxes,fontsize=35, weight='bold')
    title1 = ax.text(0.,0.928,year_interval,transform=ax.transAxes,fontsize=35, weight='bold')
    title2 = ax.text(0.,0.886,season,transform=ax.transAxes,fontsize=35, weight='bold')
    title3 = ax.text(0.790,0.928,'Valid: Between {}'.format(year_interval),transform=ax.transAxes,fontsize=18,weight='bold')
    title4 = ax.text(0.790, 0.97, "Kutay & Berkay DONMEZ",transform=ax.transAxes, size=19,zorder=13,
                     bbox=dict(boxstyle="square",alpha=0.7,
                       ec='black',
                       fc='white',
                       ))

    cb = plt.colorbar(mesh2,fraction=0.0247 , pad=0.01 ,orientation='vertical', ticks=np.arange(-1,1.01,0.1))
    cb.ax.tick_params(labelsize=14)
    plt.savefig(save_where, bbox_inches='tight')
