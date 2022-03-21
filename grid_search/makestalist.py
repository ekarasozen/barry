from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
from obspy import UTCDateTime
from obspy.clients.fdsn.header import FDSNNoDataException
import numpy as np
#network = "AK"
#station = "BAE,BAT,KNK"
#location = "*"
#channel = "*"

def makestalistIris(network,station,channel,location):
    stalist = np.empty((7, 100))
    inv = client.get_stations(network=network,station=station,channel=channel,location=location,level='response')
    stn = inv[0] #stations
    nos = len(stn)
    chn = stn[0] #channels
    noc = len(chn)
    for s in range(nos):
        net = inv[0].code
        sta = stn[s].code
        stalat = stn[s].latitude
        stalon = stn[s].longitude
        staelv = stn[s].elevation
        for c in range(noc):
           cha = chn[c].code
           loc = chn[c].location_code
           stalist = np.append(stalist, [stalat]) #save to traveltime table 
           #stalist = sta,stalat,stalon,staelv,cha,loc,net
           np.savetxt('stalist.out', stalist, delimiter=',',newline='\n')

  #  return inv

