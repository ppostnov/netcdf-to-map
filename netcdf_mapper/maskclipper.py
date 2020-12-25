"""
    MaskClipper, основной объект, который обеспечивает
    функционал для обработки выгруженных данных с
    copernicus.eu. Данный класс имеет 6 основных
    методов. Метод первый - retrieve_centroid(),
    метод создает центроид для пространственного
    объекта или группы пространсвенных объектов,
    результат метода используется для отрисовки
    результирующего слоя карты. Метод второй -
    get_collors_from_netcdf(), метод обеспечивает
    функционал для получения цветовой схемы объектов
    их netcdf формата. Третий метод - create_variable(),
    метод обращается к выгруженному формату netcfd и
    основываясь на параметре, переданном как аргумент
    метода возвращает необходимую переменную с данными
    из формата netcdf. Метод четвертый - subset(), метод
    выполняет локирование данных в netcdf формате на
    основе пространственных полигональных данных
    заданного региона. Пятый метод - clip(), метод
    осуществляет финальное определение данных из netcdf
    формата, которые находятся внутри каждого региона.
    Шестой метод - statistic_calculation(), прозводит
    рассчет процентного вхождения в каждый регион, для
    каждого типа данных из netcdf формата.     
"""

import geopandas as gpd
import salem
import matplotlib.pyplot as plt
import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as colors
import csv
import pandas
import geopandas
import cartopy.crs as ccrs
import cartopy
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from netCDF4 import Dataset


