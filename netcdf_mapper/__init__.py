"""
    Инициализурующий файл основного модуля netcdf_mapper.
    Файл импортирует два класса - downloader и maskclipper,
    и инициализирует их в своем объекте Absorber. Absorber
    в свою очередь имеет метод execute() который отвечает
    за запуск отсновного функционала приложения. Здесь же
    определена базовая конфигурация для логгирования во
    всем приложении.
"""


import logging
from netcdf_mapper import downloader
from netcdf_mapper import maskclipper


logging.basicConfig(
    format='%(levelname)-4s [%(asctime)s] (%(module)s.py)'
           + ' [def %(funcName)-5s()] --> %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)


class Absorber():
    """
    """
    def __init__(self):
        self.file = downloader.FileRecipient()

    def execute(self, nc_path: str, shp_path: str):
        mc = maskclipper.MaskClipper(nc_path, shp_path)
        mc.create_variable(
            variable='lccs_class',
            timevalue=0
            )
        mc.subset()
        mc.clip()
        mc.statistic_calculation()
