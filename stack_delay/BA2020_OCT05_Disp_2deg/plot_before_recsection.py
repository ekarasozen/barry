from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
import os
import functions as func
import numpy as np
from obspy import UTCDateTime 
from obspy import Stream
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory
from obspy.clients.fdsn.header import FDSNNoDataException
from obspy import read


name = "BA_2020_OCT5_"
#name = "BA_2021_Aug9"
#name = "Taan_Fjord"
#s1 = UTCDateTime("2015-10-18 05:19:00") #  Taan Fjord
s1 = UTCDateTime("2020-10-05 05:02:50") # 2020 October 5 landslide seen at BAE ends roughly around 05:04:12
#s1= UTCDateTime("2021-08-09 07:45:47") # 2021 August landslide seen at BAE 07:46:37
#evlat=60.175 #Taan Fjord
#evlon=-141.187 #Taan Fjord
evlat=61.153 #BA October 5 2020
evlon=-148.163 #BA October 5 2020
#evlat=61.242 #BA August 9 2021
#evlon=-147.94 #BA August 9 2021

starttime = (60*2)
endtime = 60*5


st = read ("BA_2020_OCT5_before_3.6.mseed")                 
#us1 = UTCDateTime(startime)  
for tr in st: 
    inv = func.getStationsIris("AK",tr.stats.station,"BHZ",s1, s1+endtime) 
    net = inv[0] 
    sta = net[0] 
    dist = client_distaz.distaz(sta.latitude,sta.longitude,evlat,evlon) 
    distdeg = dist['distance'] 
    distm = dist['distancemeters'] 
   # distance = np.append(distance, [distm]) #distances are saved in meters 
    tr.stats.distance = distm 
st.sort(keys=['distance'])
fig0 = plt.figure()
st.plot(type="section",plot_dx=20e3, 
  time_down=True, linewidth=.75, grid_linewidth=.25,
  show=False, fig=fig0)
ax0 = fig0.axes[0]
transform = blended_transform_factory(ax0.transData, ax0.transAxes)
for tr in st:
   ax0.text(tr.stats.distance / 1e3, 1.0, tr.stats.station, rotation=270,
       va="bottom", ha="center", transform=transform, zorder=10)
fig0.savefig('taan_fjord_before.png')   
