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
