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

#########
########Code to get waveforms from IRIS
########

def getEventsIRIS(network,station,location,channel,starttime,endtime):
    st = client.get_waveforms(network, station, location, channel, starttime, endtime, attach_response=True)
    return st
    
def getStationsIris(network,station,channel,starttime,endtime):
    inv = client.get_stations(network=network,station=station,channel=channel,starttime=starttime,endtime=endtime)
    return inv
