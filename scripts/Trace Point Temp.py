# -*- coding: utf-8 -*-

from IPython import get_ipython
get_ipython().magic('clear')

import numpy as np
import xarray as xr
import pandas as pd

caves_coord = np.array([
    [-41.0184, -12.6182],  # Paixão Cave
    #[-46.35, -13.81],  # São Matheus
    [-56.58333, -21.08333],  # Jaragua (Novello et al., 2017)
    #[-44.281481, -19.495504],  # Gruta Rei do Mato
    #[-44.6281, -16.1503],  # Lapa Sem Fim
    #[-44.28, -14.37],  # Lapa Grande
    # [-55.45, -4.07],  # Paraiso (Wang et al., 2017)
    # [-37.6432, -5.5782],  # Caverna Rainha
    [-49.1569, -27.2247],  # Botuverá
    # [-48.403672, -24.635886],  # caverna do  Diabo
    # [-77.9, -5.7],  # Shatuca
    [-77.5, -5.733333],  # cueva del Diamante
    # [-75.82, -11.24], #Pacupahuain
    # [-39.33, -9.71], #Jeronimo
    # [-41.56, -12.38], #Diva e Ioio
    # [-69.82,  -35.80], #Brujas
    # [-73.750110, 6.333464], #Carracos
    # [-39.87, -15.74], #Abelhão
    # [-39.49, -15.77], #Deusdete
    # [-39.46, -15.79], #Nascente da gruna
    # [-39.36, -15.44], #Lapão
    # [-39.49, -15.76], #São Gotardo
    # [-44.06, -13.21], #Padre
    # [-46.41, -12.69], #Rãs
    # [-41.03, -12.58], #Marota
    # [-41.60, -12.33], #Lapa Doce
    # [-48.590932, -24.483756], #Casa de Pedra
    # [-37.924065, -10.651668] #Gruta do Bom Pastor
       ])
#%% Open the NetCDF File

temp_netcdf = xr.open_dataset(r"G:\Meu Drive\MBA ESALQ USP\TCC\Códigos\Trace 21ka\land\trace.01-36.22000BP.clm2.TSA.22000BP_decavg_400BCE.nc")
clim_temp = temp_netcdf['TSA'].values
clim_temp[clim_temp < 0] = np.nan
clim_temp = clim_temp-273
lon = np.round(temp_netcdf['lon'].values, 4)
lat = np.round(temp_netcdf['lat'].values, 4)

#%% Convert longitudes
def convert_longitude(lon):
    lon[lon > 180] -= 360
    return lon

lon = convert_longitude(lon)

#%% defines map and data spacial boundaries

xx1 = np.where(lon == -90)[0][0]
xx2 = np.where(lon == -11.25)[0][0]
yy1 = np.where(lat == 16.7001)[0][0]
yy2 = np.where(lat == -61.2316)[0][0]
temp1 = clim_temp[:, yy2:yy1, xx1:xx2]
lon1 = lon[xx1:xx2]
lat1 = lat[yy2:yy1]

#gerar dataframe
results = pd.DataFrame()

# loop cada caverna
for cave in caves_coord:
    lon_cave, lat_cave = cave

    lat_idx = np.abs(lat1 - lat_cave).argmin()
    lon_idx = np.abs(lon1 - lon_cave).argmin()
    temp_time_series = temp1[:, lat_idx, lon_idx]
    cave_name = f"Cave_{lat_cave}_{lon_cave}"
    results[cave_name] = temp_time_series

results['Time'] = temp_netcdf['time'].values

results.to_excel (r"G:\Meu Drive\MBA ESALQ USP\TCC\Códigos\Trace 21ka\land\Point_temp_extract_Trace21.csv", index = False)