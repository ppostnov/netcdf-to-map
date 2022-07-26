import geopandas as gpd
import salem
import matplotlib.pyplot as plt
import logging

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as colors

from netCDF4 import Dataset
import csv

import cartopy.crs as ccrs
import cartopy
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

class MaskClipper:
    def __init__(self, nc_path, shape_path):
        # открываем netcdf и шейп
        #logger.info('Open files..')
        print('Open files..')
        self.nc_path = nc_path
        self.shape_path = shape_path
        # читаем датасет
        self.data_set = salem.open_xr_dataset(self.nc_path)
        # читаем шейп
        self.shapes = salem.read_shapefile(self.shape_path)
        # делаем список шейпов из прочитанного шейпа
        self.shape_list = [self.shapes.loc[self.shapes["name"] == i] for i in self.shapes["name"]]
        # получаем центроид
        self.centroid = self.retrieve_centroid(self.shape_list)
        # получаем данные о классах, их цветах и значениях из файла
        self.fv, self.fc, self.fm =self.get_colors_from_netcdf(self.nc_path)

        print(help(salem.Map))
        print(help(self.data_set.salem.quick_map))
        print(help(self.data_set.salem.get_map))

    def retrieve_centroid(self, shape_list):
        '''
        Метод для получения центроида для полигона или группы полигонов (получаем средневзвешанную точку центроидов полигонов)
        :param shape_list:
        :return:
        '''

        try:
            # копируем список  шейпов
            points = shape_list.copy()
            # получаем список центроидов всех полигонов
            x = [i['geometry'].centroid.x[0] for i in points]
            y = [i['geometry'].centroid.y[0] for i in points]
            # получаем средний центроид
            centroid = (sum(x)/len(points), sum(y)/len(points))
        except:
            # если ошибка ставим нули
            centroid = (0, 0)
        return centroid

    def get_colors_from_netcdf(self, file_path):
        '''
        метод для вытаскивания информации о классах из датасета
        :param file_path:
        :return:
        '''

        # читаем датасет
        ds = Dataset(file_path)
        # берем список значений классов (в цифрах)
        fv = ds['lccs_class'].flag_values.tolist()
        # берем список советуемых цветов классов (список строк)
        fc = ds['lccs_class'].flag_colors.split()
        # берем список значений классов (список строк)
        fm = ds['lccs_class'].flag_meanings.split()
        # вставляем черный цвет для 'no data' - его в датасете нет
        fc.insert(0, '#000000')
        # вставляем значение 230 - нужно для правильной отрисовки цветовой шкалы
        # - иначе последние значения в нем не отразятся (которые про воду и лёд)
        fv.append(230)
        # вставляем значение пустое значение для 230 - чтобы на шкале на уровне 230 ничего не писалось
        fm.append('')
        return fv, fc, fm

    def create_variable(self, variable, timevalue=0):
        # вычленяем нужную переменную (по ключу)
        # и ставим для ее временной переменной нужное значение
        # (важно! имя времени в нашем netcdf "time" поэтому ей и присваиваем )
        #logger.info('Variable creation..')
        print('Variable creation..')
        self.var_to_analyze = self.data_set[variable].isel(time=timevalue)

    def subset(self):
        '''
        Метод для очистки датасета (видимо данные, которые не находятся "рядом" с шейпом уходят из анализа)
        :return:
        '''
        #print("Subsetting..")
        #logger.info('Subsetting..')
        print('Subsetting..')
        self.var_to_analyze = self.var_to_analyze.salem.subset(shape=self.shapes, margin=2)
        #print(self.var_to_analyze)

    def clip(self):
        '''
        Метод для клиппинга датасета в область шейпа
        :return:
        '''
        #print("Clipping..")
        #logger.info('Clipping..')
        print('Clipping..')
        self.var_to_analyze = self.var_to_analyze.salem.roi(shape=self.shapes)

    def statistic_calculation(self, file_out='names.csv'):
        """
        Метод для оценки статистики по разным классам поверхности
        """
        logging.info('Stats..')

        # открываем файл для записи
        with open(file_out, 'w', newline='', encoding='utf-8') as csvfile:

            # cписок классов по которым считается статистика
            flag_values = [
                0, 10, 11, 12, 20, 30, 40, 50,
                60, 61, 62, 70, 71, 72, 80,
                81, 82, 90, 100, 160, 170,
                110, 130, 180, 190, 120, 121,
                122, 140, 150, 151, 152, 153,
                200, 201, 202, 210, 220
            ]

            # cоздаем список колонок для выходного файла
            fieldnames = ['shape_name', 'file_name']
            fieldnames.extend(flag_values)

            # cоздаем обьект записывателя
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            # пишем заголовки
            writer.writeheader()

            # для каждого шейпа из списка..
            for shape in self.shape_list:
                # вырезаем данные под шейп
                self.var_to_calculate = self.var_to_analyze.salem.roi(shape=shape)
                # считаем сколько точек там всего
                whole = self.var_to_calculate.count()
                # считаем сколько точек для каждого класса (в процентах)
                part_dict = {i: self.var_to_calculate.where(self.var_to_calculate == i).count() / whole * 100 for i in flag_values}
                # переписываем этот словарик чистыми значениями
                dict = {i: part_dict[i].values for i in part_dict}
                # обновляем словарик для экспорта
                dict.update({'shape_name': shape["name"], 'file_name': self.nc_path})
                # пишем словарь в файл
                writer.writerow(dict)

    def draw_map(self):
        """
        Dataset drawling
        """
        logging.info('Drawing..')
        self.map_object = self.var_to_analyze.salem.quick_map()
        plt.show()

    def draw_beautiful_map(self):
        '''
        Метод для отрисовки карты
        Используется ортографическая проекция с сцентром в точке центроида шейпа (списка шейпов)
        :return:
        '''
        import numpy as np
        from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
        import glob

        print("Drawing")
        # Grafico
        fig = plt.figure(figsize=(10, 4))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        print('берега')
        ax.coastlines()
        print('глобал')
        ax.set_global()
        print('countour')
        #ct = ax.contourf(self.var_to_analyze, transform=ccrs.PlateCarree(), cmap="bwr")
        #ct = ax.plot(self.var_to_analyze, transform=ccrs.PlateCarree(), cmap="bwr")
        ct = ax.pcolormesh(self.var_to_analyze, transform=ccrs.PlateCarree(), cmap="bwr")
        ax.gridlines()
        print('color')
        cb = plt.colorbar(ct, orientation="vertical", extendrect='True')
        cb.set_label("Temperatura [°C]")
        print('прочая срань')
        ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
        ax.set_yticks(np.arange(-90, 91, 30), crs=ccrs.PlateCarree())
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)
        plt.show()

    def print_types(self):
        print(type(self.data_set), self.data_set)


