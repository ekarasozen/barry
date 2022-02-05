from obspy.clients.fdsn import Client
from obspy import UTCDateTime
client = Client("IRIS")
from obspy import read
from obspy import Stream
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

#t1 = UTCDateTime("2020-10-05 05:02:40") # 2020 October landslide 
#t2 = UTCDateTime("2021-08-09 07:45:40") # 2021 August landslide
#t1 = UTCDateTime("2022-01-08 16:26:00") #test event
t1 = UTCDateTime("2017-06-17 23:39:00") #test event
t2 = UTCDateTime("2017-06-18 00:39:00") #test event

#ls3 = UTCDateTime("2021-10-26 08:04:00") # 2021 October rockfall
#ls4 = UTCDateTime("2021-10-17 21:19") # 2020 October 2nd landslide - not confirmed

starttime = 60*1
endtime = 60*60
#net= "AK"
#stn = "BAE"
#chn = "BHZ"
net= "DK"
stn = "NUUG"
chn = "BH*"


st = client.get_waveforms(net, stn, "*", "HH*", starttime=t1, endtime=t2, attach_response=True)

print(st)
print(st[0].stats.endtime)

st.detrend("linear")
st.detrend("demean")
st.taper(max_percentage=0.05, type='cosine')
st.filter('bandpass', freqmin=0.01, freqmax=0.05)
#st.filter('highpass', freq=5)
##st = np.absolute(st)
##np.mean(arr.reshape(-1, 3), axis=1)
##st.remove_response(output="DISP")  
timevector = st[0].times("matplotlib")
fig1 = plt.figure(figsize=(8, 8))
nos = len(st)
for s in range(nos):
    tr = st[s]
    text = (tr.stats.station + "." + tr.stats.channel)
    ax1 = fig1.add_subplot(nos, 1,s+1)
    ax1.plot(tr.times("matplotlib"), tr.data, "k-", linewidth=0.8)
    ax1.set_xlim(timevector[0], timevector[-1]) 
  #  ax1.set_ylim(ymin=-500, ymax=500)
    ax1.text(0.88, 0.95, text, transform=ax1.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
    ax1.set_ylabel('Counts')
#   ax1.axvline(starttime, lw=0.8, c='darkblue', ls='--', label='event onset')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
    ax1.xaxis_date()
##    ax1.set_ylabel('Velocity (m/s)')
##ax1.set_title(st[0].stats.station + " " + st[0].stats.channel)
ax1.set_xlabel('Time (s)')
#ax1.legend(loc='lower left', fontsize=9)
#
##ylimits = ax1.get_ylim()
##ax1.set_ylim(ymin=ylimits[0], ymax=ylimits[1])
fig1.autofmt_xdate()
#
fig1.savefig('nuuk_event.png', bbox_inches='tight')
#fig2.savefig('landslide_waveforms_abs_bae.png', bbox_inches='tight')
#