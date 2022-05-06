import pygmt
import pandas as pd
import numpy as np

gtevlat=58.736 #Orville-Wilbur
gtevlon=-137.272 #Orville-Wilbur

stdf = pd.read_csv("stafile.csv",index_col=None,keep_default_na=False)
evdf = pd.read_csv("stacked_locfile.csv",index_col=None,keep_default_na=False)


latmin = np.round(np.min(stdf.latitude))-3
latmax = np.round(np.max(stdf.latitude))+2
lonmin = np.round(np.min(stdf.longitude))-4
print(lonmin)
lonmax = np.round(np.max(stdf.longitude))+2


region=[lonmin, lonmax, latmin, latmax]
val=str((lonmin+lonmax)/2)
projection='S'+ val + '/90/8i'

lonlatgrid = np.load("lonlatgridfile.npy")
stacked_strength = np.load("stacked_strengthfile.npy")

y= lonlatgrid[0]
x= lonlatgrid[1]
z = stacked_strength
xx, yy, zz = x.flatten(), y.flatten(), z.flatten()
region2=[np.amin(x), np.amax(x), np.amin(y), np.amax(y)]
#region2=[-155.0,-150.0,58,62]

print(region)
print(region2)
fig = pygmt.Figure()
pygmt.config(COLOR_NAN="white")
ds = pygmt.xyz2grd(x=xx, y=yy, z=zz,region=region2, spacing=0.1)
#print(ds)
grid = pygmt.datasets.load_earth_relief(resolution="15s", region=region,)
fig.basemap(region=region, projection=projection, frame=True)
fig.grdimage(grid=grid,projection=projection,cmap='grayC',shading='+a45+nt0.5',)
pygmt.makecpt(cmap='hot',series='0/1/0.1',continuous=True,reverse=True,)
fig.grdimage(grid=ds,projection=projection,cmap=True,transparency="30",)
#fig.grdview(region=region2,grid=grid,projection=projection,cmap='hot',shading='+a45+nt0.5',surftype="i",drapegrid=ds,)

fig.coast(water="white", borders="1/0.5p", shorelines="1/0.5p", frame="ag",)
fig.plot(x=stdf.longitude, y=stdf.latitude, style="i0.4c", color="darkblue", pen="black")
fig.plot(x=evdf.longitude, y=evdf.latitude, style="a0.7c", color="darkred", pen="black")
fig.plot(x=gtevlon, y=gtevlat, style="a0.7c", color="darkgreen", pen="black")
fig.show()
fig.savefig("station_distribution_map.png")