if __name__ == '__main__':
    # Прописываем пути к файлам
    nc_path = r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc'
    import cartopy.crs as ccrs
    import cartopy.feature as cf
    import matplotlib.pyplot as plt
    import numpy as np

    proj = ccrs.LambertConformal(central_latitude=60,
                                 central_longitude=50,
                                 standard_parallels=(25, 25))



    print('subsetting')
    dat = salem.open_xr_dataset(nc_path)
    dat = dat['lccs_class'].isel(time=0)

    #dat.salem.quick_map()
    #shapes = salem.read_shapefile("..\data\\regions\szfo\Arkhangelskaya_oblast.shp")
    shapes = salem.read_shapefile("..\data\\regions\szfo\Respublica_Komi.shp")
    #shapes = salem.read_shapefile("..\data\\regions\szfo\Leningradskaya_oblast.shp")
    dat = dat.salem.subset(shape=shapes, margin=2)
    p = dat.plot(
        subplot_kws=dict(projection=ccrs.Orthographic(50, 70), facecolor="gray"),
        transform=ccrs.PlateCarree(),
    )
   # p.axes.set_global()
    p.axes.coastlines()
    p.axes.gridlines()

    print('set values')
    lat=dat.coords['lat'].values
    lon=dat.coords['lon'].values
    print(dat)
   # dat=dat.values
    print(dat)
    print("grid")
   # grid = dat.salem.grid
    print('grid ok')

    print('plot')
    #ax = plt.axes(projection=proj)
    #ax = plt.axes(projection=ccrs.Orthographic(265, 25))
   # ax = plt.axes(projection=ccrs.Orthographic(30, 50))
   # lccproj = ccrs.LambertConformal(central_latitude=25,
    #                                central_longitude=265,
    #                                standard_parallels=(25, 25))
   # lccproj = ccrs.PlateCarree()



    #ax.pcolormesh(lon, lat, dat, transform=lccproj)

    #dat.plot(ax=ax, transform=proj, cmap=cmap, norm=norm)
    #dat.plot(ax=ax, transform=proj)

    #ax.set_global()
    #dat=dat.salem.transform(proj)
    #dat.salem.quick_map()
    #dat.plot(ax=ax, transform=proj, cmap=cmap, norm=norm)

    #dat.plot(ax=ax, transform=ccrs.PlateCarree())

    #dat2=dat.salem.transform(proj)
    #dat2.salem.quick_map()

    print('other')
 #   ax.add_feature(cf.NaturalEarthFeature(
    #    category='cultural',
   #     name='admin_1_states_provinces_lines',
    #    scale='50m',
    #    facecolor='none'))
    #ax.coastlines('50m')
    # рисуются береговые линии
   # ax.coastlines()
    # координантые линии
  #  ax.gridlines()
   # ax.add_feature(cf.BORDERS)
    plt.show()

    # shp_path = "data\\regions\szfo\Arkhangelskaya_oblast.shp"
    #shp_path = "..\data\\regions\szfo\Arkhangelskaya_oblast.shp"
    shp_path = "..\data\\regions\szfo\Murmanskaya_oblast.shp"
    #shp_path = "..\data\\regions\szfo\Pskovskaya_oblast.shp"
    # Создаем обьект Клиппера и кидаем в него пути к файлам
    #MC = MaskClipper(nc_path, shp_path)
    # Указываем какую переменную будем рисовать и для какого момента времени
    #MC.create_variable(variable='lccs_class', timevalue=0)
    # просто принт того, какого типа данные считались
    # MC.print_types()
    # обрезаем датасет под интересующую область
    #MC.subset()
    # обрезаем датасет под шейп
    #MC.clip()
    # считаем стату
   # MC.statistic_calculation()
    # рисуем то, что получилось
    # MC.draw_map()
    #MC.draw_beautiful_map()