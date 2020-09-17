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
# читаем шейп с этой либой
shape = shapefile.Reader(r'..\..\storage\Belgorod\Adminbndy3')
# Дочитываем - на выходе GeoJSON
feature = shape.shapeRecords()[0]
first = feature.shape.__geo_interface__
print(first) # (GeoJSON format)

# Теперь этот GeoJson нужно скормить shapely и ее методам для построения полигонов
# Импортируем классы по строительству полигонов и точек
from shapely.geometry import Polygon
from shapely.geometry import Point

# создаем обьект точку с парой координат (тут их много, тестил попадание точек в полигон)
point = Point([(37.2,50.7)])
point = Point([(37.2,50.7)])
point = Point([(38,49.7)])
point = Point([(38.752,51.02)])

# создаем полигон, прочитанный из шейпа
# (там есть кейворд "coordinates", в котором лежат координаты полигонов - берем первый)
polygon = Polygon(first['coordinates'][0])

# Проверяем лежит ли точка внутри полигона или нет
# (тут два способа, чем отличаются пока не ясно- работают вроде одинаково)
print(point.within(polygon))
print(polygon.contains(point))

# Рисуем полигон в матплотлибе
# как рисовать точку пока не разобрался - получается неправильно
x,y = polygon.exterior.xy
plt.plot(x,y)
plt.show()
