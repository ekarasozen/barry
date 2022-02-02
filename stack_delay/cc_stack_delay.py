from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
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
s1 = UTCDateTime("2015-10-18 05:19:00") #  Taan Fjord
evlat=60.175
evlon=-141.87
vel = 3.5 
distance = np.empty((0, 100))
traveltime = np.empty((0,100))
endtime = 60*7
net= "AK,AV"
chn = "BHZ"
stn_list = ['MESA','YAH','RKAV','CYK','BAGL','BARK','KULT'] 
st = Stream() #initial stream
st_stack = Stream() #stream to stack

#In Python, load vertical component waveforms for the event, filter them, 

inv = client.get_stations(network = net, station="MESA,YAH,RKAV,CYK,BAG,BARK,KULT,TABL", starttime=s1, endtime=s1+endtime)
print(inv)
net = inv[0]
nos = len(net)
for s in range(nos):
   tr = client.get_waveforms("AK", stn_list[s], "*", "BHZ", s1, s1+endtime, attach_response=True)
   st += tr
   print(st)
   stalat=net[s].latitude
   stalon=net[s].longitude
   dist=client_distaz.distaz(stalat,stalon,evlat,evlon) #calculate the distance from the source to each of the stations
   dist=dist['distancemeters']/1000
   distance = np.append(distance, [dist])
   tt = np.divide(float(dist),float(vel))
   traveltime = np.append(traveltime, [tt])
   #print(tt)
   s2=s1+tt
   trs = client.get_waveforms("AK", stn_list[s], "*", "BHZ", s2, s2+endtime, attach_response=True)
   st_stack += trs
   print(st_stack)

#remove instrument response (and possibly integrate to displacement?)
st.sort(keys=['starttime'])
st.detrend("linear")
st.detrend("demean")
st.taper(max_percentage=0.05, type='cosine')
st.filter('bandpass', freqmin=0.01, freqmax=0.05)
#st.remove_response(output='DISP')
print(st)

fig1 = plt.figure(figsize=(8,8))

for i in range(nos):
    ax1 = fig1.add_subplot(nos, 1,i+1)
    tr = st[i]
    ax1.plot(tr.times("matplotlib"), tr.data, 'k', linewidth=0.2)
    text = (tr.stats.station + ' ' + tr.stats.channel)
    ax1.text(0.85, 0.90, text, transform=ax1.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')
    ax1.xaxis_date()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.set_ylim(ymin=-250, ymax=250)
fig1.autofmt_xdate()
plt.tight_layout()
plt.draw()
fig1.autofmt_xdate()
fig1.savefig('before_tt_correction.png')

st_stack.detrend("linear")
st_stack.detrend("demean")
st_stack.taper(max_percentage=0.05, type='cosine')
st_stack.filter('bandpass', freqmin=0.01, freqmax=0.05)
#st_stack.remove_response(output='DISP')
st_stack.sort(keys=['starttime']) #not sure if this is needed?
print(st_stack)


fig2 = plt.figure(figsize=(8,8))

for i in range(nos):
    ax2 = fig2.add_subplot(nos, 1,i+1)
    tr = st_stack[i]
    ax2.plot(tr.times("matplotlib"), tr.data, 'k', linewidth=0.2)
    text = (tr.stats.station + ' ' + tr.stats.channel)
    ax2.text(0.85, 0.90, text, transform=ax2.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')
    ax2.xaxis_date()
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax2.set_ylim(ymin=-250, ymax=250)
fig2.autofmt_xdate()
plt.tight_layout()
plt.draw()
fig2.autofmt_xdate()
fig2.savefig('after_tt_correction.png')


st_stack.normalize()
st_new = st_stack.stack()
gs = gridspec.GridSpec(2, 1)
gs.update(wspace=0.01, hspace=0.50) # set the spacing between axes. 
fig3 = plt.figure(figsize=(8, 8))

ax3 = fig3.add_subplot(gs[0])
ax3.plot(st_new[0].times(), st_new[0].data, "k-", linewidth=0.8, label='stream')
text = (str(vel) + 'km/sec')
ax3.text(0.85, 0.90, text, transform=ax3.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')

#ax2.set_xlim(xmin=0, xmax=streamend) 
#ax1.set_ylim(ymin=-500, ymax=500)
#ax2.text(0.88, 0.95, text, transform=ax1.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
#ax1.set_ylabel('Counts')
#ax1.set_xlabel('Time (s)')
#ax1.legend(loc='lower right', fontsize=9)
#ax1.set_xlabel("time after %s [s]" % st[0].stats.starttime)
#ylimits = ax1.get_ylim()
#ax1.set_ylim(ymin=ylimits[0], ymax=ylimits[1])
#fig2.autofmt_xdate()

fig3.savefig('stack.png')
