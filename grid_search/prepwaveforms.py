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
from obspy import Trace
from obspy.clients.fdsn.header import FDSNNoDataException
from obspy import read, read_inventory


def prepwaveformsIris(stnlist,datetime,duration):
    s1 = UTCDateTime(datetime)  
    print(s1)
    st = Stream() #initial stream
    df = pd.read_csv(stnlist,index_col=None,keep_default_na=False)
    print(df)
    nos = len(df) #number of stations
    network = df['network']
    station = df['station']
    location = df['location']
    channel = df['channel']
    inv = read_inventory("station.xml")  
    net = inv[0]
    print(net[0])
    for s in range(nos):
        try:
            st += client.get_waveforms(network=network[s], station=station[s], location=location[s], channel=channel[s], starttime=s1, endtime=s1+duration, attach_response=True)
        except FDSNNoDataException:
            print('No data available for request. Creating a blank trace for this station: ' + station[s])
            tr = Trace()
            tr.attach_response(inv)
            tr.stats.starttime=s1 #DIFFERENT STARTTIMES?
            print(tr.stats.response)
            tr.stats.network = network[s] 
            tr.stats.station = station[s] #or XXX?
            tr.stats.location = location[s]
            tr.stats.channel = channel[s]
            tr.stats.sampling_rate = 50 #?
            print(tr.stats)
            tr.stats.npts=duration*tr.stats.sampling_rate
#            tr.trim(s1,tr.stats.endtime-0.02)
            st += tr            
    print(st)
    st.detrend("linear")
    st.detrend("demean")
    st.taper(max_percentage=0.05, type='cosine')
    st.filter('bandpass', freqmin=0.01, freqmax=0.05)
   # st.remove_response(output='DISP') #this is a problem when data is not available
    st.write('readytostack.mseed', format="MSEED")  
    st.plot()

#REMAINING
#If data is not available for one of the sta_file rows, we should probably include a trace of zeros(?) 
#to ensure we have the same k traces as ttgrid. This code should include whatever pre-processing is 
#required before stacking (gap filling, detrending, filtering, resampling, …)
#gap filling? 
#resampling?
#add check whether all traces have same sampling rate. and length
# gap filling, 
