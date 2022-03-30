from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
from obspy import UTCDateTime
from obspy.clients.fdsn.header import FDSNNoDataException
import pandas as pd

df =  pd.DataFrame(columns = ['network','station','channel','location','latitude','longitude','elevation'])

def makestalistIris(network,station,channel,location,datetime):
    starttime = UTCDateTime(datetime)  
    inv = client.get_stations(network=network,station=station,channel=channel,location=location,starttime=starttime,level='response')
    noi = len(inv) #number of networks
  #  print(inv)
    for i in range(noi):
        net = inv[i]
        netcod = inv[i].code
        nos = len(net)  #number of stations in each network
        for s in range(nos):
            stacod=net[s].code 
            stalat=net[s].latitude
            stalon=net[s].longitude
            staelv=net[s].elevation
            chn = net[s] 
            noc = len(chn) #number of channels in each station
            for c in range(noc):
               cha = chn[c].code
               loc = chn[c].location_code
            data = netcod,stacod,cha,loc,stalat,stalon,staelv
            df.loc[s] = data 
#            df.loc[s+(i*5)] = data # 5 is hardwired here. need to figure out a way to get total number of stations if more than one network is needed. 
    print(df)
    df.to_csv('stafile.csv',index=False)
   # inv.write("station.xml",format="STATIONXML") #need in prepwaveforms to attach response to blank races