
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

import cartopy.crs as ccrs
import cartopy
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature



class MaskClipper:
    def __init__(self, nc_path, shape_path):
        # открываем netcdf и шейп
        logger.info('Open files..')
        self.data_set = salem.open_xr_dataset(nc_path)
        self.shape_path = salem.read_shapefile(shape_path)

        #self.shape_list = [self.shape_path.loc[self.shape_path["POLYGON_NM"] == i] for i in self.shape_path["POLYGON_NM"]]
        ##print(self.shape_list)
        ##self.shape_path = self.shape_path.loc[self.shape_path["POLYGON_NM"].isin([r"Belgorodskaya oblast'"])]
        pass

    def create_variable(self, variable, timevalue=0):
        # вычленяем нужную переменную (по ключу)
        # и ставим для ее временной переменной нужное значение
        # (важно! имя времени в нашем netcdf "time" поэтому ей и присваиваем )
        logger.info('Variable creation..')
        self.var_to_analyze = self.data_set[variable].isel(time=timevalue)

    def subset(self):
        '''
        Метод для очистки датасета (видимо данные, которые не находятся "рядом" с шейпом уходят из анализа)
        :return:
        '''
        #print("Subsetting..")
        logger.info('Subsetting..')
        self.var_to_analyze = self.var_to_analyze.salem.subset(shape=self.shape_path, margin=0)
        #print(self.var_to_analyze)

    def clip(self):
        '''
        Метод для клиппинга датасета в область шейпа
        :return:
        '''
        #print("Clipping..")
        logger.info('Clipping..')
        self.var_to_analyze = self.var_to_analyze.salem.roi(shape=self.shape_path)

    def every_clip(self):
        '''
        Метод для клиппинга датасета в область шейпа
        :return:
        '''
        #print("Clipping..")
        logger.info('Clipping..')

        #self.var_to_analyze = self.var_to_analyze.salem.roi(shape=self.shape_list[0])
        self.var_to_analyze = self.var_to_analyze.salem.roi(shape=self.shape_path)
        print(self.var_to_analyze)
        print("just do it!", type(self.var_to_analyze))
        print(self.var_to_analyze[344, 455])
        print(dir(self.var_to_analyze))
        print('all:', self.var_to_analyze.count())
        whole = self.var_to_analyze.count()
        flag_values=[10,11,12,
                     20,
                     30,
                     40,

                     50,
                     60,61,62,
                     70,71,72,
                     80,81,82,
                     90,
                     100,
                     160,
                     170,

                     110,
                     130,

                     180,
                     190,
                     120,121,122,
                     140,
                     150,151,152,153,
                     200,201,202,
                     210,
                     220
                     ]
        part_dict = {i: self.var_to_analyze.where(self.var_to_analyze == i).count() for i in flag_values}
        per=0
        for i in part_dict:
            per_par=part_dict[i]/whole*100
            per+=per_par
            print("parts", i, part_dict[i], per_par)
            print()
        print("whole", per)
        #print('all190:', self.var_to_analyze.where(self.var_to_analyze==190))
       # print('all0:', self.var_to_analyze.where(self.var_to_analyze == 0).count())
      #  print('all10:', self.var_to_analyze.where(self.var_to_analyze == 10).count())
       # print('all20:', self.var_to_analyze.where(self.var_to_analyze == 20).count())
      #  print('all30:', self.var_to_analyze.where(self.var_to_analyze == 30).count())
      #  print('all40:', self.var_to_analyze.where(self.var_to_analyze == 40).count())
      #  print('all50:', self.var_to_analyze.where(self.var_to_analyze == 50).count())
      #  print('all60:', self.var_to_analyze.where(self.var_to_analyze == 60).count())
       # print('all70:', self.var_to_analyze.where(self.var_to_analyze == 70).count())
      #  print('all80:', self.var_to_analyze.where(self.var_to_analyze == 80).count())
      #  print('all90:', self.var_to_analyze.where(self.var_to_analyze == 90).count())
       # print('all100:', self.var_to_analyze.where(self.var_to_analyze == 100).count())
       # print('all110:', self.var_to_analyze.where(self.var_to_analyze == 110).count())
      #  print('all120:', self.var_to_analyze.where(self.var_to_analyze == 120).count())
       # print('all130:', self.var_to_analyze.where(self.var_to_analyze == 130).count())
       # print('all140:', self.var_to_analyze.where(self.var_to_analyze == 140).count())
      #  print('all150:', self.var_to_analyze.where(self.var_to_analyze == 150).count())
       # print('all160:', self.var_to_analyze.where(self.var_to_analyze == 160).count())
      #  print('all170:', self.var_to_analyze.where(self.var_to_analyze == 170).count())
      #  print('all180:', self.var_to_analyze.where(self.var_to_analyze == 180).count())
      #  print('all190:', self.var_to_analyze.where(self.var_to_analyze == 190).count())
      #  print('all200:', self.var_to_analyze.where(self.var_to_analyze == 200).count())
       # print('all210:', self.var_to_analyze.where(self.var_to_analyze == 210).count())
       # print('all220:', self.var_to_analyze.where(self.var_to_analyze == 220).count())

        #print('all0:', self.var_to_analyze.where(self.var_to_analyze==190).count())
        #print('all170:', self.var_to_analyze.where(self.var_to_analyze==170))
        #print('all170:', self.var_to_analyze.where(self.var_to_analyze==170).count())
        #print('all180:', self.var_to_analyze.where(self.var_to_analyze==180))
        #print('all180:', self.var_to_analyze.where(self.var_to_analyze==180).count())

        #print('170:', self.var_to_analyze[self.var_to_analyze==170].count())
        #print(self.var_to_analyze.count(self.var_to_analyze==180))
        #print(self.var_to_analyze.count(self.var_to_analyze==190))
        #print(self.var_to_analyze.count(self.var_to_analyze==200))
        #print(self.var_to_analyze.count(self.var_to_analyze==210))
        #print(self.var_to_analyze.count(self.var_to_analyze==220))
        #self.var_to_analyze2 = self.var_to_analyze.salem.roi(shape=self.shape_list[1])
        #print('all2:', self.var_to_analyze2.count())

    def draw_map(self):
        '''
        Метод для отрисовки датасета (уже отклипленного шейпом)
        :return:
        '''
        #print("Drawing..")
        logger.info('Drawing..')
        # Создаем обьект quick_map
        self.map_object = self.var_to_analyze.salem.quick_map()
        # вот эта штука в нативном пайтоне рисовать не хочет\ или рисует шляпу
        #self.map_object.visualize()
        # рисуем матплотлибом
        plt.show()

    def draw_beatiful_map(self, fv, fc, fm):
        import matplotlib.pyplot as plt
        import matplotlib
        import matplotlib.colors as colors


        proj = self.var_to_analyze.salem.cartopy()
        #proj = ccrs.Orthographic(central_longitude=57, central_latitude=29)
        #ax = plt.subplot(2, 2, 2, projection=ccrs.Orthographic(central_longitude=57, central_latitude=29))

        #ax = plt.subplot(projection=ccrs.Orthographic(central_longitude=57, central_latitude=29))
        ax = plt.subplot(projection=ccrs.Orthographic(central_longitude=50, central_latitude=71))
        #ax = plt(projection=ccrs.Orthographic(central_longitude=57, central_latitude=29))

        #ax = plt.subplot(2, 2, 2, projection=proj)
        ax.coastlines()



        ax.gridlines()
        #self.var_to_analyze.plot(ax=ax, transform=proj, cmap='Oranges')
        #self.var_to_analyze.plot(ax=ax, transform=proj, cmap=matplotlib.colors.ListedColormap(fc))
        #cmap,norm = matplotlib.colors.from_levels_and_colors(fv,fc, extend='max')

        cmap,norm = matplotlib.colors.from_levels_and_colors(fv,fc)

        print()
        print()
        print()
        print('!!!!!!!!!!!!')
        print(norm)
        print(cmap)

        #self.var_to_analyze.plot(ax=ax, transform=proj, cmap=cmap, norm=norm)

        self.var_to_analyze.plot(ax=ax, transform=proj, cmap=cmap, norm=norm)
        ax1 = plt.gca()
        im = ax1.collections
        # Assume colorbar was plotted last one plotted last
        print(im)
        cb = im[-1].colorbar
        # Do any actions on the colorbar object (e.g. remove it)
        cb.remove()


        #plt.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
        #self.var_to_analyze.plot(ax=ax, transform=proj, color=fc)

       # for index, value in enumerate(fv):
       #     print(index, fv[index], fc[index])
        print()

        #cmap=colors.ListedColormap(fc)
        #boundaries=fv
        #norm=colors.BoundaryNorm(boundaries, cmap.N, clip=True)
        plt.pcolormesh(self.var_to_analyze, cmap=cmap, norm=norm)
        #cbl=plt.colorbar(spacing='uniform')
        cbl=plt.colorbar(spacing='uniform', ticks=fv)
        cbl.ax.set_yticklabels(fm)
        #cbl.ax.set_xticklabels(fm)  # horizontal colorbar
        cbl.set_label('your label hre')

        ax.add_feature(cartopy.feature.BORDERS)
        shape_feature = ShapelyFeature(Reader(r"C:\NETCDF_PROJECT\netcdf-to-map\data\regions\szfo\Pskovskaya_oblast.shp").geometries(),
                                       crs=proj, facecolor='none')
        #ax.add_feature(shape_feature)
        #ggg=Reader(r"C:\NETCDF_PROJECT\netcdf-to-map\data\regions\szfo\Pskovskaya_oblast.shp").geometries()
        #ax.add_geometries([ggg], crs=proj)

        print(dir(ax.add_geometries))
        ax.add_geometries(self.shape_path['geometry'], crs=proj, facecolor='none', edgecolor='black')
        #ax.add_feature(self.shape_path)
        #ax.set_extent(self.var_to_analyze.salem.grid.extent, crs=ccrs.Orthographic(central_longitude=57, central_latitude=29))
        ax.set_extent(self.var_to_analyze.salem.grid.extent, crs=proj)
        plt.show()


    def print_types(self):
        print(type(self.data_set), self.data_set)




