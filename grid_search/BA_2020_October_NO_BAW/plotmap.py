import pygmt
import pandas as pd
import numpy as np

gtevlat=61.153 #BA October 5 2020
gtevlon=-148.163 #BA October 5 2020

stdf = pd.read_csv("stafile.csv",index_col=None,keep_default_na=False)
evdf = pd.read_csv("stacked_locfile.csv",index_col=None,keep_default_na=False)
lonlatgrid = np.load("lonlatgridfile.npy")
stacked_strength = np.load("stacked_strengthfile.npy")

y= lonlatgrid[0]
x= lonlatgrid[1]
z = stacked_strength

region=[np.amin(x), np.amax(x), np.amin(y), np.amax(y)]
val=str((np.amin(x)+np.amax(x))/2)
projection='S'+ val + '/90/8i'

xx, yy, zz = x.flatten(), y.flatten(), z.flatten()


grid = pygmt.xyz2grd(x=xx, y=yy, z=zz,region=region, spacing=0.1)
#print(grid)
fig = pygmt.Figure()
######grid = pygmt.datasets.load_earth_relief(resolution="15s", region=region,)
fig.basemap(region=region, projection=projection, frame=True)
fig.grdimage(grid=grid,projection=projection,cmap='roma',)
fig.coast(water="white", borders="1/0.5p", shorelines="1/0.5p", frame="ag",)
fig.plot(x=stdf.longitude, y=stdf.latitude, style="i0.4c", color="darkblue", pen="black")
fig.plot(x=evdf.longitude, y=evdf.latitude, style="a0.7c", color="darkred", pen="black")
fig.plot(x=gtevlon, y=gtevlat, style="a0.7c", color="darkgreen", pen="black")
fig.show()
fig.savefig("event_location_map.png")
