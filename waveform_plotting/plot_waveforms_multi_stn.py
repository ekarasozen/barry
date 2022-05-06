from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
from obspy import read
from obspy import Stream
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
import functions_new as func
import pandas as pd

#s1 = UTCDateTime("2020-10-05 05:02:50") # 2020 October 5 landslide seen at BAE ends roughly around 05:04:12
s1= UTCDateTime("2021-08-09 07:45:47") # 2021 August landslide seen at BAE 07:46:37

starttime = 60*0.5
endtime = 60*8
network= "AK"
#station = "BAE,BAW,FID,GLI,KNK,M23K,PWL,RC01,SAW,SCM,VMT" #oct 2020
station = "BAT,BAE,PWL,KNK,GLI,M23K,SWD,EYAK,SKN,DHY,CCB,SAMH,TOLK,F15K,A21K" #agu 2021 5 deg
#station = "BAE,BAT,FID,GLI,KNK,M23K,PWL,RC01,SAW,SCM,VMT" # aug 2021
channel = "BHZ"
location="--"

#df = pd.read_csv("stafile_oct2020.csv",index_col=None,keep_default_na=False) # oct 2020
df = pd.read_csv("stafile_BA_AUG_5deg.csv",index_col=None,keep_default_na=False) # agu 2021 5 deg


#df = pd.read_csv("stafile_agu2021.csv",index_col=None,keep_default_na=False) #agu 2021
nos = len(df) #number of stations
stalat = df['latitude']
stalon = df['longitude']

st = func.getEventsIRIS(network,station,location,channel,s1-starttime,s1+endtime)
print(st)

st.detrend("linear")
st.detrend("demean")
st.filter('bandpass', freqmin=0.01, freqmax=0.05)
st.remove_response(output="VEL")  

#evlat=61.153 #BA October 5 2020
#evlon=-148.163 #BA October 5 2020
evlat=61.242 #BA August 9 2021
evlon=-147.94 #BA August 9 2021

nos = len(st)
distance = np.empty((0, 100))
for s in range(nos):
    dist=client_distaz.distaz(stalat[s],stalon[s],evlat,evlon) 
    distdeg = dist['distance']
    distm = dist['distancemeters']
#    azim = dist['azimuth']*1000
    distance = np.append(distance, [distm]) #distances are saved in meters


for s in range(nos): 
   st[s].stats.distance = distance[s]
   print(np.min(st[s].data))
   print(np.max(st[s].data))
st.sort(keys=['distance'])

tv = st[0].times("matplotlib")

fig1 = plt.figure(figsize=(4, 12))
for s in range(nos):
    tr = st[s]
    txt = (tr.stats.station + "." + tr.stats.channel)
    ax1 = fig1.add_subplot(nos, 1,s+1)
    ax1.plot(tr.times("matplotlib"), tr.data, "k-", linewidth=0.8)
    ax1.set_xlim(tv[0], tv[-1]) 
#    ax1.set_ylim(ymin1, ymax1) 
#   ax1.set_ylim(ymin=-8.00E-08, ymax=7.00E-08) #oct 2020
#    ax1.set_ylim(ymin=-2E-07, ymax=2E-07) #aug 2021
    ax1.text(0.88, 0.95, txt, transform=ax1.transAxes, fontsize=8, fontweight='bold', verticalalignment='top')
    ax1.axvline(starttime, lw=0.8, c='darkblue', ls='--', label='event onset')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.xaxis_date()
#    ax1.set_ylabel('Velocity (m/s)')
#######ax1.set_title(st[0].stats.station + " " + st[0].stats.channel)
#####ax1.set_xlabel('Time (s)')
######ax1.legend(loc='lower left', fontsize=9)
######
#ylimits = ax1.get_ylim()
#ax1.set_ylim(ymin=ylimits[0], ymax=ylimits[1])
fig1.autofmt_xdate()
######
fig1.savefig('AGU2021_multi_stn_5deg.pdf', bbox_inches='tight')
st.write('OCT_5degree.mseed', format="MSEED")  

######fig2.savefig('landslide_waveforms_abs_bae.png', bbox_inches='tight')
######