import logging

logger = logging.getLogger('dev')
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)

formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
consoleHandler.setFormatter(formatter)

logger.info('информационное сообщение')

# Прописываем пути к файлам
nc_path = r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc'

from netCDF4 import Dataset
ds = Dataset(nc_path)

fv=ds['lccs_class'].flag_values.tolist()
fc=ds['lccs_class'].flag_colors.split()
fm=ds['lccs_class'].flag_meanings.split()

print(type(fc))
print(len(fc))
print(len(fm))
print(len(fv))
fc.insert(0, '#000000')
fv.append(230)
fm.append('No data')
print(fv)
#for index, i in enumerate(fv):
#    print(fv[index],fc[index],fm[index])
#print(ds['lccs_class'])

#shp_path = r"C:\NETCDF_PROJECT\storage\Belgorod\Adminbndy3.shp"
#shp_path = r"C:\NETCDF_PROJECT\netcdf-to-map\data\regions\szfo\Pskovskaya_oblast.shp"
shp_path = r"C:\NETCDF_PROJECT\netcdf-to-map\data\regions\szfo\Arkhangelskaya_oblast.shp"

# Создаем обьект Клиппера и кидаем в него пути к файлам
MC = MaskClipper(nc_path, shp_path)

# Указываем какую переменную будем рисовать и для какого момента времени
MC.create_variable(variable='lccs_class', timevalue=0)

# просто принт того, какого типа данные считались
##MC.print_types()

# обрезаем датасет под интересующую область
MC.subset()
# обрезаем датасет под шейп
#MC.clip()
MC.every_clip()
# рисуем то, что получилось
#MC.draw_map()
MC.draw_beatiful_map(fv, fc, fm)

