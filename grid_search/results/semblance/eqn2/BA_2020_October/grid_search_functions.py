from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
from obspy.clients.fdsn.header import FDSNNoDataException
from obspy import Stream
from obspy import Trace
from obspy import read, read_inventory
import numpy as np
from numpy import loadtxt
import pandas as pd
import matplotlib.pyplot as plt

####################################################################################################################################################################################
#makestalist
#This is an informal script to aid in the creation of sta_file. Unlike the other programs, this is a script with hardwired values that users are likely to manipulate directly in order to assemble the specific set of stations they want. 
####################################################################################################################################################################################

def makestalist(network,station,channel,location,datetime):
    df =  pd.DataFrame(columns = ['network','station','channel','location','latitude','longitude','elevation'])
    starttime = UTCDateTime(datetime)  
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
   

####################################################################################################################################################################################
#createttgrid
#This code defines a grid of source locations and pre-computes travel times from each source to all stations. This is a core computational function that users should not need to alter. 

def creategrid(lonmin,lonmax,lonnum,latmin,latmax,latnum,wavespeed,stafile):
    df = pd.read_csv(stafile,index_col=None,keep_default_na=False)
    nos = len(df) #number of stations
    station = df['station']
    stalat = df['latitude']
    stalon = df['longitude']
    grdpts_x = np.array([i for i in np.arange(lonmin,lonmax,lonnum)],dtype=np.float32)
    grdpts_y = np.array([j for j in np.arange(latmin,latmax,latnum)],dtype=np.float32)
    yy, xx = np.meshgrid(grdpts_y,grdpts_x)
    lonlatgrid = np.array([yy, xx])
    distgrid = np.zeros((len(yy), len(xx[0]), nos)) #longitude rows are needed, latitude columns
    ttgrid = np.zeros((len(yy), len(xx[0]), nos))
    for s in range(nos):
        for j in range(len(yy)):
            for i in range(len(xx[0])):
                dist=client_distaz.distaz(stalat[s],stalon[s],yy[j,i],xx[j,i])    
                distdeg = dist['distance']
                distm = dist['distancemeters']
                distkm = float(distm)/1000
                distgrid[j,i,s] = distkm #distances are saved in meters
                tt = np.divide(float(distkm),float(wavespeed)) #calculate the traveltime
                ttgrid[j,i,s] = tt #save to traveltime table
    np.save("distgridfile", distgrid)  
    np.save("ttgridfile", ttgrid)  
    np.save("lonlatgridfile", lonlatgrid)
#    np.savetxt("lonlatgrid", latlongrid,delimiter=',', newline="\n")  
    
####################################################################################################################################################################################
#prepwaveforms
#this code loads waveforms and prepares them for the stacking process. This is a core computational function that users should not need to alter. 
####################################################################################################################################################################################

def prepwaveforms(stafile,datetime,duration):
    s1 = UTCDateTime(datetime)  
    st = Stream() #initial stream
    df = pd.read_csv(stafile,index_col=None,keep_default_na=False)
    nos = len(df) #number of stations
    network = df['network']
    station = df['station']
    location = df['location']
    channel = df['channel']
    for s in range(nos):
        try:
            st += client.get_waveforms(network=network[s], station=station[s], location=location[s], channel=channel[s], starttime=s1, endtime=s1+duration, attach_response=True)
        except FDSNNoDataException:
            print('No data available for request. Creating a blank trace for this station: ' + station[s])
            tr = Trace()
            tr.stats.starttime=s1 
            tr.stats.network = network[s] 
            tr.stats.station = station[s]
            tr.stats.location = location[s]
            tr.stats.channel = channel[s]
            tr.stats.sampling_rate = 50 
            tr.stats.npts=duration*tr.stats.sampling_rate
            tr.data=np.zeros(tr.stats.npts)
            st += tr            
    st.detrend("linear")
    st.detrend("demean")
    st.taper(max_percentage=0.05, type='cosine')
    st.filter('bandpass', freqmin=0.01, freqmax=0.05)
    for tr in st:
        is_all_zero = np.all((tr.data == 0))
        if not is_all_zero:
      #  if tr.data != []: #creating empty traces didn't work because mseed doesn't save them. 
            tr.remove_response(output='DISP')
    st.write('before_stack_wfs.mseed', format="MSEED")  

