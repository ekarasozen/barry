import pygmt
import pandas as pd
stdf = pd.read_csv("stafile.csv",index_col=None,keep_default_na=False)
evdf = pd.read_csv("stacked_locfile.csv",index_col=None,keep_default_na=False)
region=[210, 214, 60, 62]
projection='S212/90/8i'

fig = pygmt.Figure()
grid = pygmt.datasets.load_earth_relief(resolution="15s", region=region,)
dgrid = pygmt.grdgradient(grid=grid, radiance=[180, 10])
fig.basemap(region=region, projection=projection, frame=True)
fig.grdimage(grid=grid,projection=projection,cmap='gray',)
fig.coast(water="white", borders="1/0.5p", shorelines="1/0.5p", frame="ag",)
fig.plot(x=stdf.longitude, y=stdf.latitude, style="i0.4c", color="darkblue", pen="black")
fig.plot(x=evdf.longitude, y=evdf.latitude, style="a0.7c", color="darkred", pen="black")
fig.show()
