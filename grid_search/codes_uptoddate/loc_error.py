import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import FormatStrFormatter
from matplotlib.patches import Ellipse
from numpy import linalg as LA
import matplotlib.transforms as transforms
import pandas as pd
from pyproj import Geod


g = Geod(ellps='WGS84')
conf=0.90
gtlat=61.153 #BA October 5 2020
gtlon=-148.163 #BA October 5 2020

evdf = pd.read_csv("locfile.csv",index_col=None,keep_default_na=False)
errdf =  pd.DataFrame(columns = ['spower','confidence','loc_error','threshold','err1','err2'])
print(evdf.longitude[0])

#longitude = -148.100006104
#latitude = 61.1500015259
#plot the entire map
fig, (ax) = plt.subplots(1,1)
lonlatgrid = np.load("lonlatgridfile.npy")
stacked_strength = np.load("strengthfile.npy")
yy= lonlatgrid[0]
xx= lonlatgrid[1]
maxamp = abs(stacked_strength).max()/2         # these two lines just adjust the color scale
minamp = abs(stacked_strength).min()
im = ax.pcolormesh(xx,yy, stacked_strength,shading='nearest',cmap=cm.hot_r)
ax110 = fig.add_axes([0.92, 0.11, 0.01, 0.77])
fig.colorbar(im, cax=ax110)    
fig.savefig('stacked_strength_map_' + str(conf) + '.png', bbox_inches='tight')


power = np.amax(stacked_strength)
threshold = power*conf
stacked_strength[stacked_strength < threshold] = np.NaN 
fig1, (ax1) = plt.subplots(1,1)

im1 = ax1.pcolormesh(xx,yy, stacked_strength,shading='nearest',cmap=cm.hot_r)
ax111 = fig1.add_axes([0.92, 0.11, 0.01, 0.77])
fig1.colorbar(im1, cax=ax111)    
fig1.savefig('stacked_strength_nan_map_' +  str(conf) + '.png', bbox_inches='tight')

notnan = np.argwhere(~np.isnan(stacked_strength)) #get the indexes where there are numbers

sub_lonlatgrid = [] #put those indexes into an array
cordinx = list(zip(notnan[:,0], notnan[:,1]))
for cord in cordinx:
    lat = lonlatgrid[0][cord]
    lon = lonlatgrid[1][cord]
    sub_lonlatgrid.append([lon,lat,cord[0],cord[1]])
sub_lonlatgrid = np.array(sub_lonlatgrid)

print(sub_lonlatgrid)

maxx_inx=np.argwhere(sub_lonlatgrid == np.max(sub_lonlatgrid[:,0])) #maxx
x1 = sub_lonlatgrid[maxx_inx[0][0]][0:2]
minx_inx=np.argwhere(sub_lonlatgrid == np.min(sub_lonlatgrid[:,0])) #maxx
x2 =  sub_lonlatgrid[minx_inx[0][0]][0:2]

miny_inx=np.argwhere(sub_lonlatgrid == np.min(sub_lonlatgrid[:,1])) #maxy
y1 = sub_lonlatgrid[miny_inx[0][0]][0:2]

maxy_inx=np.argwhere(sub_lonlatgrid == np.max(sub_lonlatgrid[:,1])) #maxy
y2 = sub_lonlatgrid[maxy_inx[0][0]][0:2]


azimuth1, azimuth1, distance_2d1 = g.inv(x1[0], x1[1], x2[0], x2[1])
err1 = float(distance_2d1)/1000
print(err1)

azimuth2, azimuth2, distance_2d2 = g.inv(y1[0], y1[1], y2[0], y2[1])
err2 = float(distance_2d2)/1000
print(err2)
azimuth3, azimuth3, distance_2d3 = g.inv(evdf.longitude[0],evdf.latitude[0],gtlon,gtlat)
gterr = float(distance_2d3)/1000
loc_error = power,conf,gterr,threshold,err1,err2
errdf.loc[0] = loc_error 

print(errdf)



errdf.to_csv('locerror_' + str(conf) + '.csv',index=False)

#make sure x1 calculations are ok. they usually have more than one result. should i take the average? 
# make some plots? 

minx = int(np.min(sub_lonlatgrid[:,2]))
maxx = int(np.max(sub_lonlatgrid[:,2]))
miny = int(np.min(sub_lonlatgrid[:,3]))
maxy = int(np.max(sub_lonlatgrid[:,3]))
sub_strength = stacked_strength[minx:maxx,miny:maxy]
sub_yy= yy[minx:maxx,miny:maxy]
sub_xx= xx[minx:maxx,miny:maxy]
fig2, (ax2) = plt.subplots(1,1)
im2 = ax2.pcolormesh(sub_xx,sub_yy, sub_strength,shading='nearest',cmap=cm.hot_r)

fig2.savefig('sub_strength_map_' + str(conf) + '.png', bbox_inches='tight')


