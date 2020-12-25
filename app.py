"""
    versions for netcdf files:
        1992-2015 = v2.0.7cds
        2016-2018 = v2.1.1

    App файл, выполняет роль программного интерфейса приложения,
    с помощью которого осуществляется запуск основных программных
    процессов. Данный интерфейс импортирует объект Absorber из
    основного модуля netcdf_mapper. Описаны два этапа. Первый
    этап, инициализация объекта Absorber и использование его
    метода download() для загрузки необходимых данных с ресурса
    copernicus.eu, в качестве парметров загрузки передается
    год за который нужны данные, имя выходного архива и версия
    для формата netcdf, после этого полученный архив распаковывается
    с помощью метода unzip(). Второй этап является основным, в нем
    происходит обработка полученных данных с copernicus.eu,
    необходимые рассчеты для статистики и формирование выходных
    результирующих файлов по регионам в формате netcdf для создания
    интерактивной карты и файла статистики о процентном вхождении
    каждого объекта в рамках каждого региона.   
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
