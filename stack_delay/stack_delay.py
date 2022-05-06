from obspy.clients.fdsn import Client
from obspy import UTCDateTime
#client = Client(base_url="https://earthquake.alaska.edu", timeout=600)
client = Client("IRIS")
from obspy.clients.iris import Client
client_distaz = Client()
import os
import functions as func
import functions_new as func_new
import numpy as np
from obspy import UTCDateTime 
from obspy import Stream
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory
from obspy.clients.fdsn.header import FDSNNoDataException


#name = "BA_2020_OCT5_deneme"
#name = "BA_2021_Aug9_deneme"
#name = "Taan_Fjord"
#name = "Hubbard"
#name = "Wrangell"
#name="Orville"
#name="Lamplugh"
#name="Red"
#name="LaPerouse"	
name="Fairweather"	
#s1 = UTCDateTime("2015-10-18 05:18:48") #  Taan Fjord 05:18:48
#s1 = UTCDateTime("2012-05-21 14:25:00") #  Hubbard landslide 14:25:32
#s1 = UTCDateTime("2013-07-25 10:14:56") #  Wrangell landslide 10:14:56
#s1 = UTCDateTime("2015-03-07 19:19:07") # Orville-Wilbur landslide
#s1 = UTCDateTime("2016-06-28 16:26:06") # Lamplugh Glacier 
#s1 = UTCDateTime("2016-05-22 07:57:34") #Red Glacier
#s1 = UTCDateTime("2016-02-16 14:24:44") #Mount LaPerouse
s1 = UTCDateTime("2016-09-05 04:38:35") #Fairweather AEC#3
#s1 = UTCDateTime("2020-10-05 05:02:50") # 2020 October 5 landslide seen at BAE ends roughly around 05:04:12
#s1= UTCDateTime("2021-08-09 07:45:47") # 2021 August landslide seen at BAE 07:46:37
#evlat=60.175 #Taan Fjord
#evlon=-141.187 #Taan Fjord
#evlat=61.153 #BA October 5 2020
#evlon=-148.163 #BA October 5 2020
#evlat=61.242 #BA August 9 2021
#evlon=-147.94 #BA August 9 2021
#evlat=60.0821 #hubbard
#evlon=-139.536 #hubbard
#evlat=61.9845 #wrangell
#evlon=-143.1683 #wrangell
#evlat=58.736 #Orville-Wilbur
#evlon=-137.272 #Orville-Wilbur
#evlat=58.77918 #Lamplugh
#evlon=-136.88827 #Lamplugh
#evlat=60.0277 #Red Glacier
#evlon=-153.0749 #Red Glacier
#evlat=58.561046 #Mount LaPerouse
#evlon=-137.07371 #Mount LaPerouse

evlat=58.9393 #Fairweather AEC#3
evlon= -137.4845 #Fairweather AEC#3
vel = [i for i in np.arange(2.5,6.0,0.1)]
starttime = (60*2)
endtime = 60*5
nov = len(vel) #number of velocities to be tested 
distlim = 2
stack_power = np.empty((0, 100))
for v in range (nov):
    print(vel[v])
    inv = func.getStationsIris("AK","*","BHZ",s1-starttime,s1+endtime) 
    net = inv[0]
    nos = len(net) #number of stations in the network
    st = Stream() #initial stream
    stcorr = Stream() #stream to stack
    distance = np.empty((0, 100))
    traveltime = np.empty((0,100))
    azimuth = np.empty((0, 100))    
    for s in range(nos):
        stalat=net[s].latitude
        stalon=net[s].longitude
        dist=client_distaz.distaz(stalat,stalon,evlat,evlon) 
        distdeg = dist['distance']
        distm = dist['distancemeters']
        azim = dist['azimuth']*1000
        tt = np.divide(float(distm)/1000,float(vel[v])) #calculate the traveltime
        if distdeg < distlim:
#        if distdeg < distlim and distdeg > 0.5:
            try:
                st += func.getEventsIRIS("AK",net[s].code,"*","BHZ",s1-starttime,s1+endtime) 
            except FDSNNoDataException: #if a station is not available
                print('No data available for request. Skipping this station: ' + net[s].code)
                continue
            distance = np.append(distance, [distm]) #distances are saved in meters
            traveltime = np.append(traveltime, [tt]) #save to traveltime table
            azimuth = np.append(azimuth, [azim]) #distances are saved in meters
        else: #ignore the stations at further distances > distlim
      	    continue
    print(st)
    st.detrend("linear")
    st.detrend("demean")
    st.taper(max_percentage=0.05, type='cosine')
    st.filter('bandpass', freqmin=0.01, freqmax=0.05)
    st.remove_response(output='DISP')
    maxtt = np.max(traveltime)
    nott = len(traveltime) #number of stations in the stream
    st.write(name + 'before_' + str(vel[v]) + '.mseed', format="MSEED")  
    #TRAVELTIME CORRECTION 
    for t in range(nott): 
       st[t].trim((s1-starttime+np.around(traveltime[t],2)),(np.around(maxtt-traveltime[t],2)))
       st[t].stats.starttime = st[t].stats.starttime-traveltime[t] # this is needed for record section. not for the stacking
    st.write(name + 'after_' + str(vel[v]) + '.mseed', format="MSEED")  
    func_new.plotRecordSection(st,distance,name,vel[v]) #record section plot after tt correction
#    func_new.plotRecordSection(st,azimuth,name,vel[v]) #record section plot after tt correction
    #STACK
    st.normalize()
    npts_all = [len(tr) for tr in st]
    npts = min(npts_all)
    data = np.array([tr.data[:npts] for tr in st])
    stack = np.mean(data, axis=0)
    #stack = func.stackPhaseWrighted(data)
    np.savetxt(name + 'stack_' + str(vel[v]) + '.out', stack, delimiter=',')
    maxpower = np.max(np.abs(stack)) #max of the abs value of the stack
    stack_power = np.append(stack_power, [maxpower]) #put maxpowers into an array    
    fig2 = plt.figure(figsize=(8, 8))
    gs = gridspec.GridSpec(1, 1)    
    gs.update(wspace=0.01, hspace=0.50) # set the spacing between axes. 
    ax2 = fig2.add_subplot(gs[0])
    ax2.plot(st[0].times()[:npts] , stack, "k-", linewidth=0.8, label='stream')
    ax2.set_xlim(xmin=0)
    fig2.savefig(name + 'stack_' + str(vel[v]) + '.png')
fig3 = plt.figure(figsize=(8, 8))
ax3 =  fig3.add_subplot(1, 1, 1)
ax3.scatter(vel, stack_power, marker='x')
ax3.set_ylabel('Max of the abs value from each stack')
ax3.set_xlabel('Velocity (km/sec)')
ax3.set_xlim(xmin=2.0)
ax3.set_ylim(ymin=0.0)
fig3.savefig(name + 'vel_power.png')
