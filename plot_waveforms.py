from obspy.clients.fdsn import Client
from obspy import UTCDateTime
client = Client("IRIS")
from obspy import read
from obspy import Stream
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


t1 = UTCDateTime("2020-10-05 05:02:40") # 2020 October landslide 
t2 = UTCDateTime("2021-08-09 07:45:40") # 2021 August landslide
t3 = UTCDateTime("2022-01-08 16:26:00") #test event

#ls3 = UTCDateTime("2021-10-26 08:04:00") # 2021 October rockfall
#ls4 = UTCDateTime("2021-10-17 21:19") # 2020 October 2nd landslide - not confirmed

starttime = 60*4
endtime = 60*10
net= "AK"
stn = "BAE"
chn = "BHZ"

events = [(net, stn, "*", chn, t1-starttime, t1+endtime),
          (net, stn, "*", chn, t2-starttime, t2+endtime),
          (net, stn, "*", chn, t3-starttime, t3+endtime)]
st = client.get_waveforms_bulk(events, attach_response=True)
print(st)
#print(st[0].stats.starttime)

st.detrend("linear")
st.detrend("demean")
st.taper(max_percentage=0.05, type='cosine')
st.filter('bandpass', freqmin=0.01, freqmax=0.05)
#st.remove_response(output="VEL")  

fig1 = plt.figure(figsize=(8, 8))
nos = len(st)
for s in range(nos):
    ax1 = fig1.add_subplot(nos, 1,s+1)
    tr = st[s]
    ax1.plot(tr.times(), tr.data, "k-", linewidth=0.8)
    text = (tr.stats.starttime + starttime)
    ax1.set_xlim(xmin=0, xmax=starttime+endtime)
    ax1.set_ylim(ymin=-300, ymax=300)
#    ax1.xaxis_date()
    ax1.text(0.68, 0.95, text, transform=ax1.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
    ax1.set_ylabel('Counts')
    ax1.axvline(starttime, lw=0.8, c='darkblue', ls='--', label='event onset')
#    ax1.set_ylabel('Velocity (m/s)')
ax1.set_xlabel('Time (s)')
ax1.legend(loc='lower left', fontsize=9)

#ylimits = ax1.get_ylim()
#ax1.set_ylim(ymin=ylimits[0], ymax=ylimits[1])
#    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
#fig3.autofmt_xdate()

fig1.savefig('barry_arm_landslide_waveforms.png', bbox_inches='tight')
