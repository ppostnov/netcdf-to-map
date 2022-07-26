# весь этот скрип нужно будет куда-то засунуть в маскклиппер
# вероятно в метод draw_beatiful_map

import cartopy.crs as ccrs
import cartopy

import salem

import numpy as np

import matplotlib.pyplot as plt

# читаем и открываем файлы
ds = salem.open_xr_dataset(r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc')
shp_path = "..\data\\regions\szfo\Arkhangelskaya_oblast.shp"
shapes = salem.read_shapefile(shp_path)
ds =  ds['lccs_class'].isel(time=0)
# создаем новую сеточку долгот и широт - здесь 3600 и 1800 точек - разрешение соответственно 10 точек на градус т.е. примерно 10км (вместо 300 метров)
new_lon = np.linspace(ds.lon.values[0], ds.lon.values[-1], 3600)
new_lat = np.linspace(ds.lat.values[0], ds.lat.values[-1], 1800)
# делаем сабсет по шейпу (пока без клиппинга)
print('subset')
ds = ds.salem.subset(shape=shapes, margin=2)
# врубаем переинтерполяцию (нужно будет разобраться какие параметры можно передавать кроме новой сетки)
print('interpolation')
dsi = ds.interp(lat=new_lat, lon=new_lon)
# рисуем карту базовым методом (хз, сработает ли вся эта кухня, если начать играть с проекциями, это задача следующей фазы тестинга)
print('plt')
dsi.salem.quick_map()
print('3')
plt.show()
