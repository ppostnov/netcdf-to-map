import pandas as pd
import numpy as np
import xarray as xr
import geopandas as gpd
import salem
from salem.utils import get_demo_file

class MaskClipper:
    def __init__(self, nc_path, shape_path):
        self.data_set = salem.open_xr_dataset(nc_path)
        self.shape_path = salem.read_shapefile(shape_path)
        pass

    def create_variable(self, variable, timevalue):
        #t2 = ds.lccs_class.isel(time=0)
        self.var_to_analyze = self.data_set[variable].isel(time=timevalue)

    def subset(self):
        self.var_to_analyze = self.var_to_analyze.salem.subset(shape=self.shape_path, margin=2)

    def clip(self):
        self.var_to_analyze = self.var_to_analyze.salem.roi(shape=self.shape_path)

    def draw_map(self):
        self.map_object = self.var_to_analyze.salem.quick_map()
        self.map_object.visualize()
        #plt.show()

    def print_types(self):
        print(type(self.data_set), self.data_set)


nc_path = r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc'
shp_path = r"C:\NETCDF_PROJECT\storage\Belgorod\Adminbndy3.shp"
MC = MaskClipper(nc_path, shp_path)
MC.create_variable('lccs_class', 0)
MC.print_types()
MC.subset()
MC.clip()
MC.draw_map()


print('FUCK')
ds = salem.open_xr_dataset(r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc')

#ds = salem.open_xr_dataset(get_demo_file('wrfout_d01.nc'))
#shdf = salem.read_shapefile(get_demo_file(r"C:\NETCDF_PROJECT\storage\Belgorod\Adminbndy3.shp"))

shdf_bel = salem.read_shapefile(r"C:\NETCDF_PROJECT\storage\Belgorod\Adminbndy3.shp")

#shdf = salem.read_shapefile(get_demo_file('world_borders.shp'))
#print(type(shdf), shdf)
print(type(shdf_bel), shdf_bel)
#shdf = shdf.loc[shdf['CNTRY_NAME'].isin(['Nepal', 'Bhutan'])]
#print(type(shdf), shdf)

t2 = ds.lccs_class.isel(time=0)
#t2 = ds.T2.isel(Time=2)
#t2 = t2.salem.subset(shape=shdf, margin=2)
t2 = t2.salem.subset(shape=shdf_bel, margin=2)

#t2 = t2.salem.roi(shape=shdf)
t2 = t2.salem.roi(shape=shdf_bel)
print(t2)

smap=t2.salem.quick_map()
print(smap)
import matplotlib.pyplot as plt
plt.show()
smap.visualize()