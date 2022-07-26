from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import numpy as np
#import pdb

filename = r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc'
#pdb.set_trace()
print('1')
fh = Dataset(filename)
lons = fh.variables['lon']
lats = fh.variables['lat']
#biom = fh.variables['lccs_class'][:].squeeze()
biom = fh.variables['lccs_class']
#with Dataset(filename, mode='r') as fh:
  # lons = fh.variables['lon'][:]
  # lats = fh.variables['lat'][:]
  # biom = fh.variables['lccs_class'][:].squeeze()
print('2')
lons_sub, lats_sub = np.meshgrid(lons[::4], lats[::4])
print('3')
coarse = Basemap.interp(biom[0,:,:], lons, lats, lons_sub, lats_sub, order=1)
print('4')