class MaskClipper():
    """
    """
    def __init__(self, nc_path, shape_path):
        self.nc_path = nc_path
        self.shape_path = shape_path
        self.data_set = salem.open_xr_dataset(self.nc_path)
        # merge all files to one dataframe
        self.merged_shape = pandas.concat(
            [geopandas.read_file(shp)for shp in shape_path]
            ).pipe(geopandas.GeoDataFrame)

        # shape reading
        if type(self.shape_path) == str:
            self.shape_list = [salem.read_shapefile(self.shape_path)]
        elif type(self.shape_path) == list:
            self.shape_list = [salem.read_shapefile(i) for i in self.shape_path]

        # get centroind
        self.centroid = self.retrieve_centroid(self.shape_list, method=2)
        # get classes, colors, values
        self.fv, self.fc, self.fm = self.get_colors_from_netcdf(self.nc_path)

    def retrieve_centroid(self, shape_list, method=2):
        """
        Get a centroid for a polygon or group of polygons
        """
        if method == 1:
            try:
                points = shape_list.copy()
                x = [i['geometry'].centroid.x[0] for i in points]
                y = [i['geometry'].centroid.y[0] for i in points]
                centroid = (sum(x)/len(points), sum(y)/len(points))
            except centroid.DoesNotExist:
                centroid = (0, 0)

        elif method == 2:
            centroid = (0, 0)
            Xmin = 99999.9
            Xmax = -99999.9
            Ymin = 99999.9
            Ymax = -99999.9
            Xcent = 0
            Ycent = 0

            for shape in shape_list:
                bd = shape.bounds
                if Xmin >= bd.minx[0]:
                    Xmin = bd.minx[0]
                if Xmax <= bd.maxx[0]:
                    Xmax = bd.maxx[0]
                if Ymin >= bd.miny[0]:
                    Ymin = bd.miny[0]
                if Ymax <= bd.maxy[0]:
                    Ymax = bd.maxy[0]

            Xcent = (Xmax+Xmin)/2
            Ycent = (Ymax+Ymin)/2

            centroid = (Xcent, Ycent)

        return centroid

    def get_colors_from_netcdf(self, file_path):
        """
        Unpack a data from the netcdf dataset
        """
        ds = Dataset(file_path)
        # get numbers of classes
        fv = ds['lccs_class'].flag_values.tolist()
        # get colors of classes
        fc = ds['lccs_class'].flag_colors.split()
        # get meanings of classes
        fm = ds['lccs_class'].flag_meanings.split()
        # add black color for 'no data'
        fc.insert(0, '#000000')
        # add value to dataset for ice and water
        fv.append(230)
        # add meaning for 230 value
        fm.append('')
        return fv, fc, fm

    def create_variable(self, variable, timevalue=0):
        """
        Unpack neccesary varible
        """
        logging.info(f'Unpacking variable {variable}')
        self.var_to_analyze = self.data_set[variable].isel(time=timevalue)

    def subset(self):
        """
        Take only neccesary data from netcdf
        according to shape data
        """
        logging.info('Subsetting data')
        self.var_to_analyze = self.var_to_analyze.salem.subset(
            shape=self.merged_shape, margin=2
            )

    def clip(self):
        """
        Final erasing of netcdf data
        according to shape data
        """
        logging.info('Clipping data')
        self.var_to_analyze = self.var_to_analyze.salem.roi(
            shape=self.merged_shape
            )
        logging.info('Creating final netcdf dataset')  
        self.resave_netcdf(self.var_to_analyze, filename='netcdf_dataset.nc')

    def statistic_calculation(
            self,
            file_out='output\\statistic.csv',
            resave_every_nc=True
            ):
        logging.info('Statistic creation')
        with open(file_out, 'w', newline='', encoding='utf-8') as csvfile:
            flag_values = [
                0, 10, 11, 12, 20, 30, 40, 50,
                60, 61, 62, 70, 71, 72, 80,
                81, 82, 90, 100, 160, 170,
                110, 130, 180, 190, 120, 121,
                122, 140, 150, 151, 152, 153,
                200, 201, 202, 210, 220
            ]

            fieldnames = ['shape_name', 'file_name']
            fieldnames.extend(flag_values)
            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames,
                delimiter=';'
                )
            writer.writeheader()

            for shape in self.shape_list:
                self.var_to_calculate = self.var_to_analyze.salem.roi(
                    shape=shape
                    )

                # if resave_every_nc:
                    # filename = shape.name[0].strip().replace(' ', '') + '.nc'
                    # self.resave_netcdf(self.var_to_calculate, filename)
                # total count of points
                whole = self.var_to_calculate.count()
                # % of points for each class
                part_dict = {
                    i: self.var_to_calculate.where(self.var_to_calculate == i).count() 
                    / whole * 100 for i in flag_values
                    }

                dict = {i: part_dict[i].values for i in part_dict}
                dict.update(
                    {'shape_name': shape["name"][0], 'file_name': self.nc_path}
                    )
                writer.writerow(dict)

    def resave_netcdf(self, ds, filename):
        """
        Xarray to netcdf
        http://xarray.pydata.org/en/stable/generated/xarray.Dataset.to_netcdf.html
        """
        ds.to_netcdf(path=f'output\\{filename}')

    def coarser_grid(self, ds, res_x=0.01, res_y=0.01):
        '''
        Метод для переинтерполяции датасета на грид с другим шагом
        :param ds: входной датасет
        :param res_x: шаг по долготе (в градусах)
        :param res_y: шаг по широте (в градусах)
        :return: переинтерполированный датасет
        '''
        # модуль математики для элементарных операций
        import math
        # считаем сколько градусов между концами грида по широте и долготе
        num_lon = math.fabs(ds.lon.values[0]-ds.lon.values[-1])
        num_lat = math.fabs(ds.lat.values[0]-ds.lat.values[-1])

        # считаем точное количество точек
        num_lon = num_lon/res_x
        num_lat = num_lat/res_y

        # интерполяции нужны целые числа - округляем сверху
        # (можно округлять снизу, но я решил, что это может быть опасно потерей данных - просто чуйка ничего более)
        num_lon = int(math.ceil(num_lon))
        num_lat = int(math.ceil(num_lat))

        # создаем массивы новых широт и долгот
        new_lon = np.linspace(ds.lon.values[0], ds.lon.values[-1], num_lon)
        new_lat = np.linspace(ds.lat.values[0], ds.lat.values[-1], num_lat)

        # переинтерполируем датасет
        dsi = ds.interp(method='nearest', lat=new_lat, lon=new_lon)

        return dsi

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

        proj = self.var_to_analyze.salem.cartopy()
        # создается subplot с ортографической проекцией
        ax = plt.subplot(projection=ccrs.Orthographic(central_longitude=self.centroid[0], central_latitude=self.centroid[1]))

        # рисуются береговые линии
        ax.coastlines()
        # координантые линии
        ax.gridlines()
        # создается цветовая схема для отрисовки colorbar, разделенного на классы
        cmap, norm = matplotlib.colors.from_levels_and_colors(self.fv, self.fc)

        # Сохранение клипнутых данных в netcdf
        # self.resave_netcdf(self.var_to_analyze, filename='clipped_data.nc')


        # Переинтерполяция на более грубую сетку
        # у нас по умолчанию сетка 300м (это что-то около 0.003 градуса)
        print('interpolate')
        self.var_to_analyze = self.coarser_grid(self.var_to_analyze, res_x=0.01, res_y=0.01)

        # отрисовка данных
        print('plot')
        self.var_to_analyze.plot(ax=ax, transform=ccrs.PlateCarree(), cmap=cmap, norm=norm)

        # Костыль для удаления лишнего colorbar  (если этого не будет отрисоваться будет 2 colorbar`а)
        print('color bar')
        ax1 = plt.gca()
        im = ax1.collections # если не работает попробовать использовать ax1.images
        cb = im[-1].colorbar
        cb.remove()

        # ?: https://pyprog.pro/mpl/mpl_pcolormesh.html
        plt.pcolormesh(self.var_to_analyze, cmap=cmap, norm=norm)

        # Создаем новый colorbar c правильной расстановкой подписей классов
        cbl = plt.colorbar(spacing='uniform', ticks=self.fv)
        # Создаем подписи осям вместо цифр классов
        cbl.ax.set_yticklabels(self.fm)
        # Создаем подпись оси
        cbl.set_label('Подпись оси')

        # Добавляем шейпы стран
        ax.add_feature(cartopy.feature.BORDERS)
        # Добавляем шейп из входного файла (шейп которым резали)
        #ax.add_geometries(self.shapes['geometry'], crs=proj, facecolor='none', edgecolor='black')
        for shape in self.shape_list:
            ax.add_geometries(shape['geometry'], crs=proj, facecolor='none', edgecolor='black')
        # ? не знаю что это делает
        ax.set_extent(self.var_to_analyze.salem.grid.extent, crs=proj)
        # Открываем окно карты
        plt.show()

    def print_types(self):
        print(type(self.data_set), self.data_set)
