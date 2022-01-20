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



t1 = UTCDateTime("2020-10-05 05:02:40") # 2020 October landslide 
t2 = UTCDateTime("2021-08-09 07:45:40") # 2021 August landslide
t3 = UTCDateTime("2022-01-08 16:26:00") #test event

#ls3 = UTCDateTime("2021-10-26 08:04:00") # 2021 October rockfall
#ls4 = UTCDateTime("2021-10-17 21:19") # 2020 October 2nd landslide - not confirmed

starttime = (60*0) + 2
endtime = 60*1
net= "AK"
stn = "BAE"
chn = "BHZ"

events = [(net, stn, "*", chn, t1-starttime, t1+endtime),
          (net, stn, "*", chn, t2-starttime, t2+endtime),
          (net, stn, "*", chn, t3-starttime, t3+endtime)]
st = client.get_waveforms_bulk(events, attach_response=True)
print(st)
#print(st[0].stats.starttime)
template = client.get_waveforms("AK", "BAE", "*", "BHZ", t1, t1+60, attach_response=True)
template.filter('bandpass', freqmin=0.01, freqmax=0.05)
template.plot()
#st.detrend("linear")
#st.detrend("demean")
#st.taper(max_percentage=0.05, type='cosine')
##st.filter('bandpass', freqmin=0.01, freqmax=0.05)
#st[0].plot()
#st[1].plot()
#st[2].plot()
stream = client.get_waveforms("AK", "BAE", "*", "BHZ", t2-30, t2+120, attach_response=True)
stream.filter('bandpass', freqmin=0.01, freqmax=0.05)
stream.plot()

height = 0.2  # similarity threshold
distance = 50  # distance between detections in seconds
detections, sims = correlation_detector(stream, template, height, distance, plot=stream)
print(detections)
#cc1 = correlate(st[0], st[1], 20)
#cc1_shift, cc1_max = xcorr_max(cc1)
#cc2 = correlate(st[0], st[2], 20)
#cc2_shift, cc2_max = xcorr_max(cc2)
#
#
#print("maxcorr_ls1_ls2:", round(cc1_max,2))
#print("lag_ls1_ls2:" ,cc1_shift*st[0].stats.delta)
#print("maxcorr_ls1_ls3:", round(cc2_max,2))
#print("lag_ls1_ls3:", cc2_shift*st[0].stats.delta)


## LOAD WAVEFORM DATA. DO A LITTLE PRE-PROCESSING
#tday = UTCDateTime("2021-08-09 07:45") #landslide 1
#ls1 = UTCDateTime("2020-10-17 21:19") #landslide 2
#
#event_name = "master_event"
#print('grabbing waveforms for ' + tday.strftime("%Y%m%d"))
#template = client.get_waveforms("AK", "KNK", "*", "BHZ", tday, tday+360, attach_response=True)
#template.filter('bandpass', freqmin=0.01, freqmax=0.05)
#template.plot()
#
#
#pick = UTCDateTime('2021-08-09T07:45:40.00')
#template.trim(pick, pick + 150)
#
#stream = client.get_waveforms("AK", "KNK", "*", "BHZ", ls1, ls1+360, attach_response=True)
#stream.filter('bandpass', freqmin=0.01, freqmax=0.05)
#height = 0.3  # similarity threshold
#distance = 10  # distance between detections in seconds
#detections, sims = correlation_detector(stream, template, height, distance, plot=stream)
#
#print(detections)