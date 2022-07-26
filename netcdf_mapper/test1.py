#
# link: https://habr.com/ru/post/515328/

# чтобы геопандас работал без анаконды и прочего
# Качаем отсюда
# http://www.lfd.uci.edu/~gohlke/pythonlibs/
# GDAL и FIONA  подходящих версий
# Ставим их через pip install filename.whl
# потом ставим геопандас pip install geopandas
# а чтобы матплотлиб мог рисовать шейпы pip install descartes

import geopandas as gpd

from geopandas.geoseries import *
#p1 = Point(.5, .5)

#from shapely.geometry import Point, Polygon
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

path = r"C:\NETCDF_PROJECT\storage\Belgorod\Adminbndy3.shp"
data = gpd.read_file(path)

print(data.head())
data.plot()
plt.show()