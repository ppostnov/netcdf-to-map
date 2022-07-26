import pandas as pd
import numpy as np
import xarray as xr
import geopandas as gpd
from netCDF4 import Dataset

from rasterio import features
from affine import Affine

def transform_from_latlon(lat, lon):
    """ input 1D array of lat / lon and output an Affine transformation
    """
    lat = np.asarray(lat)
    lon = np.asarray(lon)
    trans = Affine.translation(lon[0], lat[0])
    scale = Affine.scale(lon[1] - lon[0], lat[1] - lat[0])
    return trans * scale

def rasterize(shapes, coords, latitude='latitude', longitude='longitude',
              fill=np.nan, **kwargs):
    """Rasterize a list of (geometry, fill_value) tuples onto the given
    xray coordinates. This only works for 1d latitude and longitude
    arrays.

    usage:
    -----
    1. read shapefile to geopandas.GeoDataFrame
          `states = gpd.read_file(shp_dir+shp_file)`
    2. encode the different shapefiles that capture those lat-lons as different
        numbers i.e. 0.0, 1.0 ... and otherwise np.nan
          `shapes = (zip(states.geometry, range(len(states))))`
    3. Assign this to a new coord in your original xarray.DataArray
          `ds['states'] = rasterize(shapes, ds.coords, longitude='X', latitude='Y')`

    arguments:
    ---------
    : **kwargs (dict): passed to `rasterio.rasterize` function

    attrs:
    -----
    :transform (affine.Affine): how to translate from latlon to ...?
    :raster (numpy.ndarray): use rasterio.features.rasterize fill the values
      outside the .shp file with np.nan
    :spatial_coords (dict): dictionary of {"X":xr.DataArray, "Y":xr.DataArray()}
      with "X", "Y" as keys, and xr.DataArray as values

    returns:
    -------
    :(xr.DataArray): DataArray with `values` of nan for points outside shapefile
      and coords `Y` = latitude, 'X' = longitude.


    """
    transform = transform_from_latlon(coords[latitude], coords[longitude])
    out_shape = (len(coords[latitude]), len(coords[longitude]))
    raster = features.rasterize(shapes, out_shape=out_shape,
                                fill=fill, transform=transform,
                                dtype=float, **kwargs)
    spatial_coords = {latitude: coords[latitude], longitude: coords[longitude]}
    return xr.DataArray(raster, coords=spatial_coords, dims=(latitude, longitude))

def add_shape_coord_from_data_array(xr_da, shp_path, coord_name):
    """ Create a new coord for the xr_da indicating whether or not it
         is inside the shapefile

        Creates a new coord - "coord_name" which will have integer values
         used to subset xr_da for plotting / analysis/

        Usage:
        -----
        precip_da = add_shape_coord_from_data_array(precip_da, "awash.shp", "awash")
        awash_da = precip_da.where(precip_da.awash==0, other=np.nan)
    """
    # 1. read in shapefile
    shp_gpd = gpd.read_file(shp_path)

    # 2. create a list of tuples (shapely.geometry, id)
    #    this allows for many different polygons within a .shp file (e.g. States of US)
    shapes = [(shape, n) for n, shape in enumerate(shp_gpd.geometry)]

    print(dir(xr_da))
    # 3. create a new coord in the xr_da which will be set to the id in `shapes`
    xr_da[coord_name] = rasterize(shapes, xr_da.coords,
                               longitude='longitude', latitude='latitude')

    return xr_da


#filename = r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc'
##pdb.set_trace()
#print('1')
#precip_da = Dataset(filename)

##print(precip_da)
#shp_dir = r"C:\NETCDF_PROJECT\storage\Belgorod\Adminbndy3.shp"
#awash = gpd.read_file(shp_dir)

#precip_da = add_shape_coord_from_data_array(precip_da, shp_dir, "awash")
##precip_da = add_shape_coord_from_data_array(precip_da, shp_dir, 'lccs_class')
#awash_da = precip_da.where(precip_da.awash==0, other=np.nan)
#awash_da.mean(dim="time").plot()


import rioxarray
import geopandas

#geodf = geopandas.read_file(r"C:\NETCDF_PROJECT\storage\Belgorod\Adminbndy3.shp")
#xds = xr.open_dataset(r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc')
#xds.rio.set_crs("epsg:4326")
#xds['lccs_class'].rio.to_raster(r'..\..\storage\test.tif')

#xds = rioxarray.open_rasterio(xds)
#clipped = xds.rio.clip(geodf.geometry.apply(mapping), geodf.crs)
#clipped = xds.rio.clip(geodf, geodf.crs)

import salem

from salem.utils import get_demo_file

ds = salem.open_xr_dataset(r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc')

#ds = salem.open_xr_dataset(get_demo_file('wrfout_d01.nc'))

#shdf = salem.read_shapefile(get_demo_file(r"C:\NETCDF_PROJECT\storage\Belgorod\Adminbndy3.shp"))
shdf_bel = salem.read_shapefile(r"C:\NETCDF_PROJECT\storage\Belgorod\Adminbndy3.shp")
shdf = salem.read_shapefile(get_demo_file('world_borders.shp'))
print(type(shdf), shdf)
print(type(shdf_bel), shdf_bel)
shdf = shdf.loc[shdf['CNTRY_NAME'].isin(['Nepal', 'Bhutan'])]
print(type(shdf), shdf)

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