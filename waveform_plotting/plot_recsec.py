from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
from obspy import read
from obspy import Stream
from obspy import UTCDateTime
from obspy import read, read_inventory
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
import functions_new as func
import pandas as pd
from matplotlib.transforms import blended_transform_factory

#s1 = UTCDateTime("2020-10-05 05:02:50") # 2020 October 5 landslide seen at BAE ends roughly around 05:04:12
s1= UTCDateTime("2021-08-09 07:45:47") # 2021 August landslide seen at BAE 07:46:37

starttime = 60*0.5
#endtime = 60*4
endtime = 250
network= "AK"
#station = "BAE,BAW,FID,GLI,KNK,M23K,PWL,RC01,SAW,SCM,VMT" #oct 2020
station = "BAT,BAE,PWL,KNK,GLI,M23K,SWD,EYAK,SKN,DHY,CCB,SAMH" #agu 2021 5 deg
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


fig0 = plt.figure()
st.plot(type="section", 
  time_down=True, linewidth=.75, grid_linewidth=.25, orientation='vertical',
  show=False, fig=fig0)
ax0 = fig0.axes[0]
transform = blended_transform_factory(ax0.transData, ax0.transAxes)
for tr in st:
   ax0.text(tr.stats.distance / 1e3, 1.0, tr.stats.station, rotation=270,
       va="bottom", ha="center", transform=transform, zorder=10)
plot_name = "after_ttcorr_"
###ax0.set_xlim(100, 550) 
#text = (str(vel) + 'km/sec')
#ax0.text(0.85, 0.10, text, transform=ax0.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')        
fig0.savefig('AUG9_2021_recsec.pdf')    
