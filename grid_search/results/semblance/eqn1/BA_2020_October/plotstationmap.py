import pygmt
import pandas as pd
import numpy as np

gtevlat=61.153 #BA October 5 2020
gtevlon=-148.163 #BA October 5 2020

stdf = pd.read_csv("stafile.csv",index_col=None,keep_default_na=False)
evdf = pd.read_csv("stacked_locfile.csv",index_col=None,keep_default_na=False)

print(evdf)

latmin = np.round(np.min(stdf.latitude))-1.5
latmax = np.round(np.max(stdf.latitude))+0.5
lonmin = np.round(np.min(stdf.longitude))-1
print(lonmin)
lonmax = np.round(np.max(stdf.longitude))+1
pygmt.config(FORMAT_GEO_MAP="ddd.x")


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
#fig.grdimage(grid=grid,projection=projection,cmap='grayC',shading='+a45+nt0.5',)
fig.grdimage(grid="/Users/ezgikarasozen/Documents/GitHub/barry/grid_search/aec_zoomed.grd",projection=projection,cmap='/Users/ezgikarasozen/Documents/GitHub/barry/grid_search/gray_blue_AEC_simple.cpt',shading="+a45+nt0.5")

pygmt.makecpt(cmap='hot',series='0.0833/0.0834/0.00001',continuous=True,reverse=True,)
fig.grdimage(grid=ds,projection=projection,cmap=True,transparency="30",)
fig.colorbar(position="JMR+o0.5c/0c+w8c",box=True,frame=["x+lStack power"],)

#fig.grdview(region=region2,grid=grid,projection=projection,cmap='hot',shading='+a45+nt0.5',surftype="i",drapegrid=ds,)

fig.coast(water="white", borders="1/0.5p", shorelines="1/0.5p", frame="ag",map_scale="g-149/59.65+w40+f+u",)
fig.plot(x=stdf.longitude, y=stdf.latitude, style="i0.8c", color="darkblue", pen="black")
fig.plot(x=evdf.longitude, y=evdf.latitude, style="a1.0c", color="darkred", pen="2p,black")
fig.plot(x=gtevlon, y=gtevlat, style="a1.0c", color="darkgreen", pen="2p,black")
fig.show()
fig.savefig("station_distribution_map_test.pdf")
