import xarray as xr
import numpy as np

def concat_winters(data1 , data2, var):
    """ Return concatted  CFSR dataset in which;
        1979-2010 winter dataset is concatted to the 2011-2019 winter dataset,
        with respect to the time dimension
        data1 : 1979-2010 winter dataset name without .nc (Given as str)
        data2 : 2011-2019 winter dataset name without .nc (Given as str)
        var : which variable that the dataset includes (Given as str)
              (MSLP, 1000MBTEMP, SNWCOV, PRECIPWATER )
    """
    
    data_winter_30 = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\{}.nc'.format(data1))
    data_winter_10 = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\{}.nc'.format(data2))
    concatted_data = xr.concat([data_winter_30,data_winter_10], dim='time')
    concatted_data = concatted_data.drop_sel(time = concatted_data['time'][-1].values)
    concatted.to_netcdf(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\CFSR_1979_2019_{}_winter.nc'.format(var))

def concat_springs(data1 , data2, var):
    """ Return concatted  CFSR dataset in which;
        1979-2010 winter dataset is concatted to the 2011-2019 spring dataset,
        with respect to the time dimension
        data1 : 1979-2010 spring dataset name without .nc (Given as str)
        data2 : 2011-2019 spring dataset name without .nc (Given as str)
        var : which variable that the dataset includes (Given as str)
              (MSLP, 1000MBTEMP, SNWCOV, PRECIPWATER )
    """
    
    data_spring_30 = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\{}.nc'.format(data1))
    data_spring_10 = xr.open_dataset(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\{}.nc'.format(data2))
    concatted_data = xr.concat([data_spring_30,data_spring_10], dim='time')
    concatted.to_netcdf(r'C:\Users\Lenovo\ML\Elcinhoca_proje\dataset_adjusted\CFSR_1979_2019_{}_spring.nc'.format(var))
