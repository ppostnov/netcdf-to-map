import netCDF4 as nc
from shape_reader import Polygon_reader

import geopandas
from geopandas.geoseries import *
import numpy as np
import asyncio
from shapely.geometry import Point

class netcdf:
    def __init__(self, filepath):
        # читаем датасет, определяем переменные, говорим что полигона для анализа по умолчанию нет
        self.file = nc.Dataset(filepath)
        self.poly = None
        self.variable_reader()
        self.dimensions_reader()

        #self.gdf=None
        self.gdf = geopandas.GeoDataFrame()

    def geodf(self):
        import geopandas as gpd
        #data = gpd.read_file(path)
        gdf = geopandas.GeoDataFrame
        pass

    def variable_reader(self):
        # читаем переменные (использовать далее будем только lccs_class)
        self.processed_flag = self.file.variables['processed_flag']
        #print(processed_flag)
        self.lccs_class = self.file.variables['lccs_class']
        #print(lccs_class)
        self.current_pixel_state = self.file.variables['current_pixel_state']
        #print(current_pixel_state)
        self.observation_count = self.file.variables['observation_count']
        #print(observation_count)
        self.change_count = self.file.variables['change_count']
        #print(change_count)

    def dimensions_reader(self):
        # читаем координантые переменные и ставим дефолтные значения для boundary box=весь пространственный диапазон
        self.lon = self.file.variables['lon'][:]
        self.lat = self.file.variables['lat'][:]
        self.time = self.file.variables['time']

        # Как это можно улулчшить?
        lon_idx = np.where((self.lon >= 0) & (self.lon <= 100))
        lat_idx = np.where((self.lat >= 0) & (self.lat <= 100))
        print(len(lat_idx[0])*len(lon_idx[0]))

        #print(lon_idx)
        sel_band1 = self.lccs_class[0][np.ix_(lat_idx[0], lon_idx[0])]
        print(sel_band1)
        print(np.shape(sel_band1))

        self.lon_ind_st=0
        self.lat_ind_st=0

        self.lon_ind_fin=len(self.lon[:])
        self.lat_ind_fin=len(self.lat[:])

    def gridbounds(self, left, right):
        # флипаем индексы если второй индекс меньше первого
        if left > right:
            left, right = right, left
        return left, right

    def box_definer(self,llcrnrlon, urcrnrlon, llcrnrlat, urcrnrlat):
        # сюда кидаются координаты нужного boundary box
        # определяюся индексы задаваемых широт и долгот
        self.lon_ind_st = self.FindValueIndex(self.lon[:], llcrnrlon)
        self.lon_ind_fin = self.FindValueIndex(self.lon[:], urcrnrlon)
        self.lat_ind_st = self.FindValueIndex(self.lat[:], llcrnrlat)
        self.lat_ind_fin = self.FindValueIndex(self.lat[:], urcrnrlat)

        # флипаем индексы если второй индекс меньше первого
        self.lon_ind_st, self.lon_ind_fin = self.gridbounds(self.lon_ind_st, self.lon_ind_fin)
        self.lat_ind_st, self.lat_ind_fin = self.gridbounds(self.lat_ind_st, self.lat_ind_fin)


    def what_inside(self):
        # описание датасета
        print(self.file)

    def add_poly(self, poly):
        # добавляем класс полигона анализирующего (сам класс живет в shape_reader.py)
        self.poly = poly

    def FindValueIndex(self, seq, value):
        # определяем индекс массива по значению. Наверное надо протестить эту функцию и отрефакторить, но в первом приближении она рабочая
        val = np.ones(len(seq)) * value
        r = np.where(np.diff(np.sign(seq - val)) != 0)
        print(r)
        r = r[0][0]
        print(r)
        idx = r + (value - seq[r]) / (seq[r + np.ones_like(r)] - seq[r])
        idx = np.append(idx, np.where(seq == value))
        idx = np.sort(idx)
        idx = int(np.round(idx)[0])
        return idx

    async def long_runner(self, index_i, i):
        if self.poly:
            #print((self.lat_ind_st-self.lat_ind_fin)*(self.lon_ind_st-self.lon_ind_fin))
            for index_j, j in enumerate(self.lat[self.lat_ind_st:self.lat_ind_fin]):
                if self.poly.is_point_inside(lat=j, lon=i):
                    #print(index_i, index_j, i, j, self.lccs_class[0, index_j, index_i])
                    pass

    def create_asynco_list(self):
        self.futures = []
        for index_i, i in enumerate(self.lon[self.lon_ind_st:self.lon_ind_fin]):
            self.futures.append(self.long_runner(index_i,i))


    def all_point_iteration(self):
        # Если есть класс полигона добавлен - итерируем все точки в границах boundary box и определяем попадают ли точки в полигон
        # если попадают - просто делаем принт
        if self.poly:

            for index_i, i in enumerate(self.lon[self.lon_ind_st:self.lon_ind_fin]):
                print(index_i)
                self.gdf_list = []
                self.lats=[]
                self.lons=[]
                #print(index_i, i, len(self.lon[self.lon_ind_st:self.lon_ind_fin]))
                for index_j, j in enumerate(self.lat[self.lat_ind_st:self.lat_ind_fin]):
                    if self.poly.is_point_inside(lat=j, lon=i):
                        #self.gdf_list.append(Point(i, j))
                        self.lons.append(i)
                        self.lats.append(j)
                        #print(index_i, index_j, i, j, self.lccs_class[0, index_j, index_i])
                        pass

                #if self.gdf.empty:
                #self.gdf.append(geopandas.GeoDataFrame(geometry=geopandas.points_from_xy(self.lons,self.lats)))
                #else:
                self.gdf=geopandas.GeoDataFrame(geometry=geopandas.points_from_xy(self.lons,self.lats))

                print(self.gdf.shape)



        else:
            print("No poly added")

# Создаем обьект полигона
poly = Polygon_reader(r'..\..\storage\Belgorod\Adminbndy3', poly_id=0)
# Просто тестим что он по-прежнему работает
print(poly.is_point_inside(lat=35.43472222222223, lon=51.41805555555555))


# Создаем обьект анализатора nc файла
netcdf_analis = netcdf(r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc')
# добавляем туда наш полигон
netcdf_analis.add_poly(poly)
# добавляем границы boundary box
netcdf_analis.box_definer(llcrnrlat=50.0, urcrnrlat=52.0, llcrnrlon=35.0, urcrnrlon=40.0)
# врубаем итерацию по всем точкам внутри boundary box  и проверяем попадают ли эти точки в полигон
#from time import time
#t0=time()
#netcdf_analis.create_asynco_list()
#loop = asyncio.get_event_loop()
#loop.run_until_complete(asyncio.wait(netcdf_analis.futures))
#print("Ended", time()-t0)
#netcdf_analis.all_point_iteration()