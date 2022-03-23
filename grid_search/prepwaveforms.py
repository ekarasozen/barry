from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
from obspy import UTCDateTime
from obspy.clients.fdsn.header import FDSNNoDataException
import numpy as np
from numpy import loadtxt
import pandas as pd
from obspy import Stream
from obspy.clients.fdsn.header import FDSNNoDataException


def prepwaveformsIris(stnlist,datetime,duration):
    s1 = UTCDateTime(datetime)  #this is necessary to avoid multiple channels/location codes due to station lat/long changes over time
    st = Stream() #initial stream
    df = pd.read_csv(stnlist,index_col=0,keep_default_na=False)
    print(df)
    nos = len(df) #number of stations
    network = df['network']
    station = df['network']
    location = df['location']
    channel = df['channel']
    station = df['station']
    for s in range(nos):
        try:
            st += client.get_waveforms(network=network[s], station=station[s], location=location[s], channel=channel[s], starttime=s1, endtime=s1+duration, attach_response=True)
        except FDSNNoDataException: #not sure why there is an error like this but this is the way around:
            print('No data available for request. Skipping this station: ' + net[s].code)
            continue
    print(st)

#REMAINING
#If data is not available for one of the sta_file rows, we should probably include a trace of zeros(?) 
#to ensure we have the same k traces as ttgrid. This code should include whatever pre-processing is 
#required before stacking (gap filling, detrending, filtering, resampling, …)
#
#
