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
    print(ttgrid.shape)
    st = read(wfs)
    print(st)

#output
#stacked_strength:     A grid of the stack strength
#at each potential source location. This matrix will be size i x j. 
#stacked_location:     lon,lat,stack strength, and 
#error for the grid point with the maximum stack strength. This is the presumed source location. It may be wise to output this into a file so that the values can be called later by other functions??
#stacked_wfs:          an obspy stream of length k+1 
#containing the k waveforms that have been time-shifted to correspond to the stack_location. The last trace in the stream is the stacked waveform itself. This will be needed later by plotting routines. 


#description
#This code iterates through the i x j grid of source locations. For each grid point the code shifts and stacks waveforms using the pre-computed travel times. 
#For each grid point, some type of stack amplitude measure is retained. Eventually this function should also include an estimate of the location error 
#(perhaps based on the second derivative at the stack maximum?) This is a core computational function that users should not be tweaking. 
