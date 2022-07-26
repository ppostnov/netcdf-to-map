'''
Скрипт для открытия полигона в формате shp и проверки,
попадает ли точка, задаваемая парой координат внутрь этого полигона
Для чтения shp используется shapefile (pip install pyshp)
для анализа используется shapely (pip install shapely)

Дополнительных зависимостей не требуется (если требуется, уточним)
'''

# Матплотлиб чтобы нарисовать полигон
import matplotlib.pyplot as plt
# Либа для чтения шейпов
import shapefile
# Импортируем классы по строительству полигонов и точек
from shapely.geometry import Polygon
from shapely.geometry import Point

class Polygon_reader:
    def __init__(self, filepath, poly_id):
        # читаем шейп
        self.shape = shapefile.Reader(filepath)
        self.poly_id = poly_id
        self.polygon_creator()

    def polygon_creator(self):
        # Дочитываем - на выходе GeoJSON
        self.feature = self.shape.shapeRecords()[self.poly_id]
        self.first = self.feature.shape.__geo_interface__
        # создаем полигон, прочитанный из шейпа
        # (там есть кейворд "coordinates", в котором лежат координаты полигонов - берем первый)
        self.polygon = Polygon(self.first['coordinates'][0])

    def is_point_inside(self, lat, lon):
        # создаем обьект точку с парой координат
        point = Point(lon, lat)
        #print(point)
        # Проверяем лежит ли точка внутри полигона или нет
        return self.polygon.contains(point)

    def draw(self):
        # Рисуем полигон в матплотлибе
        # как рисовать точку пока не разобрался - получается неправильно
        x, y = self.polygon.exterior.xy
        plt.plot(x, y)
        plt.show()



