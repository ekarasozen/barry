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
s1 = UTCDateTime("2021-08-09 07:45:47") 


evlat=61.242 
evlon=-147.94
vel = [i for i in np.arange(2.5,6.0,0.1)]
starttime = (60*2)
endtime = 60*5
nov = len(vel) #number of velocities to be tested 
distlim = 1.0
stack_power = np.empty((0, 100))
name = "BA2021_AUG9_"
for v in range (nov):
    print(vel[v])
    inv = func.getStationsIris("AK","*","BHZ",s1-starttime,s1+endtime) 
    net = inv[0]
    nos = len(net) #number of stations in the network
    st = Stream() #initial stream
    stcorr = Stream() #stream to stack
    distance = np.empty((0, 100))
    traveltime = np.empty((0,100))
    for s in range(nos):
        stalat=net[s].latitude
        stalon=net[s].longitude
        dist=client_distaz.distaz(stalat,stalon,evlat,evlon) 
        distdeg = dist['distance']
        distm = dist['distancemeters']
        tt = np.divide(float(distm)/1000,float(vel[v])) #calculate the traveltime
        if distdeg < distlim:
            try:
                st += func.getEventsIRIS("AK",net[s].code,"*","BHZ",s1-starttime,s1+endtime) 
            except FDSNNoDataException: #not sure why there is an error like this but this is the way around:
                print('No data available for request. Skipping this station: ' + net[s].code)
                continue
            distance = np.append(distance, [distm]) #distances are saved in meters
            traveltime = np.append(traveltime, [tt]) #save to traveltime table
        else: #ignore the stations at further distances > distlim
      	    continue
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
       st[t].stats.distance = distance[t]
       st[t].stats.starttime = st[t].stats.starttime-traveltime[t]
    st.sort(keys=['starttime'])
    print(st)
    st.write(name + 'after_' + str(vel[v]) + '.mseed', format="MSEED")  
    #RECORD SECTION PLOT
    text = (str(vel[v]) + 'km/sec')
    fig1 = plt.figure()
    st.plot(type="section",plot_dx=20e3, 
      time_down=True, linewidth=.75, grid_linewidth=.25,
      show=False, fig=fig1)
    ax1 = fig1.axes[0]
    transform = blended_transform_factory(ax1.transData, ax1.transAxes)
    for tr in st:
       ax1.text(tr.stats.distance / 1e3, 1.0, tr.stats.station, rotation=270,
           va="bottom", ha="center", transform=transform, zorder=10)
    ax1.text(0.85, 0.10, text, transform=ax1.transAxes, fontsize=10, fontweight='bold', color='blue', verticalalignment='top')
    fig1.savefig(name + 'after_ttcorr_' + str(vel[v]) + '.png')    
    #STACK
    st.normalize()
    npts_all = [len(tr) for tr in st]
    npts = min(npts_all)
    data = np.array([tr.data[:npts] for tr in st])
    stack = np.mean(data, axis=0)
    np.savetxt(name + 'stack_' + str(vel[v]) + '.out', stack, delimiter=',')
    maxpower = np.max(np.abs(stack)) #max of the abs value of the stack
    stack_power = np.append(stack_power, [maxpower]) #put maxpowers into an array    
    fig2 = plt.figure(figsize=(8, 8))
    gs = gridspec.GridSpec(1, 1)    
    gs.update(wspace=0.01, hspace=0.50) # set the spacing between axes. 
    ax2 = fig2.add_subplot(gs[0])
    ax2.plot(st[0].times()[:npts] , stack, "k-", linewidth=0.8, label='stream')
    fig2.savefig(name + 'stack_' + str(vel[v]) + '.png')
fig3 = plt.figure(figsize=(8, 8))
ax3 =  fig3.add_subplot(1, 1, 1)
ax3.scatter(vel, stack_power, marker='x')
ax3.set_ylabel('Max of the abs value from each stack')
ax3.set_xlabel('Displacement (m)')
#ax6.set_xlim(xmin=vel[0], xmax=vel[-1])
ax3.set_ylim(ymin=0.0)
fig3.savefig(name + 'vel_power' + str(vel[v]) + '.png')
