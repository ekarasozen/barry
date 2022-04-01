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


def prepwaveformsIris(stafile,datetime,duration):
    s1 = UTCDateTime(datetime)  
    print(s1)
    st = Stream() #initial stream
    df = pd.read_csv(stafile,index_col=None,keep_default_na=False)
    print(df)
    nos = len(df) #number of stations
    network = df['network']
    station = df['station']
    location = df['location']
    channel = df['channel']
    for s in range(nos):
        try:
            st += client.get_waveforms(network=network[s], station=station[s], location=location[s], channel=channel[s], starttime=s1, endtime=s1+duration, attach_response=True)
        except FDSNNoDataException:
            print('No data available for request. Creating a blank trace for this station: ' + station[s])
            tr = Trace()
            tr.stats.starttime=s1 
            tr.stats.network = network[s] 
            tr.stats.station = station[s]
            tr.stats.location = location[s]
            tr.stats.channel = channel[s]
            tr.stats.sampling_rate = 50 
            tr.stats.npts=duration*tr.stats.sampling_rate
            tr.data=np.zeros(tr.stats.npts)
            st += tr            
    print(st)
    st.detrend("linear")
    st.detrend("demean")
    st.taper(max_percentage=0.05, type='cosine')
    st.filter('bandpass', freqmin=0.01, freqmax=0.05)
    for tr in st:
        print(tr.data)
        is_all_zero = np.all((tr.data == 0))
        if not is_all_zero:
      #  if tr.data != []: #creating empty traces didn't work because mseed doesn't save them. 
            tr.remove_response(output='DISP')
        tr.plot()
    st.write('readytostack.mseed', format="MSEED")  
   # stp = read("readytostack.mseed") #check whether empty(zero) traces are saved
   # print(stp)
   #st.plot()

#REMAINING
# This code should include whatever pre-processing is required before stacking (gap filling,resampling, …)
#add check whether all traces have same sampling rate. and length
#do we need to get longer duration traces for instrument response? ask Mike. 
