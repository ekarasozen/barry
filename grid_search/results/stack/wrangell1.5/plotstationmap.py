import pygmt
import pandas as pd
import numpy as np

gtevlat=61.9845 #wrangell
gtevlon=-143.1683 #wrangell

stdf = pd.read_csv("stafile.csv",index_col=None,keep_default_na=False)
evdf = pd.read_csv("stacked_locfile.csv",index_col=None,keep_default_na=False)


latmin = np.round(np.min(stdf.latitude))-1
latmax = np.round(np.max(stdf.latitude))+1
lonmin = np.round(np.min(stdf.longitude))
lonmax = np.round(np.max(stdf.longitude))+1


region=[lonmin, lonmax, latmin, latmax]
val=str((lonmin+lonmax)/2)
projection='S'+ val + '/90/8i'


print(latmin)
fig = pygmt.Figure()
grid = pygmt.datasets.load_earth_relief(resolution="15s", region=region,)
fig.basemap(region=region, projection=projection, frame=True)
fig.grdimage(grid=grid,projection=projection,cmap='gray',)
fig.coast(water="white", borders="1/0.5p", shorelines="1/0.5p", frame="ag",)
fig.plot(x=stdf.longitude, y=stdf.latitude, style="i0.4c", color="darkblue", pen="black")
fig.plot(x=evdf.longitude, y=evdf.latitude, style="a0.7c", color="darkred", pen="black")
fig.plot(x=gtevlon, y=gtevlat, style="a0.7c", color="darkgreen", pen="black")
fig.show()
fig.savefig("station_distribution_map.png")
