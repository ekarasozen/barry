import pygmt
import pandas as pd
import numpy as np


gtevlat=58.736 #Orville-Wilbur
gtevlon=-137.272 #Orville-Wilbur
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
pygmt.makecpt(cmap='hot',series='0/1/0.1',continuous=True,reverse=True,)
#pygmt.makecpt(cmap='hot',series=str(np.min(zz))+'/'+str(np.max(zz))+'/0.1',continuous=True,reverse=True,)
fig.grdimage(grid=grid,projection=projection,cmap=True,)
fig.coast(water="white", borders="1/0.5p", shorelines="1/0.5p", frame="ag",)
fig.plot(x=stdf.longitude, y=stdf.latitude, style="i0.4c", color="darkblue", pen="black")
fig.plot(x=evdf.longitude, y=evdf.latitude, style="a0.7c", color="darkred", pen="black")
fig.plot(x=gtevlon, y=gtevlat, style="a0.7c", color="darkgreen", pen="black")
fig.show()
fig.savefig("event_location_map.png")
