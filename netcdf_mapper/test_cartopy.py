import cartopy.crs as ccrs
import cartopy

import salem

import matplotlib.pyplot as plt

from salem import wgs84

grid = salem.Grid(nxny=(360, 180), dxdy=(1, 1), x0y0=(0.0, 0.0), proj=wgs84)

print('1')
ccrs.PlateCarree()

central_lon, central_lat = -10, 45
extent = [-40, 20, 30, 60]
ax = plt.axes(projection=ccrs.Orthographic(central_lon, central_lat))
ax.set_extent(extent)
ax.gridlines()
ax.coastlines(resolution='50m')
print('2')

import xarray as xr
ds = xr.open_dataset(r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc')
print('3')

sst = ds['lccs_class'].isel(time=0)
sst = sst.salem.subset(corners=((-40., 20.), (30., 60.)), crs=salem.wgs84)
sst = sst.salem.subset(shape=shapes, margin=2)

print('4')
sst=sst.salem.lookup_transform(sst)
#fig = plt.figure(figsize=(9, 6))
#ax = plt.axes(projection=ccrs.Robinson())
#ax.coastlines()
#ax.gridlines()
print('4-2')
sst.plot(ax=ax, transform=ccrs.PlateCarree(),
         vmin=2, vmax=30, cbar_kwargs={'shrink': 0.4})
print('5')
plt.show()