from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
from obspy import read
from obspy import Stream
from obspy import UTCDateTime
import obspy.signal
from obspy.clients.fdsn.header import FDSNNoDataException
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
from matplotlib.transforms import blended_transform_factory

lonmin = -149.0
lonmax = -148.0
latmin = 60.0
latmax = 61.0
stepsize = 0.1
vel = [i for i in np.arange(3.2,3.3,0.1)]
s1 = UTCDateTime("2020-10-05 05:02:50") # 2020 October 5 landslide seen at BAE ends roughly around 05:04:12
endtime = 60*1.5


grdpts_x = np.array([i for i in np.arange(lonmin,lonmax,stepsize)],dtype=np.float32)
grdpts_y = np.array([i for i in np.arange(latmin,latmax,stepsize)],dtype=np.float32)
print(grdpts_x,grdpts_y)
xx, yy = np.meshgrid(grdpts_x,grdpts_y)
#lt.plot(xx, yy, marker='.', color='k', linestyle='none')
#plt.show()

def distance_2d(x_point, y_point, x, y):
    return np.hypot(x-x_point, y-y_point)

def geodistance_2d(x_point, y_point, x, y):
    return client_distaz.distaz(x-x_point, y-y_point)


distances = distance_2d(-149.34, 60.26, xx, yy )  # distance to point (1, 2)
print(distances)
nov = len(vel) #number of velocities to be tested 

for v in range (nov):
   print(vel[v])
   inv = client.get_stations(network = "AK", station="*", channel="BHZ", starttime=s1, endtime=s1+endtime)
   st = Stream() #initial stream
   stcorr = Stream() #stream to stack
   distance = np.empty((0, 100))
   traveltime = np.empty((0,100))
   net = inv[0]
   nos = len(net) #number of stations in the network
   for s in range(nos):
      #calculate the distance from the source to each of the stations
      stalat=net[s].latitude
      stalon=net[s].longitude
      #dist=client_distaz.distaz(stalat,stalon,xx,yy) 
      distances = distance_2d(stalat, stalon, xx, yy )  # distance to point (1, 2)
      print(distances) 







#
#sta_list:		7 column matrix containing:
#				net, sta, chan, loc,
#				latitude, longitude, elevation
#				this matrix is size k x 7
##s1 = UTCDateTime("2020-10-05 05:02:50") # 2020 October 5 landslide seen at BAE ends roughly around 05:04:12
##endtime = 60*1.5
##
###inv = client.get_stations(network = "AK", station="BAW,BAE,GLI,KNK,PWL,EYAK,SWD,SKN,M23K,DHY,CCB,SAMH,R16K,F15K,TOLK,121K", level='response')
##inv = client.get_stations(network = "AK", station="BAW,BAE", channel="BHZ",location="*",level='response')
##stn = inv[0] #stations
##nos = len(stn)
##chn = stn[0] #channels
##noc = len(chn)
##for s in range(nos):
##   net = inv[0].code
##   sta = stn[s].code
##   stalat = stn[s].latitude
##   stalon = stn[s].longitude
##   staelv = stn[s].elevation
##   for c in range(noc):
##      cha = chn[c].code
##      lpc = chn[c].location_code
###  # print(sta[0].channel)
##
#sta_list = 
#
#
#evlat=61.153 #BA October 5 2020
#evlon=-148.163 #BA October 5 2020
#
#vel = 3
#endtime = 60*1.5
#
#inv = client.get_stations(network = "AK", station="BAW,BAE,GLI,KNK,PWL,EYAK,SWD,SKN,M23K,DHY,CCB,SAMH,R16K,F15K,TOLK,121K", starttime=s1, endtime=s1+endtime)
#st = Stream() #initial stream
#st_corr = Stream() #stream to stack
#distance = np.empty((0, 100))
#traveltime = np.empty((0,100))
#print("Stations being called:")
#print(inv[0])
#net = inv[0]
#nos = len(net)
#for s in range(nos):
#   tr = client.get_waveforms(network="AK", station=net[s].code, location="*", channel="BHZ", starttime=s1, endtime=s1+endtime, attach_response=True)
#   #print(tr)
#   st += tr
#   stalat=net[s].latitude
#   stalon=net[s].longitude
#   #print(net[s],stalat,stalon)
#   dist=client_distaz.distaz(stalat,stalon,evlat,evlon) #calculate the distance from the source to each of the stations
#  #####TO CONTROL WHICH STATIONS TO INCLUDE BY DISTANCE
#   if dist['distance'] >= 1.0:
#   	 continue
#   else: 
#      dist=dist['distancemeters']/1000
#   #print(dist)
#   distance = np.append(distance, [dist])
#   tt = np.divide(float(dist),float(vel[v]))
#  traveltime = np.append(traveltime, [tt])
