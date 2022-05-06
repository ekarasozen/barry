from obspy.clients.fdsn import Client
from obspy import UTCDateTime
client = Client("IRIS")
from obspy import read
from obspy import Stream
from obspy import UTCDateTime
from obspy.signal.filter import envelope

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

evname = "BA_events"
t1 = UTCDateTime("2020-10-05 05:02:40") # 2020 October landslide 
t2 = UTCDateTime("2020-10-17 21:19:00") # 2020 October landslide #2
t3 = UTCDateTime("2021-08-09 07:45:40") # 2021 August landslide
###t3 = UTCDateTime("2022-01-08 16:26:00") #test event

#seiche events
#t1 = UTCDateTime("2022-01-08 16:26:00") #
#t2 = UTCDateTime("2022-01-20 02:34:58") #
#t3 = UTCDateTime("2022-01-20 03:31:23") #
#t4 = UTCDateTime("2022-01-20 16:55:58") #
#t5 = UTCDateTime("2022-02-01 18:49:05") #
#


#ls3 = UTCDateTime("2021-10-26 08:04:00") # 2021 October rockfall
#ls4 = UTCDateTime("2021-10-17 21:19") # 2020 October 2nd landslide - not confirmed

starttime = 60*1
endtime = 60*4
net= "AK"
stn = "BAE"
chn = "BHZ"

events = [(net, stn, "*", chn, t1-starttime, t1+endtime),
          (net, stn, "*", chn, t2-starttime, t2+endtime),
          (net, stn, "*", chn, t3-starttime, t3+endtime)]
     #     (net, stn, "*", chn, t4-starttime, t4+endtime),
     #     (net, stn, "*", chn, t5-starttime, t5+endtime)]
st = client.get_waveforms_bulk(events, attach_response=True)
print(st)
print(st[0].stats)

st.detrend("linear")
st.detrend("demean")
st.taper(max_percentage=0.05, type='cosine')
st.filter('bandpass', freqmin=0.01, freqmax=0.05)

#st = np.absolute(st)
#np.mean(arr.reshape(-1, 3), axis=1)
#st.remove_response(output="VEL")  
fig1 = plt.figure(figsize=(16, 8))
fig2 = plt.figure(figsize=(16, 8))
nos = len(st)
for s in range(nos):
    tr = st[s]
    text = (tr.stats.starttime + starttime)
    text2 = (tr.stats.station + '.' + tr.stats.channel)
    ax1 = fig1.add_subplot(nos, 1,s+1)
    ax1.plot(tr.times(), tr.data, "k-", linewidth=0.8)
    ax1.set_xlim(xmin=0, xmax=starttime+endtime)
    ax1.set_ylim(ymin=-150, ymax=200)
    ax1.text(0.84, 0.95, text, transform=ax1.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
    ax1.text(0.84, 0.85, text2, transform=ax1.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
    ax1.set_ylabel('Counts')
    ax1.axvline(starttime, lw=0.8, c='darkblue', ls='--', label='event onset on KNK')
    ax2 = fig2.add_subplot(nos, 1,s+1)
    #tr_env =envelope(tr.data)
    ax2.plot(tr.times(), envelope(tr.data), "k-", linewidth=0.8)
   # ax2.plot(tr.times().reshape(-1,10*50), np.sqrt(np.average(np.square(tr.data).reshape(-1,10*50),axis=1)), "k-", linewidth=0.8)
    ax2.set_xlim(xmin=0, xmax=starttime+endtime)
    #ax2.set_ylim(ymin=0, ymax=200)
    ax2.text(0.84, 0.95, text, transform=ax2.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
    ax2.text(0.84, 0.85, text2, transform=ax2.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
    ax2.set_ylabel('Counts')
    ax2.axvline(starttime, lw=0.8, c='darkblue', ls='--', label='event onset')
    ax2.set_ylim(ymin=0, ymax=200)
#    ax1.xaxis_date()
#ax1.set_title(st[0].stats.station + " " + st[0].stats.channel)
ax1.set_xlabel('Time (s)')
ax1.legend(loc='lower left', fontsize=9)
ax2.set_xlabel('Time (s)')
ax2.legend(loc='lower left', fontsize=9)

#ylimits = ax1.get_ylim()
#ax1.set_ylim(ymin=ylimits[0], ymax=ylimits[1])
#    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
#fig3.autofmt_xdate()

fig1.savefig(evname + '_waveforms_' + stn + '.png', bbox_inches='tight')
fig2.savefig(evname + '_waveforms_env_' + stn + '.png', bbox_inches='tight')
