import netCDF4 as nc

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap




file = nc.Dataset(r'..\..\storage\C3S-LC-L4-LCCS-Map-300m-P1Y-2018-v2.1.1.nc')

print(file)
print(file.variables.keys())

processed_flag = file.variables['processed_flag']
print(processed_flag)
lccs_class = file.variables['lccs_class']
print(lccs_class)
current_pixel_state = file.variables['current_pixel_state']
print(current_pixel_state)
observation_count = file.variables['observation_count']
print(observation_count)
change_count = file.variables['change_count']
print(change_count)
lon = file.variables['lon']
lat = file.variables['lat']
time = file.variables['time']


def FindValueIndex(seq, value):
    val = np.ones(len(seq)) * value
    r = np.where(np.diff(np.sign(seq - val)) != 0)
    print(r)
    r=r[0][0]
    print(r)
    idx = r + (value - seq[r]) / (seq[r + np.ones_like(r)] - seq[r])
    idx = np.append(idx, np.where(seq == value))
    idx = np.sort(idx)
    idx = int(np.round(idx)[0])
    return idx


def findvalue2(seq, val):
    value = np.ones(len(seq)) *val
    diffseq = seq - value
    signseq = np.sign(diffseq)
    zero_crossings = signseq[0:-2] != signseq[1:-1]
    indices = np.where(zero_crossings)[0]
    for i, v in enumerate(indices):
        if abs(seq[v + 1] - val) < abs(seq[v] - val):
            indices[i] = v + 1
    return indices

seq = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
val=7.5
print("FOUND")
print(FindValueIndex(seq, val))
#print(findvalue2(seq,val))
#print(findvalue(seq, val))
print("FOUND2")

llcrnrlat=50.0
urcrnrlat=66.6
#urcrnrlat=53

llcrnrlon=22.0
#urcrnrlon=24.0
urcrnrlon=42.0

# слишком хорошее разрешение пространственное данных
# нужно определить индексы массивов?
lon_ind_st = FindValueIndex(lon[:], llcrnrlon)
lon_ind_fin = FindValueIndex(lon[:], urcrnrlon)
lat_ind_st = FindValueIndex(lat[:], llcrnrlat)
lat_ind_fin = FindValueIndex(lat[:], urcrnrlat)


print(lon_ind_st,lon_ind_fin)
print(lat_ind_st,lat_ind_fin)
print(lon[lon_ind_st])
print(lon[lon_ind_fin])
print(lat[lat_ind_st])
print(lat[lat_ind_fin])

mp = Basemap(  # рисование карты
             projection='merc', # проекция
             llcrnrlat=llcrnrlat, #левый нижний угол бокса -широта
             llcrnrlon=llcrnrlon, #левй нижний угол бокса - долгота
             urcrnrlat=urcrnrlat, # правый верхний - широта
             urcrnrlon=urcrnrlon, # правый верхний - долгота
             resolution='i',  # хз чо?
           )

#
def gridbounds(left, right):
    if left > right:
        left, right = right, left
    return left, right

lon_ind_st,lon_ind_fin =gridbounds(lon_ind_st, lon_ind_fin)
lat_ind_st,lat_ind_fin =gridbounds(lat_ind_st, lat_ind_fin)
print(lon_ind_st,lon_ind_fin)
print(lat_ind_st,lat_ind_fin)

print("meshgrid")
lon_g, lat_g = np.meshgrid(lon[lon_ind_st:lon_ind_fin], lat[lat_ind_st:lat_ind_fin ]) # хз чо это
x,y = mp(lon_g, lat_g)
print(np.shape(lccs_class))
print("color scheme")
#color_scheme = mp.pcolor(x, y, lccs_class[0, lon_ind_st:lon_ind_fin, lat_ind_st:lat_ind_fin], cmap='jet')
#color_scheme = mp.pcolor(x, y, lccs_class[0, lat_ind_st:lat_ind_fin, lon_ind_st:lon_ind_fin], cmap='jet')
color_scheme = mp.pcolor(x, y, np.squeeze(lccs_class[0, lat_ind_st:lat_ind_fin, lon_ind_st:lon_ind_fin]), cmap='jet')
print("coastlines")
mp.drawcoastlines()
print("countries")
mp.drawcountries()
print("states")
mp.drawstates()
print("title")
plt.title("Surface classes mothefuccka!")
print("showing...")
plt.show()


# просто рисование матплотлибом
##cs = plt.contourf(lon[100:110], lat[100:110], current_pixel_state[0,100:110,100:110])
##cs = plt.imshow(lon[100:110], lat[100:110], current_pixel_state[0,100:110,100:110], cmap='hot', interpolation='nearest')
#cs = plt.imshow(lccs_class[0,:,:], cmap='hot', interpolation='nearest')
#cs = plt.contourf(processed_flag[0,:,:])
#print("wtf")
##print(processed_flag[0,100:110,100:110])
#print("wtf")
#plt.show()