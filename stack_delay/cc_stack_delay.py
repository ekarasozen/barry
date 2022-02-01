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
s1 = UTCDateTime("2020-10-05 05:18:00") #  Taan Fjord
#s1 = UTCDateTime("2015-10-18 05:17:20") # Taan Fjord
#t1 = UTCDateTime("2015-10-18 05:18:35") # Taan Fjord
evlat=60.175
evlon=-141.87
vel = 3.5
distance = np.empty((0, 100))
traveltime = np.empty((0,100))
#starttime = (60 * 15)
endtime = 60*7
net= "AK"
#stn = "MESA" #for the template
chn = "BHZ"

#In Python, load vertical component waveforms for the event, filter them, 
#remove instrument response (and possibly integrate to displacement?)

inv = client.get_stations(network = net, station="MESA,YAH,RKAV,CYK,BAGL,BARK,KULT", starttime=s1, endtime=s1+endtime)
net = inv[0]
nos = len(net)
for s in range(nos):
   st = client.get_waveforms("AK", "MESA,YAH,RKAV,CYK,BAGL,BARK,KULT", "*", "BHZ", s1, s1+endtime, attach_response=True)
   st.detrend("linear")
   st.detrend("demean")
   st.taper(max_percentage=0.05, type='cosine')
   st.filter('bandpass', freqmin=0.01, freqmax=0.05)
   st.remove_response(output='DISP')
   #print(st[s])
   #print(net[s])
   stalat=net[s].latitude
   stalon=net[s].longitude
   dist=client_distaz.distaz(stalat,stalon,evlat,evlon) #calculate the distance from the source to each of the stations
   dist=dist['distancemeters']/1000
   distance = np.append(distance, [dist])
   tt = np.divide(float(dist),float(vel))
   traveltime = np.append(traveltime, [tt])
   #print(tt)
   s2=s1+tt
   st_stack = client.get_waveforms("AK", "MESA,YAH,RKAV,CYK,BAGL,BARK,KULT", "*", "BHZ", s2, s2+endtime, attach_response=True)
   st_stack.detrend("linear")
   st_stack.detrend("demean")
   st_stack.taper(max_percentage=0.05, type='cosine')
   st_stack.filter('bandpass', freqmin=0.01, freqmax=0.05)
   st_stack.remove_response(output='DISP')
   #print(st_stack[s])
#print(distance)
#print(traveltime)

st.plot()
st_stack.plot()
stack = st_stack.stack()
stack.plot()
