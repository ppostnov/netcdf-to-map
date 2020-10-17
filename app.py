"""
    versions for netcdf files:
        1992-2015 = v2.0.7cds
        2016-2018 = v2.1.1

"""

import urllib3
import warnings
from netcdf_mapper import Absorber

warnings.simplefilter('ignore')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

absorber = Absorber()
absorber.file.download(
    '2009',
    'netcdf_2009',
    'v2.0.7cds'
    )
absorber.file.unzip('netcdf_2009')

# route to data path
nc_path = 'data\\netcdf\\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2009-v2.0.7cds.nc'
shp_path = [
    'data\\shape\\regions\\szfo\\Arkhangelskaya_oblast.shp',
    'data\\shape\\regions\\szfo\\Kirovskaya_oblast.shp'
]

absorber.execute(nc_path, shp_path)
