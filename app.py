# from netcdf_mapper import downloader



import logging

logger = logging.getLogger('dev')
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)

formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
consoleHandler.setFormatter(formatter)

logger.info('информационное сообщение')

from netcdf_mapper.maskclipper import MaskClipper

# # the example how download the data for one year
# d = downloader.FileRecipient()
# d.download('2008', '2008-test')
# # d.unzipper('2018-test')




# Прописываем пути к файлам
nc_path = r'..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc'
#shp_path = "data\\shape\\regions\szfo\Respublica_Komi.shp"
shp_path = "data\\shape\\county\szfo.shp"
shp_path = [
"data\\shape\\regions\szfo\Respublica_Komi.shp",
"data\\shape\\regions\szfo\Arkhangelskaya_oblast.shp",
"data\\shape\\regions\szfo\Kaliningradskaya_oblast.shp",
]
#shp_path = "data\\regions\szfo\Pskovskaya_oblast.shp"
# Создаем обьект Клиппера и кидаем в него пути к файлам
MC = MaskClipper(nc_path, shp_path)


# Указываем какую переменную будем рисовать и для какого момента времени
MC.create_variable(variable='lccs_class', timevalue=0)
# просто принт того, какого типа данные считались
##MC.print_types()
# обрезаем датасет под интересующую область
MC.subset()
# обрезаем датасет под шейп
MC.clip()
# считаем стату
MC.statistic_calculation()
# рисуем то, что получилось
##MC.draw_map()
MC.draw_beautiful_map()


import netcdf_mapper
from netcdf_mapper import Absorber
