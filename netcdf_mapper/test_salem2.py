
# Зависимости библиотеки salem и прочая полезная информация содержится тут:
# https://salem.readthedocs.io/en/latest/installing.html
# 1) в первую очередь нужен geopandas:
    # чтобы геопандас работал без анаконды и прочего
    # Качаем отсюда
    # http://www.lfd.uci.edu/~gohlke/pythonlibs/
    # GDAL и FIONA  подходящих версий
    # Ставим их через pip install filename.whl
    # потом ставим геопандас pip install geopandas
    # а чтобы матплотлиб мог рисовать шейпы pip install descartes
# 2) через pip ставятся
    # netcdf4
    # xarray
    # joblib
    # sckit_image
# 3) я не уверен нужен ли rasterio (но его wheel тоже можно скачать по ссылке в пункте 1 )
# этого венегрета должно хватить

# Импортируем все
# geopandas напрямую не используется, но salem его юзает, поэтому его отсюда не убираем

import geopandas as gpd
import salem

# если понадобятся демофайлики и шейпы
from salem.utils import get_demo_file

# для отрисовки
import matplotlib.pyplot as plt


class MaskClipper:
    def __init__(self, nc_path, shape_path):
        # открываем netcdf и шейп
        self.data_set = salem.open_xr_dataset(nc_path)
        self.shape_path = salem.read_shapefile(shape_path)
        pass

    def create_variable(self, variable, timevalue=0):
        # вычленяем нужную переменную (по ключу)
        # и ставим для ее временной переменной нужное значение
        # (важно! имя времени в нашем netcdf "time" поэтому ей и присваиваем )
        self.var_to_analyze = self.data_set[variable].isel(time=timevalue)

    def subset(self):
        '''
        Метод для очистки датасета (видимо данные, которые не находятся "рядом" с шейпом уходят из анализа)
        :return:
        '''
        print("Subsetting..")
        self.var_to_analyze = self.var_to_analyze.salem.subset(shape=self.shape_path, margin=2)

    def clip(self):
        '''
        Метод для клиппинга датасета в область шейпа
        :return:
        '''
        print("Clipping..")
        self.var_to_analyze = self.var_to_analyze.salem.roi(shape=self.shape_path)

    def draw_map(self):
        '''
        Метод для отрисовки датасета (уже отклипленного шейпом)
        :return:
        '''
        print("Drawing..")
        # Создаем обьект quick_map
        self.map_object = self.var_to_analyze.salem.quick_map()
        # вот эта штука в нативном пайтоне рисовать не хочет\ или рисует шляпу
        #self.map_object.visualize()
        # рисуем матплотлибом
        plt.show()


    def print_types(self):
        print(type(self.data_set), self.data_set)


# Прописываем пути к файлам
nc_path = r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc'
shp_path = r"C:\NETCDF_PROJECT\storage\Belgorod\Adminbndy3.shp"

# Создаем обьект Клиппера и кидаем в него пути к файлам
MC = MaskClipper(nc_path, shp_path)

# Указываем какую переменную будем рисовать и для какого момента времени
MC.create_variable(variable='lccs_class', timevalue=0)

# просто принт того, какого типа данные считались
MC.print_types()

# обрезаем датасет под интересующую область
MC.subset()
# обрезаем датасет под шейп
MC.clip()
# рисуем то, что получилось
MC.draw_map()

