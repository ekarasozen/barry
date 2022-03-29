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
import matplotlib.pyplot as plt


def createGrid(lonmin,lonmax,lonnum,latmin,latmax,latnum,wavespeed,stnlist):
    df = pd.read_csv(stnlist,index_col=None,keep_default_na=False)
    nos = len(df) #number of stations
    station = df['station']
    stalat = df['latitude']
    stalon = df['longitude']
    grdpts_x = np.array([i for i in np.arange(lonmin,lonmax,lonnum)],dtype=np.float32)
    grdpts_y = np.array([j for j in np.arange(latmin,latmax,latnum)],dtype=np.float32)
    xx, yy = np.meshgrid(grdpts_x,grdpts_y)
    latlongrid = np.array([xx, yy])
    distance = np.zeros((len(xx[0]), len(yy), nos)) #longitude rows are needed, latitude columns
    traveltime = np.zeros((len(xx[0]), len(yy), nos))
    for s in range(nos):
        for i in range(len(xx)):
            for j in range(len(yy)):
              #  print(xx[j,i], yy[j,i])
                dist=client_distaz.distaz(stalat[s],stalon[s],yy[j,i],xx[j,i])                 
                distdeg = dist['distance']
                distm = dist['distancemeters']
                distkm = float(distm)/1000
                distance[i,j,s] = distkm #distances are saved in meters
                tt = np.divide(float(distkm),float(wavespeed)) #calculate the traveltime
                traveltime[i,j,s] = tt #save to traveltime table
    print(distance.shape)
    np.save("distance_array", distance)  
    np.save("traveltime_array", traveltime)  
    np.save("lonlatgrid", latlongrid)
#    np.savetxt("lonlatgrid", latlongrid,delimiter=',', newline="\n")  
    