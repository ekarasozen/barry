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


name = "taan_fjord_waveforms_cc"
#s1 = UTCDateTime("2020-10-05 05:00:00") # 2020 October 5 stream for detection
s1 = UTCDateTime("2015-10-18 05:18:38") # Taan Fjord
t1 = UTCDateTime("2015-10-18 05:18:35") # Taan Fjord
#s1 = UTCDateTime("2021-08-09 07:42:00") # 2021 August stream for detection
#s1 = UTCDateTime("2022-01-08 16:24:00") # 2022 January stream for detection

#template timings to use for BAE
#t1 = UTCDateTime("2020-10-05 05:02:40") # 2020 October 5 landslide seen at BAE 
#t1 = UTCDateTime("2021-10-17 21:19:00") # 2020 October 17 landslide seen at BAE
#t1 = UTCDateTime("2021-08-09 07:45:40") # 2021 August landslide seen at BAE
#t1 = UTCDateTime("2022-01-08 16:26:00") # 2022 January event seen at BAE 

#template timings to use for KNK
#t1 = UTCDateTime("2020-10-05 05:03:00") # 2020 October 5 landslide seen at KNK
#t1 = UTCDateTime("2021-10-17 21:19:00") # 2020 October 17 landslide seen at KNK xxxxxxxx
#t1 = UTCDateTime("2021-08-09 07:45:40") # 2021 August landslide seen at KNK
#t1 = UTCDateTime("2022-01-08 16:26:00") # 2022 January event seen at KNK xxx

#template timings to use for GLI
#t1 = UTCDateTime("2020-10-05 05:03:10") # 2020 October landslide seen at GLI
#t1 = UTCDateTime("2021-10-17 21:19:00") # 2020 October 17 landslide seen at GLI xxxxxxxx
#t1 = UTCDateTime("2021-08-09 07:45:40") # 2021 August landslide seen at GLI xxx
#t1 = UTCDateTime("2022-01-08 16:26:00") # 2022 January event seen at GLI xxxx



#ls3 = UTCDateTime("2021-10-26 08:04:00") # 2021 October rockfall
#ls4 = UTCDateTime("2021-10-17 21:19") # 2020 October 2nd landslide - not confirmed

starttime = (60 * 2)
endtime = 60*5
net= "AK"
stn = "MESA" #for the template
chn = "BHZ"

#######stream: the event to be detected: 
st = client.get_waveforms(net, "MESA", "*", "BHZ", s1, s1+180, attach_response=True)
print(st[0].stats)
st.detrend("linear")
st.detrend("demean")
st.taper(max_percentage=0.05, type='cosine')
st.filter('bandpass', freqmin=0.01, freqmax=0.05)
st.plot()
#tr = st[0]

st2 = client.get_waveforms(net, "RKAV", "*", "BHZ", t1, t1+100, attach_response=True)
print(st2)
st2.detrend("linear")
st2.detrend("demean")
st2.taper(max_percentage=0.05, type='cosine')
st2.filter('bandpass', freqmin=0.01, freqmax=0.05)
st2.plot()
#tr2 = st2[0]

#st.plot()
#st.trim(s1+35, s1+90)
#st.plot()
ccbasic = correlate(st[0],st2[0],20)
cc_shift, cc_max = xcorr_max(ccbasic)
print(cc_shift,cc_max)
##print(st[0].stats.starttime)


timevector = st[0].times("matplotlib")
gs = gridspec.GridSpec(2, 1)
gs.update(wspace=0.01, hspace=0.50) # set the spacing between axes. 
fig1 = plt.figure(figsize=(8, 8))
date_format = mdates.DateFormatter('%H:%M')

ax1 = fig1.add_subplot(gs[0])
text = (st[0].stats.station + "." + st[0].stats.channel)
ax1.plot(st[0].times(), st[0].data, "k-", linewidth=0.8, label='stream')
ax1.set_xlim(xmin=0, xmax=endtime) 
#ax1.set_ylim(ymin=-500, ymax=500)
ax1.text(0.88, 0.95, text, transform=ax1.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
ax1.set_ylabel('Counts')
ax1.set_xlabel('Time (s)')
ax1.legend(loc='lower right', fontsize=9)
ax1.set_xlabel("time after %s [s]" % st[0].stats.starttime)
ylimits = ax1.get_ylim()
ax1.set_ylim(ymin=ylimits[0], ymax=ylimits[1])


########template: the event to use as a template
#temp = client.get_waveforms(net, stn, "*", "BHZ", t1, t1+50, attach_response=True)
#temp.detrend("linear")
#temp.detrend("demean")
#temp.taper(max_percentage=0.05, type='cosine')
#temp.filter('bandpass', freqmin=0.01, freqmax=0.05)
#print(temp)
#
#
#text = (temp[0].stats.station + "." + temp[0].stats.channel)
#ax2 = fig1.add_subplot(gs[1])
#
#ax2.plot(temp[0].times(), temp[0].data, "k-", linewidth=0.8, label='template')
##ax2.set_ylim(ymin=-500, ymax=500)
#ax2.text(0.88, 0.95, text, transform=ax2.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
#ax2.set_xlim(xmin=-50, xmax=endtime) 
#ax2.set_ylim(ymin=ylimits[0], ymax=ylimits[1])
#ax2.set_ylabel('Counts')
#ax2.set_xlabel('Time (s)')
#ax2.legend(loc='lower right', fontsize=9)
#ax2.set_xlabel("time after %s [s]" % temp[0].stats.starttime)
#
#
#fig1.savefig(name + '.png')
#


height = 0.3  # Similarity values to trigger a detection, one for each template
distance = 1  # The distance in seconds between two detections.
detections, sims = correlation_detector(st, st2, height, distance, plot=st, filename='deneme_det.png')
print(detections)
#
#pick = detections[0]['time']
#
#st_cc = st.copy()
#st_cc.trim(pick, pick + 100)
#st_cc.plot()
#
#ccbasic = correlate(st_cc[0],temp[0],20)
#cc_shift, cc_max = xcorr_max(ccbasic)
#print(cc_shift,cc_max)
##