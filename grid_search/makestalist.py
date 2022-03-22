from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
from obspy import UTCDateTime
from obspy.clients.fdsn.header import FDSNNoDataException
import numpy as np

def makestalistIris(network,station,channel,location,datetime):
    starttime = UTCDateTime(datetime)  #this is necessary to avoid multiple channels/location codes due to station lat/long changes over time
    inv = client.get_stations(network=network,station=station,channel=channel,location=location,starttime=starttime,level='response')
    noi = len(inv) #number of networks
    for i in range(noi):    
        net = inv[i]
        netcod = inv[i].code
        nos = len(net)  #number of stations in each network
        for s in range(nos):
            stacod=net[s].code 
            stalat=net[s].latitude
            stalon=net[s].longitude
            staelv=net[s].elevation
            chn = net[s] #number of channels in each station
            noc = len(chn)
            for c in range(noc):
               cha = chn[c].code
               loc = chn[c].location_code
               print(netcod,",",stacod,",",cha,",",loc,",",stalat,",",stalon,",",staelv)