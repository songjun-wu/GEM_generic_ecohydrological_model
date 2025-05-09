import numpy as np
import pandas as pd
import os
from def_GEM import *
import GEM_tools




def gdal_read_raster(raster_path):
    ds = gdal.Open(raster_path)
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray().astype(np.float_)
    return data



spatial_path = Path.data_path + 'spatial/'
climate_path = Path.data_path + 'climate/'

nodata = -9999.0

chnmask = np.loadtxt(spatial_path + 'channel.asc', skiprows=6)

tmp = np.loadtxt(spatial_path + 'dem.asc', skiprows=6)

mask = tmp != nodata
unit_nodata = np.full(tmp.shape, nodata)
unit_soil = np.full(tmp.shape, nodata)
unit_soil[mask] = 1

unit_zero = np.copy(unit_soil)
unit_zero[unit_soil==1] = 0


GEM_tools.save_to_ascii(data=unit_zero, path=spatial_path+'climate_zones.asc', ref_path=spatial_path+'dem.asc')

tmpp = np.copy(unit_nodata)
tmpp[200,200] = 0
GEM_tools.save_to_ascii(data=tmpp, path=spatial_path+'Gauge_to_Report.asc', ref_path=spatial_path+'dem.asc')

weight_list = [50,            10,        1000,      0.3,      0.3, 0.0,    0.0,    0.0,      0.3,      0.3,     0.3,    20,
               0.3,   0.25,     0.2,     0.1,    0.15,     0.2,     0.5,    0.55,     0.6,       0.08,       0.06,      0.03,             1.2,            1.4,               1.6,
               10]
fnames = ['chnwidth', 'chndepth', 'chnlength', 'depth1', 'depth2', 'I', 'snow', 'pond', 'theta1', 'theta2', 'theta3', 'GW',
          'sand1', 'sand2', 'sand3', 'clay1', 'clay2', 'clay3', 'silt1', 'silt2', 'silt3', 'organic1', 'organic2', 'organic3', 'bulkdensity1', 'bulkdensity2', 'bulkdensity3',
          'Q']
for i in range(len(fnames)):
    weight = weight_list[i]
    fname = fnames[i]
    if 'chn' in fname or fname=='Q':
        #weights =  np.random.uniform(low=weight*0.9, high=weight*1.1, size=(unit_soil.shape))
        weights = np.full(unit_soil.shape, weight)
        data = np.copy(unit_nodata)
        data[chnmask==1] = weights[chnmask==1]
        GEM_tools.save_to_ascii(data=data, path=spatial_path+fname+'.asc', ref_path=spatial_path+'dem.asc')
    else:
        #weights =  np.random.uniform(low=weight*0.9, high=weight*1.1, size=(unit_soil.shape))
        weights = np.full(unit_soil.shape, weight)
        GEM_tools.save_to_ascii(data=unit_soil*weights, path=spatial_path+fname+'.asc', ref_path=spatial_path+'dem.asc')

p_cat_list = [1, 0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.06, 0.04]
for i in range(len(p_cat_list)):
    _data = []
    for j in range(5):
        p_cat = p_cat_list[i] * 1
        data = np.copy(unit_nodata)
        data[mask] = p_cat
        _data = np.append(_data, data.flatten())
        _data.tofile(spatial_path+'category_'+str(i)+'.bin')
        #GEM_tools.save_to_ascii(data=data, path=spatial_path+'category_'+str(i)+'.asc', ref_path=spatial_path+'dem.asc')

        tmp = np.fromfile(spatial_path+'category_'+str(i)+'.bin')




# Climate inputs
df = pd.read_excel('/home/wusongj/dmc/forHydrology/Climate/climate_daily_AM.xlsx')
df1 = pd.read_csv('/home/wusongj/dmc/forHydrology/Climate/climate_interpolated.csv')
(np.repeat(df['Rain_corr_mm_Tot'], 1).to_numpy() / 1000).tofile(climate_path+'P.bin')
np.repeat(df['AirT_C_Avg'], 1).to_numpy().tofile(climate_path+'Ta.bin')


(np.repeat(df['RelHumid'], 1).to_numpy() / 100).tofile(climate_path+'RH.bin')

np.repeat(df1['lai_2'], 1).to_numpy().tofile(climate_path+'LAI.bin')
(np.repeat(df['pet'], 1).to_numpy()/1000).tofile(climate_path+'PET.bin')
np.repeat(df1['d2H_14dMV_3015'], 1).to_numpy().tofile(climate_path+'d2h_P.bin')




