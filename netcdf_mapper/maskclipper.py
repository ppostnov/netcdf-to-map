import geopandas as gpd
import salem
import matplotlib.pyplot as plt
import logging


class MaskClipper:
    def __init__(self, nc_path, shape_path):
        # открываем netcdf и шейп
        logger.info('Open files..')
        self.data_set = salem.open_xr_dataset(nc_path)
        self.shape_path = salem.read_shapefile(shape_path)
        self.shape_list = [self.shape_path.loc[self.shape_path["name"] == i] for i in self.shape_path["name"]]
        #print(self.shape_list)
        #self.shape_path = self.shape_path.loc[self.shape_path["POLYGON_NM"].isin([r"Belgorodskaya oblast'"])]
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
        self.var_to_analyze = self.var_to_analyze.salem.subset(shape=self.shape_path, margin=2)
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
        """
        Метод для клиппинга датасета в область шейпа
        """
        logging.info('Clipping..')

        self.var_to_analyze = self.var_to_analyze.salem.roi(shape=self.shape_list[0])
        print(self.var_to_analyze)
        print("just do it!", type(self.var_to_analyze))
        print(self.var_to_analyze[344, 455])
        print(dir(self.var_to_analyze))
        print('all:', self.var_to_analyze.count())
        whole = self.var_to_analyze.count()

        flag_values = [
            10, 11, 12, 20, 30, 40, 50,
            60, 61, 62, 70, 71, 72, 80,
            81, 82, 90, 100, 160, 170,
            110, 130, 180, 190, 120, 121,
            122, 140, 150, 151, 152, 153,
            200, 201, 202, 210, 220
        ]
                     
        part_dict = {i: self.var_to_analyze.where(self.var_to_analyze == i).count() for i in flag_values}
        per = 0
        for i in part_dict:
            per_par = part_dict[i]/whole*100
            per += per_par
            print("parts", i, part_dict[i], per_par)
        print("whole", per)
      
    def draw_map(self):
        """
        Dataset drawling
        """
        logging.info('Drawing..')
        self.map_object = self.var_to_analyze.salem.quick_map()
        plt.show()

    def print_types(self):
        print(type(self.data_set), self.data_set)