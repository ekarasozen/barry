from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
from obspy import UTCDateTime
from obspy.clients.fdsn.header import FDSNNoDataException
from obspy import read
import numpy as np
from numpy import loadtxt
import pandas as pd
from obspy import Stream
from obspy import Trace
import matplotlib.pyplot as plt


def shiftStack(ttgridfile,wfs):
    ttgrid = np.load(ttgridfile)
    lonlen = ttgrid.shape[0]
    latlen = ttgrid.shape[1]
    stacked_strength = np.zeros((lonlen, latlen)) 
    for i in range(lonlen):
        for j in range(latlen):
            st = Stream() #initial stream
            st = read(wfs)
            nos = len(st) #number of stations in the stream
            for s in range(nos):
                maxtt = np.max(ttgrid[i,j,:])
                st[s].trim((st[s].stats.starttime+np.around(ttgrid[i,j,s],2)),(np.around(maxtt-ttgrid[i,j,s],2))) #does maxtt needed???
            st.normalize()
            npts_all = [len(tr) for tr in st]
            npts = min(npts_all)
            data = np.array([tr.data[:npts] for tr in st])
            stack = np.mean(data, axis=0)
            trs = Trace() #save stack as a trace
            trs.data=stack
            trs.stats.starttime=st[0].stats.starttime 
            trs.stats.station = "STCK"
            trs.stats.sampling_rate = 50 
            st += trs
#           print(st)            
            st.write('stacked_wfs_' + str(i) + str(j) + '.mseed', format="MSEED")  
#           np.savetxt(name + 'stack_' + str(vel[v]) + '.out', stack, delimiter=',')
            maxpower = np.max(np.abs(stack)) #max of the abs value of the stack
            stacked_strength[i,j] = maxpower #save to traveltime table
    np.save("stacked_strengthfile", stacked_strength)  
    np.savetxt("stacked_strengthfile", stacked_strength,delimiter=',', newline="\n")  





#output
#stacked_location:     lon,lat,stack strength, and 
#error for the grid point with the maximum stack strength. This is the presumed source location. It may be wise to output this into a file so that the values can be called later by other functions??


#description
#This code iterates through the i x j grid of source locations. For each grid point the code shifts and stacks waveforms using the pre-computed travel times. 
#For each grid point, some type of stack amplitude measure is retained. Eventually this function should also include an estimate of the location error 
#(perhaps based on the second derivative at the stack maximum?) This is a core computational function that users should not be tweaking. 
