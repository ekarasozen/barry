from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
from obspy import UTCDateTime
from obspy.clients.fdsn.header import FDSNNoDataException
import numpy as np
from numpy import loadtxt
import pandas as pd
from obspy import Stream
from obspy import Trace


def createGrid(lon_min,lon_max,lon_num,lat_min,lat_max,lat_num,wavespeed,stnlist):
    df = pd.read_csv(stnlist,index_col=0,keep_default_na=False)
    print(df)
    nos = len(df) #number of stations
    stalat = df['latitude']
    stalon = df['longitude']
    grdpts_x = np.array([i for i in np.arange(lonmin,lonmax,lon_num)],dtype=np.float32)
    grdpts_y = np.array([i for i in np.arange(latmin,latmax,lat_num)],dtype=np.float32)
    print(grdpts_x,grdpts_y)
    xx, yy = np.meshgrid(grdpts_x,grdpts_y)
    distance = np.empty((0, 100))
    traveltime = np.empty((0,100))
    for s in range(nos):
        dist=client_distaz.distaz(stalat[s],stalon[s],xx,yy) 
        print(distances) 
        distdeg = dist['distance']
        distm = dist['distancemeters']
        azim = dist['azimuth']*1000
        tt = np.divide(float(distm)/1000,float(vel[v])) #calculate the traveltime
        distance = np.append(distance, [distm]) #distances are saved in meters
        traveltime = np.append(traveltime, [tt]) #save to traveltime table
        azimuth = np.append(azimuth, [azim]) #distances are saved in meters
       




####distances = distance_2d(-149.34, 60.26, xx, yy )  # distance to point (1, 2)
####print(distances)
####
####
####
####This code defines a grid of source locations and pre-computes travel times from each source to all stations. This is a core computational function that users should not need to alter. 
####usage
####
####sta_file:	     file name of csv station file 
####                containing the 7 comma-separated 
####                columns described above
####outputs
####lonlatgrid:     A grid of the lonlat values. This 
####will be needed later by plotting routines. 
####	ttgrid:	      a 3d matrix (i x j x k) where the 
####value of each cell is a travel time in seconds. See i, j, k above for dimensions. (I do not know what format this file should be. Whatever is easy to read back into shiftstack.)
####
####
####