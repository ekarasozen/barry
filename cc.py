from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy import read
from obspy import Stream
from obspy import UTCDateTime
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from obspy.signal.cross_correlation import correlation_detector
from obspy.signal.cross_correlation import correlate
from obspy.signal.cross_correlation import xcorr_max



#s1 = UTCDateTime("2020-10-05 05:00:00") # 2020 October landslide stream for detection
#s2 = UTCDateTime("2021-08-09 07:42:00") # 2021 August landslide stream for detection
s3 = UTCDateTime("2020-10-17 21:18:30") # 2020 October 2nd landslide seen at BAE - not confirmed
#s4 = UTCDateTime("2022-01-08 16:24:00") # 2022 January event stream for detection

#t1 = UTCDateTime("2020-10-05 05:02:40") # 2020 October landslide seen at BAE 
#t2 = UTCDateTime("2021-08-09 07:45:40") # 2021 August landslide seen at BAE
#t3 = UTCDateTime("2021-10-17 21:19:00") # 2020 October 2nd landslide seen at BAE - not confirmed
#t3 = UTCDateTime("2022-01-08 16:26:00") # 2022 January event seen at BAE 

#t1 = UTCDateTime("2020-10-05 05:03:00") # 2020 October landslide seen at KNK
t2 = UTCDateTime("2021-08-09 07:45:40") # 2021 August landslide seen at KNK
#t3 = UTCDateTime("2022-01-08 16:26:00") # 2022 January event seen at KNK xxx

#t1 = UTCDateTime("2020-10-05 05:03:10") # 2020 October landslide seen at GLI
#t2 = UTCDateTime("2021-08-09 07:45:40") # 2021 August landslide seen at GLI xxx
#t3 = UTCDateTime("2022-01-08 16:26:00") # 2022 January event seen at GLI xxxx



#ls3 = UTCDateTime("2021-10-26 08:04:00") # 2021 October rockfall
#ls4 = UTCDateTime("2021-10-17 21:19") # 2020 October 2nd landslide - not confirmed

starttime = (60 * 15)
endtime = 60*10
net= "AK"
stn = "KNK"
chn = "BHZ"

#stream: the event to be detected: 
st = client.get_waveforms(net, stn, "*", "BHZ", s3, s3+endtime, attach_response=True)
print(st)
st.detrend("linear")
st.detrend("demean")
st.taper(max_percentage=0.05, type='cosine')
st.filter('bandpass', freqmin=0.01, freqmax=0.05)
#print(st[0].stats.starttime)
st.plot()

#template: the event to use as a template
temp = client.get_waveforms(net, stn, "*", "BHZ", t2+0, t2+65, attach_response=True)
temp.detrend("linear")
temp.detrend("demean")
temp.taper(max_percentage=0.05, type='cosine')
temp.filter('bandpass', freqmin=0.01, freqmax=0.05)
print(temp)
temp.plot()


height = 0.7  # similarity threshold
distance = 5  # distance between detections in seconds
detections, sims = correlation_detector(st, temp, height, distance, plot=st)
print(detections)

pick = detections[0]['time']

st.trim(pick, pick + 100)
st.plot()

ccbasic = correlate(st[0],temp[0],20)
cc_shift, cc_max = xcorr_max(ccbasic)
print(cc_shift,cc_max)
