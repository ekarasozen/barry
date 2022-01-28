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
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
from obspy.signal.cross_correlation import correlation_detector
from obspy.signal.cross_correlation import correlate
from obspy.signal.cross_correlation import xcorr_max

temp = input("Choose template event (e.g. OCT05, AUG09):")
event = input("Choose stream to be detected (e.g. OCT05, AUG09):")

if temp=="OCT05":
    #tracestart = UTCDateTime("2020-10-05 05:02:50") # 2020 October 5 landslide seen at BAE   05:04:12
    tracestart = UTCDateTime("2020-10-05 05:03:19") # 2020 October 5 landslide seen at KNK 05:04:11
    #tracestart = UTCDateTime("2020-10-05 05:03:18") # 2020 October landslide seen at GLI 05:04:21
if temp=="OCT17":
    #tracestart = UTCDateTime("2021-10-17 21:18:50") # 2020 October 17 landslide seen at BAE 21:20:12
    tracestart = UTCDateTime("2021-10-17 21:19:04") # 2020 October 17 landslide seen at KNK 21:20:25
    #tracestart = UTCDateTime("2021-10-17 21:19:10") # 2020 October 17 landslide seen at GLI 21:20:34
if temp=="AUG09":
    #tracestart = UTCDateTime("2021-08-09 07:45:47") # 2021 August landslide seen at BAE 07:46:37
    tracestart = UTCDateTime("2021-08-09 07:46:00") # 2021 August landslide seen at KNK 07:46:46
    #tracestart = UTCDateTime("2021-08-09 07:46:02") # 2021 August landslide seen at GLI 07:46:48
if temp=="JAN08":
    #tracestart = UTCDateTime("2022-01-08 16:25:54") # 2022 January event seen at BAE  16:27:13 not clear
    tracestart = UTCDateTime("2022-01-08 16:26:19") # 2022 January event seen at KNK 16:27:03 not clear
    #tracestart = UTCDateTime("2022-01-08 16:26:24") # 2022 January event seen at GLI 16:27:13
   
if event=="OCT05":
    streamstart = UTCDateTime("2020-10-05 05:00:00") # 2020 October 5 stream for detection
if event=="OCT17":
    streamstart = UTCDateTime("2020-10-17 21:18:00") # 2020 October 17 stream for detection
if event=="AUG09":
    streamstart = UTCDateTime("2021-08-09 07:42:00") # 2021 August stream for detection
if event=="JAN08":
    streamstart = UTCDateTime("2022-01-08 16:24:00") # 2022 January stream for detection

name = "temp_" + temp + "_event_" + event + "_"

#ls3 = UTCDateTime("2021-10-26 08:04:00") # 2021 October rockfall
#ls4 = UTCDateTime("2021-10-17 21:19") # 2020 October 2nd landslide - not confirmed


streamend = 60*10
#traceend = 54 #oct05
traceend = 34 # oct17
#traceend = 44 # aug09
net= "AK"
stn = "KNK"
chn = "BHZ"

height = 0.85  # Similarity values to trigger a detection, one for each template
#height = 0.7  # for oct05
distance = 5  # The distance in seconds between two detections.


#######stream: the event to be detected: 
st = client.get_waveforms(net, stn, "*", "BHZ", streamstart, streamstart+streamend, attach_response=True)
print(st)
st.detrend("linear")
st.detrend("demean")
st.taper(max_percentage=0.05, type='cosine')
st.filter('bandpass', freqmin=0.01, freqmax=0.05)
#print(st[0].stats.starttime)


timevector = st[0].times("matplotlib")
gs = gridspec.GridSpec(2, 1)
gs.update(wspace=0.01, hspace=0.50) # set the spacing between axes. 
fig1 = plt.figure(figsize=(8, 8))
date_format = mdates.DateFormatter('%H:%M')

ax1 = fig1.add_subplot(gs[0])
text = (st[0].stats.station + "." + st[0].stats.channel)
ax1.plot(st[0].times(), st[0].data, "k-", linewidth=0.8, label='stream')
ax1.set_xlim(xmin=0, xmax=streamend) 
#ax1.set_ylim(ymin=-500, ymax=500)
ax1.text(0.88, 0.95, text, transform=ax1.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
ax1.set_ylabel('Counts')
ax1.set_xlabel('Time (s)')
ax1.legend(loc='lower right', fontsize=9)
ax1.set_xlabel("time after %s [s]" % st[0].stats.starttime)
ylimits = ax1.get_ylim()
ax1.set_ylim(ymin=ylimits[0], ymax=ylimits[1])


########template: the event to use as a template
temp = client.get_waveforms(net, stn, "*", "BHZ", tracestart, tracestart+traceend, attach_response=True)
temp.detrend("linear")
temp.detrend("demean")
temp.taper(max_percentage=0.05, type='cosine')
temp.filter('bandpass', freqmin=0.01, freqmax=0.05)
print(temp)


text = (temp[0].stats.station + "." + temp[0].stats.channel)
ax2 = fig1.add_subplot(gs[1])

ax2.plot(temp[0].times(), temp[0].data, "k-", linewidth=0.8, label='template')
#ax2.set_ylim(ymin=-500, ymax=500)
ax2.text(0.88, 0.95, text, transform=ax2.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
ax2.set_xlim(xmin=-50, xmax=streamend) 
ax2.set_ylim(ymin=ylimits[0], ymax=ylimits[1])
ax2.set_ylabel('Counts')
ax2.set_xlabel('Time (s)')
ax2.legend(loc='lower right', fontsize=9)
ax2.set_xlabel("time after %s [s]" % temp[0].stats.starttime)


fig1.savefig(name + stn + '.png')



detections, sims = correlation_detector(st, temp, height, distance, plot=st, filename=name + stn + '_det.png')
print(detections)

pick = detections[0]['time']

st_cc = st.copy()
st_cc.trim(pick, pick + traceend)
#st_cc.plot()

ccbasic = correlate(st_cc[0],temp[0],20)
cc_shift, cc_max = xcorr_max(ccbasic)
print(cc_shift,cc_max)