#REMAINING
# This code should include whatever pre-processing is required before stacking (gap filling,resampling, …)
#add check whether all traces have same sampling rate. and length
#do we need to get longer duration traces for instrument response? ask Mike. 

####################################################################################################################################################################################
#shiftstack
#This code iterates through the i x j grid of source locations. For each grid point the code shifts and stacks waveforms using the pre-computed travel times. For each grid point, some type of stack amplitude measure is retained. Eventually this function should also include an estimate of the location error (perhaps based on the second derivative at the stack maximum?) This is a core computational function that users should not be tweaking. 
####################################################################################################################################################################################


def shiftstack(ttgridfile,before_stack_wfs,lonlatgridfile):
    df =  pd.DataFrame(columns = ['latitude','longitude','spower'])
    ttgrid = np.load(ttgridfile)
    lonlen = ttgrid.shape[0]
    latlen = ttgrid.shape[1]
#    lonlen = 2
#    latlen = 2
    lonlatgrid = np.load(lonlatgridfile)
    stacked_strength = np.zeros((lonlen, latlen)) 
    maxpowerall = 0
    stmaxpower = Stream() #initial stream to store max power stack
    for i in range(lonlen):
        for j in range(latlen):
            st = Stream() #initial stream
            st = read(before_stack_wfs)
            nos = len(st) #number of stations in the stream
            for s in range(nos):
                maxtt = np.max(ttgrid[i,j,:])
                st[s].trim((st[s].stats.starttime+np.around(ttgrid[i,j,s],2)),(np.around(maxtt-ttgrid[i,j,s],2))) #does maxtt needed???
                st[s].stats.starttime = st[s].stats.starttime-ttgrid[i,j,s] # this is needed for record section. not for the stacking
            #st.normalize()
            print(st)
            npts_all = [len(tr) for tr in st]
            npts = min(npts_all)
            data = np.array([tr.data[:npts] for tr in st])
            np.savetxt("data", data)           
            nots = data.shape[1] #number of time samples
            sden = np.zeros((1, nots)) # semblance eqn denumerator
            ###for ts in range(nots):
            ###   sem1 = np.square(np.sum(data[:,ts]))
            ###   snum[0,ts] = sem1
            ###print(snum)
            ###semn = np.sum(snum)
            ###print(semn)
            ###for ts in range(nots):
            ###   sem2= np.sum(np.square(data[:,ts]))
            ###   sden[0,ts] = sem2
            ###semd = nos * np.sum(sden)
            ###semb = np.divide(semn,semd)
            ###print(semb)
            sigm = np.zeros((nos, 1)) # semblance eqn denumerator
            for s in range(nos):
               sig = np.sqrt((1/nots)*(np.sum(np.square(data[s,:]))))
               sigm[s,0] = sig
#            print(data[:,0]/sigm[:,0])
            for ts in range(nots):
               sem1= np.square(np.sum(data[:,ts]/sigm[:,0]))
               sden[0,ts] = sem1
            semb = 1/(nots * np.square(nos)) * np.sum(sden)
            print(semb)
           # print(semb)
            ##stack = np.mean(data, axis=0)
            ##trs = Trace() #save stack as a trace
            ##trs.data=stack
            ##trs.stats.starttime=st[0].stats.starttime 
            ##trs.stats.station = "STCK"
            ##trs.stats.sampling_rate = 50 
            ##st += trs
            #maxpower = np.max(np.abs(stack)) #max of the abs value of the stack
            stacked_strength[i,j] = semb #save to traveltime table
            if semb > maxpowerall:
             #  stmaxpower = st.copy()
               maxpowerall = semb
            else: 
               continue
  #  stmaxpower.write('best_stack_wfs.mseed', format="MSEED")  
    #maxpowerall = np.max(np.abs(stacked_strength))
    print(maxpowerall)
    maxinx=np.where(stacked_strength == maxpowerall)
    cordinx = list(zip(maxinx[0], maxinx[1]))
    for cord in cordinx:
        evlat = lonlatgrid[0][cord]
        evlon = lonlatgrid[1][cord]
    stacked_location=evlat,evlon,maxpowerall
    df.loc[0] = stacked_location 
    print(df)
    df.to_csv('stacked_locfile.csv',index=False)
    np.save("stacked_strengthfile", stacked_strength)
    np.savetxt("stacked_strengthfile", stacked_strength,delimiter=',', newline="\n")  
