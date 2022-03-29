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


def createGrid(lonmin,lonmax,lonnum,latmin,latmax,latnum,wavespeed,stnlist):
    df = pd.read_csv(stnlist,index_col=None,keep_default_na=False)
    nos = len(df) #number of stations
    station = df['station']
    stalat = df['latitude']
    stalon = df['longitude']
    grdpts_x = np.array([i for i in np.arange(lonmin,lonmax,lonnum)],dtype=np.float32)
    grdpts_y = np.array([i for i in np.arange(latmin,latmax,latnum)],dtype=np.float32)
    xx, yy = np.meshgrid(grdpts_x,grdpts_y)
    distance = np.zeros((len(xx), len(yy), nos))
    traveltime = np.zeros((len(xx), len(yy), nos))
    for s in range(nos):
        for i in range(len(xx)):
            for j in range(len(xx[i])):
               # print(xx[i][j], yy[i][j])
                dist=client_distaz.distaz(stalat[s],stalon[s],yy[i][j],xx[i][j]) 
                distdeg = dist['distance']
                distm = dist['distancemeters']
                distkm = float(distm)/1000
                distance = np.append(distance, [distkm]) #distances are saved in meters
                tt = np.divide(float(distkm),float(wavespeed)) #calculate the traveltime
                traveltime = np.append(traveltime, [tt]) #save to traveltime table
                print(i,j,station[s],tt)
      #     print(distkm)       
 
 

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