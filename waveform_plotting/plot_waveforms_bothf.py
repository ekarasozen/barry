from obspy.clients.fdsn import Client
from obspy import UTCDateTime
client = Client("IRIS")
from obspy import read
from obspy import Stream
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
import functions_new as func

#s1 = UTCDateTime("2020-10-05 05:02:50") # 2020 October 5 landslide seen at BAE ends roughly around 05:04:12
s1= UTCDateTime("2021-08-09 07:45:47") # 2021 August landslide seen at BAE 07:46:37

starttime = 60*0.5
endtime = 60*2
network= "AK"
station = "BAE"
channel = "BH*"
location="*"


st = func.getEventsIRIS(network,station,location,channel,s1-starttime,s1+endtime)
print(st)

st.detrend("linear")
st.detrend("demean")
st.taper(max_percentage=0.05, type='cosine')
sthf = st.copy()
stlp = st.copy()
sthf.filter('highpass', freq=5)
stlp.filter('bandpass', freqmin=0.01, freqmax=0.05)
sthf.remove_response(output="VEL")  
stlp.remove_response(output="VEL")  

tv1 = sthf[0].times("matplotlib")
tv2 = stlp[0].times("matplotlib")
ymin1 = np.min(np.array([np.min(sthf[0].data),np.min(sthf[1].data),np.min(sthf[2].data)]))
ymax1 = np.max(np.array([np.max(sthf[0].data),np.max(sthf[1].data),np.max(sthf[2].data)]))
ymin2 = np.min(np.array([np.min(stlp[0].data),np.min(stlp[1].data),np.min(stlp[2].data)]))
ymax2 = np.max(np.array([np.max(stlp[0].data),np.max(stlp[1].data),np.max(stlp[2].data)]))
#print(ymin2,ymax2)
fig1 = plt.figure(figsize=(4, 12))
nos = len(st)
for s in range(nos):
    trhf = sthf[s]
    trlp = stlp[s]
    txt1 = (trhf.stats.station + "." + trhf.stats.channel)
    txt2 = (trlp.stats.station + "." + trlp.stats.channel)
    ax1 = fig1.add_subplot(nos*2, 1,((2*s)+1))
    ax2 = fig1.add_subplot(nos*2, 1,((2*s)+2))
    ax1.plot(trhf.times("matplotlib"), trhf.data, "k-", linewidth=0.8)
    ax2.plot(trlp.times("matplotlib"), trlp.data, "b-", linewidth=0.8)
    ax1.set_xlim(tv1[0], tv1[-1]) 
    ax2.set_xlim(tv2[0], tv2[-1]) 
    ax1.set_ylim(ymin1, ymax1) 
    ax2.set_ylim(ymin2-(0.5E-07), ymax2+(0.5E-07))
    ax1.text(0.82, 0.95, txt1, transform=ax1.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
    ax1.axvline(starttime, lw=0.8, c='darkblue', ls='--', label='event onset')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%%H:%M:%S'))
    ax1.xaxis_date()
#    ax1.set_ylabel('Velocity (m/s)')
    ax2.text(0.82, 0.95, txt2, transform=ax2.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
    ax2.axvline(starttime, lw=0.8, c='darkblue', ls='--', label='event onset')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax2.xaxis_date()
#   ax2.set_ylabel('Velocity (m/s)')
#######ax1.set_title(st[0].stats.station + " " + st[0].stats.channel)
#####ax1.set_xlabel('Time (s)')
######ax1.legend(loc='lower left', fontsize=9)
######
#ylimits = ax1.get_ylim()
#ax1.set_ylim(ymin=ylimits[0], ymax=ylimits[1])
fig1.autofmt_xdate()
######
fig1.savefig('AUG9_all_channels.pdf', bbox_inches='tight')
######fig2.savefig('landslide_waveforms_abs_bae.png', bbox_inches='tight')
######